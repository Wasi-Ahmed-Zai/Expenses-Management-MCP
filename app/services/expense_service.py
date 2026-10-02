from datetime import datetime, timezone
from uuid import uuid4

from gspread.exceptions import APIError, WorksheetNotFound

from app.services.google_sheets import get_worksheet


HEADERS = [
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


def _now():
    return datetime.now(timezone.utc).isoformat()


def _row_to_dict(row):
    row = row + [""] * (len(HEADERS) - len(row))
    return dict(zip(HEADERS, row))


def _get_all_rows():
    try:
        worksheet = get_worksheet()
        return worksheet.get_all_values()
    except WorksheetNotFound:
        raise RuntimeError(
            "The Expenses sheet was not found. "
            "Please check your Google Sheet configuration."
        )
    except APIError:
        raise RuntimeError(
            "Could not connect to Google Sheets. "
            "Please check your Google credentials and permissions."
        )
    except Exception as error:
        raise RuntimeError(
            f"Unable to read expenses right now: {error}"
        )


def _validate_expense_id(expense_id):
    if not expense_id or not expense_id.strip():
        raise ValueError(
            "Please provide an expense ID. "
            "Example: EXP-A1B2C3D4"
        )


def _find_expense_row(expense_id):
    _validate_expense_id(expense_id)

    rows = _get_all_rows()

    for index, row in enumerate(rows[1:], start=2):
        if row and row[0].strip().upper() == expense_id.strip().upper():
            return index, row

    raise ValueError(
        f"Expense '{expense_id}' was not found. "
        "Please check the expense ID and try again."
    )


def add_expense(
    amount: float,
    currency: str = "PKR",
    category: str | None = None,
    description: str | None = None,
    merchant: str | None = None,
    expense_date: str | None = None,
    payment_method: str | None = None,
    account: str | None = None,
    notes: str | None = None,
):
    if amount <= 0:
        raise ValueError(
            "Expense amount must be greater than 0."
        )

    if not currency or not currency.strip():
        raise ValueError(
            "Please provide a currency. Example: PKR or USD."
        )

    try:
        worksheet = get_worksheet()

        expense_id = f"EXP-{uuid4().hex[:8].upper()}"
        now = _now()

        row = [
            expense_id,
            amount,
            currency.upper(),
            category or "",
            description or "",
            merchant or "",
            expense_date or datetime.now().date().isoformat(),
            payment_method or "",
            account or "",
            notes or "",
            now,
            now,
        ]

        worksheet.append_row(row)

        return _row_to_dict(row)

    except APIError:
        raise RuntimeError(
            "The expense could not be saved to Google Sheets. "
            "Please check your Google Sheet access."
        )
    except Exception as error:
        raise RuntimeError(
            f"Could not create the expense: {error}"
        )


def get_expense(expense_id: str):
    _, row = _find_expense_row(expense_id)
    return _row_to_dict(row)


def list_expenses():
    rows = _get_all_rows()

    if len(rows) <= 1:
        return []

    return [
        _row_to_dict(row)
        for row in rows[1:]
        if row
    ]


def update_expense(
    expense_id: str,
    amount: float | None = None,
    currency: str | None = None,
    category: str | None = None,
    description: str | None = None,
    merchant: str | None = None,
    expense_date: str | None = None,
    payment_method: str | None = None,
    account: str | None = None,
    notes: str | None = None,
):
    if amount is not None and amount <= 0:
        raise ValueError(
            "Expense amount must be greater than 0."
        )

    row_number, row = _find_expense_row(expense_id)

    current = _row_to_dict(row)

    updates = {
        "amount": amount,
        "currency": currency,
        "category": category,
        "description": description,
        "merchant": merchant,
        "expense_date": expense_date,
        "payment_method": payment_method,
        "account": account,
        "notes": notes,
    }

    for key, value in updates.items():
        if value is not None:
            current[key] = value

    current["updated_at"] = _now()

    new_row = [
        current[column]
        for column in HEADERS
    ]

    try:
        worksheet = get_worksheet()

        worksheet.update(
            range_name=f"A{row_number}:L{row_number}",
            values=[new_row],
        )

        return current

    except APIError:
        raise RuntimeError(
            "The expense could not be updated in Google Sheets. "
            "Please check your Google Sheet access."
        )
    except Exception as error:
        raise RuntimeError(
            f"Could not update the expense: {error}"
        )


def delete_expense(expense_id: str):
    row_number, _ = _find_expense_row(expense_id)

    try:
        worksheet = get_worksheet()

        worksheet.delete_rows(row_number)

        return {
            "success": True,
            "message": f"Expense '{expense_id}' was deleted successfully.",
            "expense_id": expense_id,
        }

    except APIError:
        raise RuntimeError(
            "The expense could not be deleted from Google Sheets. "
            "Please check your Google Sheet access."
        )
    except Exception as error:
        raise RuntimeError(
            f"Could not delete the expense: {error}"
        )
