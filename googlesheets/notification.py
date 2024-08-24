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
GRADES_RANGE_NAME = "A4:M"
GRADES_UPDATE_RANGE_NAME = "D4:G"

COMPLETION_SHEET_ID = "14Uo9HBfeEo-j7kzHLQ3NDRsjKyshA_EcfhX2S4GKRBM" 
COMPLETION_RANGE_NAME = "C2:J"
COMPLETION_COL_START = 4
COMPLETION_COL_END = 8
COMPLETION_MAX_NUM = 5

UPLOADS_SHEET_ID = "1-nkn_oOwenidq_dHRcgW5Ic_G5_zcei668oG5TCmVFE"
UPLOADS_RANGE_NAME = "Online Uploads!C2:J"
# UPLOADS_RANGE_NAMES = ["Online Uploads!C2:D", "Online Uploads!E2:I"]
UPLOADS_COL_START = 3
UPLOADS_COL_END = 7
UPLOADS_MAX_NUM = 5

ASSIGNMENTS_SHEET_ID = "1-nkn_oOwenidq_dHRcgW5Ic_G5_zcei668oG5TCmVFE"
STORY_ASSIGNMENTS_RANGE_NAME = "Story Assignments!A2:F"
ART_ASSIGNMENTS_RANGE_NAME = "Art Assignments!A2:I"
SOCIAL_MEDIA_RANGE_NAME = "Social Media!A2:F"

def parse_story_assignments(values: list, assignments: dict):
    if not values:
        return {}
    
    print(f'Writer, Incomplete Assignments')    
    
    for row in values:
        print(f'parse_story_assignments(): {row}')
        writer = row[2].lower()
        if row and writer != 'writer' and row[0] != '':
            name_key = utils.get_writer_name(writer)
            story = row[1]
            status = row[5] # if row[5] else const.COMPLETION_STATUS_INCOMPLETE
            if status != const.COMPLETION_STATUS_COMPLETE:
                if name_key not in assignments:                    
                    assignments[name_key] = [f'{story} is {status}']
                else: 
                    assignments[name_key].append(f'{story} is {status}')
            
            # print(f'parse_story_assignments(): {assignments}')

    print(f'parse_story_assignments(): Got {len(assignments)} items DONE')

def parse_art_assignments(grades: dict, values: list):
    if not values:
        return {}
    
    print(f'Writer  ')
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
            
            print(f'parse_art_assignments(): {g}') 

def parse_social_media(values: list, assignments: dict) -> dict:
    if not values:
        return {}
    
    results = {}
    print(f'Writer  Assignments ')
    for row in values:
        print(f'parse_social_media(): {row}')
        writer = row[2].lower()
        if row and writer != 'writer' and row[0] != '':
            name_key = utils.get_writer_name(writer)
            story = row[1]
            try: 
                photo_status = row[3] # if row[3] else ''
                status1 = row[4] # if row[4] else const.COMPLETION_STATUS_INCOMPLETE
                status2 = row[5] # if row[5] else const.COMPLETION_STATUS_INCOMPLETE
            except IndexError:
                pass
            if photo_status != 'TRUE' or \
                status1 != const.COMPLETION_STATUS_COMPLETE or \
                status2 != const.COMPLETION_STATUS_COMPLETE:
                if name_key not in assignments:                    
                    assignments[name_key] = [f'{story} is incomplete']
                else: 
                    assignments[name_key].append(f'{story} is pending')
      
    print(f'parse_social_media(): Got {len(values)} assignments DONE')
    
    return results

def check_assignments() -> dict:
    assignments = {}
    parse_story_assignments(utils.get_sheet_values(ASSIGNMENTS_SHEET_ID, STORY_ASSIGNMENTS_RANGE_NAME), assignments)
    # parse_social_media(utils.get_sheet_values(ASSIGNMENTS_SHEET_ID, SOCIAL_MEDIA_RANGE_NAME), assignments)
    # parse_art_assignments()

    print(f'check_assignments(): got {len(assignments)} writers with pending tasks')
    return assignments



