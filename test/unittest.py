import httpx

response_url = "https://hooks.slack.com/commands/T076DJA8HQE/7572736295831/ofF5DDrUcTIpVAadX9qHW2re"

resp_url = "https://hooks.slack.com/services/T0xxx"

response_text = "After processing, grading DONE" # "This is the delayed response after 10 seconds."

with httpx.Client() as client:
    delayed_resp = {
        "text": response_text
    }

    # try:
    resp = client.post(url=resp_url, 
                        json=delayed_resp)
                        # headers={"Content-Type": "application/json"})

    # print(resp.json())
    print(f'request = {resp.request}, {resp.request.content}, {resp.request.headers}')
    print(f'posted to {resp_url} - {resp.status_code}, {resp.reason_phrase}, {resp.text}, {resp.content}, {resp.headers}')

    # except httpx.TimeoutException:
    #     print("Request timed out!")
    # except httpx.HTTPStatusError:
    #     print("Error response")



