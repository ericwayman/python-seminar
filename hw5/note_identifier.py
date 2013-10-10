
def note_identifier(path, plt_name):
	"""Returns the notes identified from a sound file.
		inputs: 
			path: a string containing the path to a sound file
			plt_name: a string that's the name for the plot file
		output: none.  Prints the peak frequency, the nearest note frequency and the corresponding note
	"""
	#imports
	import numpy as np
	import scipy as sp
	from scipy import signal
	import aifc
	import matplotlib.pyplot as plt
	
	#make a dict with keys frequences and values the corresponding notes
	#the number at the ned of the note indicates the octave
	note_dict ={16.351: 'C0',
	17.324: 'C# / Db0',
	18.354: 'D0',
	19.445: 'D# / Eb0',
	20.601: 'E0',
	21.827: 'F0',
	23.124: 'F# / Gb0',
	24.499: 'G0',
	25.956: 'G# / Ab0',
	27.5: 'A0',
	29.135: 'A# / Bb0',
	30.868: 'B0',
	32.703: 'C1',
	34.648: 'C# / Db1',
	36.708: 'D1',
	38.891: 'D# / Eb1',
	41.203: 'E1',
	43.654: 'F1',
	46.249: 'F# / Gb1',
	48.999: 'G1',
	51.913: 'G# / Ab1',
	55: 'A1',
	58.27: 'A# / Bb1',
	61.735: 'B1',
	65.406: 'C2',
	69.296: 'C# / Db2',
	73.416: 'D2',
	77.782: 'D# / Eb2',
	82.407: 'E2',
	87.307: 'F2',
	92.499: 'F# / Gb2',
	97.999: 'G2',
	103.826: 'G# / Ab2',
	110: 'A2',
	116.541: 'A# / Bb2',
	123.471: 'B2',
	130.813: 'C3',
	138.591: 'C# / Db3',
	146.832: 'D3',
	155.563: 'D# / Eb3',
	164.814: 'E3',
	174.614: 'F3',
	184.997: 'F# / Gb3',
	195.998: 'G3',
	207.652: 'G# / Ab3',
	220: 'A3',
	233.082: 'A# / Bb3',
	246.942: 'B3',
	261.626: 'C4',
	277.183: 'C# / Db4',
	293.665: 'D4',
	311.127: 'D# / Eb4',
	329.628: 'E4',
	349.228: 'F4',
	369.994: 'F# / Gb4',
	391.995: 'G4',
	415.305: 'G# / Ab4',
	440: 'A4',
	466.164: 'A# / Bb4',
	493.883: 'B4',
	523.251: 'C5',
	554.365: 'C# / Db5',
	587.33: 'D5',
	622.254: 'D# / Eb5',
	659.255: 'E5',
	698.456: 'F5',
	739.989: 'F# / Gb5',
	783.991: 'G5',
	830.609: 'G# / Ab5',
	880: 'A5',
	932.328: 'A# / Bb5',
	987.767: 'B5',
	1046.502: 'C6',
	1108.731: 'C# / Db6',
	1174.659: 'D6',
	1244.508: 'D# / Eb6',
	1318.51: 'E6',
	1396.913: 'F6',
	1479.978: 'F# / Gb6',
	1567.982: 'G6',
	1661.219: 'G# / Ab6',
	1760: 'A6',
	1864.655: 'A# / Bb6',
	1975.533: 'B6',
	2093.005: 'C7',
	2217.461: 'C# / Db7',
	2349.318: 'D7',
	2489.016: 'D# / Eb7',
	2637.021: 'E7',
	2793.826: 'F7',
	2959.955: 'F# / Gb7',
	3135.964: 'G7',
	3322.438: 'G# / Ab7',
	3520: 'A7',
	3729.31: 'A# / Bb7',
	3951.066: 'B7',
	4186.009: 'C8',
	4434.922: 'C# / Db8',
	4698.636: 'D8',
	4978.032: 'D# / Eb8',
	5274.042: 'E8',
	5587.652: 'F8',
	5919.91: 'F# / Gb8',
	6271.928: 'G8',
	6644.876: 'G# / Ab8',
	7040: 'A8',
	7458.62: 'A# / Bb8',
	7902.132: 'B8',
	8372.018: 'C9',
	8869.844: 'C# / Db9',
	9397.272: 'D9',
	9956.064: 'D# / Eb9',
	10548.084: 'E9',
	11175.304: 'F9',
	11839.82: 'F# / Gb9',
	12543.856: 'G9',
	13289.752: 'G# / Ab9',
	14080: 'A9',
	14917.24: 'A# / Bb9',
	15804.264: 'B9'}


	#import audio file
	#path = "./sound_files/1.aif"
	audio = aifc.open(path, 'rb')
	data = audio.readframes(audio.getnframes())
	int_data = np.fromstring(data, dtype=np.int32)
	RATE = audio.getframerate()
	time = np.arange(np.size(int_data)) / float(RATE)
	
	#take the fft of the data to identify the frequencies
	data_fft = np.fft.fft(int_data)
	
	#compute the power spectrum of the frequencies
	power_spect = abs(data_fft)**2

	#compute the frequencies
	freqs = np.fft.fftfreq(int_data.size, time[1]-time[0])

	#take positive frequencies only
	pos_ind = np.where(freqs > 0)
	freqs = freqs[pos_ind]
	power_spect = power_spect[pos_ind]

	#location of max signal
	indx = power_spect.argmax()
	strongest_freq = freqs[indx]
	print "The peak frequency is:"
	print strongest_freq
	dists = abs(strongest_freq - np.asarray(note_dict.keys()))
	closest_indx = dists.argmin()
	key = note_dict.keys()[closest_indx]
	note = note_dict[key]
	print "the  closest frequency is:"
	print key
	note = note_dict[key]
	print "The corresponding note is:"
	print note
	
	#make plots
	fig, (ax1, ax2) = plt.subplots(1, 2)
	#amplitude vs time plot
	plot_title = ("Audio Analysis")
	ax1.plot(time, int_data, color="red", linestyle="-")
	ax1.set_xlabel("Time [s]")
	ax1.set_ylabel("Amplitude")
	ax1.set_xlim(min(time), max(time))
	ax1.set_title(plot_title)

	#frequency power spectrum plot
	plot_title = ("Frequency Analysis")
	ax2.plot(freqs, power_spect, color="blue", linestyle="-")
	ax2.set_xlabel("Frequency [Hz]")
	ax2.set_ylabel("Frequency power Spectrum")
	#ax2.set_xlim(min(freqs),max(freqs))
	ax2.set_xlim(0,16000)
	ax2.set_title(plot_title)
	#plt.show()
	plt.savefig("%s.png" %plt_name)


if __name__== "__main__":
	"""Function to be run in the terminal.  Should include two arguments at command line,
	both are strings so don't forget quotes around them.  
	The first argument is the path to the audio file.  The second is the name for the plots
	"""
	import argparse
	parser=argparse.ArgumentParser(description="Compute the note from an audio file")
	parser.add_argument("path",
						type =str,
						nargs=1,
						help="a string that is path for an audio file of a note. Don't forget quotes",
						metavar="PATH")
	parser.add_argument("name",
						type =str,
						nargs=1,
						help="a string that is a name for the plots. Don't forget quotes",
						metavar="NAME")
	args = parser.parse_args()
	note_identifier("".join(args.path), "".join(args.name))

