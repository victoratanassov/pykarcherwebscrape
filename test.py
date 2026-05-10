import ijson
import requests
import gzip
import io

url = "https://karcher-borotrade.com/bg/productExport"

# Request and decompress manually
headers = {'Accept-Encoding': 'gzip'}  # Optional, but often helpful
with requests.get(url, stream=True, headers=headers) as response:
    response.raise_for_status()
    gzip_stream = gzip.GzipFile(fileobj=response.raw)
    items = ijson.items(gzip_stream, '')  # Use the correct prefix later

    count = 0
    for item in items:
        count += 1
        print(f"Item {count}: {str(item)[:200]}...")  # Preview first 200 chars
