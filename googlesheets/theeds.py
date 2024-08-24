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
# UPLOADS_RANGE_NAMES = ["Online Uploads!C2:D", "Online Uploads!E2:I"]
UPLOADS_COL_START = 2
UPLOADS_COL_END = 6
UPLOADS_MAX_NUM = 5

STORY_ASSIGNMENTS_RANGE_NAME = "Story Assignments!A2:F"

def parse_completions(grades: dict, values: list):
    if not values:
        return {}
    
    print(f'Writer, Seed, 5 Story Ideas, 5 Sources, Outline, Rough Draft, Final Draft')    
    for row in values:
        print(f'parse_completions(): {row}')
        total = 0
        if row and row[0].lower() != 'writer'.lower():
            name_key = utils.get_writer_name(row[0])
            g = grades.get(name_key)
            print(f'parse_completions(): {g}')
            if not g:
                continue
            
            # completions = itertools.islice(row, COMPLETION_COL_START, COMPLETION_COL_END)
            completions = row[COMPLETION_COL_START:COMPLETION_COL_END]
            print(f'parse_completions(): {completions}')
            for key, value in zip(const.COMPLETION_ITEMS, completions):
                # print(f'parse_completions(): {key}, {value}, {Completion_points[key]}')
                if value == const.COMPLETION_STATUS_COMPLETE:                    
                    setattr(g, key, const.Completion_points[key])
                    total += const.Completion_points[key]
                
            g.total = total
            g.grade = g.total / const.POINTS_MAX * 100
            print(f'parse_completions(): {g}')

    print(f'parse_completions(): Got {len(grades)} items DONE')

def parse_uploads(grades: dict, values: list):
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

def parse_grades(values: list) -> dict:
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

def grade():
    """
        Give grades based on status on production sheets
    """
    try:
        writers = utils.get_sheet_values(GRADES_SHEET_ID, GRADES_RANGE_NAME)
        if not writers: 
            print('grade(): failed to grade - NO writers')
            return {}
        grades = parse_grades(writers)
        completions = utils.get_sheet_values(COMPLETION_SHEET_ID, COMPLETION_RANGE_NAME)
        parse_completions(grades, completions)
        uploads = utils.get_sheet_values(UPLOADS_SHEET_ID, UPLOADS_RANGE_NAME)
        parse_uploads(grades, uploads)
        print(f'grade(): got {len(grades)} grades, updating...')
        grades = update_grades(GRADES_SHEET_ID, writers, grades)
        # for g in grades.values():
        #     print(f'{g}')
        # return 'OK'
        return grades
    
    except HttpError as err:
        print(err)
        return [err]

if __name__ == "__main__":
    grade()

