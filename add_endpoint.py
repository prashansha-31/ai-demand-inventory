new_endpoint = """

@app.get("/api/model-info")
async def get_model_info():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    feature_names = metadata.get("features", []) if metadata else []
    feature_importances = model.feature_importances_.tolist() if hasattr(model, "feature_importances_") else []

    fi_list = [
        {"feature": name, "importance": round(imp, 6)}
        for name, imp in sorted(zip(feature_names, feature_importances), key=lambda x: -x[1])
    ] if feature_names and feature_importances else []

    return {
        "model_name": metadata.get("model_name", "Random Forest") if metadata else "Random Forest",
        "algorithm": "Random Forest Regressor",
        "dataset": "Walmart Weekly Retail Sales (2010-2012)",
        "r2_score": round(metadata.get("r2_score", 0.9627), 4) if metadata else 0.9627,
        "mae": round(metadata.get("mae", 1669.06), 2) if metadata else 1669.06,
        "rmse": round(float(metadata.get("rmse", 4403.81)), 2) if metadata else 4403.81,
        "features": feature_names,
        "feature_count": len(feature_names),
        "best_params": metadata.get("best_params", {}) if metadata else {},
        "training_samples": 337256,
        "test_samples": 84314,
        "total_records": 421570,
        "stores_count": 45,
        "departments_count": 81,
        "date_range": "2010-02-05 to 2012-10-26",
        "model_comparison": [
            {"name": "Random Forest",     "test_r2": 0.9627, "test_mae": 1669.06, "test_rmse": 4403.81, "cv_r2": 0.9482, "best": True},
            {"name": "Gradient Boosting", "test_r2": 0.9604, "test_mae": 1784.18, "test_rmse": 4540.60, "cv_r2": 0.9527, "best": False},
            {"name": "XGBoost",           "test_r2": 0.9599, "test_mae": 1807.70, "test_rmse": 4566.90, "cv_r2": 0.9526, "best": False},
            {"name": "Decision Tree",     "test_r2": 0.9483, "test_mae": 1877.84, "test_rmse": 5185.28, "cv_r2": 0.9294, "best": False},
            {"name": "Stacking Ensemble", "test_r2": 0.9342, "test_mae": 2119.99, "test_rmse": 5849.39, "cv_r2": 0.0,    "best": False},
            {"name": "Voting Ensemble",   "test_r2": 0.9263, "test_mae": 2566.75, "test_rmse": 6191.14, "cv_r2": 0.0,    "best": False},
            {"name": "Linear Regression", "test_r2": 0.9132, "test_mae": 2378.02, "test_rmse": 6718.36, "cv_r2": 0.9068, "best": False},
            {"name": "Ridge Regression",  "test_r2": 0.9132, "test_mae": 2376.96, "test_rmse": 6718.39, "cv_r2": 0.9068, "best": False},
            {"name": "Lasso Regression",  "test_r2": 0.9126, "test_mae": 2335.08, "test_rmse": 6740.34, "cv_r2": 0.9063, "best": False},
            {"name": "ElasticNet",        "test_r2": 0.9126, "test_mae": 2333.10, "test_rmse": 6741.50, "cv_r2": 0.9063, "best": False},
            {"name": "AdaBoost",          "test_r2": 0.8864, "test_mae": 4336.64, "test_rmse": 7686.68, "cv_r2": 0.8832, "best": False},
        ],
        "feature_importance": fi_list
    }
"""

with open("main.py", "a") as f:
    f.write(new_endpoint)
print("Done!")
