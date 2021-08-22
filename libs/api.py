import json

from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote, parse_qsl
from urllib.error import HTTPError

def call_api(data):
    url = 'https://www.hrbkovi.eu/pyDominion.php'
    header = { 'Content-Type' : 'application/json' }
    first = True
    if data != None:
        for param in data:
            if first == True:
                url = url + '?' + param + '=' + quote(str(data[param]))
                first = False
            else:
                url = url + '&' + param + '=' + quote(str(data[param]))
    request = Request(url = url , data = None, headers = header)
    try:
        html = urlopen(request).read()
        if html and len(html) > 0:
            data = json.loads(html)
            return data
        else:
            return []
    except HTTPError as e:
        return { 'err' : e.reason }  

