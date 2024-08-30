# from flask import Flask
from fastapi import FastAPI, Request, BackgroundTasks
import uvicorn
import time
import ssl
from slack import WebClient
import requests

# from slackeventsapi import SlackEventAdapter

from googlesheets.theeds import do_grading
from googlesheets.notification import get_incompleted
import slacks.api as slackAPI
import config

CHANNEL_ID_CAMPY = "#campy"
COMMAND_CAMPY = "/campy"

SUB_COMMAND_NOTIFY = "notify"
SUB_COMMAND_GRADE = "grade"

app = FastAPI()

# Slack access token
SLACK_CLIENT_TOKEN = config.slack_client_token
# SLACK_SIGNING_SECRET = config.slack_signing_secret
 
def get_slack_client():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    client = WebClient(token=SLACK_CLIENT_TOKEN, ssl=ssl_context)
    # client = slack.WebClient(token=SLACK_CLIENT_TOKEN)
    # client.chat_postMessage(channel=CHANNEL_ID_CAMPY,text='Hello your bot here, what can I do for you?')    
    
    return client
    # slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, '/slack/events', app)

def gen_results(response_url: str, response_text: str):
    print(f'gen_results(): waiting for grading...')
    start_time = time.time()

    # Simulate a long-running task    
    # time.sleep(66)
    # print(f'production_status(): DONE waiting {(time.time() - start_time)} sec...')

    grades = do_grading()
    # await grade()
    
    if not grades:
        # slack_client.chat_postMessage(channel='#campy', text=f'Getting grades...!')
        print(f"gradeing failed...")
    else:
        # slack_client.chat_postMessage(channel='#campy', text=f'Calculated some grades: DONE!')    
        print(f'gen_results(): DONE grading...{(time.time() - start_time)})')

    #  with aiohttp.ClientSession() as session:
    with requests.Session() as session:
        print(f'send_results(): sending http POST - {response_url} -> {response_text}')
        delayed_resp = {
            "text": response_text
        }
        with session.post(response_url, json=delayed_resp) as resp:
            print(f'gen_results(): posted to webhook {response_url} - {resp.status_code}, {resp.text}, {resp.content}\n')
            print(f'gen_results(): response headers = {resp.headers}')

def launch_task(background_tasks: BackgroundTasks, param1: str, param2: str):
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

def grade(client: WebClient, response_url: str, background_tasks: BackgroundTasks):

        # Send immediate acknowledgment
        client.chat_postMessage(
            channel=CHANNEL_ID_CAMPY,
            text="Your request is being processed. You will receive a response shortly."
        )

        ack_response = "Processing your request. This might take a few seconds..."
        
        # Send delayed response
        response_text = "After processing, production status checked, grading DONE" # "This is the delayed response after 10 seconds."
        launch_task(background_tasks, response_url, response_text)

        return ack_response
    
        # slack_client.chat_postMessage(
        #     channel=channel_id,
        #     text=response_text
        # )
        # slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'Hey <@U076YT1E28Z> Calculated some grades: DONE!')
        # slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'Hi <!channel> Calculated some grades: All DONE!')

        # return {"message": "production status checked, grading DONE"}

def send_reminder(client: WebClient, assignments: dict, users: dict):
    for writer, tasks in assignments.items():
        user_id = slackAPI.get_id_by_name(users, writer)
        if user_id is not None:
            mesg = f'Hey <@{user_id}>, a friendly reminder that your'
            for task in tasks:
                mesg += " " + task 
            print(f'send_reminder(): assignment = {mesg}')
            
            client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'{mesg}.')

def notify(client: WebClient, users):
    assignments = get_incompleted()
    send_reminder(client, assignments, users)

@app.post("/productions")
async def production_status(request: Request, background_tasks: BackgroundTasks):
    slack_client = get_slack_client()
    print("production_status(): Got a campy request... ")
       
    users = slackAPI.get_users(slack_client)
    
    # headers = request.headers
    # print(f'production_status(): headers = {headers}')
    data = await request.form()
    
    print(f'production_status(): formData = {data}')
    if data is not None and data.get('command') == COMMAND_CAMPY:        
        text = data.get('text')
        response_url = data.get('response_url')
        user_id = data.get('user_id')
        channel_id = data.get('channel_id')
        print(f'production_status(): command = {text} in channel {channel_id}')
        if text is None or text == "":
            print("production_status(): no sub_command, show Help")
            help_text = "Campy is a bot that manages production cycle: \n\n" + \
                        "* `/campy notify`: Notifies writers of incomplete assignemnts\n" + \
                        "* `/campy grade`: Does grading for writers work\n" + \
                        "* `/campy`: Displays this help text"
            slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, 
                                            text=f'{help_text}')
        sub_command = text.lower()
        if sub_command == SUB_COMMAND_NOTIFY:
            print(f'production_status(): notify...')
            notify(slack_client, users)
        elif sub_command == SUB_COMMAND_GRADE:
            print(f'production_status(): grading...')
            grade(slack_client, response_url, background_tasks)
   
    # slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'Enjoy!')
        

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


