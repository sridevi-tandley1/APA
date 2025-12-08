---

# **README.md — Mini MLflow + Flask + CI/CD Example**

This project demonstrates a **lightweight, fully local machine-learning workflow** including:

* ✔ Training an ML model
* ✔ Tracking & versioning with **MLflow** (local backend, no Spark)
* ✔ Serving predictions through a **Flask API**
* ✔ Running automated tests & training in **GitHub Actions CI**
* ✔ Optional container deployment (Docker)
---

## 📁 **Project Structure**

```
mini-mlflow-flask-ci/
├─ requirements.txt
├─ data.csv
├─ train.py
├─ model_utils.py
├─ app.py
├─ tests/
│  └─ test_model.py
└─ .github/
   └─ workflows/
      └─ ci.yml
```

---

## 🚀 **1. Setup**

### **Create virtual environment**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

### **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## 📘 **2. Train the Model + Log to MLflow**

```bash
python train.py
```

This creates a local MLflow tracking folder:

```
mlruns/
```

---

## 📊 **3. View MLflow UI**

```bash
mlflow ui --backend-store-uri ./mlruns --port 5000
```

Open: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

You will see:

* metrics
* parameters
* saved model artifact (`salary_model`)
* different model versions (each run)

---

## 🌐 **4. Run the Flask Prediction API**

```bash
python app.py
```

### **Test API (single prediction)**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"experience_years": 4}' \
     http://127.0.0.1:8000/predict
```

### **Test API (batch prediction)**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"instances": [[2],[5],[8]]}' \
     http://127.0.0.1:8000/predict
```

---

## 🧪 **5. Run Tests**

```bash
pytest -q
```

---

## 🤖 **6. GitHub Actions CI/CD**

The workflow automatically:

* installs dependencies
* runs unit tests
* trains the model
* uploads **mlruns** as an artifact

### To activate CI:

Push the repo to GitHub.

Workflow file:

```
.github/workflows/ci.yml
```

---

## 🐳 **7. (Optional) Docker Deployment**

### Build the image:

```bash
docker build -t mini-ml-api .
```

### Run the container:

```bash
docker run -p 8000:8000 mini-ml-api
```

API will be available at:

```
http://127.0.0.1:8000/predict
```

---

## ✅ **Summary**

This project gives you a complete **Module 4.1-ready pipeline**:

| Component  | Tool           | Purpose                             |
| ---------- | -------------- | ----------------------------------- |
| Training   | scikit-learn   | Lightweight regression model        |
| Tracking   | MLflow         | Versioning + metrics + artifacts    |
| Serving    | Flask API      | Real-time predictions               |
| CI/CD      | GitHub Actions | Automated tests + training pipeline |
| Deployment | Docker         | Containerized API ready for cloud   |

---
