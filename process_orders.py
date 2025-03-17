import json
import logging

# Configures logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Defines a file path for the JSON file
json_file_path = "orders.json"

def load_json(file_path):
    """
    Loads and parses a JSON file safely.
    Ensures that the file contains a list of records (orders).
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            assert isinstance(data, list), "JSON should be a list of orders!"
            logging.info(" JSON file loaded successfully.")
            return data
    except Exception as e:
        logging.error(f" Error loading JSON file: {e}")
        return []

# Loads data
orders_data = load_json(json_file_path)

# Logs a sample of the data for verification
logging.info(f" Sample data: {json.dumps(orders_data[:2], indent=4)}")
