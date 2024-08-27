# Campy Slack Bot

A Slack bot for Journalism Production Cycle Management


## Introduction
This is a Slack Bot for Journalism Production that allows users to notify staff writers on pending assignments and grade their works. The Slack bot is a service on cloud that responds to the user commands on Slack. It automates the management process for users and their assignments on the Slack channels.

## Features

- Notify users of incomplete assignments in the team.
- Grade works based on submissions.

## Installation

To use the Campy Slack Bot, follow these steps:

- Install (latest) Python 3.12, if not yet

- Create Python Virtual env:
`python3 -m venv venv`
`source ./venv/bin/activate`
`cd venv`

- Clone the repository:
`git clone https://github.com/kate-j-xia/campy-bot.git`


- Navigate to the project directory:
`cd campy-bot`

- Install the dependencies:
`npm install -r requirements.txt`

(NOTE, you might need to adjust the requirements.txt file to accommodate your env)

## Pre-requisites

- Join the Campy workspace and channels as necessary
- Create the necessary Google Spreadsheets, eg. Completions, etc.
- Make sure the Google sheets are filled with correct columns and values
- Prepare configuration/env variables:
update config.py: `slack_client_token = <Your slack client TOKEN>`


## Usage

Use following commands:
- `/campy notify` to notify users
- `/campy grade` to start grading


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


## License
MIT License