# Personal Finance Tracker

A simple, lightweight tool to track your daily expenses and monitor spending habits. It offers both a powerful Command Line Interface (CLI) for speed and a Graphical User Interface (GUI) for ease of use.

## Features

- **Add Expenses**: Log expenditures with category validation.
- **List & Filter**: View all transactions or filter them by category or date.
- **Spending Summaries**: Generate total spend reports for overall, weekly, or monthly periods.
- **Manage Data**: Delete incorrect entries via unique IDs.
- **Local Storage**: All data is stored locally in a `expenses.json` file.

## Usage Examples

### Graphical User Interface (GUI)
To launch the visual application, run:
```bash
python3 gui.py
```
The GUI allows you to add expenses via a form, filter transactions using dropdowns and text fields, and view your total spending in real-time.

### Command Line Interface (CLI)
**Adding an Expense**
```bash
python3 finance.py add --amount 12.50 --category Food --description "Lunch at Taco Bell"
```

**Listing Expenses**
- **All expenses:**
  ```bash
  python3 finance.py list
  ```
- **Filter by category:**
  ```bash
  python3 finance.py list --category Food
  ```
- **Filter by date (YYYY-MM-DD):**
  ```bash
  python3 finance.py list --date 2026-06-17
  ```

**Generating a Summary Report**
- **Overall spend:**
  ```bash
  python3 finance.py summary
  ```
- **Last month's spend:**
  ```bash
  python3 finance.py summary --period month
  ```

**Deleting an Expense**
```bash
python3 finance.py delete --id <expense_id>
```

**Listing Available Categories**
```bash
python3 finance.py list-categories
```

## Project Structure

- `gui.py`: The Graphical User Interface entry point (Tkinter).
- `finance.py`: The CLI entry point. Handles user input and output formatting.
- `manager.py`: Contains the `FinanceManager` class which handles data persistence and business logic.
- `expenses.json`: Local JSON file where your expenses are stored.

## Data Schema

Expenses are stored as an array of objects:
```json
{
  "id": "UUID",
  "date": "ISO8601 Timestamp",
  "amount": float,
  "category": string,
  "description": string
}
```
