from pymongo import MongoClient
import pandas as pd
DB_NAME = "Proj1"
COLLECTION_NAME = "Proj1-Data"
CONNECTION_URL = "mongodb+srv://pagadi:pagadi@cluster0.gm2pt3w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a client
client = MongoClient(CONNECTION_URL)

# Access the database and collection
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Read data into DataFrame
df = pd.DataFrame(list(collection.find()))
print(df.head(2))