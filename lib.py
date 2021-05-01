import requests
from requests.auth import HTTPBasicAuth

import config

def push(dataModel):
    push = requests.post(
        f"{config.API_URL}{config.ENDPOINT_SAVE_LOG}",
        auth=HTTPBasicAuth(config.AUTH_USERNAME, config.AUTH_PASSWORD),
        json=dataModel
    )
    return push.status_code
