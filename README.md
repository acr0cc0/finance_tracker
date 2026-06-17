# Personal Finance Tracker CLI

A simple, lightweight command-line tool to track your daily expenses and monitor spending habits.

## Features

- **Add Expenses**: Log expenditures with category validation.
- **List & Filter**: View all transactions or filter them by category or date.
- **Spending Summaries**: Generate total spend reports for overall, weekly, or monthly periods.
- **Manage Data**: Delete incorrect entries via unique IDs.
- **Local Storage**: All data is stored locally in a `expenses.json` file.

## Installation & Setup

1. Clone this repository or copy the files to your local machine.
2. Ensure you have Python 3.x installed.
3. Navigate to the project directory:
   ```bash
   cd finance_tracker
   ```

## Usage Examples

### Adding an Expense
```bash
python3 finance.py add --amount 12.50 --category Food --description "Lunch at Taco Bell"
```

### Listing Expenses
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

### Generating a Summary Report
- **Overall spend:**
  ```bash
  python3 finance.py summary
  ```
- **Last month's spend:**
  ```bash
  python3 finance.py summary --period month
  ```

### Deleting an Expense
```bash
python3 finance.py delete --id <expense_id>
```

### Listing Available Categories
```bash
python3 finance.py list-categories
```

## Project Structure

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
