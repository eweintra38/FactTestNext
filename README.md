# 🧪 FactTest: Factuality Testing in Large Language Models with Finite-Sample and Distribution-Free Guarantees

<div align="center">

[![arXiv](https://img.shields.io/badge/arXiv-2411.02603-b31b1b.svg)](https://arxiv.org/abs/2411.02603)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


</div>

---

## 👥 Fact Test Paper Authors

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

## 👥 Fact Test (partial) Experiments Reproduction

<table>
<tr>
<td align="center">
<strong>Matan Haroush</strong>
</a>
</td>
<td align="center">
<strong>Itay Lamprecht</strong>
</td>
<td align="center">
<strong>Erez Weintraub</strong>
</td>
<td align="center">
</a>
</td>
</tr>
</table>

---

## 📰 News

- **🎉 May 27, 2025**: Source code released!
- **🎉 May 28, 2025**: Upload all four datasets!
- **🎉 Feb 2026**: Reproduction of Experiments by Technion Team.

---

## Reproduction Results

### ParaRel — Vanilla Entropy (VE5)

**Configuration:** VE5 (Vanilla Entropy, `num_try=5`), α = 0.05, δ = 0.01, τ = -1.6094, Model: OpenLLaMA-3B

| Metric | Our ID | Paper ID (VE5) | Our OOD | Paper OOD |
|---|---|---|---|---|
| **Total samples** | 5,584 | — | 11,180 | — |
| **Pretrained accuracy** | 20.00% | 36.66% | 14.90% | — (Fig. 4 only) |
| **Certain samples** | 63 | — | 163 | — |
| **Certain accuracy** | **26.98%** | **60.54%** | 20.86% | — (Fig. 4 only) |
| **Certain 95% CI** | (15.87%, 38.10%) | — | (14.72%, 26.99%) | — |
| **Uncertain samples** | 5,521 | — | 11,017 | — |
| **Uncertain accuracy** | 19.92% | — | 14.81% | — |
| **FNR (Type II)** | 0.0103 | — | 0.0136 | — |
| **FPR (Type I)** | 0.9848 | 0.0455 | 0.9796 | — (Fig. 4 only) |


### ParaRel — Semantic Entropy (SE5)

**Configuration:** SE5 (Semantic Entropy, `num_try=5`), α = 0.05, δ = 0.01, τ = -5.7775, Model: OpenLLaMA-3B

| Metric | Our ID | Paper ID (SE5) |
|---|---|---|
| **Total samples** | 5,584 | — |
| **Pretrained accuracy** | 20.00% | 36.66% |
| **Pretrained AP** | 0.2728 | — |
| **Certain samples** | 362 | — |
| **Certain accuracy** | **33.70%** | **60.10%** |
| **Certain 95% CI** | (29.01%, 38.67%) | — |
| **Uncertain samples** | 5,222 | — |
| **Uncertain accuracy** | 19.05% | — |
| **FNR (Type II)** | 0.0537 | — |
| **FPR (Type I)** | 0.8908 | — |

> **Note**: Compared to VE5 (τ = -1.6094, 63 certain samples), SE5 uses a much lower threshold (τ = -5.7775) and classifies significantly more samples as certain (362 vs 63). The certain accuracy improves from 26.98% (VE5) to 33.70% (SE5), and the FPR drops from 0.9848 to 0.8908. However, the certain accuracy remains far below the paper's reported 60.10%.


### FEVER — Vanilla Entropy (VE5)

**Configuration:** VE5 (Vanilla Entropy, `num_try=5`), α = 0.05, δ = 0.01, τ = -0.6730, Model: OpenLLaMA-3B

| Metric | Our Reproduction | Paper (VE5) |
|---|---|---|
| **Total samples** | 9,999 | 10,000 |
| **Total accuracy** | 32.47% | — |
| **Pretrained AP** | **0.3825** | **0.3974** |
| **Certain samples** | 8,122 (81.2%) | — |
| **Certain accuracy** | **32.79%** | **60.24%** |
| **Uncertain samples** | 1,877 | — |
| **Uncertain accuracy** | 31.11% | — |
| **FNR (Type II)** | 0.8085 | — |
| **FPR (Type I)** | 0.1799 | 0.0164 |

> **Note**: The FPR (0.18) is much better than ParaRel (~0.98), indicating the threshold is less restrictive. However, the certain accuracy (32.79%) is far below the paper's reported 60.24%, and the FNR (0.81) is very high — meaning the model rejects most correct answers as uncertain. The pretrained AP (0.38) is close to the paper's (0.40), confirming the base model performance is similar.

---

### Why FEVER?

After the initial ParaRel reproduction (see below), the results did not align with the paper. To further validate the framework, we chose to reproduce on the **FEVER** dataset for the following reasons:

- **Multiple-choice format** (3 options: SUPPORTED, REFUTED, NOT ENOUGH INFO) — simple to run, same as WiCE
- **Large dataset** (10k samples) — provides more stable and reproducible estimates compared to WiCE's small test set
- **Clear accuracy improvement** in the paper: Pretrained 39.74% → VE5 60.24% → VE15 62.50%, a solid ~20pp gain
- **Well-controlled Type I error** in the paper (0.0164 for VE5 with OpenLLaMA-3B)
- **WiCE was considered** due to its high pretrained baseline (64.72%), but its small test set leads to noisy estimates and wide confidence intervals, making it harder to confirm reproduction

---

### 🔑 Key Differences: FEVER vs ParaRel

| Aspect | ParaRel | FEVER |
|--------|---------|-------|
| **Format** | Free-form QA (`[question, answer]`) | Multiple-choice A/B/C (`{label, claim, evidence}`) |
| **Inference** | 15 tokens generated, temp=1.0 | 1 token (A/B/C softmax), temp=0.7 |
| **ID/OOD split** | Yes (`--domain ID/OOD`) | No — single test set |
| **Prompt** | `"Question:{q} Answer:"` | `"Evidence:{e}\nClaim:{c}\nQuestion:...\nA:..B:..C:..\nAnswer:"` |
| **Output file** | `ours_{domain}_{n}_vanilla_{model}.json` | `ours_{n}_vanilla_{model}.json` |

---

## 🚀 Quick Start


### 📋 Prerequisites

```bash
# Clone the repository
git clone https://github.com/fannie1208/FactTest.git
cd FactTest

pip install -r requirements.txt
```

---

## 🔧 Usage

### ParaRel Pipeline (α = 0.05)

#### 🎯 Step 1: Collect Calibration Dataset

Navigate to the ParaRel calibration directory:
```bash
cd calibration/pararel
```

Run greedy inference on the training set to split into certain/uncertain:
```bash
python collect_dataset.py \
    --model openlm-research/open_llama_3b
```

This reads `dataset/pararel/training_data.json` and saves:
- `calibration/training_data/pararel_open_llama_3b_certain.json`
- `calibration/training_data/pararel_open_llama_3b_uncertain.json`

#### 🎚️ Step 2: Calibration and Threshold Selection

##### 2a. Compute certainty scores (GPU-intensive):
```bash
python calculate_vanilla_threshold.py \
    --dataset uncertain \
    --model openlm-research/open_llama_3b \
    --num_try 5
```

Saves scores to `calibration/training_data/pararel_uncertain_5_open_llama_3b_certainties.json`.

##### 2b. Compute threshold (CPU-only, fast — uses stored scores):
```bash
python calculate_vanilla_threshold.py \
    --dataset uncertain \
    --model openlm-research/open_llama_3b \
    --num_try 5 \
    --alpha 0.05 \
    --delta 0.01 \
    --stored
```

The threshold (τ) is appended to `calibration/training_data/pararel.txt`.

> **💡 Tip**: The `--stored` flag allows you to quickly recompute thresholds for different α values without re-running the expensive model evaluation.

#### 📈 Step 3: Evaluation on Test Set

```bash
cd evaluation/pararel
python evaluate_vanilla.py \
    --model openlm-research/open_llama_3b \
    --domain ID \
    --num_try 5
```

> **💡 Note**: Use `--domain OOD` for out-of-distribution evaluation. Default is `ID`.

Reads `dataset/pararel/ID_test_pararel.json` (or `OOD_test_pararel.json`) and saves results to `evaluation/pararel/results/`.

#### 📊 Step 4: Calculate Evaluation Metrics

```bash
python eval.py \
    --method vanilla \
    --domain ID \
    --num_try 5 \
    --tau <your_threshold> \
    --model openlm-research/open_llama_3b
```

> **💡 Note**: Replace `<your_threshold>` with the τ value from Step 2b. Use `--domain OOD` for out-of-distribution metrics.

---

### FEVER Pipeline (α = 0.05)

#### 🎯 Step 1: Collect Calibration Dataset

Navigate to the FEVER calibration directory:
```bash
cd calibration/FEVER
```

Run greedy inference on the training set to split into certain/uncertain:
```bash
python collect_dataset.py \
    --dataset fever_10k \
    --model openlm-research/open_llama_3b \
    --result FEVER
```

This reads `dataset/FEVER/fever_10k.json` and saves:
- `calibration/training_data/FEVER_open_llama_3b_certain.json`
- `calibration/training_data/FEVER_open_llama_3b_uncertain.json`

#### 🎚️ Step 2: Calibration and Threshold Selection

##### 2a. Compute certainty scores (GPU-intensive):
```bash
python calculate_vanilla_threshold.py \
    --dataset uncertain \
    --model openlm-research/open_llama_3b \
    --num_try 5
```

Saves scores to `calibration/training_data/FEVER_uncertain_5_open_llama_3b_certainties.json`.

##### 2b. Compute threshold (CPU-only, fast — uses stored scores):
```bash
python calculate_vanilla_threshold.py \
    --dataset uncertain \
    --model openlm-research/open_llama_3b \
    --num_try 5 \
    --alpha 0.05 \
    --delta 0.01 \
    --stored \
    --result FEVER
```

The threshold (τ) is appended to `calibration/training_data/FEVER.txt`.

> **💡 Tip**: The `--stored` flag allows you to quickly recompute thresholds for different α values without re-running the expensive model evaluation.

#### 📈 Step 3: Evaluation on Test Set

```bash
cd evaluation/FEVER
python evaluate_vanilla.py \
    --model openlm-research/open_llama_3b \
    --num_try 5 \
    --tau <your_threshold>
```

> **💡 Note**: Replace `<your_threshold>` with the τ value from Step 2b. The default is `0.5` if omitted.

Reads `dataset/FEVER/fever_10k_test.json` and saves results to `evaluation/FEVER/results/ours_5_vanilla_open_llama_3b.json`.

#### 📊 Step 4: Calculate Evaluation Metrics

```bash
python eval.py \
    --method vanilla \
    --num_try 5 \
    --tau <your_threshold> \
    --model openlm-research/open_llama_3b
```

> **💡 Note**: Replace `<your_threshold>` with the threshold value obtained from Step 2b.

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

