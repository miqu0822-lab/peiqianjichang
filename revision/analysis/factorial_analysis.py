import numpy as np, pandas as pd, itertools
from scipy import stats
pd.set_option('display.width',200); pd.set_option('display.max_columns',50)

# Table 7 (HR) and Table 8 (LR)
cols = ['Model','Enc','Fus','Reg','FID','SSIM','eta','WIoU','SIoU','Score','Params']
HR = [
 ['A0','DCE','Had','None',19.62,0.970,0.858,0.616,0.550,0.512,228.6],
 ['A1','DCE','CA','None',13.31,0.977,0.869,0.691,0.653,0.598,229.9],
 ['A2','CLIP','Had','SNEMA',14.65,0.975,0.876,0.665,0.602,0.569,237.3],
 ['A3','CLIP','Had','None',14.33,0.975,0.886,0.666,0.571,0.556,237.3],
 ['A4','DCE','CA','SNEMA',12.85,0.977,0.931,0.705,0.586,0.607,229.9],
 ['A5','CLIP','CA','SNEMA',13.79,0.977,0.870,0.694,0.632,0.591,238.6],
 ['A6','DCE','Had','SNEMA',16.52,0.968,0.888,0.612,0.431,0.465,228.6],
 ['A7','CLIP','CA','None',12.95,0.977,0.906,0.708,0.622,0.613,238.6]]
LR = [
 ['A0','DCE','Had','None',37.93,0.940,0.857,0.558,0.524,0.476,228.6],
 ['A1','DCE','CA','None',36.13,0.932,0.852,0.526,0.497,0.449,229.9],
 ['A2','CLIP','Had','SNEMA',36.60,0.932,0.864,0.539,0.507,0.464,237.3],
 ['A3','CLIP','Had','None',38.65,0.930,0.852,0.534,0.511,0.458,237.3],
 ['A4','DCE','CA','SNEMA',34.85,0.935,0.855,0.545,0.523,0.470,229.9],
 ['A5','CLIP','CA','SNEMA',33.09,0.937,0.848,0.549,0.522,0.468,238.6],
 ['A6','DCE','Had','SNEMA',36.66,0.939,0.858,0.557,0.509,0.470,228.6],
 ['A7','CLIP','CA','None',38.32,0.936,0.848,0.548,0.524,0.469,238.6]]
hr = pd.DataFrame(HR,columns=cols).set_index('Model')
lr = pd.DataFrame(LR,columns=cols).set_index('Model')

# coded factors: -1 = DCE / Hadamard / None ; +1 = CLIP / CrossAttn / SN+EMA
def code(df):
    d = df.copy()
    d['E'] = np.where(d.Enc=='CLIP',1,-1)
    d['F'] = np.where(d.Fus=='CA',1,-1)
    d['R'] = np.where(d.Reg=='SNEMA',1,-1)
    return d
hr, lr = code(hr), code(lr)

METRICS = ['Score','WIoU','SIoU','eta','SSIM','FID']

def yates(d, metric):
    """Full 2^3 effect decomposition. Effect = mean(+) - mean(-) for each term."""
    y = d[metric].values
    E,F,R = d.E.values, d.F.values, d.R.values
    terms = {'E (CLIP-DCE)':E, 'F (CA-Had)':F, 'R (SNEMA-none)':R,
             'ExF':E*F, 'ExR':E*R, 'FxR':F*R, 'ExFxR':E*F*R}
    out = {}
    for k,c in terms.items():
        out[k] = y[c==1].mean() - y[c==-1].mean()
    out['grand mean'] = y.mean()
    return out

print("="*90); print("1. FACTORIAL EFFECT DECOMPOSITION (full 2x2x2, effect = mean(+)-mean(-))"); print("="*90)
rows=[]
for res,d in [('HR',hr),('LR',lr)]:
    for m in METRICS:
        e = yates(d,m); e['res']=res; e['metric']=m; rows.append(e)
eff = pd.DataFrame(rows).set_index(['res','metric'])
order = ['grand mean','E (CLIP-DCE)','F (CA-Had)','R (SNEMA-none)','ExF','ExR','FxR','ExFxR']
print(eff[order].round(4).to_string())

print()
print("--- ScoreIoU effects as % of grand mean ---")
for res,d in [('HR',hr),('LR',lr)]:
    e = yates(d,'Score'); gm = e['grand mean']
    s = {k: 100*e[k]/gm for k in order[1:]}
    print(res, {k:round(v,2) for k,v in s.items()}, f"| grand mean={gm:.4f}")

