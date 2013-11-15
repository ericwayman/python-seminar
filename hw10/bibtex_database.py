#some imports
import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename

app = Flask(__name__)

#create an  SQLALCHEMY application object
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////tmp/bib.db'
db = SQLAlchemy(app)
eng = db.create_engine('sqlite:////tmp/bib.db')

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug = True

#define table
#columns: citation tag, author list, journal, volume, pages, year, title, and collection
class bib_tab(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	cit_tag = db.Column(db.String(80),unique=True)
	auth_list=db.Column(db.String(120))
	journal = db.Column(db.String(120))
	volume = db.Column(db.String(80))
	page = db.Column(db.String(80))
	year = db.Column(db.Integer)
	title = db.Column(db.String(120),unique=True)
	collection=db.Column(db.String(120))


#create the table
db.create_all()

#define route functions
@app.route("/")
def main_page():
	return render_template("main_page.html")

@app.route("/query", methods = ['GET','POST'])
def query():

	if request.method == 'POST':
		query=request.form['query']
		result = eng.execute('select * from article WHERE' + request.form['input'])
		if query not in (""," ",None):
			return "your query was %s" % query
			return result
		else:
			return "Invalid query"
	else:
		return render_template("query.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/insert_collection", methods=['GET', 'POST'])
def add_collection():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('add_collection'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))


if __name__=="__main__":
	app.run()