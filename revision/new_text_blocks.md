# 新增/替换英文正文（与 manuscript_revised.docx 完全一致）

本文件是 `manuscript_revised.docx` 中所有新写或替换段落的纯文本副本，便于直接复制粘贴到其他版本的稿件里。
表格用 Markdown 表示，原稿中为三线表。

---

## Abstract（整段替换）

Image fidelity alone does not establish the engineering acceptability of generated structural layouts. We train a complete 2 × 2 × 2 factorial of text-guided generative adversarial networks — text encoder (discrete concept encoding, DCE, versus frozen CLIP ViT-B/32), conditioning fusion (Hadamard gating versus cross-attention), and an SN+EMA regularization treatment — at two native resolutions, and evaluate 96 plan–condition pairs grouped into 24 base plans. Decomposing the factorial, rather than reading configuration rankings off a table, yields three results that individual pairwise contrasts cannot show. First, at high resolution the fusion mechanism is the dominant design decision: cross-attention raises ScoreIoU by 0.077 (13.6% of the grand mean), accounts for 63% of the between-configuration sum of squares against 14% for the encoder and 1.5% for regularization, and is favoured in all four background conditions. Second, the encoder and the fusion mechanism act as substitutes rather than as complements: replacing DCE with CLIP is worth +15.1% under Hadamard gating but −0.1% once cross-attention is present, an encoder × fusion interaction of −0.037 that cancels the encoder main effect of +0.037. This quantifies why the fully augmented configuration does not lead. Third, resolution gates the entire comparison: at 256 × 128 no architectural main effect exceeds 0.005, between-configuration variance is 37 times smaller than at high resolution, the full spread of all eight configurations is only 35% of a single high-resolution fusion effect, and the two grids rank the same eight configurations almost independently (Spearman ρ = −0.24). A complementary P01 case study converts 19 source layouts into distinct ETABS 22 models. All models satisfy the specified numerical quality-control checks, but all 16 matched eight-degree models exceed the 0.001 elastic storey-drift benchmark, with governing drifts of 1.31–4.25 times that benchmark, and the configuration with the highest dataset-level composite image score does not produce the lowest drift. These findings separate geometric resemblance, numerical solvability and structural performance as distinct evaluation outcomes, and they relocate the design recommendation from a single winning configuration to a ranked set of design decisions.

## Highlights（整组替换）

- Fusion choice dominates high-resolution fidelity: 63% of between-configuration variance.
- Text encoder and cross-attention are substitutes; their interaction cancels the encoder effect.
- At 256 × 128 every architectural main effect vanishes and rankings do not transfer (ρ = −0.24).
- Cross-attention returns about 13 times the ScoreIoU per added parameter of the CLIP branch.
- Numerical quality-control success does not establish drift acceptability.

## 1 Introduction（第 17 段，一句一致性修改）

We examine these two evaluation levels using eight GAN configurations and a common-plan reconstruction study. A complete factorial design varies text encoding, feature fusion, and SN+EMA regularization at two native resolutions. Decomposing that design into its three main effects and four interactions, rather than listing the twelve single-factor contrasts it contains, describes checkpoint performance on 96 test pairs. Nineteen P01 layouts are then reconstructed in ETABS 22 to distinguish numerical quality control from elastic response assessment. Figure 1 illustrates this pipeline from architectural sketches and design sentences to the final structural design.

## 4.1 Checkpoint-Level Image Fidelity（标题改名 + 末段替换）

原标题 *4.1 Image Fidelity and Objective Specific Optima* → **4.1 Checkpoint-Level Image Fidelity**

At HR the observed ScoreIoU spans 0.465–0.613, and the component metrics do not order the configurations identically: the highest composite, wall-ratio and contour values fall in different rows (A7, A4 and A1, respectively). At LR the same eight configurations span a much narrower 0.449–0.476. The margins between adjacent configurations are small relative to the reported test-group intervals — A7 exceeds A4 by 1.0% of ScoreIoU — so these tables are not read here as a ranking. Section 4.2 instead analyses the same eight cells as the factorial design they form.

---

## 4.2 Factorial Effect Decomposition（全新一节）

The eight configurations form a complete 2 × 2 × 2 design, so the twelve pairwise contrasts of Table 5 can be replaced by the seven orthogonal terms of the design itself. Table 9 reports, for each resolution separately, the effect of every main factor and interaction on ScoreIoU together with its share of the between-configuration sum of squares. Because the eight cells are single evaluated checkpoints rather than replicated training runs, these terms are exact decompositions of the observed grid and not estimates of population effects; we therefore report them alongside the sign-consistency evidence of Table 11, which requires no replication. The twelve individual contrasts are retained as a record in Appendix C.

