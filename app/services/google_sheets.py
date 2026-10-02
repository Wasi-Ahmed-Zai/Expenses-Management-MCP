import json

import gspread
from google.oauth2.service_account import Credentials

from app.config import settings


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


def _get_credentials():
    """Load Google credentials from a JSON file or environment variable."""

    if settings.google_credentials_json:
        credentials_info = json.loads(
            settings.google_credentials_json
        )

        return Credentials.from_service_account_info(
            credentials_info,
            scopes=SCOPES,
        )

    if settings.google_credentials_file:
        return Credentials.from_service_account_file(
            settings.google_credentials_file,
            scopes=SCOPES,
        )

    raise RuntimeError(
        "Google credentials are not configured. "
        "Set GOOGLE_CREDENTIALS_JSON or "
        "GOOGLE_CREDENTIALS_FILE."
    )


def get_worksheet():
    """Connect to Google Sheets and return the Expenses worksheet."""

    credentials = _get_credentials()

    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(
        settings.google_spreadsheet_id
    )

    worksheet = spreadsheet.worksheet(
        settings.google_worksheet_name
    )

    return worksheet


def setup_sheet():
    """Create or update the Expenses worksheet headers."""

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