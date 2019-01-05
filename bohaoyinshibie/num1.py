import numpy as np
import wave
from matplotlib import pyplot as plt
from scipy.io import wavfile
snd = wavfile.read('dtmf-1.wav')
f=wave.open(r"dtmf-1.wav","rb")
params=f.getparams()
nchannels,samplewidth,framerate,nframes=params[:4]
str_data=f.readframes(nframes)
f.close()
wave_data=np.fromstring(str_data,dtype=np.short)
wave_data.shape=-1,1
if nchannels==2:
    wave_data.shape=-1,2
else:
    pass
wave_data=wave_data.T
time=np.arange(0,nframes)*(1.0/framerate)
plt.subplot(211)
plt.plot(time,wave_data[0],'r-')
plt.xlabel('Time/s')
plt.ylabel('Ampltitude')
plt.title('Num '+'1'+' time/ampltitude')
plt.show()

df=framerate/(nframes-1)
freq=[df*n for n in range(0,nframes)]
transformed=np.fft.fft(wave_data[0])
d=int(len(transformed)/2)
while freq[d]>4000:
    d-=10
freq=freq[:d]
transformed=transformed[:d]
for i,data in enumerate(transformed):
    transformed[i]=abs(data)
plt.subplot(212)

plt.plot(freq,transformed,'b-')
plt.xlabel('Freq/Hz')
plt.ylabel('Ampltitude')
plt.title('Num '+'1'+' freq/ampltitude')
plt.show()