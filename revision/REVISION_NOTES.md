# 实验数据分析改写说明

对象：`manuscript.docx`（*Image Fidelity and Mechanical Screening in Text Guided Structural Plan Generation*）
产物：`manuscript_revised.docx`（在原稿上直接改，保留全部原有格式、字体、三线表样式与图片）

改写依据是《论文修改方案：强化实验数据分析与结论》与 `analysis/factorial_results.txt`。
ETABS 部分（原 4.4、附录 A/B）的**内容一字未动**，只更新了因插入新表新图而变化的表号图号。

---

## 一、做了什么

把一个完整的 2×2×2 因子设计从"12 组两两对比"升级为"主效应 + 交互项 + 方差归因 + 稳健性检验"，
并把结论从"哪个配置最好"改写为"哪个设计决策最重要"。

| 位置 | 操作 |
|---|---|
| Abstract | 整段替换：三条因子分解结论进正文中部；ETABS 两句保留原意 |
| Highlights | 五条整组替换 |
| 1 Introduction | 一句一致性修改（"twelve single-factor contrasts" → 主效应/交互项） |
| 3.4.4 | 交叉引用 Table 10 → Table 13 |
| 4.1 | 标题改为 *Checkpoint-Level Image Fidelity*；末段删去"谁第一"的论断，改为指向 4.2 |
| **4.2（新）** | *Factorial Effect Decomposition*，含 Table 9/10/11 + Figure 9 + 4.2.1 *Resolution as a Gating Factor* |
| 4.3（原 4.2） | 标题扩为 *Metric Decomposition, Composite Behaviour, and Parameter Cost*；末尾新增三段 + Table 12；原 Table 10 移入此节改号为 Table 13 |
| **4.4（新）** | *Robustness: Influence of the A6-HR Checkpoint*，异常点影响力 + winsorise 重算 |
| 4.5（原 4.4） | 仅标题顺延，ETABS 内容未动 |
| 4.6（原 4.5） | 标题顺延；替换 SN+EMA 段与 A5 段 |
| 5 Conclusion | 替换第 2 段、第 3 段首句、末段 |
| **附录 C（新）** | *Single-Factor Contrast Record*，收纳原 Table 9（12 组对比，改号 Table 17）及原 4.3 的三段描述 |

## 二、表号 / 图号对照

插入四张新表和一张新图后必须顺延编号。**ETABS 章节的文字没有改，只改了它引用的编号。**

| 原 | 现 | 内容 |
|---|---|---|
| Table 7 / 8 | 不变 | HR / LR 逐配置结果 |
| — | **Table 9** | 因子分解（7 项，两分辨率分开） |
| — | **Table 10** | HR 边际均值与条件效应（含 winsorise 行） |
| — | **Table 11** | 符号一致性 + 参数成本 |
| — | **Table 12** | ScoreIoU 对三分量的标准化回归 |
| Table 10 | Table 13 | 聚合方式敏感性 |
| Table 11 | Table 14 | 19 个 P01 ETABS 模型 |
| Table 12 | Table 15 | A7-HR 三工况 |
| Table 13 | Table 16 | 附录 B 位移角利用率 |
| Table 9 | Table 17 | 12 组单因子对比（移入附录 C） |
| Figure 1–8 | 不变 | — |
| — | **Figure 9** | 三面板因子分析图（已嵌入，600 dpi） |
| Figure 9 | Figure 10 | P01 重建几何与响应 |

全稿交叉引用已逐条核对，无残留旧编号。

## 三、对原方案中四处数字的更正

改写时逐项复核了方案里的数值（`analysis/verify_reported_numbers.py` 可复算），发现四处需要更正，
`manuscript_revised.docx` 里用的是更正后的说法：

1. **可加性缺口的百分比说反了。** 方案写"shortfall = 0.029 or 34% of the smaller of the two increments"，
   但 0.029 / 0.044 = 66%，不是 34%。34% 是另一回事：CLIP 增益在已有交叉注意力时**保留下来的比例**
   （+0.015 对 +0.044 = 34%）。同样，"recovers about two thirds"也不准确——实际叠加后拿到两项单独增益之和的
   **78%**（+0.101 / +0.130）。正文已改为：
   *"a shortfall of 0.029. Equivalently, the CLIP upgrade retains only 34% of its standalone value once
   cross-attention is already present (+0.015 against +0.044), and the stacked pair realises 78% of the sum of
   the two separate gains."*
