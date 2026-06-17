import argparse
from manager import FinanceManager

def print_expenses_table(expenses):
    """Helper to print a list of expenses in a formatted table."""
    if not expenses:
        print("No matching expenses found.")
        return

    print(f"{'ID':<38} {'Date':<25} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 100)
    for exp in expenses:
        print(f"{exp['id']:<38} {exp['date']:<25} {exp['category']:<15} ${exp['amount']:<9.2f} {exp['description']}")

def main():
    manager = FinanceManager()
    parser = argparse.ArgumentParser(description="Personal Finance Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", type=str, required=True)
    add_parser.add_argument("--description", type=str, required=True)
    add_parser.add_argument("--date", type=str, help="Date in ISO format (optional)")

    # List command
    list_parser = subparsers.add_parser("list", help="List expenses")
    list_parser.add_argument("--category", type=str)
    list_parser.add_argument("--date", type=str, help="Filter by date (YYYY-MM-DD)")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show spending summary")
    summary_parser.add_argument("--period", type=str, choices=["all", "week", "month"], default="all")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense by ID")
    delete_parser.add_argument("--id", type=str, required=True)

    # Categories command
    subparsers.add_parser("list-categories", help="List all available categories")

    args = parser.parse_args()

    if args.command == "add":
        try:
            manager.add_expense(args.amount, args.category, args.description, args.date)
            print(f"Successfully added expense: {args.description}")
        except ValueError as e:
            print(f"Error: {e}")

    elif args.command == "list":
        expenses = manager.list_expenses(category=args.category, date=args.date)
        print_expenses_table(expenses)

    elif args.command == "summary":
        summary = manager.get_summary(period=args.period)
        period_label = "overall" if args.period == "all" else f"the last {args.period}"
        print(f"--- Summary Report ({period_label}) ---")
        print(f"Total Spent: ${summary['total']:.2f} (across {summary['count']} items)")
        print("-" * 30)
        print("Spending by Category:")
        for cat, total in summary['by_category']:
            print(f"{cat:<15}: ${total:.2f}")
        print("-" * 30)

    elif args.command == "delete":
        if manager.delete_expense(args.id):
            print(f"Successfully deleted expense with ID: {args.id}")
        else:
            print(f"Error: No expense found with ID {args.id}")

    elif args.command == "list-categories":
        print("Standard Categories:")
        for cat in manager.get_categories():
            print(f"- {cat}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
