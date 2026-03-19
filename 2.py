# =============
# House Prices 
# =============

import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor

# Load data
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

test_ids = test["Id"]

# Target transformation
y = np.log1p(train["SalePrice"])
X = train.drop("SalePrice", axis=1)

# Encode categorical variables
for col in X.select_dtypes(include="object"):

    le = LabelEncoder()

    combined = pd.concat([X[col], test[col]], axis=0).astype(str)
    le.fit(combined)

    X[col] = le.transform(X[col].astype(str))
    test[col] = le.transform(test[col].astype(str))

# Handle missing values
imp = SimpleImputer(strategy="median")

X = imp.fit_transform(X)
test = imp.transform(test)

# Split data
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Models
models = {
    "Ridge": Ridge(alpha=10),
    "GradientBoosting": GradientBoostingRegressor()
}

best_model = None
best_mae = float("inf")

for name, model in models.items():

    model.fit(X_train, y_train)
    preds = model.predict(X_val)

    mae = mean_absolute_error(np.expm1(y_val), np.expm1(preds))

    print(name, "MAE:", mae)

    if mae < best_mae:
        best_mae = mae
        best_model = model

print("Best MAE:", best_mae)

# Train best model
best_model.fit(X, y)

# Predict
preds = np.expm1(best_model.predict(test))

# Save submission
submission = pd.DataFrame({
    "Id": test_ids,
    "SalePrice": preds
})

submission.to_csv("houseprice_submission.csv", index=False)

print("Submission file saved as houseprice_submission.csv")