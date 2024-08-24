import requests

WEB_HOOK_CAMPY = 'https://hooks.slack.com/services/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'

def send_delayed_response(response_url, message):
    data = {"text": message}
    response = requests.post(response_url, json=data)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")


