# 🧪 FactTest: Semantic Entropy (SE) Pipeline

This document describes the **Semantic Entropy (SE)** method for uncertainty quantification, as an alternative to Vanilla Entropy (VE).

---

## 🔑 Key Differences: Semantic Entropy vs Vanilla Entropy

| Aspect | Vanilla Entropy (VE) | Semantic Entropy (SE) |
|--------|---------------------|----------------------|
| **Certainty score** | Token-level entropy only | Clusters answers via DeBERTa NLI, then computes entropy |
| **Extra model** | None | `microsoft/deberta-v2-xlarge-mnli` |
| **Script suffix** | `*_vanilla_*` | `*_semantic_*` |
| **`--method` flag** | `vanilla` | `semantic` |
| **GPU memory** | Lower | Higher (loads DeBERTa + LLM) |

**How SE works:**
1. Generate `num_try` answers with temperature sampling
2. Use DeBERTa-v2-xlarge-mnli to cluster semantically equivalent answers
3. Aggregate log-likelihoods within each semantic cluster
4. Compute entropy over the aggregated clusters

---

## 🔧 Usage

### ParaRel — Semantic Entropy Pipeline (α = 0.05)

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

> **💡 Note**: This step is identical to the VE pipeline — the same calibration data is used.

#### 🎚️ Step 2: Calibration and Threshold Selection

##### 2a. Compute certainty scores (GPU-intensive):
```bash
python calculate_semantic_threshold.py \
    --dataset uncertain \
    --model openlm-research/open_llama_3b \
    --num_try 5
```

Saves scores to `calibration/training_data/pararel_uncertain_5_open_llama_3b_semantic_certainties.json`.

> **⚠️ Warning**: This step loads both the LLM and DeBERTa model — ensure sufficient GPU memory (~16GB+ recommended).

##### 2b. Compute threshold (CPU-only, fast — uses stored scores):
```bash
python calculate_semantic_threshold.py \
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
python evaluate_semantic.py \
    --model openlm-research/open_llama_3b \
    --domain ID \
    --num_try 5
```

> **💡 Note**: Use `--domain OOD` for out-of-distribution evaluation. Default is `ID`.

Reads `dataset/pararel/ID_test_pararel.json` (or `OOD_test_pararel.json`) and saves results to `evaluation/pararel/results/ours_ID_5_semantic_open_llama_3b.json`.

#### 📊 Step 4: Calculate Evaluation Metrics

```bash
python eval.py \
    --method semantic \
    --domain ID \
    --num_try 5 \
    --tau <your_threshold> \
    --model openlm-research/open_llama_3b
```

> **💡 Note**: Replace `<your_threshold>` with the τ value from Step 2b. Use `--domain OOD` for out-of-distribution metrics.

---

### FEVER — Semantic Entropy Pipeline (α = 0.05)

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

> **💡 Note**: This step is identical to the VE pipeline.

#### 🎚️ Step 2: Calibration and Threshold Selection

##### 2a. Compute certainty scores (GPU-intensive):
```bash
python calculate_semantic_threshold.py \
    --dataset uncertain \
    --model openlm-research/open_llama_3b \
    --num_try 5
```

Saves scores to `calibration/training_data/FEVER_uncertain_5_open_llama_3b_semantic_certainties.json`.

##### 2b. Compute threshold (CPU-only, fast — uses stored scores):
```bash
python calculate_semantic_threshold.py \
    --dataset uncertain \
    --model openlm-research/open_llama_3b \
    --num_try 5 \
    --alpha 0.05 \
    --delta 0.01 \
    --stored \
    --result FEVER
```

The threshold (τ) is appended to `calibration/training_data/FEVER.txt`.

#### 📈 Step 3: Evaluation on Test Set

```bash
cd evaluation/FEVER
python evaluate_semantic.py \
    --model openlm-research/open_llama_3b \
    --num_try 5 \
    --tau <your_threshold>
```

> **💡 Note**: Replace `<your_threshold>` with the τ value from Step 2b.

Reads `dataset/FEVER/fever_10k_test.json` and saves results to `evaluation/FEVER/results/ours_5_semantic_open_llama_3b.json`.

#### 📊 Step 4: Calculate Evaluation Metrics

```bash
python eval.py \
    --method semantic \
    --num_try 5 \
    --tau <your_threshold> \
    --model openlm-research/open_llama_3b
```

---

## 📁 Output Files Summary

| Dataset | Step | Output File |
|---------|------|-------------|
| ParaRel | 2a | `calibration/training_data/pararel_uncertain_5_open_llama_3b_semantic_certainties.json` |
| ParaRel | 2b | `calibration/training_data/pararel.txt` (appended) |
| ParaRel | 3 | `evaluation/pararel/results/ours_{ID\|OOD}_5_semantic_open_llama_3b.json` |
| FEVER | 2a | `calibration/training_data/FEVER_uncertain_5_open_llama_3b_semantic_certainties.json` |
| FEVER | 2b | `calibration/training_data/FEVER.txt` (appended) |
| FEVER | 3 | `evaluation/FEVER/results/ours_5_semantic_open_llama_3b.json` |

---

## 🛠️ Requirements

The SE pipeline requires the additional DeBERTa model:
- `microsoft/deberta-v2-xlarge-mnli` (~900MB)

This is automatically downloaded on first run. Ensure your environment has:
```bash
pip install transformers accelerate torch scipy tqdm
```

---

## 📊 Expected Behavior

Semantic Entropy typically:
- **Lower entropy values** than VE (fewer unique semantic clusters than unique token sequences)
- **More robust** to paraphrases and minor wording changes
- **Slower** due to pairwise NLI comparisons between unique answers

The threshold τ from SE calibration will generally differ from VE — always use the threshold computed with `calculate_semantic_threshold.py`.
