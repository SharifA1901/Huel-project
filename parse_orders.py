import json
import pandas as pd
import logging
from datetime import datetime

# Configures logging for debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# This is the File path
json_file_path = "orders.json"

# Function to load JSON data
def load_json(file_path):
    """Loads and parses JSON file, ensuring it contains a list."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        assert isinstance(data, list), "JSON file should contain a list of records"
        logging.info("JSON file loaded successfully.")
        return data
    except Exception as e:
        logging.error(f" Error loading JSON file: {e}")
        return []

# Loads orders JSON
orders_data = load_json(json_file_path)

# Create lists for storing normalised data
orders = []
customers = []
order_items = []
discounts = []
shipping_details = []

# Iterate through JSON records to normalise data
for record in orders_data:
    order = record.get("event_payload", {}).get("order", {})

    # Extract Order Details
    order_id = order.get("orderId")
    order_date = order.get("placedAt")
    total_price = order.get("amounts", {}).get("total", 0)
    currency = order.get("currency")
    source = order.get("source")
    customer_reference = order.get("customerReference")

    # This handles different timestamp formats
    if order_date:
        try:
            order_date = datetime.strptime(order_date, "%Y-%m-%dT%H:%M:%S.%f")  # Should be the expected format
        except ValueError:
            try:
                order_date = datetime.fromtimestamp(float(order_date))  # This converts integer timestamps
                logging.warning(f" Converted integer timestamp for order {order_id}.")
            except (ValueError, TypeError):
                logging.warning(f" Invalid timestamp format for order {order_id}: {order_date}")
                order_date = None  # Handle missing or malformed timestamps

    orders.append({
        "order_id": order_id,
        "customer_reference": customer_reference,
        "order_date": order_date,
        "total_price": total_price,
        "currency": currency,
        "source": source
        
    })

    # Extract Customer Details
    customer = order.get("customerDetails", {})
    customer_reference = order.get("customerReference")

    customers.append({
        "customer_reference": customer_reference,
        "first_name": customer.get("firstName"),
        "last_name": customer.get("lastName"),
        "email": customer.get("email"),
    })

    # Extracting Order Items
    for item in order.get("lineItems", []):
        order_items.append({
            "order_id": order_id,
            "product_id": item.get("productId"),
            "variant_id": item.get("variantId"),
            "sku": item.get("sku"),
            "quantity": item.get("quantity"),
            "subtotal": item.get("amounts", {}).get("subtotal", 0),
            "total": item.get("amounts", {}).get("total", 0)
        })

    # Extracting Discounts
    applied_discounts = order.get("appliedDiscounts", [])
    if applied_discounts:
        for discount in applied_discounts:
            discounts.append({
                "order_id": order_id,
                "discount_code": discount.get("code"),
                "discount_type": discount.get("type"),
                "discount_value": discount.get("value"),
            })

    # Extracting Shipping Details
    shipping = order.get("shippingDetails", {}).get("address", {})
    shipping_details.append({
        "order_id": order_id,
        "city": shipping.get("city"),
        "country": shipping.get("country"),
        "postcode": shipping.get("postcode"),
        "address_line1": shipping.get("line1"),
        "address_line2": shipping.get("line2")
    })

# Converts lists to Pandas DataFrames
df_orders = pd.DataFrame(orders)
df_customers = pd.DataFrame(customers).drop_duplicates()
df_order_items = pd.DataFrame(order_items)
df_discounts = pd.DataFrame(discounts)
df_shipping = pd.DataFrame(shipping_details)

# Assertions to ensure valid data
assert not df_orders.empty, " Orders DataFrame is empty!"
assert not df_customers.empty, " Customers DataFrame is empty!"
assert not df_order_items.empty, " Order Items DataFrame is empty!"
assert not df_discounts.empty, " Discounts DataFrame is empty (this might be expected)."
assert not df_shipping.empty, " Shipping DataFrame is empty!"

logging.info(" All dataframes successfully created.")

# Saves DataFrames as CSV files 
df_orders.to_csv("orders.csv", index=False) 
df_customers.to_csv("customers.csv", index=False)
df_order_items.to_csv("order_items.csv", index=False)
df_discounts.to_csv("discounts.csv", index=False)
df_shipping.to_csv("shipping.csv", index=False)

logging.info(" Data successfully parsed and saved as CSV files.")
