# 💰 Expense Management MCP Server

A production-ready **Model Context Protocol (MCP) server** for managing expenses through AI assistants.

The server connects AI clients such as **Claude, Cursor, and other MCP-compatible applications** directly to **Google Sheets**, providing structured tools for creating, retrieving, updating, and deleting expense records.

Built with **Python, uv, FastMCP, gspread, Google Sheets API, and Pydantic Settings**.

---

## ✨ Features

* **Full CRUD Operations** — Create, read, update, and delete expenses.
* **Google Sheets Backend** — Store expense data directly in your own Google Spreadsheet.
* **AI-Ready MCP Tools** — Expose structured expense-management tools to MCP-compatible AI clients.
* **Automatic Expense IDs** — Generates unique IDs such as `EXP-A1B2C3D4`.
* **Automatic Timestamps** — Tracks `created_at` and `updated_at` in UTC ISO 8601 format.
* **Multi-Currency Support** — Supports currencies such as PKR, USD, EUR, and GBP.
* **Input Validation** — Validates required fields and prevents invalid expense amounts.
* **Clean Service Architecture** — Separates MCP tools, business logic, configuration, and Google Sheets integration.
* **Streamable HTTP** — Uses FastMCP's modern Streamable HTTP transport.
* **Cloud Deployable** — Can be deployed as a remote MCP server for compatible clients.

---

## 🏗️ Architecture

```text
AI Assistant / MCP Client
          │
          ▼
   FastMCP MCP Server
          │
          ▼
   Expense Service Layer
          │
          ▼
     Google Sheets API
          │
          ▼
    Google Spreadsheet
```

The application is organized into separate layers:

* **MCP Layer** — Exposes expense-management tools.
* **Service Layer** — Handles business logic and CRUD operations.
* **Google Sheets Layer** — Handles spreadsheet authentication and data access.
* **Configuration Layer** — Loads environment variables securely.

---

## 🛠️ Tech Stack

| Technology        | Purpose                               |
| ----------------- | ------------------------------------- |
| Python 3.13+      | Application runtime                   |
| uv                | Dependency and environment management |
| FastMCP           | MCP server framework                  |
| gspread           | Google Sheets integration             |
| Google Sheets API | Spreadsheet data access               |
| Pydantic Settings | Environment configuration             |
| Streamable HTTP   | Remote MCP transport                  |

---

## 📁 Project Structure

```text
expense-management-mcp/
│
├── app/
│   ├── __init__.py
│   │
│   ├── config.py
│   │   └── Environment configuration
│   │
│   ├── mcp/
│   │   ├── __init__.py
│   │   └── server.py
│   │       └── FastMCP server and tool definitions
│   │
│   └── services/
│       ├── __init__.py
│       ├── expense_service.py
│       │   └── Expense business logic and CRUD operations
│       │
│       └── google_sheets.py
│           └── Google Sheets connection and worksheet setup
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── uv.lock
```

> `google-credentials.json` and `.env` are intentionally excluded from version control.

---

# 📊 Google Sheets Schema

The `Expenses` worksheet contains the following fields:

| Column | Field            | Description               | Example                     |
| ------ | ---------------- | ------------------------- | --------------------------- |
| A      | `id`             | Unique expense identifier | `EXP-9F3A1B2C`              |
| B      | `amount`         | Expense amount            | `2500`                      |
| C      | `currency`       | Currency code             | `PKR`                       |
| D      | `category`       | Expense category          | `Food & Dining`             |
| E      | `description`    | Expense description       | `Grocery shopping`          |
| F      | `merchant`       | Vendor or merchant        | `Imtiaz Super Market`       |
| G      | `expense_date`   | Expense date              | `2026-10-02`                |
| H      | `payment_method` | Payment method            | `Credit Card`               |
| I      | `account`        | Bank or account           | `Meezan Bank`               |
| J      | `notes`          | Additional notes          | `Monthly grocery run`       |
| K      | `created_at`     | Creation timestamp        | `2026-10-02T13:24:00+00:00` |
| L      | `updated_at`     | Last update timestamp     | `2026-10-02T13:25:30+00:00` |

The server automatically creates the required headers when the worksheet is initialized.

---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure you have:

