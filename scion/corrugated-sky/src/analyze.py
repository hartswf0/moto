import numpy as np, librosa, json, sys
y,sr=librosa.load(sys.argv[1],sr=22050)
tempo,beats=librosa.beat.beat_track(y=y,sr=sr,units='time')
S=np.abs(librosa.stft(y)); f=librosa.fft_frequencies(sr=sr)
low=S[f<150].sum(0); low/=low.max(); lt=librosa.frames_to_time(np.arange(len(low)),sr=sr)
pk=librosa.util.peak_pick(low,pre_max=5,post_max=5,pre_avg=10,post_avg=10,delta=0.08,wait=8); k=lt[pk]
b=np.array(beats); i=np.arange(len(b)); P0=np.polyfit(i,b,1)[0]
best=None
for per in np.linspace(P0*0.99,P0*1.01,81):
  for off in np.linspace(0,per,120,endpoint=False):
    ph=((k-off)/per+0.5)%1-0.5; s=np.mean(np.abs(ph)<0.06)
    if best is None or s>best[0]: best=(s,per,off)
s,per,off=best
rms=librosa.feature.rms(y=y,hop_length=2205)[0]
prof=[(round(j*0.1,1),round(float(20*np.log10(v+1e-9)),1)) for j,v in enumerate(rms)]
json.dump({'grid':{'period':per,'offset':off,'bpm':60/per,'kick_alignment':s,'method':'grid search on low-band onsets'},'tempo_librosa':float(np.atleast_1d(tempo)[0]),'rms_0p1s':prof},open(sys.argv[2],'w'))
print('bpm',60/per,'offset',off,'align',s,'librosa',tempo)
# energy per 2 beats
for bb in range(0,int(len(y)/sr/per),8):
  t=off+bb*per; seg=rms[int(t*10):int((t+8*per)*10)]
  print(f'b{bb} t{t:.1f} {20*np.log10(seg.mean()+1e-9):.1f}dB')
