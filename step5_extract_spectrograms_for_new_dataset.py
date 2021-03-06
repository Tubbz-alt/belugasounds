#
# extract_spectrograms_for_new_dataset.py
#
# Generate spectrograms for a data set on which we want to run the models trained
# in steps 1-4.
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
#

#%% Imports

import glob
import os
import wave
import pylab
from matplotlib import pyplot
from joblib import Parallel, delayed   ## version 0.12.0
import multiprocessing
import gc


#%% Path configuration

current_dir = "./Whale_Acoustics/"
data_dir = current_dir + "Data/"
audio_dir = data_dir + "Raw_Audio_Full_Analysis/" 
output_spectrogram_dir = data_dir + "Extracted_Spectrogram_Full_Analysis/" 

if not os.path.exists(output_spectrogram_dir):
    os.makedirs(output_spectrogram_dir)


#%% Spectrogram generation
    
audio_filenames = glob.glob(audio_dir + '/*.wav')
print("Total number of New Audio Files to Score:", len(audio_filenames))

def get_wav_info(audio_filename):
    wav = wave.open(audio_filename, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.frombuffer(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

def graph_spectrogram(spectrogram_second_length, audio_filename):
    sound_info, frame_rate = get_wav_info(audio_filename)
    audio_length_second = int(len(sound_info) / frame_rate)
    for j in range(0, audio_length_second, spectrogram_second_length):
        pyplot.figure(num=None, figsize=(19, 12))
        pyplot.subplot(222)
        ax = pyplot.axes()
        ax.set_axis_off()
        pyplot.specgram(sound_info[frame_rate * j: frame_rate * (j + spectrogram_second_length)], Fs = frame_rate)
        pyplot.savefig(output_spectrogram_dir + audio_filename.split('\\')[1][:-4] + '_' + str(j) + '_' + str(j + spectrogram_second_length) + '.png', bbox_inches='tight', transparent=True, pad_inches=0.0)
        pyplot.close()
    gc.collect()

def generate_spectrograms(i):
    audio_filename = audio_filenames[i]
    try:
        return graph_spectrogram(2, audio_filename)
    except:
        pass

num_cores = multiprocessing.cpu_count()
spectrograms = Parallel(n_jobs=num_cores)(delayed(generate_spectrograms)(i) for i in range(len(audio_filenames)))
