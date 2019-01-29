
## Mocking Bot - Task 1.1: Note Detection

#  Instructions
#  ------------
#
#  This file contains Main function and note_detect function. Main Function helps you to check your output
#  for practice audio files provided. Do not make any changes in the Main Function.
#  You have to complete only the note_detect function. You can add helper functions but make sure
#  that these functions are called from note_detect function. The final output should be returned
#  from the note_detect function.
#
#  Note: While evaluation we will use only the note_detect function. Hence the format of input, output
#  or returned arguments should be as per the given format.
#  
#  Recommended Python version is 2.7.
#  The submitted Python file must be 2.7 compatible as the evaluation will be done on Python 2.7.
#  
#  Warning: The error due to compatibility will not be entertained.
#  -------------


## Library initialisation

# Import Modules
# DO NOT import any library/module
# related to Audio Processing here
import numpy as np
import math
import wave
import os
import struct
import scipy.signal


# Teams can add helper functions
# Add all helper functions here

############################### Your Code Here ##############################################

def note_detect(audio_file):

	#   Instructions
	#   ------------
	#   Input   :   audio_file -- a single test audio_file as input argument
	#   Output  :   Detected_Note -- String corresponding to the Detected Note
	#   Example :   For Audio_1.wav file, Detected_Note = "A4"

	# Add your code here
    sampling_freq = 44100
    window = 399
    dft = []  
    start = []  
    end = []  
    Identified_Notes = []  

    Identified_Notes[:] = []  
    start[:] = []
    end[:] = []

    array = [17.32,19.45,23.12,25.96,29.14,
         34.65,38.89,46.25,51.91,58.27,
         69.30,77.78,92.50,103.83,116.54,
         138.59,155.56,185.00,207.65,233.08,
         277.18,311.13,369.99,415.30,466.16,
         554.37,622.25,739.99,830.61,932.33,
         1108.73,1244.51,1479.98,1661.22,1864.66,
         2217.46,2489.02,2959.96,3322.44,3729.31,
         4434.92,4978.03,5919.91,6644.88,7458.62,
         16.35,18.35,20.60,21.83,24.50,27.50,30.87,
         32.70,36.71,41.20,43.65,49.00,55.00,61.74,
         65.41,73.42,82.41,87.31,98.00,110.00,123.47,
         130.81,146.83,164.81,174.61,196.00,220.00,246.94,   
         261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88,
         523.25, 587.33, 659.25, 698.46, 783.99, 880.00, 987.77,
         1046.50, 1174.66, 1318.51, 1396.91, 1567.98, 1760.00, 1975.53,
         2093.00, 2349.32, 2637.02, 2793.83, 3135.96, 3520.00, 3951.07,
         4186.01, 4698.63, 5274.04, 5587.65, 6271.93, 7040.00, 7902.13,
         ]

    notes = ['C#0', 'D#0', 'F#0', 'G#0', 'A#0',
         'C#1', 'D#1', 'F#1', 'G#1', 'A#1',
         'C#2', 'D#2', 'F#2', 'G#2', 'A#2',
         'C#3', 'D#3', 'F#3', 'G#3', 'A#3',
         'C#4', 'D#4', 'F#4', 'G#4', 'A#4',
         'C#5', 'D#5', 'F#5', 'G#5', 'A#5',
         'C#6', 'D#6', 'F#6', 'G#6', 'A#6',
         'C#7', 'D#7', 'F#7', 'G#7', 'A#7',
         'C#8', 'D#8', 'F#8', 'G#8', 'A#8',
         'C0', 'D0', 'E0', 'F0', 'G0', 'A0', 'B0',
         'C1', 'D1', 'E1', 'F1', 'G1', 'A1', 'B1',
         'C2', 'D2', 'E2', 'F2', 'G2', 'A2', 'B2',
         'C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3',
         'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4',
         'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5',
         'C6', 'D6', 'E6', 'F6', 'G6', 'A6', 'B6',
         'C7', 'D7', 'E7', 'F7', 'G7', 'A7', 'B7',
         'C8', 'D8', 'E8', 'F8', 'G8', 'A8', 'B8',
         ]

    file_length = audio_file.getnframes()
    sound = np.zeros(file_length)
    for i in range(file_length):
        data = audio_file.readframes(1)
        data = struct.unpack("<h", data)
        sound[i] = int(data[0])
    sound = np.divide(sound, float(2 ** 15))
    sound_square = np.square(sound)

    i = 0
    j = 0
    c = 0
    count = 0
    xsum = []

    while (i < (file_length) - window):
        s = 0.00
        j = 0

        while (j <= window):
            s = s + sound_square[i + j]
            j = j + 1

        xsum.append(s)
        c = c+1
        count += s
        i = i + window

    i = 0
    fx=0
    avg = count/c
    threshold = avg/20.0

    for i in range(len(xsum)):
        if xsum[i]>threshold and fx==0:
            fx=1
            start.append(i*window)
        elif xsum[i]<threshold and fx==1:
            end.append(i*window)
            fx=0
        
        else:
            continue

    if len(start)!=len(end):
        end.append(i*window)
    i = 0

    while (i < len(start)): 
        
        dft = np.array(np.fft.fft(sound[start[i]:end[i]]))
        indexes, _ = scipy.signal.find_peaks(dft, height=45, distance=45)
        i_max = indexes[0]
        fr = ((i_max)*sampling_freq)/(end[i]-start[i])
        idx = (np.abs(array-fr)).argmin()
        Detected_Note = notes[idx]
        i = i + 1
	return Detected_Note


############################### Main Function ##############################################

if __name__ == "__main__":

	#   Instructions
	#   ------------
	#   Do not edit this function.

	# code for checking output for single audio file
	path = os.getcwd()
	
	file_name = path + "\Task_1.1_Audio_files\Audio_1.wav"
	audio_file = wave.open(file_name)

	Detected_Note = note_detect(audio_file)

	print("\n\tDetected Note = " + str(Detected_Note))

	# code for checking output for all audio files
	x = raw_input("\n\tWant to check output for all Audio Files - Y/N: ")
	
	if x == 'Y':

		Detected_Note_list = []

		file_count = len(os.listdir(path + "\Task_1.1_Audio_files"))

		for file_number in range(1, file_count):

			file_name = path + "\Task_1.1_Audio_files\Audio_"+str(file_number)+".wav"
			audio_file = wave.open(file_name)

			Detected_Note = note_detect(audio_file)
			
			Detected_Note_list.append(Detected_Note)

		print("\n\tDetected Notes = " + str(Detected_Note_list))
	
	
