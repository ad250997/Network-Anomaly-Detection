# Network Intrusion Detection System (ML)

## Summary
This project implements an **end-to-end machine learning pipeline** to detect malicious network activity and classify attack types. It demonstrates structured problem-solving across data analysis, statistical validation, modeling, and deployment, with a focus on interpretability and real-world usability.

---

## Problem Statement
Network intrusions are difficult to detect because malicious traffic often resembles normal behavior and attack types are highly imbalanced. The goal of this project is to:

- Reliably detect whether a network connection is malicious  
- Identify the type of attack when one occurs  
- Deliver results suitable for deployment and monitoring  

---

## Targets and Evaluation Metrics

### Targets
- **Binary:** Normal vs Attack  
- **Multiclass:** DoS, Probe, R2L, U2R  

### Metrics
- **Binary:** F1-score, ROC-AUC  
- **Multiclass:** Macro F1-score, per-class recall  

**Final Scores Achieved:**  
*(Add final results here)*

---

## Approach

### Exploratory Data Analysis (EDA)
- Identified skewed traffic distributions and class imbalance  
- Removed near-constant features with minimal predictive value  

### Hypothesis Testing
- Validated key traffic and protocol differences statistically  
- Eliminated features with no meaningful relationship to attacks  

### Modeling
- Adopted a **two-stage classification strategy**:
  - Binary detection as a filtering step  
  - Multiclass classification applied only to detected attacks  
- Evaluated linear and tree-based models with task-specific preprocessing  

---

## Key Insights
- Separating detection and classification improved performance and clarity  
- Linear models performed strongly with appropriate feature treatment  
- Rare attack categories remain challenging due to limited data  

---

## Recommendations
- Deploy binary detection as a real-time safeguard  
- Use attack-type classification as decision support  
- Retrain periodically to adapt to changing network behavior  

---

## Deployment
The system is deployed as a **Flask-based REST API**:

- Binary and multiclass models loaded at startup  
- JSON-based prediction endpoint  
- Early exit for normal traffic to reduce latency  
- Attack-type outputs exposed as **confidence scores**, not true probabilities  

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

