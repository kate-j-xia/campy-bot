import os.path

# import asyncio
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tokenize import tokenize
import itertools

from .gauth import authenticate
from .production import Production
from . import utils
from . import constants as const

GRADES_SHEET_ID = "18Eeer2gG0OCfR9LwxlFhiXLE2kyLXTMMTvse3SUiaYo"
GRADES_RANGE_NAME = "A4:L"
GRADES_UPDATE_RANGE_NAME = "E4:F"

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

def update_incompletes(assignments: dict, writer: str, value: str):
    if writer not in assignments:
        assignments[writer] = []

    assignments[writer].append(value)

    
def parse_story_assignments(assignments: dict, values: list):
    if not values:
        return {}
    
    # print(f'Writer, Incomplete Assignments')    
    for row in values:        
        if row and row[2].lower() != 'writer':
            # print(f'parse_story_assignments(): {row}')
            writer = utils.get_writer_name(row[2])
            story_name = row[1]
            status = row[5]
            if status != STATUS_COMPLETE:
                update_incompletes(assignments, writer, story_name + " is " + status)
                # print(f'parse_story_assignments(): {assignments[writer]}')
            

    print(f'parse_story_assignments(): incomplete assignments = {assignments}')

    print(f'parse_story_assignments(): Got {len(assignments)} incompleted assignments.')

def parse_social_media(grades: dict, values: list):
    if not values:
        return {}
    
    print(f'Writer  Showcase?  Category: Graphic/Credits 3 Tags/Hyperlinks If Photo -> Full Immersive')
    for row in values:
        if row and row[0].lower() != 'writer'.lower():
            name_key = utils.get_writer_name(row[0])
            g = grades.get(name_key)
            if not g:
                continue
            
            for u in itertools.islice(row, UPLOADS_COL_START, UPLOADS_COL_END):
                if u == 'TRUE':
                    g.uploads += 1
                
            # if all pieces are uploaded, can earn the upload points
            if g.uploads >= UPLOADS_MAX_NUM:
                g.uploaded += const.POINTS_UPLOADED
                g.total += const.POINTS_UPLOADED
                g.grade = g.total / const.POINTS_MAX * 100
            
            print(f'parse_uploads(): {g}') 

def parse_art_assignments(values: list) -> dict:
    if not values:
        return {}
    
    results = {}
    print(f'Writer  Grade  Total ')
    for row in values:
        if row and row[0].lower() != 'writer'.lower():
            lastname = row[0].lower()
            firstname = row[1].lower()     
            p = Production(firstname, lastname)

            # print(f'parse_grades(): {p}')

            # TODO: change key to fullname after fixing the sheets
            results[firstname] = p
        
    print(f'parse_grades(): Got {len(results)} grades DONE')
    
    return results

def update_grades(sheet_id: str, writers: list, grades: dict):
    """
        Updates writers grades on the grade sheet
    """  
    try:        
        index = const.GRADES_UPDATE_STARTING_ROW  # data starts at row 4
        for row in writers:
            index += 1
            if row and row[0].lower() != 'writer'.lower():
                lastname = row[0].lower()
                firstname = row[1].lower() 
                # TODO: use fullname as the key  
                g = grades.get(firstname)    
                range = f'E{index}:F{index}'
                values = [[g.grade, g.total]]                

                utils.update_values(sheet_id, range, "USER_ENTERED", values)        
                print(f'update_grades(): range = {range}, grade = {values}')  
    except HttpError as error:
        print(f"An error occurred in update_grades(): {error}")
        return error
    

def get_incompleted() -> dict:
    """
        Get incompleted assignments on production sheets
    """
    try:
        assignments = {}
        parse_story_assignments(assignments, utils.get_sheet_values(ASSIGNMENTS_SHEET_ID, STORY_RANGE_NAME))
                                    
        # parse_art_assignments(assignments, utils.get_sheet_values(UPLOADS_SHEET_ID, ART_RANGE_NAME))

        # parse_social_media(assignments, utils.get_sheet_values(UPLOADS_SHEET_ID, SOCIAL_MEDIA_RANGE_NAME))
        print(f'notify(): got {len(assignments)} incomplete assignments...')

        return assignments
    
    except HttpError as err:
        print(err)
        return [err]



