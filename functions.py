import logging
import json
import requests
from requests.models import Response
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def import_database_credentials(file_name="mongodb_credentials.json"):
    with open(file_name, mode='w') as f:
        data=json.loads(f)
    username =data.get("username")
    password = data.get("password")

    return username, password


def http_response(**url_details):
    request_args={}
    request_args.update(url_details)
    url_response=None
    if request_args.get("request_type") =='get':
        url_response = requests_retry().get(request_args.get("url", ''),
                                            params=request_args.get("payload", {}),
                                            headers=request_args.get("headers", {}))
    elif request_args.get("request_type") =='post':
        pass
    if check_request_status_code(url=request_args.get("url"), response=url_response):
        return url_response
    else:
        return create_dummy_response(response_code=url_response.status_code, error=None)


def requests_retry(retries=3, back_off_factor=0.3,
                   status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry=Retry(
        total=retries,
        read=retries,
        connect=retries,
        redirect=retries-1,
        backoff_factor=back_off_factor,
        status_forcelist=status_forcelist
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('http://', adapter)
    return session


def check_request_status_code(url=None, response=None):
    if response.status_code != requests.codes.ok:
        logging.warning("URL :" + str(url) + ". Error in retrieving data due to status code " +
                     str(response.status_code) + ". Check url ")
        return False
    else:
        return True


def create_dummy_response(response_code=None, error=None):
    dummy_response = Response()
    dummy_response.status_code = response_code
    dummy_response.error_type=error
    return dummy_response