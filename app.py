# from flask import Flask
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, status
import uvicorn
import time

from slack import WebClient
import requests

# from slackeventsapi import SlackEventAdapter

from googlesheets.theeds import do_grading
from googlesheets.notification import get_incompleted
import slacks.api as slackAPI

CHANNEL_ID_CAMPY = "#campy"
COMMAND_CAMPY = "/campy"

SUB_COMMAND_NOTIFY = "notify"
SUB_COMMAND_GRADE = "grade"

app = FastAPI()

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
        print(f"grading failed...")
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
    slack_client = slackAPI.get_slack_client()
    print("Getting production status... ")
       
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
        response_text = "After processing, production status checked, grading DONE"
        launch_task(background_tasks, response_url, response_text)

        return ack_response
    
def send_reminder(client: WebClient, assignments: dict, users: dict):
    mesg = ""
    for writer, tasks in assignments.items():
        user_id = slackAPI.get_id_by_name(users, writer)
        if user_id is not None:
            mesg = mesg + f'Hey <@{user_id}>, a friendly reminder that you still have'
            for task in tasks:
                mesg += task 
            mesg = mesg + ".\n"
    if mesg is None or len(mesg) <= 0:   
        mesg = "There are no incompleted assignments."   
    # print(f'send_reminder(): mesg = {mesg}')      
    client.chat_postMessage(channel=CHANNEL_ID_CAMPY, text=f'{mesg}')
   

def notify(client: WebClient, users, commands):
    incompletes = get_incompleted(commands)
    if incompletes is None:
        header = "Hi there, please select a correct option. \nUsage: \n"
        display_help(client, header)
        return
    # print(f'notify(): send following reminders - {incompletes}')
    send_reminder(client, incompletes, users)

def display_help(slack_client: WebClient, header=None):
    if header is None or header == "":
        header = "Hi there, campy is a tool that manages production cycle. \nUsage: \n"
    help_text =  header + \
            "* `/campy notify <number>`: Notifies writers of incomplete assignemnts, \n" + \
            "          where _number_ is optional: \n" \
            "          0 or empty - all incompeleted assignments \n" \
            "          1 - story ideas; 2 - sources; 3 - outlines; 4 - first draft; 5 - final draft\n" \
            "          eg. `/campy notify 2` will notify all incmpleted *sources*\n" \
            "* `/campy grade`: Does grading for writers work\n" + \
            "* `/campy`: Displays this help text"
    slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, 
                                  text=f'{help_text}')

def process_commands(slack_client: WebClient, text: str) -> list:
    if text is None or text == "":
        # print("process_commands(): no sub_command, show Help")
        display_help(slack_client)
        return 
    
    sub_commands = text.lower().split()
    print(f'process_commands(): {sub_commands}')
    return sub_commands

@app.post("/productions")
async def production_status(request: Request, background_tasks: BackgroundTasks):
    try:
        slack_client = slackAPI.get_slack_client()
        print("production_status(): Got a campy request... ")
        
        users = slackAPI.get_users(slack_client)
        
        # headers = request.headers
        # print(f'production_status(): headers = {headers}')
        data = await request.form()
        
        print(f'production_status(): formData = {data}')
        if data is not None and data.get('command') == COMMAND_CAMPY:        
            text = data.get('text')
            response_url = data.get('response_url')
            # user_id = data.get('user_id')
            channel_id = data.get('channel_id')
            print(f'production_status(): command = {text} in channel {channel_id}')
            sub_commands = process_commands(slack_client, text)
            if sub_commands is None or len(sub_commands) == 0:
                return
            if sub_commands[0] == SUB_COMMAND_NOTIFY:
                print(f'production_status(): notify... {sub_commands}')
                notify(slack_client, users, sub_commands)
            elif sub_commands[0] == SUB_COMMAND_GRADE:
                print(f'production_status(): grading...')
                grade(slack_client, response_url, background_tasks)
    except HTTPException as exc:
        print(f'production_status(): HTTPException - {exc.status_code} {exc.detail}')
        # slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, 
        #                              text=f'Something wrong happened on Slack, please contact admin.')
        raise exc
    except Exception as e:        
        print(f"production_status(): ERROR - {e}")
        slack_client.chat_postMessage(channel=CHANNEL_ID_CAMPY, 
                                      text=f'*_There is some problem on the server, please retry later._*')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="Internal Server Error")
        

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