print()
print("--- variance explained by each term (sum of squares share, ScoreIoU) ---")
for res,d in [('HR',hr),('LR',lr)]:
    e = yates(d,'Score')
    ss = {k: 2*(e[k]**2) for k in order[1:]}   # SS = n*effect^2/... ; proportional form
    tot = sum(ss.values())
    print(res, {k: f"{100*v/tot:.1f}%" for k,v in sorted(ss.items(),key=lambda x:-x[1])})

print(); print("="*90); print("2. HR vs LR RANKING AGREEMENT"); print("="*90)
for m in METRICS:
    rho,p = stats.spearmanr(hr[m],lr[m]); tau,pt = stats.kendalltau(hr[m],lr[m])
    r,pr = stats.pearsonr(hr[m],lr[m])
    print(f"{m:6s} Spearman rho={rho:+.3f} (p={p:.3f})  Kendall tau={tau:+.3f}  Pearson r={r:+.3f}")
print()
print("Rank order HR (best->worst) by ScoreIoU:", list(hr.Score.sort_values(ascending=False).index))
print("Rank order LR (best->worst) by ScoreIoU:", list(lr.Score.sort_values(ascending=False).index))
print("Spread: HR ScoreIoU range = %.3f (%.1f%% of mean); LR range = %.3f (%.1f%% of mean)"%(
    hr.Score.max()-hr.Score.min(), 100*(hr.Score.max()-hr.Score.min())/hr.Score.mean(),
    lr.Score.max()-lr.Score.min(), 100*(lr.Score.max()-lr.Score.min())/lr.Score.mean()))
print("Coefficient of variation: HR %.3f%%  LR %.3f%%"%(100*hr.Score.std()/hr.Score.mean(),100*lr.Score.std()/lr.Score.mean()))
for m in METRICS:
    print(f"  CV {m:6s}: HR {100*hr[m].std()/abs(hr[m].mean()):5.2f}%   LR {100*lr[m].std()/abs(lr[m].mean()):5.2f}%")

print(); print("="*90); print("3. METRIC CORRELATION STRUCTURE (across 8 configurations)"); print("="*90)
for res,d in [('HR',hr),('LR',lr)]:
    print(f"\n-- {res} Spearman --")
    print(d[METRICS+['Params']].corr(method='spearman').round(3).to_string())

print(); print("="*90); print("4. COMPOSITE DECOMPOSITION: what drives ScoreIoU?"); print("="*90)
for res,d in [('HR',hr),('LR',lr)]:
    print(f"\n-- {res} --")
    for m in ['WIoU','SIoU','eta']:
        rho,_ = stats.spearmanr(d[m],d.Score); r,_ = stats.pearsonr(d[m],d.Score)
        print(f"  {m:5s} vs ScoreIoU: Spearman {rho:+.3f}  Pearson {r:+.3f}  CV={100*d[m].std()/d[m].mean():.2f}%")
    # reconstruct nominal score
    d['Score_nom'] = d.eta*(0.5*d.WIoU+0.5*d.SIoU)
    d['gap'] = d.Score - d.Score_nom
    print("  per-image mean vs formula-of-means gap (covariance term):")
    print("   ", d[['Score','Score_nom','gap']].round(4).to_string().replace("\n","\n    "))
    print(f"    mean gap = {d.gap.mean():+.4f}  ({100*d.gap.mean()/d.Score.mean():+.2f}% of mean score), range {d.gap.min():+.4f}..{d.gap.max():+.4f}")

print(); print("="*90); print("5. PARAMETER EFFICIENCY"); print("="*90)
for res,d in [('HR',hr),('LR',lr)]:
    dd = d.copy()
    dd['score_per_100M'] = dd.Score/dd.Params*100
    base = dd.loc['A0']
    dd['dScore_vs_A0'] = dd.Score-base.Score
    dd['dParams_vs_A0'] = dd.Params-base.Params
    dd['score_per_Mparam_added'] = np.where(dd.dParams_vs_A0>0, dd.dScore_vs_A0/dd.dParams_vs_A0*1000, np.nan)
    print(f"\n-- {res} --")
    print(dd[['Params','Score','score_per_100M','dScore_vs_A0','dParams_vs_A0','score_per_Mparam_added']].round(4).to_string())
# cost of CLIP branch
print("\nCLIP branch cost (+8.7M ~ +3.8% params). Mean ScoreIoU by encoder:")
for res,d in [('HR',hr),('LR',lr)]:
    g = d.groupby('Enc').Score.mean()
    print(f"  {res}: DCE={g['DCE']:.4f}  CLIP={g['CLIP']:.4f}  diff={g['CLIP']-g['DCE']:+.4f} ({100*(g['CLIP']-g['DCE'])/g['DCE']:+.2f}%)")