**Table 9. Factorial decomposition of ScoreIoU (complete 2 × 2 × 2, each resolution analysed separately).**

| Term | HR effect | HR % of mean | HR SS share | LR effect | LR % of mean | LR SS share |
|---|---|---|---|---|---|---|
| Encoder (CLIP − DCE) | +0.0367 | +6.5% | 14.4% | −0.0015 | −0.3% | 0.9% |
| Fusion (cross-attn − Hadamard) | +0.0767 | +13.6% | 62.9% | −0.0030 | −0.6% | 3.6% |
| Regularization (SN+EMA − none) | −0.0118 | −2.1% | 1.5% | +0.0050 | +1.1% | 10.0% |
| Encoder × Fusion | −0.0373 | −6.6% | 14.8% | +0.0105 | +2.3% | 44.1% |
| Encoder × Regularization | +0.0072 | +1.3% | 0.6% | −0.0025 | −0.5% | 2.5% |
| Fusion × Regularization | +0.0052 | +0.9% | 0.3% | +0.0050 | +1.1% | 10.0% |
| Encoder × Fusion × Reg. | −0.0228 | −4.0% | 5.5% | −0.0085 | −1.8% | 28.9% |
| Grand mean | 0.5639 | — | — | 0.4655 | — | — |

Effect = mean(+ level) − mean(− level) over the four cells at each level. SS share is the term’s share of the total between-configuration sum of squares. Computed from the original unrounded checkpoint summaries of Tables 7 and 8; the eight cells are single checkpoints, so the terms are exact for the observed grid and are not estimates across training seeds.

At high resolution the decomposition is strongly concentrated. The fusion mechanism contributes +0.0767 ScoreIoU, 13.6% of the grand mean and 62.9% of the between-configuration sum of squares, against 14.4% for the text encoder and 1.5% for the SN+EMA treatment. Cross-attention is favoured in all four background conditions, with a median contrast of +0.0715 (Table 11); a sign test on four backgrounds cannot reach conventional significance (p = 0.125), but no other factor achieves a unanimous sign pattern at either resolution. Within the evaluated checkpoints, therefore, the conditioning mechanism — not the text encoder and not the regularization package — is the design decision that separates configurations.

The encoder × fusion interaction (−0.0373) is almost exactly as large as the encoder main effect (+0.0367) and opposite in sign, which means the two are not independent design choices. Table 10 gives the marginal means. Under Hadamard gating, replacing DCE with CLIP raises ScoreIoU from 0.4885 to 0.5625 (+15.1%); under cross-attention the same substitution changes ScoreIoU from 0.6025 to 0.6020 (−0.1%). Symmetrically, cross-attention is worth +23.3% on top of DCE but only +7.0% on top of CLIP. The two components therefore behave as substitutes for one another rather than as complements: each supplies a route by which the design condition can modulate image features at finer granularity, and whichever is introduced first captures nearly all of the available gain. Figure 9(b) shows this as the convergence of the two encoder levels.

**Table 10. Marginal means and conditional effects of encoder and fusion at HR (ScoreIoU).**

| Encoder | Hadamard | Cross-attention | Fusion effect |
|---|---|---|---|
| DCE | 0.4885 | 0.6025 | +23.3% |
| CLIP | 0.5625 | 0.6020 | +7.0% |
| Encoder effect | +15.1% | −0.1% | E × F = −0.0373 |
| DCE (A6 winsorised) | 0.5149 | 0.6025 | +17.0% |
| Encoder effect (winsorised) | +9.2% | −0.1% | E × F = −0.0240 |

Each marginal mean averages the two regularization levels. The final two rows repeat the analysis with the anomalous A6-HR SIoU replaced by the seven-configuration minimum (Section 4.4); the substitution pattern is unchanged.

This substitution accounts quantitatively for the behaviour of the fully augmented configuration. Adding cross-attention alone to A0 is worth +0.086 and adding CLIP alone is worth +0.044, so a purely additive model predicts 0.642 for A7; the observed value is 0.613, a shortfall of 0.029. Equivalently, the CLIP upgrade retains only 34% of its standalone value once cross-attention is already present (+0.015 against +0.044), and the stacked pair realises 78% of the sum of the two separate gains. The further addition of SN+EMA (A5) does not close the gap. The ordering A7 > A5 is thus not evidence that regularization is harmful; it is the expected consequence of combining two components that address the same bottleneck.

