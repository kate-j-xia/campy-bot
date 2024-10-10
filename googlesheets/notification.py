import os.path

# import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tokenize import tokenize
import itertools
from pathlib import Path

from .gauth import authenticate
from .production import Production
from . import utils
from . import constants as const
import config

""" GRADES_SHEET_ID = "18Eeer2gG0OCfR9LwxlFhiXLE2kyLXTMMTvse3SUiaYo"
GRADES_RANGE_NAME = "A4:M"
GRADES_NOTIFY_RANGE_NAME = "H4:M"
GRADES_BASE_COLUMN = 6
GRADES_INCOMP_COL_START = 1
GRADES_INCOMP_COL_END = 5

SEED_SHEET_ID = "1Gyuh0IaMBrzfruZvKXVEH2KCS8sW-49VAn8QYWpxQ-w"
SEED_RANGE_NAME = "A2:I"
SEED_NOTIFY_RANGE_NAME = "E2:I"
SEED_BASE_COLUMN = 3
SEED_INCOMP_COL_START = 1
SEED_INCOMP_COL_END = 5
 """
COMPLETION_SHEET_ID = "14Uo9HBfeEo-j7kzHLQ3NDRsjKyshA_EcfhX2S4GKRBM" 
COMPLETION_RANGE_NAME = "C2:I"
COMPLETION_COL_START = 2
COMPLETION_COL_END = 7
COMPLETION_MAX_NUM = 5

UPLOADS_SHEET_ID = "1-nkn_oOwenidq_dHRcgW5Ic_G5_zcei668oG5TCmVFE"
UPLOADS_RANGE_NAME = "Online Uploads!C2:I"
UPLOADS_COL_START = 2
UPLOADS_COL_END = 6
UPLOADS_MAX_NUM = 5

ASSIGNMENTS_SHEET_ID = "1-nkn_oOwenidq_dHRcgW5Ic_G5_zcei668oG5TCmVFE"
STORY_RANGE_NAME = "Story Assignments!A2:H"
STORY_COL_START = 2
STORY_COL_END = 6
STORY_MAX_NUM = 5

ART_RANGE_NAME = "Art Assignments!A2:I"
SOCIAL_MEDIA_RANGE_NAME = "Social Media!A2:I"

STATUS_INCOMPLETE = "Incomplete"
STATUS_COMPLETE = "Complete"

GRADES_BASE_COLUMN = 6

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def update_incompletes(incompletes: dict, writer: str, value: str):
    if writer not in incompletes:
        incompletes[writer] = []
    else:
        incompletes[writer].append(", ")

    incompletes[writer].append(value)
    
def check_seed_incompletes(incompletes: dict, values: list, which_column=0):
    if not values: #  or which_column >= len(values):
        return {}
    
    print(f'check_seed_incompletes(): requested for column {which_column}...')    
    for row in values:        
        if row and row[2] and row[2].lower() != 'writer':
            print(f'check_seed_incompletes(): {row}')
            writer = utils.get_writer_name(row[2])
            # column_name = const.Incompletes(which_column).name
            # status = int(row[SEED_BASE_COLUMN + which_column])           
            column_name = const.NUMBER_TO_ASSIGNMENTS[which_column] + " for your " + row[0] # story category
            if row[1] is not None: # story name
                column_name += " story _" + row[1] + "_"           
            status = row[config.SEED_BASE_COLUMN + which_column]
            if status != STATUS_COMPLETE:
            # if status <= 0:
                if status is None:
                    status = STATUS_INCOMPLETE
                update_incompletes(incompletes, writer, column_name + " is " + str(status).lower())
                
                # print(f'check_incompletes(): {incompletes[writer]}')
    # print(f'check_seed_incompletes(): incomplete assignments = {incompletes}')
    print(f'check_seed_incompletes(): Got {len(incompletes)} incompleted assignments.')

def parse_story_assignments(assignments: dict, values: list):
    if not values:
        return {}
    
    # print(f'Writer, Incomplete Assignments')    
    for row in values:        
        if row and row[2] and row[2].lower() != 'writer':
            # print(f'parse_story_assignments(): {row}')
            writer = utils.get_writer_name(row[2])
            story_name = row[1]
            status = row[5]
            if status != STATUS_COMPLETE:
                update_incompletes(assignments, writer, story_name + " is " + status)
                # print(f'parse_story_assignments(): {assignments[writer]}')
    # print(f'parse_story_assignments(): incomplete assignments = {assignments}')
    print(f'parse_story_assignments(): Got {len(assignments)} incompleted assignments.')

def parse_art_assignments(values: list) -> dict:
    if not values:
        return {}
    
    results = {}
    print(f'Writer  Grade  Total ')
    for row in values:
        if row and row[0] and row[0].lower() != 'writer':
            lastname = row[0].lower()
            firstname = row[1].lower()     
            p = Production(firstname, lastname)
            # print(f'parse_grades(): {p}')
            # TODO: change key to fullname after fixing the sheets
            results[firstname] = p
        
    print(f'parse_grades(): Got {len(results)} grades DONE')    
    return results

def get_incompleted(commands):
    """
        Get incompleted assignments on production sheets
    """
    try:
        incompletes = {}
        # assignments = utils.get_sheet_values(GRADES_SHEET_ID, GRADES_RANGE_NAME)
        assignments = utils.get_sheet_values(config.SEED_SHEET_ID, config.SEED_RANGE_NAME)
        # parse_story_assignments(incompletes, utils.get_sheet_values(ASSIGNMENTS_SHEET_ID, STORY_RANGE_NAME))                                    
        # parse_art_assignments(incompletes, utils.get_sheet_values(UPLOADS_SHEET_ID, ART_RANGE_NAME))
        # parse_social_media(incompletes, utils.get_sheet_values(UPLOADS_SHEET_ID, SOCIAL_MEDIA_RANGE_NAME))
        if len(commands) > 1:
            which_column = int(commands[1])            
            print(f'get_incompleted(): get column {which_column} incompletes only.')
            if which_column < config.SEED_INCOMP_COL_START or which_column > config.SEED_INCOMP_COL_END:
                print(f'get_incompleted(): invalid column for SEED sheet - {which_column}')
                return None
            check_seed_incompletes(incompletes, assignments, which_column)
        else: # check for all assignments
            for inc in const.Incompletes:
                print(f'get_incompleted(): {inc.value}')
                check_seed_incompletes(incompletes, assignments, inc.value)

        print(f'get_incompleted(): got total {len(incompletes)} incompleted assignments...')

        return incompletes
    
    except HttpError as err:
        print(err)
        return [err]



