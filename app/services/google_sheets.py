import gspread
from google.oauth2.service_account import Credentials

from app.config import settings


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_worksheet():
    credentials = Credentials.from_service_account_file(
        settings.google_credentials_file,
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        settings.google_spreadsheet_id
    )

    worksheet = spreadsheet.worksheet(
        settings.google_worksheet_name
    )

    return worksheet


def setup_sheet():
    worksheet = get_worksheet()

    headers = [
        "id",
        "amount",
        "currency",
        "category",
        "description",
        "merchant",
        "expense_date",
        "payment_method",
        "account",
        "notes",
        "created_at",
        "updated_at",
    ]

    existing_headers = worksheet.row_values(1)

    if existing_headers != headers:
        worksheet.update(
            range_name="A1:L1",
            values=[headers],
        )

    return worksheet