The SN+EMA treatment has no detectable main effect at this sample size: −0.0118 ScoreIoU, 1.5% of the sum of squares, with two positive and two negative signs across backgrounds and a median contrast of −0.0065. We therefore report it as undetermined under the present protocol rather than as a stability–detail trade-off, which the data do not resolve.

**Table 11. Sign consistency across the four background conditions, and parameter cost.**

| Factor | HR sign pattern | HR median Δ | LR sign pattern | LR median Δ | Added params | ScoreIoU per added M-param (HR) |
|---|---|---|---|---|---|---|
| Fusion (cross-attn) | + + + + (4/4) | +0.0715 | − + 0 + (2/4) | +0.0020 | +1.3 M | 0.066 – 0.073 |
| Encoder (CLIP) | + + + − (3/4) | +0.0295 | − + − − (1/4) | −0.0040 | +8.7 M | 0.005 – 0.007 |
| Regularization (SN+EMA) | − + + − (2/4) | −0.0065 | − + + − (2/4) | +0.0025 | 0 M | — |

The sign pattern lists the four fixed-background contrasts of Table 5 in the order given there; 0 denotes an exactly zero contrast (A4 − A6 at LR). Added parameters are relative to the DCE + Hadamard baseline; the inference-time EMA copy is excluded, as in Figure 8. Marginal efficiency is the ScoreIoU gain over A0 divided by the added parameters, across the two backgrounds in which the component is added.

**Figure 9. Factorial analysis of the eight configurations. (a) Effect decomposition of ScoreIoU at both native resolutions; at LR every term collapses towards zero. (b) Encoder × fusion interaction at HR: the two encoders differ by 15.1% under Hadamard gating and converge to within 0.1% once cross-attention is present, that is, the two components act as substitutes. (c) ScoreIoU rank of the same eight configurations on the two native grids (Spearman ρ = −0.24); the HR leader A7 ranks fourth at LR and the LR leader A0 ranks seventh at HR.**

### 4.2.1 Resolution as a Gating Factor

The two native grids do not behave as two levels of a fourth factor with a simple main effect; the low-resolution grid suppresses the architectural factors altogether. No LR main effect exceeds 0.005 in absolute value, against a largest HR effect of 0.077; the between-configuration variance is 37.5 times smaller (7.1 × 10⁻⁵ against 2.68 × 10⁻³), and the coefficient of variation drops from 9.17% to 1.82%. The comparison that makes this concrete is one of scale: the full spread of all eight configurations at LR (0.027) is only 35% of the single fusion main effect at HR (0.077). Architectural choices that are worth making at 1024 × 512 are not worth making at 256 × 128, where the LR terms with the largest sum-of-squares shares are the interaction terms — that is, residual variation without a consistent direction.

Rankings consequently do not transfer. Across the eight configurations the two grids give Spearman ρ = −0.24 and Kendall τ = −0.11 on ScoreIoU, with the same absence of agreement on WIoU_c (ρ = −0.31), SIoU (ρ = −0.24) and η_SWratio (ρ = −0.06). The HR leader A7 ranks fourth at LR; the LR leader A0 ranks seventh at HR; the weakest HR configuration A6 ranks third at LR (Figure 9c). A configuration selected on one native grid therefore carries essentially no information about its standing on the other, and reporting a single architecture ranking without naming the deployment resolution is not meaningful.

Section 4.6 relates this collapse to the bottleneck capacity of the shared GlobalGenerator, which presents sixteen times fewer spatial query positions at LR than at HR and therefore bounds what any conditioning mechanism can exploit; the same capacity argument predicts the direction of the encoder effect, which is also absent at LR.

---

## 4.3 Metric Decomposition, Composite Behaviour, and Parameter Cost（原 4.2，标题改名 + 末尾新增三段与新表）

The composite ranking is not driven by the three components in equal measure. Regressing ScoreIoU on its standardised components across the eight configurations (Table 12) gives β = 0.675 for SIoU, 0.267 for η_SWratio and 0.233 for WIoU_c at HR (R² = 0.9995), because the components differ sharply in dispersion: the coefficient of variation is 11.9% for SIoU, 5.7% for WIoU_c and 2.7% for η_SWratio. Two consequences follow. First, the asymmetry and unboundedness of η_SWratio discussed in Section 3.4.2, although real, have limited influence on the ordering reported here, since η varies by only 0.073 across all eight configurations. Second, and less comfortably, the ordering is governed principally by SIoU, which is the component whose implementation carries the weakest guarantee: its reference-directed contour matching is not constrained to be one-to-one, so hierarchy, holes and repeated matching can affect the aggregate. Any future revision of the contour-matching rule would therefore act directly on the reported rankings, and we flag this as the principal metric-side limitation of the comparison.

