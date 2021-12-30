import requests


def valid_response(r: requests.Response) -> bool:
    return str(r) == "<Response [200]>"
