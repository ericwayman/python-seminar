#some imports
import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from pybtex.database.input import bibtex

app = Flask(__name__)

#create an  SQLALCHEMY application object
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////tmp/bib.db'
db = SQLAlchemy(app)
eng = db.create_engine('sqlite:////tmp/bib.db')

#configure app to allow files to be uploaded to '/tmp/'
#this will handle the bibtex files that a user can upload
UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt','bib'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.debug = True

#define table
#columns: citation tag, author list, journal, volume, pages, year, title, and collection
class table(db.Model):
	__tablename__ ='bibliographies'
	id = db.Column(db.Integer, primary_key=True)
	cit_tag = db.Column(db.String(80),unique=True)
	auth_list=db.Column(db.String(120))
	journal = db.Column(db.String(120))
	volume = db.Column(db.Integer)
	page = db.Column(db.String(80))
	year = db.Column(db.Integer)
	title = db.Column(db.String(120),unique=True)
	collection=db.Column(db.String(120))

	def __init__(self,collection_name,cit_tag,auth_list,journal,volume,page,year,title):
		self.collection  = collection_name
		self.cit_tag = cit_tag
		self.auth_list = auth_list
		self.journal = journal
		self.volume = volume
		self.page = page
		self.year = year
		self.title = title

#create the table
db.create_all()

#define route functions
@app.route("/")
def main_page():
	return render_template("main_page.html")

def display_results(row):
	row_summary = " \n ".join([str(key) + " : " + str(row[key]) for key in row.keys()])
	print row_summary
	return row_summary

@app.route("/query", methods = ['GET','POST'])
def query():

	if request.method == 'POST':
		query=request.form['query']
		if query not in (""," ",None):
			results = eng.execute('select * from bibliographies WHERE ' + query)
			result_list = [row for row in results]
			for row in result_list:
				return display_results(row)
			return "your query was %s:" % query

		else:
			return "Invalid query"
	else:
		return render_template("query.html")

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def add_bib_data(filename,collection_name):
	#open a bibtex file
	parser = bibtex.Parser()
	bibdata = parser.parse_file(UPLOAD_FOLDER+ filename)
	#extract the reference tags
	ref_tags = [ref_tag for ref_tag in bibdata.entries.keys()]
	#initialize a variable to cycle through all the ref_tags
	i=0
	#loop through the individual references
	for bib_id in bibdata.entries:
		b = bibdata.entries[bib_id].fields
		try:
			author_list = [author.last()[0] for author in bibdata.entries[bib_id].persons["author"]]
			authors = ', '.join(author_list)
			#print authors
			#print ref_tags[i]
			entry = table(collection_name,ref_tags[i],authors,b['journal'],b['volume'],b['pages'],b['year'],b['title'])
			db.session.add(entry)
			db.session.commit()
		# field may not exist for a reference
		except(KeyError):
			continue
		i =i+1

@app.route("/insert_collection", methods=['GET', 'POST'])
def add_collection():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			#save the file
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			collection_name = request.form['collection_name']
			add_bib_data(filename,collection_name)
			return redirect(url_for('add_collection'))
	return """
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form action="" method=post enctype=multipart/form-data>
		<p><input type=file name=file>
		<input type = "text" name="collection_name">
		<input type=submit value=Upload>
	</form>
	<p>%s</p>
	""" % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))


if __name__=="__main__":
	app.run()