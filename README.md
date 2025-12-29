# Network Intrusion Detection System (ML)

## Summary
This project implements an **end-to-end machine learning pipeline** to detect Network Anomalies and classify attack types.

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

### Final Scores for best bodels:
- **Binary (Logistic):** Test F1-score = 0.98, Test ROC-AUC = 0.9969
- **Multiclass (Linear SVC):**

  Macro F1 = 0.89

  Per-class recall: DoS = 1.00, Probe = 1.00, R2L = 0.96, U2R = 1.00


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

```
git clone <your-repo-url>
cd <repo-name>
```

### 2. Create and activate a virtual environment

python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Start the API

```
python app.py
```

### 5. Test the API in a new terminal(Examples)

**Normal connection**

```
$body = @{
    duration = 0
    protocoltype = "tcp"
    service = "http"
    flag = "SF"
    srcbytes = 181
    dstbytes = 5450
    land = 0
    wrongfragment = 0
    urgent = 0
    hot = 0
    numfailedlogins = 0
    loggedin = 1
    numcompromised = 0
    rootshell = 0
    suattempted = 0
    numroot = 0
    numfilecreations = 0
    numshells = 0
    numaccessfiles = 0
    numoutboundcmds = 0
    ishostlogin = 0
    isguestlogin = 0
    count = 2
    srvcount = 2
    serrorrate = 0.0
    srvserrorrate = 0.0
    rerrorrate = 0.0
    srvrerrorrate = 0.0
    samesrvrate = 1.0
    diffsrvrate = 0.0
    srvdiffhostrate = 0.0
    dsthostcount = 9
    dsthostsrvcount = 9
    dsthostsamesrvrate = 1.0
    dsthostdiffsrvrate = 0.0
    dsthostsamesrcportrate = 0
    dsthostsamedstportrate = 1.0
    dsthostsrvdiffhostrate = 0.0
    dsthostserrorrate = 0.0
    dsthostsrvserrorrate = 0.0
    dsthostrerrorrate = 0.0
    dsthostsrvrerrorrate = 0.0
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://localhost:5000/predict `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Attacked Connection**

```
$body = @{
    duration = 0
    protocoltype = "tcp"
    service = "private"
    flag = "S0"
    srcbytes = 0
    dstbytes = 0
    land = 0
    wrongfragment = 0
    urgent = 0
    hot = 0
    numfailedlogins = 0
    loggedin = 0
    numcompromised = 0
    rootshell = 0
    suattempted = 0
    numroot = 0
    numfilecreations = 0
    numshells = 0
    numaccessfiles = 0
    numoutboundcmds = 0
    ishostlogin = 0
    isguestlogin = 0
    count = 123
    srvcount = 6
    serrorrate = 1
    srvserrorrate = 1
    rerrorrate = 0
    srvrerrorrate = 0
    samesrvrate = 0.05
    diffsrvrate = 0.07
    srvdiffhostrate = 0
    dsthostcount = 255
    dsthostsrvcount = 26
    dsthostsamesrvrate = 0.1
    dsthostdiffsrvrate = 0.05
    dsthostsamesrcportrate = 0
    dsthostsrvdiffhostrate = 0
    dsthostserrorrate = 1
    dsthostsrvserrorrate = 1
    dsthostrerrorrate = 0
    dsthostsrvrerrorrate = 0
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://localhost:5000/predict `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```