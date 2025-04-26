import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import yaml

class DataPreprocessor:
    def __init__(self, config_path: Path):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["preprocessing"]
    
    def preprocess(self, df: pd.DataFrame):
        # Create output directories if they don't exist
        Path(self.config["train_path"]).parent.mkdir(parents=True, exist_ok=True)
        Path(self.config["test_path"]).parent.mkdir(parents=True, exist_ok=True)

        # Rest of preprocessing code
        df = df.drop(self.config["columns_to_drop"], axis=1)
        df = df.dropna()
        df["Sex"] = df["Sex"].map({"male": 1, "female": 0})
        df = pd.get_dummies(df, columns=["Embarked"], drop_first=True)
        
        X = df.drop(self.config["target"], axis=1)
        y = df[self.config["target"]]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.config["test_size"], 
            random_state=self.config["random_state"]
        )
        
        # Explicitly save files
        pd.concat([X_train, y_train], axis=1).to_csv(
            self.config["train_path"], index=False
        )
        pd.concat([X_test, y_test], axis=1).to_csv(
            self.config["test_path"], index=False
        )

if __name__ == "__main__":
    raw_df = pd.read_csv("data/raw/titanic.csv")
    preprocessor = DataPreprocessor(Path("configs/data_config.yml"))
    preprocessor.preprocess(raw_df)
    print("Preprocessing completed successfully!")