2. **"every LR main effect falls below 0.005" 卡在边界上。** LR 正则化主效应正好是 +0.0050，不是"低于"。
   摘要、4.2.1 与结论一律改为 **"no architectural main effect exceeds 0.005"**。
3. **winsorise 后的交互项。** 方案写 −0.0241，精确值是 **−0.0240**（脚本 round 到 4 位输出 −0.024）。Table 10 已用 −0.0240。
4. **LR 融合的符号模式里有一个精确的 0。** A4 与 A6 在 LR 下同为 0.470，差值恰为 0.000，脚本把它计成了"−"。
   Table 11 改为 **"− + 0 +"**，并在表注里说明 0 代表恰好为零的对比。

## 四、一处结构性处理

方案给的新 4.2.1 第三段（GlobalGenerator 瓶颈、64×32 = 2048 对 16×8 = 128）与原稿 4.5 节第 2 段几乎逐字重复。
两处都留会被审稿人当成冗余。处理方式是：**原稿 4.5（现 4.6）那段机理解释保持原样不动**，
4.2.1 末尾改成一句指向 4.6 的交叉引用，同时把"同一容量论证也预测编码器效应方向"这层意思保留下来。

## 五、还没做、需要你本地数据的部分

方案第五部分的三项增量分析都需要逐图评测记录（96 × 8 × 2 的单图分数），已发表的汇总值算不出来，因此本次未做：

1. **把 cluster bootstrap 置信区间搬进 Table 7/8，并对 12 组对比（或 7 个因子项）做配对重采样。**
   现在 CI 只出现在 Figure 5（现仍为 Figure 5）里，正文和表格一个数字都没有。这是用现有数据能拿到的最大增量。
2. **混合效应模型** `ScoreIoU ~ Encoder * Fusion * Reg + (1|base_plan) + (1|condition_variant)`，两分辨率各拟合一次，
   可把 4.2 的论断从"exact decomposition of the observed grid"升级为真正的推断。
3. **≥3 个 seed**（至少 A0/A6 与 A1/A4 两对），这是唯一能解决 SN+EMA 的办法，也能确认 A6-HR 的塌陷是偶发还是系统性的。

另外两点提请注意：

- **图片物理位置。** 新 Figure 9 按首次引用顺序编号（4.1 先引 Figures 5–8，4.2 再引 Figure 9），编号规则是对的；
  但在 Word 里它的图片位置排在 Figure 5 之前（因为新 4.2 排在原 4.2 之前）。投稿若要求图片按顺序排版，
  两个办法：把图集中放到文末（多数期刊接受），或者把这张图改号为 Figure 5、原 5–8 顺延为 6–9。需要的话我来改。
- **本环境的 LibreOffice 无法加载任何 docx（对原始文件同样报错），所以没能生成 PDF 预览。**
  文件本身结构完好：zip 校验通过、`document.xml` 解析正常、10 个图片部件（原 9 + 新增 1），python-docx 可正常重新打开。
  请在 Word 里打开确认排版。

## 六、文件清单

```
revision/
├── manuscript_revised.docx          改好的稿件（直接用这个）
├── new_text_blocks.md               所有新写/替换段落的纯文本副本，便于粘到其他版本
├── REVISION_NOTES.md                本文件
├── figures/
│   ├── Figure9_factorial.png        600 dpi 位图（已嵌入 docx）
│   └── Figure9_factorial.pdf        矢量版
└── analysis/
    ├── factorial_analysis.py        原分析脚本
    ├── factorial_results.txt        脚本完整输出
    ├── verify_reported_numbers.py   复核第三节四处更正的脚本
    ├── build_lib.py / build.py / content.py   生成 manuscript_revised.docx 的脚本
```

复现改写：`build_lib.py` 里的 `SRC` 指向原始 `manuscript.docx` 路径，改好后在 `analysis/` 目录下
（需要 `Figure9_factorial.png` 在同级目录）运行 `python3 build.py` 即可重新生成。
