# 🧪 FactTest: Factuality Testing in Large Language Models with Finite-Sample and Distribution-Free Guarantees

<div align="center">

[![arXiv](https://img.shields.io/badge/arXiv-2411.02603-b31b1b.svg)](https://arxiv.org/abs/2411.02603)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


</div>

---

## 👥 Authors

<table>
<tr>
<td align="center">
<a href="https://scholar.google.com/citations?user=o2lsU8YAAAAJ&hl=en">
<strong>Fan Nie</strong>
</a>
</td>
<td align="center">
<strong>Xiaotian Hou</strong>
</td>
<td align="center">
<strong>Shuhang Lin</strong>
</td>
<td align="center">
<a href="https://www.james-zou.com/">
<strong>James Zou</strong>
</a>
</td>
<td align="center">
<a href="https://www.huaxiuyao.io/">
<strong>Huaxiu Yao</strong>
</a>
</td>
<td align="center">
<a href="https://linjunz.github.io/index.html">
<strong>Linjun Zhang</strong>
</a>
</td>
</tr>
</table>

---

## 📰 News

- **🎉 May 27, 2025**: Source code released!
- **🎉 May 28, 2025**: Upload all four datasets!

---

## 🚀 Quick Start

This repository provides tools for testing factuality in Large Language Models with statistical guarantees. Follow the steps below to get started with ParaRel as an example.

### 📋 Prerequisites

```bash
# Clone the repository
git clone https://github.com/fannie1208/FactTest.git
cd FactTest

pip install -r requirements.txt
```

---

## 🔧 Usage

### 🎯 Step 1: Calibration

Navigate to the calibration directory:
```bash
cd calibration/pararel
```

#### 📊 Calibration Dataset Construction
```bash
python collect_dataset.py --model openlm-research/open_llama_3b
```

#### 🎚️ Calibration and Threshold Selection

**For Vanilla Entropy Score Function:**

Initial calibration run (computes and saves scores):
```bash
python calculate_vanilla_threshold.py \
    --model openlm-research/open_llama_3b \
    --alpha 0.05 \
    --num_try 15
```

**Reusing Saved Scores:**

After the initial run, you can quickly calculate thresholds for different alpha values using the stored scores:
```bash
python calculate_vanilla_threshold.py \
    --model openlm-research/open_llama_3b \
    --alpha 0.1 \
    --stored \
    --num_try 15
```

The `--stored` flag allows you to experiment with different significance levels without re-running the expensive model evaluation.

### 📈 Step 2: Evaluation

```bash
cd evaluation/pararel
python evaluate_vanilla.py \
    --model openlm-research/open_llama_3b \
    --num_try 15
```

#### 📊 Calculate Evaluation Metrics
After evaluation, compute the metrics using:
```bash
python eval.py \
    --model openlm-research/open_llama_3b \
    --num_try 15 \
    --method vanilla \
    --tau <your_threshold>
```

> **💡 Note**: Replace `<your_threshold>` with the threshold value obtained from the calibration step.

---

## Reproduction Results

### Why FEVER?

After the initial ParaRel reproduction (see below), the results did not align with the paper. To further validate the framework, we chose to reproduce on the **FEVER** dataset for the following reasons:

- **Multiple-choice format** (3 options: SUPPORTED, REFUTED, NOT ENOUGH INFO) — simple to run, same as WiCE
- **Large dataset** (10k samples) — provides more stable and reproducible estimates compared to WiCE's small test set
- **Clear accuracy improvement** in the paper: Pretrained 39.74% → VE5 60.24% → VE15 62.50%, a solid ~20pp gain
- **Well-controlled Type I error** in the paper (0.0164 for VE5 with OpenLLaMA-3B)
- **WiCE was considered** due to its high pretrained baseline (64.72%), but its small test set leads to noisy estimates and wide confidence intervals, making it harder to confirm reproduction

### ParaRel — Vanilla Entropy (VE5)

**Configuration:** VE5 (Vanilla Entropy, `num_try=5`), α = 0.05, δ = 0.01, τ = -1.6094, Model: OpenLLaMA-3B

| Metric | ID (ParaRel) | OOD (ParaRel-OOD) |
|---|---|---|
| **Total samples** | 5,584 | 11,180 |
| **Total accuracy** | 20.00% | 14.90% |
| **Certain samples** | 63 | 163 |
| **Certain accuracy** | 26.98% | 20.86% |
| **Certain 95% CI** | (15.87%, 38.10%) | (14.72%, 26.99%) |
| **Uncertain samples** | 5,521 | 11,017 |
| **Uncertain accuracy** | 19.92% | 14.81% |
| **FNR (Type II)** | 0.0103 | 0.0136 |
| **FPR (Type I)** | 0.9848 | 0.9796 |

> **Note**: The high FPR (~0.98) indicates the threshold is too restrictive with `num_try=5`, classifying only ~1% of samples as certain. The paper uses `num_try=15` and reports ~60–67% certain accuracy on ParaRel ID with OpenLLaMA-3B.

---

## Citation

If you find this work useful, please cite our paper:

```bibtex
@misc{nie2024facttest,
      title={FactTest: Factuality Testing in Large Language Models with Finite-Sample and Distribution-Free Guarantees}, 
      author={Fan Nie and Xiaotian Hou and Shuhang Lin and James Zou and Huaxiu Yao and Linjun Zhang},
      year={2024},
      eprint={2411.02603},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2411.02603}, 
}
```

