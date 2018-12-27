import numpy as np    #numpy 用于计算的库，np代指numpy
import wave
from matplotlib import pyplot as plt
from scipy.io import wavfile
snd = wavfile.read('dtmf-3.wav')
f=wave.open(r"dtmf-3.wav","rb")
#打开wav文件 ，open返回一个的是一个Wave_read类的实例，
# 通过调用它的方法读取WAV文件的格式和数据。
#读取格式信息  
#一次性返回所有的WAV文件的格式信息，
# 它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采  
#样频率, 采样点数, 压缩类型, 压缩类型的描述。
# wave模块只支持非压缩的数据，因此可以忽略最后两个信息
params=f.getparams()
nchannels,samplewidth,framerate,nframes=params[:4]
#n通道，采样宽度，采样器，无样本
str_data=f.readframes(nframes)#读取波形数据  
#读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位）
f.close()#关闭文件f
wave_data=np.fromstring(str_data,dtype=np.short)
#将波形数据转换成数组
#需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组  
wave_data.shape=-1,1
#将wave_data数组改为1列，行数自动匹配。
#在修改shape的属性时，需使得数组的总长度不变。
if nchannels==2:
    wave_data.shape=-1,2
else:
    pass
wave_data=wave_data.T
time=np.arange(0,nframes)*(1.0/framerate)
#通过取样点数和取样频率计算出每个取样的时间
plt.subplot(211)
plt.plot(time,wave_data[0],'r-')
plt.xlabel('Time/s')
plt.ylabel('Ampltitude')
plt.title('Num '+'3'+' time/ampltitude')
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
plt.title('Num '+'3'+' freq/ampltitude')
plt.show()
