import numpy as np 
import wave 
from matplotlib import pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.utils import make_chunks
import tkinter as tk
 
#以500ms为单位切割sound.wav音频
myaudio = AudioSegment.from_file("sound11.wav" , "wav") 
chunk_length_ms = 500 # 分块的毫秒数
chunks = make_chunks(myaudio, chunk_length_ms) #将文件切割成1秒每块

#保存切割的音频到文件
for i, chunk in enumerate(chunks):
    chunk_name = "chunka{0}.wav".format(i)
    print ("exporting", chunk_name)
    chunk.export(chunk_name, format="wav")

#把识别出的号码保存到数组List中
List=[1 for a in range(0,11)]
#逐段导入切割好的音频，进入循环，识别号码
for a in range(0,11):

    #打开wav文件 ，open返回一个的是一个Wave_read类的实例，
    #通过调用它的方法读取WAV文件的格式和数据。
    #读取格式信息  
    #一次性返回所有的WAV文件的格式信息，
    #wave模块只支持非压缩的数据，因此可以忽略最后两个信息，即：压缩类型，压缩类型的描述
    snd = wavfile.read('chunk'+str(a)+'.wav')
    f=wave.open(r'chunk'+str(a)+'.wav','rb')
    params=f.getparams()
    nchannels,samplewidth,framerate,nframes=params[:4]
    #它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 
    # 采样频率, 采样点数, 压缩类型, 压缩类型的描述。
    str_data=f.readframes(nframes)
    #读取波形数据  
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

    #plt.subplot(2,1,1)
    #plt.plot(time,wave_data[0],'r-')
    #plt.xlabel('Time/s')
    #plt.ylabel('Ampltitude')
    #plt.title('Num '+str(a+1)+' time/ampltitude')
    #plt.show()

    #傅里叶变换，时域图转化为频域图
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

    #plt.subplot(2,1,2)
    #plt.plot(freq,transformed,'b-')
    #plt.xlabel('Freq/Hz')
    #plt.ylabel('Ampltitude')
    #plt.title('Num '+str(a+1)+' time/ampltitude')
    #plt.show()

    #读取第一峰和第二峰的峰值
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
    #print(freq_1,freq_2)

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
    #print(freq_2)
    

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
            freq_1=1477
    elif freq_1>1477 and freq_1<=1633:
        if freq_1-1477<1633-freq_1:
            freq_1=1477
        else:
            freq_1=1633
    elif freq_1>1633:
        freq_1=1633
    #print(freq_1)


    
    vala=[697,770,852,941]
    valb=[1209,1336,1477,1633]
    #def jm(freq_2,freq_1):                #通过两个共振峰选择对应的数字
    if freq_2==vala[0]:
        if freq_1==valb[0]:
            b=1
            #print(1)
            List[a]=b
        elif freq_1==valb[1]:
            b=2
            #print(2)
            List[a]=b
        elif freq_1==valb[2]:
            b=3
            #print(3)
            List[a]=b
            
    elif freq_2==vala[1]:
        if freq_1==valb[0]:
            b=4
            #print(4)
            List[a]=b
        elif freq_1==valb[1]:
            b=5
            #print(5)
            List[a]=b
        elif freq_1==valb[2]:
            b=6
            #print(6)
            List[a]=b

    elif freq_2==vala[2]:
        if freq_1==valb[0]:
            b=7
            #print(7)
            List[a]=b
        elif freq_1==valb[1]:
            b=8
            #print(8)
            List[a]=b
        elif freq_1==valb[2]:
            b=9
            #print(9)
            List[a]=b
            
    elif freq_2==vala[3]:
        if freq_1==valb[1]:
            b=0
            #print(0)
            List[a]=b
print(List)

# 第1步，实例化object，建立窗口window
window = tk.Tk()
 
# 第2步，给窗口的可视化起名字
window.title('拨号音识别')
 
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('300x200')  # 这里的乘是小x
 
# 第4步，在图形界面上设定标签
var = tk.StringVar()    
# 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
l = tk.Label(window, textvariable=var, bg='black',
 fg='white', font=('Arial', 12), width=30, height=2)
# 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，
# 这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
l.pack()
 
# 定义一个函数功能（内容自己自由编写），
# 供点击Button按键时调用，调用命令参数command=函数名
on_hit = False
def hit_me():
    global on_hit
    if on_hit == False:
        on_hit = True
        var.set(List)
    else:
        on_hit = False
        var.set('')
# 第5步，在窗口界面设置放置Button按键
b = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, 
command=hit_me)

b.pack()
 
# 第6步，主窗口循环显示
window.mainloop()
