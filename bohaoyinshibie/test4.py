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

plt.subplot(2,1,1)
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

plt.subplot(2,1,2)
plt.plot(freq,transformed,'b-')
plt.xlabel('Freq/Hz')
plt.ylabel('Ampltitude')
plt.title('Num '+'1'+' freq/ampltitude')
plt.show()

local_max=[]
#num=[]
for i in np.arange(1,len(transformed)-1):
    if transformed[i]>transformed[i-1] and transformed[i]>transformed[i+1]:
        local_max.append(transformed[i])
local_max=sorted(local_max)
loc1=np.where(transformed==local_max[-1])
freq_1=freq[loc1[0][0]]
loc1=np.where(transformed==local_max[-2])
freq_2=freq[loc1[0][0]]
if freq_1<freq_2:
    freq_1,freq_2=freq_2,freq_1
print(freq_1,freq_2)#freq_1为第二共振峰，freq_2为第一共振峰
#num.append((freq_1,freq_2))    
#print(num)