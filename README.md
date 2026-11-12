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
├─ pytest.ini
├─ Dockerfile
└─ tests/
   ├─ test_model.py
   └─ test_api.py

.github/workflows/ci.yml   (at the repository root, where GitHub Actions looks for it)
```

---

## 🚀 **1. Setup**

### **Create virtual environment**

```bash
cd mini-mlflow-flask-ci
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

This creates a local MLflow tracking database and artifact folder, and registers a new version of `salary_model`:

```
mlflow.db
mlruns/
```

Recent MLflow releases refuse the old file-only `./mlruns` tracking store, so this project tracks runs in SQLite. Both files are git-ignored: never commit them.

---

## 📊 **3. View MLflow UI**

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Open: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

You will see:

* metrics
* parameters
* the logged model (`salary_model`)
* registered model versions (one per training run) under **Models**

---

## 🌐 **4. Run the Flask Prediction API**

```bash
python app.py
```

`python app.py` is the development server (works on Windows, Mac and Linux). On Mac or Linux you can also run the production server: `gunicorn --bind 0.0.0.0:8000 app:app`.

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

The tests train the model, check a simple quality gate (salary must rise with experience), and call the API with good and bad payloads.

---

## 🤖 **6. GitHub Actions CI/CD**

The workflow automatically:

* installs dependencies
* runs the tests (including the quality gate)
* trains and registers the model
* uploads `mlflow.db` and `mlruns/` as a build artifact

It runs on every push or pull request that touches `mini-mlflow-flask-ci/`. The workflow file lives at the repository root:

```
.github/workflows/ci.yml
```

---

## 🐳 **7. (Optional) Docker Deployment**

### Build the image (from inside `mini-mlflow-flask-ci/`):

```bash
docker build -t mini-ml-api .
```

The build installs the requirements, trains the model inside the image, and serves it with gunicorn.

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
