import json
import uuid
from datetime import datetime
import argparse
import os

DATA_FILE = "expenses.json"
DEFAULT_CATEGORIES = ["Food", "Transport", "Entertainment", "Health", "Utilities", "Shopping", "Other"]

def load_expenses():
    """Loads expenses from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_expenses(expenses):
    """Saves expenses to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

def add_expense(amount, category, description, date=None):
    """Adds a new expense and saves it."""
    if category not in DEFAULT_CATEGORIES:
        print(f"Error: Invalid category '{category}'.")
        print(f"Available categories are: {', '.join(DEFAULT_CATEGORIES)}")
        return

    expenses = load_expenses()
    
    if date is None:
        date = datetime.now().isoformat()
    
    new_expense = {
        "id": str(uuid.uuid4()),
        "date": date,
        "amount": float(amount),
        "category": category,
        "description": description
    }
    
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Successfully added expense: {description} (${amount})")

def list_categories():
    """Prints the list of standard categories."""
    print("Standard Categories:")
    for cat in DEFAULT_CATEGORIES:
        print(f"- {cat}")

def list_expenses():
    """Lists all expenses in a formatted table."""
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Header
    print(f"{'ID':<38} {'Date':<25} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 100)

    for exp in expenses:
        print(f"{exp['id']:<38} {exp['date']:<25} {exp['category']:<15} ${exp['amount']:<9.2f} {exp['description']}")

def main():
    parser = argparse.ArgumentParser(description="Personal Finance Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'add' command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Amount of the expense")
    add_parser.add_argument("--category", type=str, required=True, help="Category (e.g., Food, Transport)")
    add_parser.add_argument("--description", type=str, required=True, help="Brief description")
    add_parser.add_argument("--date", type=str, help="Date in ISO format (optional)")

    # 'list-categories' command
    subparsers.add_parser("list-categories", help="List all available categories")

    # 'list' command
    subparsers.add_parser("list", help="List all expenses")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.category, args.description, args.date)
    elif args.command == "list-categories":
        list_categories()
    elif args.command == "list":
        list_expenses()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
