def fetch(url, options):
    import requests
    import json

    res = requests.get(url)
    response = json.loads(res.text)
    return response
