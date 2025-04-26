import pandas as pd
from pathlib import Path
import yaml
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression

class ModelTrainer:
    def __init__(self, config_path: Path):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["model"]
        
        # Ensure mlruns directory exists
        Path("mlruns").mkdir(exist_ok=True)
        mlflow.set_tracking_uri("mlruns")
        
        # Set or create an experiment
        experiment_name = "TitanicSurvivalExperiment"
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            mlflow.create_experiment(experiment_name)
        mlflow.set_experiment(experiment_name)
        
    def train(self):
        train_df = pd.read_csv("data/processed/train.csv")
        X_train = train_df.drop("Survived", axis=1)
        y_train = train_df["Survived"]

        model = LogisticRegression(**self.config["params"])
        model.fit(X_train, y_train)

        with mlflow.start_run():
            # Log parameters
            mlflow.log_params(self.config["params"])
            
            # Log model with signature and input example
            input_example = X_train.iloc[[0]]  # First row as input example
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                input_example=input_example,
                registered_model_name="titanic-survival"
            )
            
            # Log metrics
            train_accuracy = model.score(X_train, y_train)
            mlflow.log_metric("train_accuracy", train_accuracy)

if __name__ == "__main__":
    trainer = ModelTrainer(Path("configs/params.yml"))
    trainer.train()
    print("Training completed successfully!")