# Newspaper Production Slackbot

A Slack bot for Production Cycle Management

## Introduction

This is a Slackbot for journalism production that allows users to notify staff writers on pending assignments and grade their works. The Slackbot is a service on cloud that responds to the user commands on Slack. It automates the management process for users and their assignments on the Slack channels.

## Features

- Notify users of incomplete assignments in the team.
- Grade works based on submissions.

## Installation

To use the Campy Slack Bot, follow these steps:

- Install (latest) Python 3.12, if not yet

- Create Python Virtual env:

```
python3 -m venv venv
source ./venv/bin/activate
cd venv
```

- Clone the repository:

```
git clone https://github.com/kate-j-xia/campy-bot.git
```


- Navigate to the project directory:

```
cd campy-bot
```

- Install the dependencies:

```
pip install -r requirements.txt
```

(NOTE, you might need to adjust the requirements.txt file to accommodate your env)

## Pre-requisites

- Join the Campy workspace and channels as necessary
- Create the necessary Google Spreadsheets, eg. SEED, GRADES, etc.
- Make sure the Google sheets are filled with **correct/valid columns and values**
- Prepare configuration/env variables:

  1. update config.py and copy it to `campy-bot` directory:
     
     ```
     SLACK_CLIENT_TOKEN = "<Your slack client TOKEN>"
     SLACK_CHANNEL_ID = "#campy"
     SLACK_COMMAND = "/campy"
  
     GRADES_SHEET_ID = "<YOUR GRADES SHEET ID>"
     GRADES_RANGE_NAME = "A4:M"
     GRADES_BASE_COLUMN = 6
     GRADES_INCOMP_COL_START = 1
     GRADES_INCOMP_COL_END = 5
      
     SEED_SHEET_ID = "<YOUR SEED SHEET ID>"
     SEED_RANGE_NAME = "A2:I"
     SEED_BASE_COLUMN = 3
     SEED_INCOMP_COL_START = 1
     SEED_INCOMP_COL_END = 5
     ```
     
  3. copy `key.json` file to `campy-bot` directory

## Usage

Use following commands:

- `/campy`: display the help text
- `/campy notify <number 1 - 5>`: notify users of incompleted assignments

    where _number_ is optional \
    0 or empty - all incompeleted assignments \
    1 - story ideas; 2 - sources; 3 - outlines; 4 - first draft; 5 - final draft \
    eg. `/campy notify 2` will notify all incmpleted *sources* \
- `/campy grade`: grade


## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes.
- Commit your changes.
- Push your changes to your forked repository.
- Submit a pull request (PR)
- Please make sure to update tests as appropriate.
- Once the PR is merged into `main`
- rebuild/restart the project from `main` 
- verify the changes are effective on the site and on Slack channels