print("Cross-attention cost (+1.3M ~ +0.6% params). Mean ScoreIoU by fusion:")
for res,d in [('HR',hr),('LR',lr)]:
    g = d.groupby('Fus').Score.mean()
    print(f"  {res}: Had={g['Had']:.4f}  CA={g['CA']:.4f}  diff={g['CA']-g['Had']:+.4f} ({100*(g['CA']-g['Had'])/g['Had']:+.2f}%)")

print(); print("="*90); print("6. CONDITIONAL (SIMPLE) EFFECTS - the interaction made explicit"); print("="*90)
for res,d in [('HR',hr),('LR',lr)]:
    print(f"\n-- {res} ScoreIoU simple effects --")
    print("  Fusion effect (CA - Had) within each background:")
    for enc in ['DCE','CLIP']:
        for reg in ['None','SNEMA']:
            sub=d[(d.Enc==enc)&(d.Reg==reg)]
            ca=sub[sub.Fus=='CA'].Score.iloc[0]; ha=sub[sub.Fus=='Had'].Score.iloc[0]
            print(f"    {enc:4s}/{reg:5s}: {ca-ha:+.4f}  ({100*(ca-ha)/ha:+5.1f}%)")
    print("  Encoder effect (CLIP - DCE) within each background:")
    for fus in ['Had','CA']:
        for reg in ['None','SNEMA']:
            sub=d[(d.Fus==fus)&(d.Reg==reg)]
            cl=sub[sub.Enc=='CLIP'].Score.iloc[0]; dc=sub[sub.Enc=='DCE'].Score.iloc[0]
            print(f"    {fus:4s}/{reg:5s}: {cl-dc:+.4f}  ({100*(cl-dc)/dc:+5.1f}%)")
    print("  Regularization effect (SN+EMA - none) within each background:")
    for enc in ['DCE','CLIP']:
        for fus in ['Had','CA']:
            sub=d[(d.Enc==enc)&(d.Fus==fus)]
            sn=sub[sub.Reg=='SNEMA'].Score.iloc[0]; no=sub[sub.Reg=='None'].Score.iloc[0]
            print(f"    {enc:4s}/{fus:4s} : {sn-no:+.4f}  ({100*(sn-no)/no:+5.1f}%)")

print(); print("="*90); print("7. RESOLUTION AS A FACTOR (HR-LR paired)"); print("="*90)
comb = pd.DataFrame({'HR':hr.Score,'LR':lr.Score})
comb['diff']=comb.HR-comb.LR; comb['rel%']=100*comb['diff']/comb.LR
print(comb.round(4).to_string())
print(f"\nmean HR-LR gain = {comb['diff'].mean():+.4f} ({comb['rel%'].mean():+.1f}%), range {comb['rel%'].min():+.1f}%..{comb['rel%'].max():+.1f}%")
w = stats.wilcoxon(comb.HR,comb.LR); print("Wilcoxon signed-rank HR vs LR:",w)
# how large is resolution vs architecture?
print(f"Resolution main effect on ScoreIoU = {hr.Score.mean()-lr.Score.mean():+.4f}")
print(f"Largest architecture main effect HR = {max(abs(yates(hr,'Score')[k]) for k in ['E (CLIP-DCE)','F (CA-Had)','R (SNEMA-none)']):.4f}")
print(f"Full HR architecture span (best-worst) = {hr.Score.max()-hr.Score.min():.4f}")

print(); print("="*90); print("8. THREE-WAY INTERACTION / 'DIMINISHING STACK' TEST"); print("="*90)
for res,d in [('HR',hr),('LR',lr)]:
    a0=d.loc['A0','Score']
    add_F=d.loc['A1','Score']-a0     # add cross-attn to A0
    add_E=d.loc['A3','Score']-a0     # add CLIP to A0
    add_R=d.loc['A6','Score']-a0     # add SN+EMA to A0
    pred_all=a0+add_F+add_E+add_R
    actual=d.loc['A5','Score']
    pred_EF=a0+add_E+add_F; act_EF=d.loc['A7','Score']
    print(f"-- {res} --")
    print(f"  A0 baseline                  = {a0:.4f}")
    print(f"  +cross-attn alone (A1)       = {add_F:+.4f}")
    print(f"  +CLIP alone (A3)             = {add_E:+.4f}")
    print(f"  +SN+EMA alone (A6)           = {add_R:+.4f}")
    print(f"  additive prediction for A7 (E+F) = {pred_EF:.4f} ; actual A7 = {act_EF:.4f} ; shortfall = {act_EF-pred_EF:+.4f}")
    print(f"  additive prediction for A5 (all) = {pred_all:.4f} ; actual A5 = {actual:.4f} ; shortfall = {actual-pred_all:+.4f} ({100*(actual-pred_all)/pred_all:+.1f}%)")
