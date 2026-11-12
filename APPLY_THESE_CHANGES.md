# How to apply this patch to github.com/sridevi-tandley1/APA

## 1. Remove these files from the public repository
They are copyrighted, cached or stale. Keep your own private copies.

| File | Why remove it |
|---|---|
| `Predictive Analytics for Dummies - John Wiley & Sons. Anasse Bari, Mohamed Chaouchi, Tommy Jung.pdf` | Full copyrighted book in a public repo. The hub now links the Wiley India page instead. |
| `Conjoint Analysis_CaseStudy.pdf` | Darden School Foundation note, "All rights reserved". The hub now links the Darden store. |
| `mini-mlflow-flask-ci/mlruns/` | Its `meta.yaml` points to `mlflow-artifacts:/0`, which makes `python train.py` crash on a fresh clone. |
| `mini-mlflow-flask-ci/__pycache__/` | Compiled cache files: never commit these. |
| `Module3_Time_Series_Forecasting copy.ipynb` | Check first. It differs from `Module3_Time_Series_Forecasting.ipynb` (15 cells vs 20), so keep whichever is current and delete or rename the other. |

## 2. Copy these files in, keeping the folder paths
- `.gitignore` → repository root
- `.github/workflows/ci.yml` → repository root (GitHub Actions only reads workflows from here)
- `README.md` → repository root (replaces the current one)
- everything in `mini-mlflow-flask-ci/` → replaces the files of the same name
- `Advanced_Predictive_Analytics_Module2.ipynb` and `Full_Telco_End_to_End_Worked_Solution.ipynb` → repository root (replace the current ones)
- `data/` → repository root (new folder: the synthetic datasets the deck labs use)
- **New (Modules 3–5):** `Module3_TimeSeries_Lab.ipynb`, `Module4_Deployment_Lab.ipynb`, `Module5_Applications_Lab.ipynb` → repository root. These back every code slide in the Level 3, 4 and 5 decks and ran top to bottom with 0 errors (outputs saved).
- `Mod3_Final_Time Series_UseCase.ipynb` → replaces the current one (two deprecation fixes; runs clean)

## 3. Using git (optional)
```bash
git rm --cached -r "mini-mlflow-flask-ci/mlruns" "mini-mlflow-flask-ci/__pycache__"
git rm "Predictive Analytics for Dummies - John Wiley & Sons. Anasse Bari, Mohamed Chaouchi, Tommy Jung.pdf"
git rm "Conjoint Analysis_CaseStudy.pdf"
# copy the patch files in, then:
git add .
git commit -m "Fix deploy demo for current MLflow, add CI and Dockerfile, remove copyrighted PDFs"
git push
```
Deleting a file does not remove it from git history. If the copyrighted PDFs must disappear completely, rewrite the history (for example with `git filter-repo`) or recreate the repository.

## What was fixed in `mini-mlflow-flask-ci`
1. **Training crashed on a fresh clone.** The committed `mlruns` pointed to an MLflow server, and MLflow 3.x refuses the old `./mlruns` file store. The demo now tracks runs in `sqlite:///mlflow.db` and registers each model version.
2. **`pytest` could not import `train`.** Added `pytest.ini` with `pythonpath = .`.
3. **Feature-name warnings.** Predictions now use a DataFrame with the training column names.
4. **Bad input returned an HTML 415 page.** The API now returns a JSON 400 error for missing, non-JSON or non-numeric input, and a 503 if no model has been trained yet.
5. **The debug server was always on and open to the network.** It now listens on 127.0.0.1, with debug off unless `FLASK_DEBUG=1`.
6. **The README promised CI and Docker files that didn't exist.** Added `ci.yml`, a `Dockerfile` (gunicorn) and `.dockerignore`.
7. **`requirements.txt` was bloated.** It listed pyspark, fastapi, uvicorn, evidently and linters the code never imports, plus duplicates. It now lists only what the demo uses, with minimum versions.
8. **Tests are more useful.** Added API tests and a simple quality gate: salary must rise with experience.

## What was fixed in the notebooks
**Advanced_Predictive_Analytics_Module2.ipynb.** On current libraries the old file hit 9 errors.
- `mean_squared_error(..., squared=False)` no longer exists in scikit-learn 1.6 and later. It is now `np.sqrt(mean_squared_error(...))`, in 3 cells.
- The mini-project checked for `*_data_sample.csv` but loaded `*_data_samples.csv`, a typo.
- The Part 1 CSVs had no `customer_id` column, so every mini-project merge failed. The mini-project now adds the ID when it's missing.
- The MLP did not converge. It now uses `max_iter=2000, early_stopping=True`.
- `!pip install lifelines` is now `%pip install`, which installs into the notebook's own kernel.
- Result: the whole notebook runs top to bottom with 0 errors (outputs saved).

**Full_Telco_End_to_End_Worked_Solution.ipynb.** It stopped with "dataset not found" unless students downloaded the Kaggle file themselves. If the file is missing, it now downloads IBM's public copy of the same Telco data from GitHub. It ran top to bottom with 0 errors.

## The Module 3 forecasting notebooks that were NOT replaced
`Module3_Time_Series_Forecasting.ipynb`, `Module3_Time_Series_Forecasting copy.ipynb` and `Module3_TimeSeriesForecasting1.1.ipynb` have saved errors
(scipy/sklearn import failures, missing `pycaret.time_series` and `darts`, a `pd` NameError). Their first 10–12 cells are pip/conda environment-repair commands
(uninstall matplotlib, create a conda env, restart the kernel) that cannot run inside a notebook on Colab. **Recommendation:** keep one of them as an "advanced reference" with a
note that it needs a dedicated environment (`pip install pycaret darts` on Python 3.10/3.11), or retire them. The new `Module3_TimeSeries_Lab.ipynb` covers the same syllabus
(SARIMAX, Holt-Winters, Prophet, LSTM/GRU, structural models, rolling CV, Optuna, VAR, CRPS, Monte Carlo) without those dependencies.

## The `data/` folder
`make_lab_data.py` recreates three **synthetic** teaching datasets with fixed seeds:
- `loan_applications.csv` — Level 1 fairness lab. It has a built-in approval gap and a pin-code proxy.
- `claims_data.csv` — Level 2 Poisson lab. It is overdispersed on purpose.
- `customer_churn.csv` — Level 2 survival lab. Tenure is right-censored.
- `retail_sales_monthly.csv` — Level 3 and 4 labs (monthly sales with ad spend, a moving Diwali flag and a 2020 lockdown).
- `energy_demand_daily.csv` — Level 3 LSTM/GRU lab.

The deck code was run against these files, and every snippet ran without errors or warnings.

## Tested
- With MLflow 3.18.0, scikit-learn 1.9.1, Flask 3.1.3 and Python 3.13 (November 2026): `pytest` gave 4 passed, then `python train.py`, then gunicorn with `/health` and `/predict` calls.
- **Not tested:** the Docker image build (no Docker daemon was available) and the GitHub Actions run (it only runs once pushed).