**Table 12. Standardised regression of ScoreIoU on its three components across the eight configurations.**

| Resolution | β WIoU_c | β SIoU | β η_SWratio | R² | CV WIoU_c | CV SIoU | CV η |
|---|---|---|---|---|---|---|---|
| HR (1024 × 512) | +0.233 | +0.675 | +0.267 | 0.9995 | 5.7% | 11.9% | 2.7% |
| LR (256 × 128) | +0.518 | +0.494 | +0.247 | 0.9983 | 2.0% | 2.0% | 0.6% |

β are standardised coefficients; CV is the coefficient of variation of each component across the eight configurations. At HR the composite ranking is driven principally by SIoU, the component with the weakest implementation guarantee (non one-to-one contour matching, Section 3.4.2).

A related caveat can now be quantified. ScoreIoU is averaged per image, and substituting the separately averaged components into the formula does not reproduce that mean; the gap is +0.0101 on average at HR but varies from +0.0019 (A6) to +0.0142 (A5) across configurations. This 0.012 spread is of the same order as the 0.022 that separates A7 from A5, so the covariance between components is itself capable of reordering adjacent configurations.

The parameter accounting reinforces the same conclusion as the effect decomposition. Cross-attention adds 1.3 M generator parameters, 0.6% of the baseline, and is associated with a 14.6% higher mean HR ScoreIoU; the CLIP conditioning branch adds 8.7 M, 3.8% of the baseline, for 6.7%. Expressed as ScoreIoU gained per additional million parameters relative to A0, cross-attention returns 0.066–0.073 and the CLIP branch 0.005–0.007, a difference of roughly thirteen-fold. At LR the marginal return of every addition is negative. Where parameter count is constrained, A4 (DCE + cross-attention + SN+EMA) is within 1.0% of A7 while using 8.7 M fewer parameters.

Table 13 examines the sensitivity of the ordering to the aggregation rule itself, holding the checkpoints fixed.

（其后接原 Table 10 → 现 **Table 13** 及其讨论段，内容未改）

---

## 4.4 Robustness: Influence of the A6-HR Checkpoint（全新一节）

One evaluated checkpoint dominates the largest reported contrasts and requires separate treatment. A6-HR (DCE + Hadamard + SN+EMA) records SIoU = 0.431 against 0.550–0.653 for the other seven HR checkpoints, a standardised deviation of −4.74; its WIoU_c (0.612, z = −2.05) and η_SWratio (0.888, z = +0.11) are within the normal range, and its LR counterpart ranks third of eight. The failure is therefore specific to contour agreement at high resolution and is not reproduced when the same configuration is trained on the low-resolution grid, which is more consistent with a degenerate contour structure in one checkpoint than with a property of the DCE + Hadamard + SN+EMA combination.

Three of the twelve contrasts in Appendix C involve A6, and they are the first, second and fifth largest by absolute magnitude at HR (+30.3%, +22.2%, −9.1%). The mean absolute contrast is 20.5% among the three A6 contrasts and 5.8% among the remaining nine. We therefore repeat the decomposition with A6-HR winsorised to the seven-configuration minimum SIoU. The fusion main effect falls from +0.0767 to +0.0635 and its sum-of-squares share rises to 75%; the encoder main effect falls from +0.0367 to +0.0235 and the encoder × fusion interaction from −0.0373 to −0.0240, so the interaction continues to cancel the main effect and the substitution pattern of Table 10 is preserved (+9.2% under Hadamard gating, −0.1% under cross-attention). Restricting the fusion contrast to the three backgrounds that do not involve A6 leaves +0.0550, or +10.1% relative to the Hadamard cells against which it is measured. The conclusions of Section 4.2 therefore do not depend on this checkpoint, although the magnitudes reported in Appendix C do.

---

## 4.6 Mechanistic Interpretation of the Observed Results（原 4.5，替换两段）

**替换原第 3 段（"The SN+EMA treatment behaves as a stability–detail trade-off…"）：**

The SN+EMA treatment cannot be characterised from these data. Its main effect on ScoreIoU is −0.0118, it accounts for 1.5% of the between-configuration sum of squares, and its four background contrasts split two positive and two negative. Spectral normalization bounds the discriminator and exponential moving averaging smooths the generator, so a stability–detail trade-off is a plausible mechanism, but the present grid neither supports nor excludes it, and the two components were applied jointly and cannot be separated. We report the treatment as undetermined and note that resolving it requires replicated training runs rather than a larger configuration grid.