import numpy as np, pandas as pd
from scipy import stats
exec(open('analyze.py').read().split("print(\"=\"*90)")[0])  # reuse data frames hr, lr

def yates(d, metric):
    y=d[metric].values; E,F,R=d.E.values,d.F.values,d.R.values
    t={'E':E,'F':F,'R':R,'ExF':E*F,'ExR':E*R,'FxR':F*R,'ExFxR':E*F*R}
    return {k: y[c==1].mean()-y[c==-1].mean() for k,c in t.items()}

print("="*90);print("A. OUTLIER DIAGNOSTICS - is A6-HR a degenerate checkpoint?");print("="*90)
for m in ['Score','WIoU','SIoU','eta','SSIM','FID']:
    v=hr[m]; others=v.drop('A6')
    z=(v['A6']-others.mean())/others.std()
    print(f"  HR {m:6s}: A6={v['A6']:.4f}  others mean={others.mean():.4f} sd={others.std():.4f}  z={z:+.2f}")
print()
v=hr['SIoU']; print("  HR SIoU sorted:", v.sort_values().round(3).to_dict())
print("  gap A6 -> next lowest = %.3f ; spread of remaining seven = %.3f"%(v.sort_values().iloc[1]-v.min(), v.drop('A6').max()-v.drop('A6').min()))
print()
print("  LR counterpart A6-LR Score=%.3f (rank %d of 8) -> the HR collapse is not reproduced at LR"%(
    lr.loc['A6','Score'], list(lr.Score.sort_values(ascending=False).index).index('A6')+1))
print("  WIoU_c A6-HR=%.3f is normal (rank %d of 8); only SIoU collapses -> contour-level failure, not segmentation-level"%(
    hr.loc['A6','WIoU'], list(hr.WIoU.sort_values(ascending=False).index).index('A6')+1))

print();print("="*90);print("B. INFLUENCE OF A6 ON THE REPORTED CONTRASTS");print("="*90)
full=yates(hr,'Score')
print("  Full-design HR effects:", {k:round(v,4) for k,v in full.items()})
# Which Table-9 contrasts involve A6?
print("  Table 9 contrasts involving A6: A6->A4 (+30.3%, fusion), A6->A2 (+22.2%, encoder), A0->A6 (-9.1%, reg)")
print("  -> 3 of 12 reported contrasts, and they are the 1st, 2nd and 5th largest |Delta| at HR.")
tab9=[('A0->A1','Fus',16.7),('A3->A7','Fus',10.2),('A6->A4','Fus',30.3),('A2->A5','Fus',3.8),
      ('A0->A3','Enc',8.7),('A1->A7','Enc',2.5),('A6->A2','Enc',22.2),('A4->A5','Enc',-2.6),
      ('A0->A6','Reg',-9.1),('A1->A4','Reg',1.5),('A3->A2','Reg',2.3),('A7->A5','Reg',-3.6)]
t=sorted(tab9,key=lambda x:-abs(x[2]))
print("  HR contrasts ranked by |Delta%|:", [(a,b,c) for a,b,c in t])
a6=[x for x in t if 'A6' in x[0]]
print("  mean |Delta| with A6 = %.1f%% ; without A6 = %.1f%%"%(
    np.mean([abs(x[2]) for x in tab9 if 'A6' in x[0]]), np.mean([abs(x[2]) for x in tab9 if 'A6' not in x[0]])))
# recompute fusion effect excluding the A6-involving cell pair
print()
print("  Fusion effect (HR ScoreIoU), all four backgrounds: ", [round(x,4) for x in
      [hr.loc['A1','Score']-hr.loc['A0','Score'], hr.loc['A7','Score']-hr.loc['A3','Score'],
       hr.loc['A4','Score']-hr.loc['A6','Score'], hr.loc['A5','Score']-hr.loc['A2','Score']]])
f3=[hr.loc['A1','Score']-hr.loc['A0','Score'], hr.loc['A7','Score']-hr.loc['A3','Score'], hr.loc['A5','Score']-hr.loc['A2','Score']]
print("  mean fusion effect incl. A6 pair = %+.4f ; excl. A6 pair = %+.4f (%.0f%% of original)"%(
      np.mean(f3+[hr.loc['A4','Score']-hr.loc['A6','Score']]), np.mean(f3),
      100*np.mean(f3)/np.mean(f3+[hr.loc['A4','Score']-hr.loc['A6','Score']])))
