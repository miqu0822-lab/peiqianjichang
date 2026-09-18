import numpy as np, pandas as pd
cols=['Model','Enc','Fus','Reg','FID','SSIM','eta','WIoU','SIoU','Score','Params']
HR=[['A0','DCE','Had','None',19.62,0.970,0.858,0.616,0.550,0.512,228.6],
 ['A1','DCE','CA','None',13.31,0.977,0.869,0.691,0.653,0.598,229.9],
 ['A2','CLIP','Had','SNEMA',14.65,0.975,0.876,0.665,0.602,0.569,237.3],
 ['A3','CLIP','Had','None',14.33,0.975,0.886,0.666,0.571,0.556,237.3],
 ['A4','DCE','CA','SNEMA',12.85,0.977,0.931,0.705,0.586,0.607,229.9],
 ['A5','CLIP','CA','SNEMA',13.79,0.977,0.870,0.694,0.632,0.591,238.6],
 ['A6','DCE','Had','SNEMA',16.52,0.968,0.888,0.612,0.431,0.465,228.6],
 ['A7','CLIP','CA','None',12.95,0.977,0.906,0.708,0.622,0.613,238.6]]
hr=pd.DataFrame(HR,columns=cols).set_index('Model')
hr['E']=np.where(hr.Enc=='CLIP',1,-1); hr['F']=np.where(hr.Fus=='CA',1,-1); hr['R']=np.where(hr.Reg=='SNEMA',1,-1)
def yates(d,m):
    y=d[m].values;E,F,R=d.E.values,d.F.values,d.R.values
    t={'E':E,'F':F,'R':R,'ExF':E*F,'ExR':E*R,'FxR':F*R,'ExFxR':E*F*R}
    return {k:y[c==1].mean()-y[c==-1].mean() for k,c in t.items()}
hr2=hr.copy()
hr2.loc['A6','SIoU']=hr.drop('A6').SIoU.min()
hr2.loc['A6','Score']=hr2.loc['A6','eta']*(0.5*hr2.loc['A6','WIoU']+0.5*hr2.loc['A6','SIoU'])+0.0019
print("imputed A6 score %.6f"%hr2.loc['A6','Score'])
w=yates(hr2,'Score')
print("winsorised effects:", {k:round(v,6) for k,v in w.items()})
# marginal means winsorised
print("DCE/Had win:", (hr2.loc['A0','Score']+hr2.loc['A6','Score'])/2)
print("enc effect Had win %%: %.2f"%(100*((hr.loc['A3','Score']+hr.loc['A2','Score'])/2-(hr2.loc['A0','Score']+hr2.loc['A6','Score'])/2)/((hr2.loc['A0','Score']+hr2.loc['A6','Score'])/2)))
print("fus effect DCE win %%: %.2f"%(100*((hr.loc['A1','Score']+hr.loc['A4','Score'])/2-(hr2.loc['A0','Score']+hr2.loc['A6','Score'])/2)/((hr2.loc['A0','Score']+hr2.loc['A6','Score'])/2)))
# additive check
a0=hr.loc['A0','Score']; addF=hr.loc['A1','Score']-a0; addE=hr.loc['A3','Score']-a0
print("addF %.3f addE %.3f pred %.3f actual %.3f shortfall %.4f"%(addF,addE,a0+addF+addE,hr.loc['A7','Score'],hr.loc['A7','Score']-(a0+addF+addE)))
print("shortfall / smaller increment = %.3f"%(abs(hr.loc['A7','Score']-(a0+addF+addE))/addE))
print("realised / additive increment = %.3f"%((hr.loc['A7','Score']-a0)/(addF+addE)))
print("CLIP increment on top of CA (A7-A1) = %.3f ; standalone (A3-A0)=%.3f ; retained %.1f%%"%(
   hr.loc['A7','Score']-hr.loc['A1','Score'], addE, 100*(hr.loc['A7','Score']-hr.loc['A1','Score'])/addE))
print("CA increment on top of CLIP (A7-A3) = %.3f ; standalone (A1-A0)=%.3f ; retained %.1f%%"%(
   hr.loc['A7','Score']-hr.loc['A3','Score'], addF, 100*(hr.loc['A7','Score']-hr.loc['A3','Score'])/addF))
# SS share winsorised
ss={k:2*v**2 for k,v in w.items()}; tot=sum(ss.values())
print("SS share win:", {k:f"{100*v/tot:.1f}%" for k,v in sorted(ss.items(),key=lambda x:-x[1])})