**替换原第 4 段（"The fact that the fully augmented A5…"）：**

The failure of the fully augmented A5 to outperform A7 is not a general argument for simplicity; it is the specific consequence of the encoder × fusion substitution quantified in Section 4.2. CLIP conditioning and cross-attention both increase the granularity with which the design brief can modulate image features — the first by enlarging the conditioning representation, the second by letting each spatial position query it — and the bottleneck can only exploit so much of that granularity. Once either is present, the marginal value of the other falls to within 0.1% of zero. Adding a third component that acts on neither the representation nor the query mechanism, as SN+EMA does, has no reason to recover the shortfall. The design rule that follows is narrower and more useful than “less is more”: components should be selected so that they relieve different bottlenecks, and two components that address the same one should be costed against each other rather than stacked.

---

## 5 Conclusion（替换第 2 段、第 3 段首句、末段）

**替换第 2 段（原 "Three findings emerge from the factorial comparison…"）：**

Decomposing the complete factorial, rather than ranking the eight configurations, yields three results. First, the conditioning mechanism is the dominant design decision at high resolution: cross-attention contributes +0.077 ScoreIoU, 62.9% of the between-configuration sum of squares, and is favoured in all four background conditions, while the text encoder contributes 14.4% and the SN+EMA treatment 1.5% with no consistent sign. Second, the text encoder and the fusion mechanism are substitutes rather than complements: their interaction (−0.037) cancels the encoder main effect (+0.037), so upgrading the encoder is worth +15.1% under Hadamard gating and −0.1% once cross-attention is present. This is the mechanism behind the failure of the fully augmented A5 to lead, and it generalises beyond this grid as a costing rule: components that relieve the same bottleneck should be chosen between, not accumulated. Third, native resolution gates the comparison rather than shifting it. At 256 × 128 no architectural main effect exceeds 0.005, the full spread of all eight configurations is 35% of a single high-resolution fusion effect, and the two grids rank the configurations almost independently (ρ = −0.24). We therefore report design decisions rather than a winning configuration: the margin between the leading configurations (A7 over A4, 1.0%) is an order of magnitude smaller than the fusion effect that separates the design families, and should not be read as a recommendation.

**替换第 3 段首句（其余 ETABS 内容保留不动）：**

The reconstruction and elastic-assessment stage shows that this image-side ordering does not carry over to mechanical adequacy.

**替换末段（原 "Taken together, the results argue that 'less is more'…"）：**

Two limitations bound these conclusions and set the immediate agenda. The eight cells are single evaluated checkpoints, so the decomposition is exact for the observed grid but is not an estimate of effects across training seeds; the sign-consistency and winsorisation analyses of Sections 4.2 and 4.4 are the strongest evidence available without replication, and replicated runs remain the necessary next step, particularly for the SN+EMA treatment, which the present data leave undetermined. Separately, the high-resolution ordering is governed principally by SIoU (standardised β = 0.675), the metric component whose contour matching is not constrained to be one-to-one; revising that rule would act directly on the reported rankings. Beyond these, the factorial should be extended to conditioning mechanisms that act on the bottleneck in different ways — spatially dense conditioning such as SPADE, or an enlarged bottleneck — since the substitution result implies that further gains will come from relieving a different bottleneck rather than from stacking components that relieve the same one, and future work should test whether explicit geometric or mechanical objectives can close the remaining gap between visual fidelity and drift-limited structural adequacy.

---

## Appendix C Single-Factor Contrast Record（全新附录，收纳原 Table 9）

Table 17 retains the twelve single-factor contrasts of Table 5 as a record of the individual cell comparisons that underlie the decomposition of Section 4.2. Percentages are relative ScoreIoU changes computed from the original unrounded checkpoint summaries; they are not inferential effect estimates across seeds, and three of them involve the A6-HR checkpoint analysed in Section 4.4.

**Table 17. Descriptive relative ScoreIoU changes for 12 single-factor contrasts, computed from the original unrounded checkpoint summaries. Percentages are not inferential effect estimates across seeds.**

（表体为原 Table 9 的 12 组对比，数值未改）

（其后接原 4.3 的三段描述性说明，文字未改）

These contrasts are reported here as a record of the individual cell comparisons. The corresponding main effects, interactions, sign consistency and robustness to the A6-HR checkpoint are given in Sections 4.2 and 4.4.
