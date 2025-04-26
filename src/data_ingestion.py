import pandas as pd
from pathlib import Path
import yaml

class DataIngestor:
    def __init__(self, config_path: Path):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)["data_ingestion"]
        
    def ingest(self) -> pd.DataFrame:
        df = pd.read_csv(self.config["source_url"])
        df.to_csv(Path(self.config["raw_path"]), index=False)
        return df

if __name__ == "__main__":
    ingestor = DataIngestor(Path("configs/data_config.yml"))
    ingestor.ingest()