import logging
from gh_utils import make_github_rest_api_call, set_check_on_pr

"""
SPECIALIZED WEBHOOK HANDLERS 
=======================

Becaue we may receive many webhooks for many different reasons, it's a good idea
to "hand off" control from `process_message()` to a dedicated function ASAP.

This is a good place for these specialized handlers

"""
log = logging.getLogger(__name__)


def add_pr_comment(webhook):
    log.info('New Pull Request opened. Adding comment.')

    # Gather the requried information from the payload to send a successful request to GitHub REST API.
    repo_full_name = str(webhook.repository.full_name)
    pr_number = str(webhook.pull_request.number)

    comments_url = f'repos/{repo_full_name}/issues/{pr_number}/comments'

    # Make the API call.
    make_github_rest_api_call(
        comments_url,
        'POST', {
            'body': "Hello there, thanks for creating a new Pull Request!"
        }
    )


def check_testing_done(webhook):
    log.info('PR description changes. Check for the testing done section')

    # Gather the requried information from the payload to send a successful request to GitHub REST API.
    repo_full_name = str(webhook.repository.full_name)
    pr_number = str(webhook.pull_request.number)
    description = str(webhook.pull_request.body)

    testing_done = description.lower().split('testing done')

    check_name = 'Testing Done'
    check_status = 'completed'
    head_sha = str(webhook.pull_request.head.sha)
    output_title = 'Status of completion of Testing Done Section'

    if len(testing_done) > 1 and len(testing_done[1]) > 5:  # Naively assume there is something there.
        log.info("This PR already has a testing done section. Do nothing.")
        check_conclusion = 'success'
        output_summary = 'Testing Done section present. Thank you!'
    else:
        log.info("No Testing done section found.")
        check_conclusion = 'failure'
        output_summary = 'Please complete the Testing Done section of the description for compliance.'

    set_check_on_pr(repo_full_name, check_name, check_status, check_conclusion, head_sha, output_title, output_summary)
