"""Create the synthetic practice datasets used in the Level 1 and Level 2 decks.

All three files are SYNTHETIC: generated with fixed random seeds for teaching,
not real customers. Re-run this script to recreate them exactly:

    python make_lab_data.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(41)

# 1. loan_applications.csv  (Level 1 fairness lab)
#    A biased history: approvals depend on income and on pin_band, and pin_band
#    is correlated with gender, so pin_band acts as a proxy.
n = 2000
gender = rng.choice(["F", "M"], n, p=[0.4, 0.6])
is_female = (gender == "F").astype(int)
age = rng.integers(21, 65, n)
income = np.round(rng.lognormal(np.log(55000), 0.45, n) * np.where(is_female, 0.9, 1.0), -2)
credit_score = np.clip(rng.normal(690, 60, n), 300, 900).round()
pin_band = np.clip(rng.integers(1, 6, n) - is_female * rng.integers(0, 2, n), 1, 5)
logit = -9 + 0.00006 * income + 0.009 * credit_score + 0.35 * pin_band
approved = (rng.uniform(size=n) < 1 / (1 + np.exp(-logit))).astype(int)
pd.DataFrame({"applicant_id": np.arange(1, n + 1), "gender": gender, "is_female": is_female,
              "age": age, "income": income, "credit_score": credit_score,
              "pin_band": pin_band, "approved": approved}).to_csv("loan_applications.csv", index=False)

# 2. claims_data.csv  (Level 2 Poisson GLM lab) - overdispersed on purpose
n = 1500
age = rng.integers(20, 70, n)
income = np.round(rng.normal(60, 18, n).clip(15, 150), 1)          # in thousands
policy_type = rng.choice(["basic", "plus", "premium"], n, p=[0.5, 0.3, 0.2])
mu = np.exp(-1.2 + 0.012 * age + 0.004 * income
            + pd.Series(policy_type).map({"basic": 0.0, "plus": 0.25, "premium": 0.45}).to_numpy())
k = 0.7                                                            # NB dispersion: small k = strong overdispersion
claims = rng.negative_binomial(k, k / (k + mu))
pd.DataFrame({"policy_id": np.arange(1, n + 1), "age": age, "income": income,
              "policy_type": policy_type, "claims": claims}).to_csv("claims_data.csv", index=False)

# 3. customer_churn.csv  (Level 2 survival lab) - right-censored tenure
n = 1200
age = rng.integers(18, 70, n)
engagement = np.round(rng.uniform(0, 1, n), 3)                     # 0 = inactive, 1 = very active
hazard = 0.04 * np.exp(-0.015 * (age - 40) - 1.4 * (engagement - 0.5))
time_to_churn = rng.exponential(1 / hazard)
observed_until = rng.uniform(3, 36, n)                             # months each customer was watched
pd.DataFrame({"customer_id": np.arange(1, n + 1), "age": age, "engagement": engagement,
              "tenure": np.round(np.minimum(time_to_churn, observed_until), 1) + 0.1,
              "churned": (time_to_churn <= observed_until).astype(int)}).to_csv("customer_churn.csv", index=False)

print("Wrote loan_applications.csv, claims_data.csv, customer_churn.csv (synthetic)")
