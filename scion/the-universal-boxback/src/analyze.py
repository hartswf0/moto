import numpy as np, librosa, json, sys
y,sr=librosa.load(sys.argv[1],sr=22050,mono=True)
tempo,beats=librosa.beat.beat_track(y=y,sr=sr,units='time')
S=np.abs(librosa.stft(y)); f=librosa.fft_frequencies(sr=sr)
low=S[f<150].sum(0); low/=low.max(); lt=librosa.frames_to_time(np.arange(len(low)),sr=sr)
pk=librosa.util.peak_pick(low,pre_max=5,post_max=5,pre_avg=10,post_avg=10,delta=0.08,wait=8); k=lt[pk]
i=np.arange(len(beats)); p=np.polyfit(i,beats,1)
best=None
for per in np.linspace(p[0]-0.004,p[0]+0.004,81):
  for off in np.linspace(-per/2,per/2,121):
    ph=((k-off)/per+0.5)%1-0.5; s=np.mean(np.abs(ph)<0.06)
    if best is None or s>best[0]: best=(s,per,off)
s,per,off=best
rms=librosa.feature.rms(y=y,hop_length=2205)[0]
db=(20*np.log10(rms+1e-9)).tolist()
C=np.vstack([librosa.feature.chroma_cqt(y=y,sr=sr),librosa.feature.mfcc(y=y,sr=sr,n_mfcc=13)])
bt=librosa.frames_to_time(librosa.segment.agglomerative(C,10),sr=sr).tolist()
json.dump({'grid':{'period':per,'offset':off,'bpm':60/per,'kick_alignment':s,'method':'grid search on low-band onsets'},'tempo_librosa':float(np.atleast_1d(tempo)[0]),'sections':bt,'rms_db_0.1s':db},open(sys.argv[2],'w'))
print('bpm',60/per,'off',off,'align',s,'sections',np.round(bt,1))
for a in range(0,174,6): 
  seg=db[a*10:(a+6)*10]; print(a,'b%.1f'%((a-off)/per),round(float(np.mean(seg)),1))
