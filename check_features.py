import pickle

with open("models/demand_model_advanced.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/model_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

print("Feature names in metadata:", metadata.get("features", []))
print("Model feature names:", getattr(model, "feature_names_in_", "N/A"))
