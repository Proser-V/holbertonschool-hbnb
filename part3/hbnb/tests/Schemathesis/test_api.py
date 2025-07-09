import requests
import schemathesis
import pytest

def download_swagger():
    url = "http://127.0.0.1:5001/swagger.json"
    r = requests.get(url)
    r.raise_for_status()
    with open("swagger.json", "w") as f:
        f.write(r.text)

schema = schemathesis.openapi.from_url("http://127.0.0.1:5001/swagger.json")

@schema.parametrize()
def test_api(case):
    response = case.call()
    case.validate_response(response)
