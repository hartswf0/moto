import numpy as np, librosa, json, sys
y,sr=librosa.load(sys.argv[1],sr=22050)
tempo,beats=librosa.beat.beat_track(y=y,sr=sr,units='time')
S=np.abs(librosa.stft(y)); f=librosa.fft_frequencies(sr=sr)
low=S[f<150].sum(0); low/=low.max(); lt=librosa.frames_to_time(np.arange(len(low)),sr=sr)
pk=librosa.util.peak_pick(low,pre_max=5,post_max=5,pre_avg=10,post_avg=10,delta=0.08,wait=8); k=lt[pk]
b=np.array(beats); i=np.arange(len(b)); P,O=np.polyfit(i,b,1)
best=None
for per in np.linspace(P-0.004,P+0.004,81):
  for off in np.linspace(-per/2,per/2,101):
    ph=((k-off)/per+0.5)%1-0.5; s=np.mean(np.abs(ph)<0.06)
    if best is None or s>best[0]: best=(s,per,off)
s,per,off=best
rms=librosa.feature.rms(y=y,hop_length=2205)[0]
print('tempo',tempo,'grid bpm',60/per,'off',off,'align',s)
bars=[(round(t,1), round(B,1), round(20*np.log10(rms[int(t*10):int(t*10)+20].mean()+1e-9),1)) for t,B in [(x,(x-off)/per) for x in np.arange(0,len(y)/sr,per*8)]]
print(bars)
json.dump({'grid':{'period':float(per),'offset':float(off),'bpm':float(60/per),'kick_alignment':float(s),'method':'grid search on low-band onsets'},'rms_10hz':[float(v) for v in rms]},open(sys.argv[2],'w'))
