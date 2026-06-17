import json
import uuid
import os
from datetime import datetime, timedelta

class FinanceManager:
    def __init__(self, data_file="expenses.json"):
        self.data_file = data_file
        self.categories = ["Food", "Transport", "Entertainment", "Health", "Utilities", "Shopping", "Other"]

    def load_expenses(self):
        """Loads expenses from the JSON file."""
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def save_expenses(self, expenses):
        """Saves expenses to the JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(expenses, f, indent=4)

    def add_expense(self, amount, category, description, date=None):
        """Adds a new expense and saves it."""
        if category not in self.categories:
            raise ValueError(f"Invalid category '{category}'. Available: {', '.join(self.categories)}")

        expenses = self.load_expenses()
        
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
        self.save_expenses(expenses)
        return new_expense

    def list_expenses(self, category=None, date=None):
        """Returns a filtered list of expenses."""
        expenses = self.load_expenses()
        
        if category:
            expenses = [e for e in expenses if e['category'].lower() == category.lower()]
        
        if date:
            expenses = [e for e in expenses if e['date'].startswith(date)]

        return expenses

    def delete_expense(self, expense_id):
        """Removes an expense by its ID."""
        expenses = self.load_expenses()
        initial_count = len(expenses)
        updated_expenses = [e for e in expenses if e['id'] != expense_id]
        
        if len(updated_expenses) == initial_count:
            return False

        self.save_expenses(updated_expenses)
        return True

    def get_summary(self, period="all"):
        """Calculates total spending and per-category totals for a given period."""
        expenses = self.load_expenses()
        now = datetime.now()
        start_date = None

        if period == "week":
            start_date = now - timedelta(days=7)
        elif period == "month":
            start_date = now - timedelta(days=30)

        filtered = []
        for e in expenses:
            exp_date = datetime.fromisoformat(e['date'])
            if start_date is None or exp_date >= start_date:
                filtered.append(e)

        total_overall = sum(e['amount'] for e in filtered)
        category_totals = {}
        for e in filtered:
            cat = e['category']
            category_totals[cat] = category_totals.get(cat, 0) + e['amount']

        return {
            "total": total_overall,
            "by_category": sorted(category_totals.items(), key=lambda x: x[1], reverse=True),
            "count": len(filtered)
        }

    def get_categories(self):
        return self.categories
