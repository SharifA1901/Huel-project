## Overview
This project takes raw JSON data, then is normalised into a structured format

## Files in this project include
- **orders.json** -> raw JSON data containing annoymised e-commerce order data
- **process_order.py** -> Python script for inspecting and verifying the JSON structure
- **parse_order.py** -> Python script to parse, transform, and export data into CSV
- **customers.csv, discounts.csv, order_items.csv, orders.csv and shipping.csv** -> which is all the data processed (These will only generate once you run the script)


## Steps to run the project

1. Install the dependencies
- **pip install pandas**

2. Run the script
- **python process_orders.py** -> This script loads the order.json file and prints a sample of the JSON structure 
- **python parse_orders.py** -> This script extracts the nested JSON fields, normalises data into separate relational tables, validates data integrity and uses assertions and saves processed data into structured CSV files ready for import

## Entity Relationship Diagram- Description

-The database follows a normalised relational structure to efficiently store and manage order data

**1. Customer Table**
*Primary Key* customer_reference 
*Attributes* first_name, last_name, email
*Relationship*
    -One-to-many relationship with Orders (Customer can place multiple orders)

**2. Orders Table**
*Primary Key* order_id
*Foreign Key* customer_reference -> References customers.customer_reference
*Attributes* order_date, total_price, currency, source
*Relationship*
    -One-to-Many with Order Items (An order can contain multiple items)
    -One-to-Many with Discounts (An order can have multiple discounts)
    -One-to-One with Shipping Details (Each order has one shipping address)

**3. Orders Items Table**
*Composite Primary Key* (order_id, product_id)
*Foreign Key* order_id -> References orders.order_id
*Attributes*  variant_id, sku, quantity, subtotal, total
*Relationship*
    -Many-to-One with Orders (Each order item belongs to one order)

**4. Discounts Table**
*Primary Key* discount_id
**Foreign Key* order_id -> References orders.order_id
*Attributes* discount_code, discount_type, discount_value
*Relationship*
    -Many-to-One with Orders (Each discount is applied to one order)

**5. Shippings Table**
*Primary Key* shipping_id
**Foreign Key* order_id -> References orders.order_id
*Attributes* city, country, postcode, address_line1, address_line2
*Relationship*
    -One-to-One with Orders (Each order has exactly one shipping record)

## Data Validation & Error Handling

- To ensure data quality, the script performs assertions to prevent empty or malformed data from being saved
- If an assertion fails, the script stores execution, preventing invalid data from being processed

assert not df_orders.empty, " Orders DataFrame is empty!"
assert not df_customers.empty, " Customers DataFrame is empty!"
assert not df_order_items.empty, " Order Items DataFrame is empty!"
assert not df_discounts.empty, " Discounts DataFrame is empty (this might be expected)."
assert not df_shipping.empty, " Shipping DataFrame is empty!"






