from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import numpy as np
import pandas as pd

from .gauth import authenticate
from .production import Production

def get_sheet():  
    """
        returns the Google Sheet object handler
    """
    creds = authenticate()

    try:
        service = build("sheets", "v4", credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        return sheet

    except HttpError as err:
        print(f'get_sheet_service(): {err}')
        return err

def get_sheet_values(sheet_id: str, range_name: str) -> list:
    """
        get a single sheet values based on the given sheetID and range name
    """
    try:
        # Call the Sheets API for single sheet range
        sheet = get_sheet()
        result = (
            sheet.values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print("No data found.")
            return

        # Googlesheets will omit empty cells
        df = pd.DataFrame(values)
        df_replace = df.replace([''], [None])

        # convert back to list with empty cells 
        results = df_replace.values.tolist()
        # print(f'get_sheet_values(): {results}')
        print(f"get_sheet_values(): got {len(results)} rows")
        return results

    except HttpError as err:
        print(err)
        return [err]
    
def update_values(sheet_id, range_name, value_input_option, values):
    """
        Update the sheet values for the given range
    """
    try:
        # service = build("sheets", "v4", credentials=creds)
        sheet = get_sheet()
        body = {"values": values}
        result = (
            sheet.values()
            .update(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

  
def batch_get_sheet_values(sheet_id: str, range_names) -> list:
  """
    get a single sheet values based on the given sheetID and range name
  """
  try:
    # Call the Sheets API for single sheet range

    sheet = get_sheet()
  
    result = (
        sheet.values()
        .batchGet(spreadsheetId=sheet_id, ranges=range_names)
        .execute()
    )
    values = result.get("valueRanges", [])

    if not values:
      print("No data found.")
      return

    print(f"batch_get_sheet_values(): got {len(values)} rows")
    return values

  except HttpError as err:
    print(err)
    return [err]

def parse_results(values: list) -> list:
    results = []
    if values:
        for row in values:
            if row:
                # print(f"{row}")
                print(f"{row[0], row[1], row[2]} ")
                p = Production(row[0], row[1], row[2])
                if p.status == "Done":
                    results.append(p)
    print(f'Got {len(results)} items DONE:')
    for p in results:
        print(f'{p}')
    return results

def get_writer_name(name_str: str) -> str:
    if name_str is None:
        return ""
    return name_str.lower()

    # name = name_str.split(' ')
    # for token in name:
    #     print(token)
    # firstname = name[0].lower()
    # lastname = name[1] # TODO: some lastname missing on the sheet
    # fullname = (firstname, lastname)

    # TODO: this is a bug - need to populate sheets with lastname first 
    # then use fullname instead of firstname as the dict key

    # return firstname

