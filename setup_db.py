import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:8080"
# Replace with your actual NocoDB Auth Token
AUTH_TOKEN = "changeme_jwt_secret_key"
PROJECT_NAME = "Confections Workshop"

HEADERS = {
    "Content-Type": "application/json",
    "Account-Token": AUTH_TOKEN
}

def create_project():
    """Ensures a project exists and returns its ID."""
    # List projects to see if one with our name exists
    response = requests.get(f"{BASE_URL}/api/v1/projects", headers=HEADERS)
    if response.status_code == 200:
        projects = response.json().get('data', [])
        for p in projects:
            if "Confections Workshop" in p['name']:
                return p['id']

    # Create if not found
    payload = {"name": PROJECT_NAME}
    response = requests.post(f"{BASE_URL}/api/v1/projects", headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201 or response.status_code == 200:
        return response.json()['data']['id']
    else:
        print(f"Error creating project: {response.text}")
        sys.exit(1)

def create_table(project_id, table_name, columns):
    """Creates a new table with initial columns."""
    url = f"{BASE_URL}/api/v1/meta/projects/{project_id}/tables"
    payload = {
        "name": table_name,
        "columns": [
            {"name": col['name'], "uidt": col['type'], "description": col.get('description', '')}
            for col in columns if col['name'] != 'id' # Skip default id
        ]
    }
    # Ensure ID column is handled (NocoDB usually adds it)
    if "id" not in [c['name'] for c in columns]:
        payload["columns"].append({"name": "id", "uidt": "Number"})

    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201 or response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to create table {table_name}: {response.text}")
        return None

def add_column(project_id, table_id, column_name, col_type, description=""):
    """Adds a column to an existing table."""
    url = f"{BASE_URL}/api/v1/meta/projects/{project_id}/tables/{table_id}/columns"
    payload = {
        "name": column_name,
        "uidt": col_type,
        "description": description
    }
    response = requests.post(url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code == 201 or response.status_code == 200:
        return response.json()['data']
    else:
        print(f"Failed to add column {column_name}: {response.text}")

def main():
    project_id = create_project()
    print(f"Working on project ID: {project_id}")

    # Define Tables and initial columns (excluding IDs/Relations for now)
    tables = {
        "clients": [
            {"name": "full_name", "type": "SingleLineText", "description": "Customer Name"},
            {"name": "phone", "type": "SingleLineText", "description": "Phone Number"},
            {"name": "special_notes", "type": "LongText", "description": "Custom preferences"}
        ],
        "orders": [
            {"name": "date_received", "type": "Date"},
            {"name": "date_delivery_promised", "type": "Date"},
            {"name": "total_amount", "type": "Decimal"},
            {"name": "outstanding_balance", "type": "Decimal"},
            {"name": "payment_status", "type": "Select", "description": "Pending, Partially Paid, Fully Paid"},
            {"name": "order_status", "type": "Select", "description": "On Hold, In Production, Ready for Embroidery, Being Embroidered, Finished, Delivered"}
        ],
        "order_items": [
            {"name": "product_type", "type": "Select", "description": "Towel, Bathrobe, Baby Onesie, Custom Tailored"},
            {"name": "quantity", "type": "Number"},
            {"name": "unit_price", "type": "Decimal"},
            {"name": "requires_embroidery", "type": "Boolean"},
            {"name": "embroidery_text", "type": "SingleLineText"},
            {"name": "design_details", "type": "LongText"},
            {"name": "measurements", "type": "LongText"}
        ],
        "embroidery_jobs": [
            {"name": "embroidery_status", "type": "Select", "description": "Pending Shipment, With Vendor, Received OK, Rejected/Error"},
            {"name": "date_sent", "type": "Date"},
            {"name": "date_returned", "type": "Date"},
            {"name": "vendor_cost", "type": "Decimal"}
        ],
        "payments": [
            {"name": "payment_date", "type": "Date"},
            {"name": "amount", "type": "Decimal"},
            {"name": "payment_method", "type": "Select", "description": "Cash, Bank Transfer, Other"},
            {"name": "notes", "type": "SingleLineText"}
        ],
        "expenses": [
            {"name": "date", "type": "Date"},
            {"name": "category", "type": "Select", "description": "Fabrics, Threads, Vendor Payments, Utilities, Machine Maintenance, Other"},
            {"name": "amount", "type": "Decimal"},
            {"name": "description", "type": "SingleLineText"}
        ]
    }

    table_info = {}

    # 1. Create Tables first
    for name, cols in tables.items():
        print(f"Creating table: {name}")
        data = create_table(project_id, name, cols)
        if data:
            table_info[name] = data

    # 2. Add Foreign Key Relationships
    print("Establishing relationships...")
    
    # client -> orders
    if "orders" in table_info:
        add_column(project_id, table_info["orders"]["id"], "client_id", "LinkToAnotherRecord")

    # orders -> order_items
    if "order_items" in table_info:
        add_column(project_id, table_info["order_items"]["id"], "order_id", "LinkToAnotherRecord")

    # order_items -> embroidery_jobs
    if "embroidery_jobs" in table_info:
        add_column(project_id, table_info["embroidery_jobs"]["id"], "order_item_id", "LinkToAnotherRecord")

    # orders -> payments
    if "payments" in table_info:
        add_column(project_id, table_info["payments"]["id"], "order_id", "LinkToAnotherRecord")

    print("Setup complete.")

if __name__ == "__main__":
    main()
