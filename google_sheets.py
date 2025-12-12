from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os

# --- CONFIG ---
SHEET_NAME = "Liczba odpowiedzi: 1"
RANGE_READ = f"{SHEET_NAME}!A2:S"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_service():
    if not os.path.exists("token.json"):
        raise RuntimeError("Missing token.json")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("sheets", "v4", credentials=creds)


def check_new_rows(spreadsheet_id):
    """
    Returns a list of (row_number, row_values) for rows where:
    - column A is not empty
    - column S is NOT equal to 'tak'
    """
    service = get_service()
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=RANGE_READ
    ).execute()

    values = result.get("values", [])
    new_rows = []

    for idx, row in enumerate(values, start=2):  # header is row 1
        col_a = row[0].strip() if len(row) >= 1 else ""
        col_s = row[18].strip().lower() if len(row) >= 19 else ""

        if col_a and not col_s:
            new_rows.append((idx, row))

    return new_rows

def set_status_in_cols_p_t(spreadsheet_id: str, row_number: int, values: list[str]):
    service = get_service()
    target_range = f"{SHEET_NAME}!P{row_number}:T{row_number}"

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=target_range,
        valueInputOption="RAW",
        body={
            "values": [values]
        }
    ).execute()

def hex_to_rgb_frac(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return {
        "red": int(hex_color[0:2], 16) / 255,
        "green": int(hex_color[2:4], 16) / 255,
        "blue": int(hex_color[4:6], 16) / 255,
    }

def get_sheet_id(spreadsheet_id: str, sheet_name: str) -> int:
    service = get_service()
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    for sheet in meta["sheets"]:
        props = sheet["properties"]
        if props["title"] == sheet_name:
            return props["sheetId"]

    raise ValueError(f"Sheet '{sheet_name}' not found")


def color_cols_a_o_green(spreadsheet_id: str, row_number: int, color: str):
    sheet_id = get_sheet_id(spreadsheet_id, SHEET_NAME)
    """
    Colors background of columns A–O in a given row to green.
    row_number is 1-based.
    sheet_id is the numeric sheetId (NOT sheet name).
    """
    service = get_service()

    requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": row_number - 1,
                    "endRowIndex": row_number,
                    "startColumnIndex": 0,  # A
                    "endColumnIndex": 15     # O (exclusive)
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "foregroundColor": hex_to_rgb_frac(color)
                        }
                    }
                },
                "fields": "userEnteredFormat.textFormat.foregroundColor"
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests}
    ).execute()


# Optional CLI entrypoint
if __name__ == "__main__":
    SPREADSHEET_ID = "1SK0wIP1_JhbvXaoXaZ4A9CVlg0Bxsq5t9OWQdxSxYVY"

    rows = check_new_rows(SPREADSHEET_ID)

    if not rows:
        print("No new rows!")
    else:
        print(f"Found {len(rows)} new row(s):")
        for row_number, row in rows:
            print(f"- Row {row_number}: {row}")
