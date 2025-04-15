import datetime
import requests

start_date = datetime.date(2025, 4, 1)
end_date = datetime.date(2025, 4, 14)

for date in [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]:
    for platform in ["ios", "android"]:
        url = f"http://127.0.0.1:8000/reporting?start_date={date.strftime('%Y-%m-%d')}&end_date={date.strftime('%Y-%m-%d')}&platform={platform}"
        response = requests.get(url)
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.status_code}")