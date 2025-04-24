import csv
import pymongo
from pymongo import MongoClient
import certifi

# MongoDB Configuration
DB_NAME = "Proj1"
COLLECTION_NAME = "Proj1-Data"
CONNECTION_URL = "mongodb+srv://pagadi:<PASSWORD>@cluster0.gm2pt3w.mongodb.net/?retryWrites=true&w=majority"

def csv_to_json(filepath):
    data = []
    with open(filepath, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Convert empty strings to None
            cleaned_row = {k: v if v != '' else None for k, v in row.items()}
            data.append(cleaned_row)
    return data

def insert_to_mongodb(data):
    try:
        # Connect to MongoDB (escape special characters in password)
        client = MongoClient(
            CONNECTION_URL.replace("<PASSWORD>", "pagadi"),  # Replace with your escaped password
            tlsCAFile=certifi.where()
        )
        
        # Verify connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Insert data
        result = collection.insert_many(data)
        print(f"Inserted {len(result.inserted_ids)} documents")
        
        return result
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Path to your CSV file
    csv_file = "data.csv"
    
    # Convert CSV to JSON-like documents
    data = csv_to_json(csv_file)
    
    if data:
        # Insert into MongoDB
        insert_result = insert_to_mongodb(data)