print("  -> fusion effect survives: still %+.1f%% relative to the Hadamard cells it is measured against."%(
      100*np.mean(f3)/np.mean([hr.loc['A0','Score'],hr.loc['A3','Score'],hr.loc['A2','Score']])))

print();print("="*90);print("C. WINSORISED / IMPUTED RE-ANALYSIS (A6-HR SIoU set to 7-config min)");print("="*90)
hr2=hr.copy()
hr2.loc['A6','SIoU']=hr.drop('A6').SIoU.min()       # 0.550
hr2.loc['A6','Score']=hr2.loc['A6','eta']*(0.5*hr2.loc['A6','WIoU']+0.5*hr2.loc['A6','SIoU'])+0.0019
print("  A6 imputed ScoreIoU = %.4f (was %.4f)"%(hr2.loc['A6','Score'],hr.loc['A6','Score']))
w=yates(hr2,'Score')
print("  Effects with imputed A6:", {k:round(v,4) for k,v in w.items()})
print("  Effects with original A6:", {k:round(v,4) for k,v in full.items()})
ss=lambda e:{k:2*e[k]**2 for k in e}
for nm,e in [('original',full),('imputed',w)]:
    s=ss(e); tot=sum(s.values())
    print(f"  SS share ({nm}):", {k:f"{100*v/tot:.0f}%" for k,v in sorted(s.items(),key=lambda x:-x[1])})

print();print("="*90);print("D. SIGN CONSISTENCY TEST (non-parametric, no seed replication needed)");print("="*90)
for res,d in [('HR',hr),('LR',lr)]:
    print(f"-- {res} --")
    for fac,pairs in [('Fusion  (CA-Had)',[('A1','A0'),('A7','A3'),('A4','A6'),('A5','A2')]),
                      ('Encoder (CLIP-DCE)',[('A3','A0'),('A7','A1'),('A2','A6'),('A5','A4')]),
                      ('Reg     (SNEMA-none)',[('A6','A0'),('A4','A1'),('A2','A3'),('A5','A7')])]:
        ds=[d.loc[a,'Score']-d.loc[b,'Score'] for a,b in pairs]
        npos=sum(x>0 for x in ds)
        # exact sign test, 4 backgrounds
        p=stats.binomtest(max(npos,4-npos),4,0.5).pvalue
        print(f"  {fac}: signs {['+' if x>0 else '-' for x in ds]}  ({npos}/4 positive)  two-sided sign test p={p:.3f}  median Delta={np.median(ds):+.4f}")

print();print("="*90);print("E. WHAT THE COMPOSITE IS ACTUALLY MEASURING");print("="*90)
for res,d in [('HR',hr),('LR',lr)]:
    import numpy.linalg as la
    X=d[['WIoU','SIoU','eta']].values
    Xs=(X-X.mean(0))/X.std(0)
    y=(d.Score.values-d.Score.mean())/d.Score.std()
    beta,*_=la.lstsq(Xs,y,rcond=None)
    print(f"  {res} standardised regression of ScoreIoU on components: WIoU={beta[0]:+.3f} SIoU={beta[1]:+.3f} eta={beta[2]:+.3f}  R2={1-((Xs@beta-y)**2).sum()/ (y**2).sum():.4f}")
    # share of rank variance
    for m,w_ in zip(['WIoU','SIoU','eta'],beta):
        print(f"      contribution of {m}: |beta|*CV = {abs(w_)*d[m].std()/d[m].mean()*100:.2f} (relative units)")

print();print("="*90);print("F. RESOLUTION x ARCHITECTURE: effect compression");print("="*90)
for m in ['Score','WIoU','SIoU','eta']:
    eh=yates(hr,m); el=yates(lr,m)
    comp=[abs(eh[k])/max(abs(el[k]),1e-9) for k in ['E','F','R']]
    print(f"  {m:6s}: |HR effect| / |LR effect|  E={comp[0]:6.1f}x  F={comp[1]:6.1f}x  R={comp[2]:6.1f}x")
print()
print("  Total between-configuration variance (ScoreIoU): HR var=%.6f  LR var=%.6f  ratio=%.1fx"%(
    hr.Score.var(), lr.Score.var(), hr.Score.var()/lr.Score.var()))
print("  LR full span (%.4f) vs HR single fusion effect (%.4f): ratio %.2f"%(
    lr.Score.max()-lr.Score.min(), yates(hr,'Score')['F'], (lr.Score.max()-lr.Score.min())/yates(hr,'Score')['F']))
