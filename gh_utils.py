import json
import logging
import requests
import sys

from requests.auth import HTTPBasicAuth

from gh_oauth_token import retrieve_token
from bot_config import API_BASE_URL, GH_USER_TOKEN, GH_USER

log = logging.getLogger(__name__)


def make_github_rest_api_call(api_path, method='GET', params=None):
    """Send API call to Github using a personal token.

Use this function to make API calls to the GitHub REST api

For example:

`GET` the current user
---
```py
me = make_github_rest_api_call('login')
```

`POST` to create a comment on a PR
---
```py
new_comment = make_github_rest_api_call(
    'repos/my_org/my_repo/issues/31/comments',
    'POST', {
        'body': "Hello there, thanks for creating a new Pull Request!"
    }
)
```
    """

    token = retrieve_token()
    # token = GH_USER_TOKEN

    # Required headers.
    headers = {'Accept': 'application/vnd.github.antiope-preview+json',
               'Content-Type': 'application/json',
                  'Authorization': f'Bearer {token}'
               }

    try:
        if method.upper() == 'POST':
            response = requests.post(f'{API_BASE_URL}/{api_path}', headers=headers, data=json.dumps(
                params))
        elif method.upper() == 'GET':
            response = requests.get(f'{API_BASE_URL}/{api_path}', headers=headers)
        else:
            raise Exception('Invalid Request Method.')
    except:
        log.exception("Could not make a successful API call to GitHub.")


def set_check_on_pr(repo_full_name, check_name, check_status, check_conclusion, head_sha, output_title=None, output_summary=None):
    payload = {
        'name': check_name,
        'status': check_status,
        'head_sha': head_sha,
    }

    if check_conclusion:
        payload['conclusion'] = check_conclusion

    if output_title and output_summary:
        payload['output'] = dict(title=output_title, summary=output_summary)

    api_path = f'repos/{repo_full_name}/check-runs'
    make_github_rest_api_call(api_path, 'POST', params=payload)
