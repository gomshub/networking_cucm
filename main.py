## create date time group in cucm
from flask import Flask, request, jsonify
import requests
import json
import urllib3
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)
cucm_ip = os.getenv('CUCM_IP')
cucm_user = os.getenv('CUCM_USER')
cucm_pass = os.getenv('CUCM_PASS')
cucm_version = os.getenv('CUCM_VERSION')
base_url = f"https://{cucm_ip}:8443/axl/"
cucm_namespace = f"http://www.cisco.com/AXL/API/{cucm_version}"
headers = {'Content-Type': 'text/xml', 'SOAPAction': f"{cucm_namespace}/"}
auth = HTTPBasicAuth(cucm_user, cucm_pass)
session = requests.Session()
session.auth = auth
session.verify = False
session.headers.update(headers)
session.timeout = 30
session.base_url = base_url
session.namespace = cucm_namespace

@app.route('/create_datetime_group', methods=['POST'])
def create_datetime_group():
    data = request.json
    name = data.get('name')
    time_zone = data.get('timeZone', 'Eastern Standard/Daylight Time')
    locale = data.get('locale', 'English_United States')
    date_format = data.get('dateFormat', 'M/D/YY')
    time_format = data.get('timeFormat', '12-hr')
    pattern = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:ns="{session.namespace}">
      <soapenv:Header/>
      <soapenv:Body>
        <ns:addDateTimeGroup>
          <dateTimeGroup>
            <name>{name}</name>
            <timeZone>{time_zone}</timeZone>
            <locale>{locale}</locale>
            <dateFormat>{date_format}</dateFormat>
            <timeFormat>{time_format}</timeFormat>
          </dateTimeGroup>
        </ns:addDateTimeGroup>
      </soapenv:Body>
    </soapenv:Envelope>
    """
    try:
        response = session.post(session.base_url, data=pattern)
        if response.status_code == 200 and "<return>" in response.text:
            return jsonify({"message": "Date/Time Group created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create Date/Time Group", "details": response.text}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ...existing code...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)