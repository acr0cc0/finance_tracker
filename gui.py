import tkinter as tk
from tkinter import ttk, messagebox
from manager import FinanceManager

class FinanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("900x600")
        
        self.manager = FinanceManager()
        
        self.setup_ui()
        self.refresh_data()

    def setup_ui(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Section 1: Add Expense
        add_frame = ttk.LabelFrame(main_frame, text="Add New Expense", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(add_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(add_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
        self.category_combo = ttk.Combobox(add_frame, values=self.manager.get_categories(), state="readonly")
        self.category_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(add_frame, text="Description:").grid(row=0, column=4, padx=5, pady=5)
        self.desc_entry = ttk.Entry(add_frame)
        self.desc_entry.grid(row=0, column=5, padx=5, pady=5)

        add_btn = ttk.Button(add_frame, text="Add Expense", command=self.handle_add)
        add_btn.grid(row=0, column=6, padx=10, pady=5)

        # Section 2: Filters and Table
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Filter Bar
        filter_frame = ttk.Frame(list_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text="Filter Category:").pack(side=tk.LEFT, padx=5)
        self.filter_cat_combo = ttk.Combobox(filter_frame, values=["All"] + self.manager.get_categories(), state="readonly")
        self.filter_cat_combo.set("All")
        self.filter_cat_combo.pack(side=tk.LEFT, padx=5)
        self.filter_cat_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_data())

        ttk.Label(filter_frame, text=" Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.filter_date_entry = ttk.Entry(filter_frame)
        self.filter_date_entry.pack(side=tk.LEFT, padx=5)
        
        filter_btn = ttk.Button(filter_frame, text="Filter", command=self.refresh_data)
        filter_btn.pack(side=tk.LEFT, padx=10)

        # Table (Treeview)
        columns = ("id", "date", "category", "amount", "description")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("category", text="Category")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("description", text="Description")

        self.tree.column("id", width=300)
        self.tree.column("date", width=200)
        self.tree.column("category", width=120)
        self.tree.column("amount", width=80)
        self.tree.column("description", width=250)

        # Scrollbar for table
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Section 3: Footer (Summary & Delete)
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(20, 0))

        self.summary_label = ttk.Label(footer_frame, text="Total Spent: $0.00", font=("Arial", 12, "bold"))
        self.summary_label.pack(side=tk.LEFT)

        delete_btn = ttk.Button(footer_frame, text="Delete Selected", command=self.handle_delete)
        delete_btn.pack(side=tk.RIGHT)

    def refresh_data(self):
        # Clear current table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filters
        cat = self.filter_cat_combo.get()
        date = self.filter_date_entry.get()
        if cat == "All":
            cat = None
            
        expenses = self.manager.list_expenses(category=cat, date=date)
        
        for exp in expenses:
            self.tree.insert("", tk.END, values=(exp['id'], exp['date'], exp['category'], f"${exp['amount']:.2f}", exp['description']))

        # Update Summary
        summary = self.manager.get_summary()
        self.summary_label.config(text=f"Total Spent: ${summary['total']:.2f} (across {summary['count']} items)")

    def handle_add(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combo.get()
            description = self.desc_entry.get()
            
            if not category or not description:
                raise ValueError("Please fill in all fields")

            self.manager.add_expense(amount, category, description)
            
            # Clear inputs
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            
            self.refresh_data()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def handle_delete(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an expense to delete")
            return

        expense_id = self.tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete expense {expense_id}?"):
            if self.manager.delete_expense(expense_id):
                self.refresh_data()
            else:
                messagebox.showerror("Error", "Could not delete the expense")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceGUI(root)
    root.mainloop()