* Python 3.13+
* [uv](https://docs.astral.sh/uv/)
* A Google Cloud project
* Google Sheets API enabled
* A Google service account
* A Google Spreadsheet

---

# ☁️ Google Cloud Setup

## 1. Create a Google Cloud Project

Open the [Google Cloud Console](https://console.cloud.google.com/) and create a project.

Example:

```text
Expense Management MCP
```

---

## 2. Enable Google Sheets API

Go to:

```text
Google Cloud Console
→ APIs & Services
→ Library
→ Google Sheets API
→ Enable
```

---

## 3. Create a Service Account

Go to:

```text
IAM & Admin
→ Service Accounts
→ Create Service Account
```

Give the service account an appropriate name, for example:

```text
expense-management-mcp
```

---

## 4. Create a Service Account Key

Open the service account:

```text
Keys
→ Add Key
→ Create new key
→ JSON
```

Download the JSON credentials file and place it in the project root as:

```text
google-credentials.json
```

**Never commit this file to GitHub.**

---

# 📑 Google Spreadsheet Setup

## 1. Create a Spreadsheet

Create a new Google Spreadsheet.

Example name:

```text
Expense Management DB
```

---

## 2. Create the Worksheet

Create or rename the worksheet tab to:

```text
Expenses
```

The application will automatically create the required column headers.

---

## 3. Get the Spreadsheet ID

From:

```text
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
```

Copy:

```text
SPREADSHEET_ID
```

---

## 4. Share the Spreadsheet

Share the spreadsheet with the **service account email address** from your Google credentials file.

Give it:

```text
Editor
```

permission.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd expense-management-mcp
```

---

## 2. Install Dependencies

Using `uv`:

```bash
uv sync
```

This creates the project's virtual environment and installs the dependencies defined in `pyproject.toml`.

---

# 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
GOOGLE_CREDENTIALS_FILE=google-credentials.json
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_WORKSHEET_NAME=Expenses
```

### `.env.example`

For GitHub, provide a safe template:

```env
GOOGLE_CREDENTIALS_FILE=google-credentials.json
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_WORKSHEET_NAME=Expenses
```

Never place real credentials or private keys in `.env.example`.

---

# ▶️ Running the Server

Start the FastMCP server with:

```bash
uv run python -m app.mcp.server
```

The server uses:

```text
Streamable HTTP
```

and is available locally at:

```text
http://127.0.0.1:8000/mcp
```

---

# 🔌 MCP Client Integration

The server can be connected to MCP-compatible clients either locally or through a deployed HTTPS endpoint.

## Local Development

For local MCP clients, configure the server using the appropriate MCP configuration for your client.

Example command-based configuration:

```json
{
  "name": "expense-management",
  "command": "uv",
  "args": [
    "--directory",
    "/absolute/path/to/expense-management-mcp",
    "run",
    "python",
    "-m",
    "app.mcp.server"
  ]
}
```

---

# ☁️ Remote Deployment

For remote MCP clients, deploy the FastMCP server to a hosting environment that supports Python applications and expose it through HTTPS.

The deployment flow is:

```text
GitHub Repository
       ↓
FastMCP Deployment
       ↓
Public HTTPS MCP Endpoint
       ↓
Claude / Cursor / Other MCP Client
```

For production deployment, make sure the Google credentials are provided through the hosting platform's secure environment/secret configuration rather than committed to the repository.

---

# 🧰 Available MCP Tools

The server currently exposes **5 MCP tools**.

## 1. `create_expense`

Creates a new expense in Google Sheets.

### Required

```text
amount
```

### Optional

```text
currency
category
description
merchant
expense_date
payment_method
account
notes
```

### Example

```text
Create an expense of 1500 PKR for lunch at Cafe Aylanto using Credit Card.
```

---

## 2. `get_expenses`

Retrieves all recorded expenses.

### Parameters

```text
None
```

### Example

```text
Show me all my expenses.
```

---

## 3. `get_expense_by_id`

Retrieves a specific expense using its unique ID.

### Required

```text
expense_id
```

Example:

```text
EXP-A1B2C3D4
```

---

## 4. `edit_expense`

Updates an existing expense.

Only the provided fields are modified; unspecified fields remain unchanged.

### Required

```text
expense_id
```

### Optional

```text
amount
currency
category
description
merchant
expense_date
payment_method
account
notes
```

### Example

```text
Update expense EXP-A1B2C3D4 and change its category to Office Supplies.
```

---

## 5. `remove_expense`

Deletes an expense by its unique ID.

### Required

```text
expense_id
```

### Example

```text
Delete expense EXP-A1B2C3D4.
```

---

# 💬 Example AI Prompts

Once connected to an MCP-compatible AI client, you can interact with the expense system using natural language.

```text
Log an expense of 1500 PKR for lunch at Cafe Aylanto using Credit Card.
```

```text
Show me all my expenses.
```

```text
Find expense EXP-1A2B3C4D.
```

```text
Update EXP-1A2B3C4D and change the category to Office Supplies.
```

```text
Delete expense EXP-1A2B3C4D.
```

---

# 🧪 Validation & Error Handling

The server includes validation and structured responses for common operations.

For example:

```text
Amount must be greater than 0.
```

Invalid expense IDs return a clear error instead of silently failing.

Tool responses follow a consistent structure:

### Success

```json
{
  "success": true,
  "message": "Expense created successfully.",
  "data": {}
}
```

### Error

```json
{
  "success": false,
  "message": "Expense was not found."
}
```

---

# 🔒 Security

This project uses a Google service account to access the spreadsheet.

Follow these security practices:

* Never commit `.env`.
* Never commit `google-credentials.json`.
* Never expose Google service account private keys.
* Store production credentials using your hosting provider's secret/environment-variable system.
* Give the service account access only to the spreadsheet(s) it needs.
* Rotate compromised credentials immediately.

---

# 🧭 Roadmap

Planned improvements may include:

* [ ] Expense summaries and analytics
* [ ] Monthly expense reports
* [ ] Category-based spending analysis
* [ ] Date-range filtering
* [ ] Budget management
* [ ] Recurring expenses
* [ ] Expense statistics
* [ ] CSV/Excel export
* [ ] Advanced search and filtering
* [ ] Production authentication
* [ ] Multi-user expense management
* [ ] Automated financial reports

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the changes.
5. Submit a pull request.

---

# 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Built as an AI-powered expense management system using **Model Context Protocol, FastMCP, Python, and Google Sheets**.

---

## ⭐ Project Goal

The goal of this project is to demonstrate how an MCP server can turn a traditional data source such as Google Sheets into an **AI-accessible expense management system** through structured tools and natural-language interactions.
