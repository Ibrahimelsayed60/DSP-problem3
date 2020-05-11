from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType

#import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
#import pygame as pgm
#from pygame import *
from playsound import playsound
ui,_ = loadUiType('Window.ui')

class guitar:
    def __init__(self,pitch , s_sample,sampling_freq,s_factor):
        self.pitch = pitch
        self.s_sample=s_sample
        self.sampling_freq = sampling_freq
        self.s_factor = s_factor
        self.data_size = sampling_freq // int(pitch)
        data = (2*np.random.randint(0,2,self.data_size)-1)
        self.data = data.astype(np.float)
        self.c_sample=0
        self.old_sample=0

    def sample(self):
        if self.c_sample >= self.s_sample:
            c_sample_mod = self.c_sample % self.data_size
            r = np.random.binomial(1,1-1/self.s_factor)
            if r ==0:
                self.data[c_sample_mod] = 0.5 *(self.data[c_sample_mod] + self.old_sample)
            sample = self.data[c_sample_mod]
            self.old_sample=sample
            self.c_sample+=1
        else:
            self.c_sample +=1
            sample=0
        return sample


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)


        self.Handel_buttons()
        self.Handel_fun()

    def Handel_buttons(self):
        self.drum_1.clicked.connect(self.play_first_tone)
        self.drum_2.clicked.connect(self.play_second_tone)
        self.tone_1.clicked.connect(self.A_tone)
        self.tone_2.clicked.connect(self.B_tone)
        self.tone_3.clicked.connect(self.C_tone)
        self.tone_4.clicked.connect(self.D_tone)
        self.tone_5.clicked.connect(self.E_tone)
        self.tone_6.clicked.connect(self.F_tone)

    def Handel_fun(self):
        self.get_tone_drum()
        self.get_guitar_tones()

    ######################################################################################################
    ################################Drum function#########################################################
    def fun_drum(self,wavetable, n_samples, prob):
        samples = []
        current_sample = 0
        previous_value = 0
        while len(samples) < n_samples:
            r = np.random.binomial(1, prob)
            sign = float(r == 1) * 2 - 1
            wavetable[current_sample] = sign * 0.5 * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)

    def get_tone_drum(self):
        fs=8000
        data_size = fs//40
        E_data=np.ones(data_size)
        # I can change the stratch factor to change The tone
        # I use values of 0.3 and 0.9 
        stratch_factor= 0.3
        o_data = self.fun_drum(E_data,1*fs,stratch_factor)
        wavfile.write('tone.wav',fs,np.array(o_data,dtype = np.float32))

    def play_first_tone(self):        
        playsound('tone1.wav')


    def play_second_tone(self):
        playsound('tone2.wav')

    #####################################################################################
    ######################Vitual guitar Tune#############################################
    def get_guitar_tones(self):
        fs=8000
        frequns = [98,123,147,196,294,392]
        delay = fs//3
        delays=[]
        s_factor=[]
        for i in range(len(frequns)):
            delays.append(delay*i)
        for j in frequns:
            s_factor.append(2*j/98)

        self.export_tone(frequns,delays,s_factor,fs)
    
    def export_tone(self,freqs,delays,s_factor,fs):
        result_data = []
        for freq, delay, stretch_factor in zip(freqs, delays, s_factor):
            s_data = guitar(freq, delay, fs, stretch_factor)
            result_data.append(s_data)

        sound = [sum(s_data.sample() for s_data in result_data) for _ in range(fs * 6)]
        wavfile.write('g_tone.wav',fs,np.array(sound,dtype = np.float32))

        


    def A_tone(self):
        playsound('guitar_tone1.wav')

    def B_tone(self):
        playsound('guitar_tone2.wav')
    def C_tone(self):
        playsound('guitar_tone3.wav')

    def D_tone(self):
        playsound('guitar_tone4.wav')

    def E_tone(self):
        playsound('guitar_tone5.wav')

    def F_tone(self):
        playsound('guitar_tone6.wav')


def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()