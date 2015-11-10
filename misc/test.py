from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange

def plotSpectrum(y,Fs):
	"""
	Plots a Single-Sided Amplitude Spectrum of y(t)
	"""
	n = len(y) # length of the signal
	k = arange(n)
	T = n/Fs
	frq = k/T # two sides frequency range
	frq = frq[range(n/2)] # one side frequency range

	Y = fft(y)/n # fft computing and normalization
	Y = Y[range(n/2)]
	 
	plot(frq,abs(Y),'r') # plotting the spectrum
	xlabel('Freq (Hz)')
	ylabel('|Y(freq)|')

import model as m
modelo =  m.Model( "../sample-mocap-data//05//05_01_ignoreFirstFrame.bvh" )
modelo.read()

import movement as mov
data = mov.getJointPosition( modelo , "LeftFoot" ) 
signal = [ position[ 1 , 0 ] for position in data ]

## Test Fast Fourier ##

import data as dt
f = dt.cubicInterpolation( signal )

Fs = 150.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = arange(0,1,Ts) # time vector

ff = 5;   # frequency of the signal
y = f(2*pi*ff*t)

subplot(2,1,1)
plot(t,y)
xlabel('Time')
ylabel('Amplitude')
subplot(2,1,2)
plotSpectrum(y,Fs)
show()