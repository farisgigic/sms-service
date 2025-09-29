import os
from dotenv import load_dotenv
import csv
import http.client
import json
import random

load_dotenv()

# Infobip API setup
BASE_HOST = "api.infobip.com"
BASE_PATH = "/sms/2/text/advanced"
API_KEY = os.getenv('API_KEY')
CSV_FILE = "./CSV/messages.csv"

# Read all CSV rows
with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
    reader = list(csv.DictReader(csvfile))
    fieldnames = reader[0].keys()

# Create connection once
conn = http.client.HTTPSConnection(BASE_HOST)

for row in reader:
    sender_id = row["SenderId"]
    msisdn = row["MSISDN"]

    # Random ID for the message text
    random_id = str(random.randint(100000, 999999))

    # Build payload as dict
    payload_dict = {
        "messages": [
            {
                "from": sender_id,
                "destinations": [{"to": msisdn}],
                "text": f"Hello! This is a test message with ID {random_id}"
            }
        ]
    }

    payload = json.dumps(payload_dict)

    # Headers
    headers = {
        "Authorization": f"App {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        # Send request
        conn.request("POST", BASE_PATH, payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        resp_data = json.loads(data)

        if "messages" in resp_data:
            message_info = resp_data["messages"][0]
            # Store Infobip messageId
            row["messageId"] = message_info.get("messageId", "No ID")
            # Store status description
            row["description"] = message_info.get("status", {}).get("description", "No description")
        else:
            row["description"] = f"Error: {data}"

    except Exception as e:
        row["description"] = f"Request failed: {str(e)}"

# Close connection after all messages are sent
conn.close()

# Write back to the same CSV
with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reader)

print("All messages processed and CSV updated in place using http.client.")
