import numpy as np 
import wave 
from matplotlib import pyplot as plt
from scipy.io import wavfile

snd = wavfile.read('dtmf-1.wav')
f=wave.open(r"dtmf-1.wav","rb")
params=f.getparams()
nchannels,samplewidth,framerate,nframes=params[:4]
#n通道，采样宽度，采样器，无样本
print(nframes)
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
print(freq_1,freq_2)

#定义第一共振峰的比较方法
if freq_2<=697:
    freq_2=697
elif freq_2>697 and freq_2<=770:
    if freq_2-697<770-freq_2:
        freq_2=697
    else:
        freq_2=770
elif freq_2>770 and freq_2<=852:
    if freq_2-770<852-freq_2:
        freq_2=770
    else:
        freq_2=852
elif freq_2>852 and freq_2<=941:
    if freq_2-852<941-freq_2:
        freq_2=852
    else:
        freq_2=941
elif freq_2>941:
    freq_2=941
print(freq_2)

#定义第二共振峰的比较方法
if freq_1<=1209:
    freq_1=1209
elif freq_1>1209 and freq_1<=1336:
    if freq_1-1209<1336-freq_1:
        freq_1=1209
    else:
        freq_1=1336
elif freq_1>1336 and freq_1<=1477:
    if freq_1-1336<1477-freq_1:
        freq_1=1336
    else:
        freq_1=1447
elif freq_1>1447 and freq_1<=1633:
    if freq_1-1477<1633-freq_1:
        freq_1=1477
    else:
        freq_1=1633
elif freq_1>1633:
    freq_1=1633
print(freq_1)

vala=[697,770,852,941]
valb=[1209,1336,1477,1633]
#def jm(freq_2,freq_1):                #通过两个共振峰选择对应的数字
if freq_2==vala[0]:
    if freq_1==valb[0]:
        print(1)
    elif freq_1==valb[1]:
        print(2)
    elif freq_1==valb[2]:
        print(3)
        
elif freq_2==vala[1]:
    if freq_1==valb[0]:
        print(4)
    elif freq_1==valb[1]:
        print(5)
    elif freq_1==valb[2]:
        print(6)

elif freq_2==vala[2]:
    if freq_1==valb[0]:
        print(7)
    elif freq_1==valb[1]:
        print(8)
    elif freq_1==valb[2]:
        print()
        
elif freq_2==vala[3]:
    if freq_1==valb[1]:
        print(0)
        
#while 1:                         #利用while循环一直调用
 #   a = int(input('第一共振峰：',freq_2))
 #   b = int(input('第二共振峰：freq_1'))
    
   # a=adz(freq_2)
    #b=bdz(freq_1)
    #vala=[697,770,852,941]
    #valb=[1209,1336,1477,1633]
    #jm(freq_2,)