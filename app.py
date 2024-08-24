# from flask import Flask
from fastapi import FastAPI, Request, Response, BackgroundTasks
import uvicorn
import time
import ssl
import slack
import requests
import asyncio
import aiohttp

# from slackeventsapi import SlackEventAdapter

from googlesheets.theeds import grade
import slacks.api as slackAPI

CHANNEL_ID_CAMPY = "#campy"
COMMAND_CAMPY = "/campy"

app = FastAPI()

# This is slack token


# app = Flask(__name__)
 
def get_slack_client():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client = slack.WebClient(token=SLACK_TOKEN, ssl=ssl_context)
    # client = slack.WebClient(token=SLACK_TOKEN)
    client.chat_postMessage(channel=CHANNEL_ID_CAMPY,text='Hello your bot here, what can I do for you?')    
    
    return client
    # slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

def gen_results(response_url: str, response_text: str):
    print(f'gen_results(): waiting for grading...')
    start_time = time.time()

    # Simulate a long-running task
    
    time.sleep(66)
    print(f'production_status(): DONE waiting {(time.time() - start_time)} sec...')

    # grades = grade()
    # await grade()
    
    # if not grades:
    #     # slack_client.chat_postMessage(channel='#campy', text=f'Getting grades...!')
    #     print(f"grades not ready...")
    # else:
    #     # slack_client.chat_postMessage(channel='#campy', text=f'Calculated some grades: DONE!')    
    #     print(f'gen_results(): DONE grading...{(time.time() - start_time)})')

    #  with aiohttp.ClientSession() as session:
    with requests.Session() as session:
        print(f'send_results(): sending http POST - {response_url} -> {response_text}')
        delayed_resp = {
            "text": response_text
        }
        with session.post(response_url, json=delayed_resp) as resp:
            print(f'gen_results(): posted to webhook {response_url} - {resp.status_code}, {resp.text}, {resp.content}\n')
            print(f'gen_results(): response headers = {resp.headers}')

async def launch_task(background_tasks: BackgroundTasks, param1: str, param2: str):
    print(f'launch_task() in background...')
    background_tasks.add_task(gen_results, param1, param2)
    # asyncio.run(gen_results(param1, param2))
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.create_task(gen_results(param1, param2))
    # loop.run_forever()

    # asyncio.run(main()


# @app.route('/productions', methods = ['GET', 'POST'])
@app.get("/productions")
async def production_status(request: Request):
    slack_client = get_slack_client()
    print("Getting production status: ")
       
    # grades = await grade()
    # await grade()
    
    # if not grades:
    #     slack_client.chat_postMessage(channel='#campy', text=f'Getting grades...!')
    #     # return "grades not ready..."
    # else:
    #     slack_client.chat_postMessage(channel='#campy', text=f'Calculated some grades: DONE!')
        
    slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'Calculated some grades: DONE!')
    return {"message": "production status checked"}

@app.post("/productions")
async def production_status(request: Request, background_tasks: BackgroundTasks):
    slack_client = get_slack_client()
    print("Starting grading process... ")
    slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, 
                                  text=f'Starting grading process, which will take a few moments, stay tuned...')
       
    slackAPI.get_users(slack_client)
    
    headers = request.headers
    print(f'production_status(): headers = {headers}')

    data = await request.form()

    print(f'production_status(): formData = {data}')
    if data is not None and data.get('command') == COMMAND_CAMPY:
        print(f'production_status(): got the grading request...')
        # command = data.get('command')
        text = data.get('text')
        response_url = data.get('response_url')
        user_id = data.get('user_id')
        channel_id = data.get('channel_id')

        # if command == '/campy':
        # Send immediate acknowledgment
        slack_client.chat_postMessage(
            channel=CHANNEL_ID_CAMPY,
            text="Your request is being processed. You will receive a response shortly."
        )

        ack_response = "Processing your request. This might take a few seconds..."
        
        # Send delayed response
        response_text = "After processing, production status checked, grading DONE" # "This is the delayed response after 10 seconds."
        await launch_task(background_tasks, response_url, response_text)

        return ack_response
    
            # return {'message': response_text}
        # slack_client.chat_postMessage(
        #     channel=channel_id,
        #     text=response_text
        # )
        # slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'Hey <@U076YT1E28Z> Calculated some grades: DONE!')
        # slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'Hi <!channel> Calculated some grades: All DONE!')

        # return {"message": "production status checked, grading DONE"}

@app.get("/")
@app.get("/index")
@app.get("/echo")
@app.get("/healthz")
async def root():
    return {"message": "Hello from Campy Bot"}

# @app.route('/')
# @app.route('/index')
# def index():   
#     return 'Hello from Campy Bot'

if __name__ == "__main__":
    # app.run(debug=True)
    uvicorn.run(app, host="0.0.0.0", port=6888)


