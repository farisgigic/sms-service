import http.client
import json
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

conn = http.client.HTTPSConnection("api.infobip.com")
payload = json.dumps({
    "messages": [
        {
            "destinations": [{"to":"38762554272"}],
            "from": "447491163443",
            "text": "Congratulations on sending your first message. Go ahead and check the delivery report in the next step."
        }
    ]
})
headers = {
    'Authorization': f'App {API_KEY}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
conn.request("POST", "/sms/2/text/advanced", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
