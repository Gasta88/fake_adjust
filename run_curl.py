import datetime
import requests
import json
import os
import shutil

start_date = datetime.date(2025, 4, 1)
end_date = datetime.date(2025, 4, 14)
file_dir = "./raw_data/"

if os.path.exists(file_dir):
    shutil.rmtree(file_dir)
os.makedirs(file_dir)

responses = []

for date in [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]:
    for platform in ["ios", "android"]:
        report_filename = f"{date.strftime('%Y-%m-%d')}_{platform}.json"
        url = f"http://127.0.0.1:8000/reporting?start_date={date.strftime('%Y-%m-%d')}&end_date={date.strftime('%Y-%m-%d')}&platform={platform}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_dir + report_filename, "w") as f:
                json.dump(response.json(), f, indent=2)
        else:
            print(f"Error: {response.status_code}")
