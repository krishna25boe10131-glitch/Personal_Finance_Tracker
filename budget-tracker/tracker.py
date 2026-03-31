import json
import os
from datetime import datetime
from pathlib import Path

class BudgetTracker:
    """Manages budget transactions and data persistence."""
    
    def __init__(self, data_file="data/budget_data.json"):
        self.data_file = data_file
        self.transactions = []
        self.load_data()
    
    def load_data(self):
        """Load transactions from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.transactions = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.transactions = []
        else:
            self.transactions = []
    
    def save_data(self):
        """Save transactions to JSON file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def add_transaction(self, amount, category, description, trans_type):
        """Add a new transaction."""
        transaction = {
            "id": len(self.transactions) + 1,
            "amount": float(amount),
            "category": category,
            "description": description,
            "type": trans_type,  # "income" or "expense"
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def delete_transaction(self, trans_id):
        """Delete a transaction by ID."""
        self.transactions = [t for t in self.transactions if t.get("id") != trans_id]
        self.save_data()
    
    def get_all_transactions(self):
        """Get all transactions."""
        return self.transactions
    
    def get_balance(self):
        """Calculate current balance."""
        income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        return income - expense
    
    def get_income_total(self):
        """Get total income."""
        return sum(t["amount"] for t in self.transactions if t["type"] == "income")
    
    def get_expense_total(self):
        """Get total expenses."""
        return sum(t["amount"] for t in self.transactions if t["type"] == "expense")
    
    def get_category_breakdown(self):
        """Get expenses by category."""
        breakdown = {}
        for t in self.transactions:
            if t["type"] == "expense":
                category = t["category"]
                breakdown[category] = breakdown.get(category, 0) + t["amount"]
        return breakdown
    
    def get_transactions_by_type(self, trans_type):
        """Get transactions filtered by type."""
        return [t for t in self.transactions if t["type"] == trans_type]
    
    def get_transactions_by_category(self, category):
        """Get transactions filtered by category."""
        return [t for t in self.transactions if t["category"] == category]
    
    def get_monthly_summary(self, month, year):
        """Get summary for a specific month."""
        monthly_trans = [
            t for t in self.transactions
            if datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S").month == month
            and datetime.strptime(t["date"], "%Y-%m-%d %H:%M:%S").year == year
        ]
        income = sum(t["amount"] for t in monthly_trans if t["type"] == "income")
        expense = sum(t["amount"] for t in monthly_trans if t["type"] == "expense")
        return {"income": income, "expense": expense, "balance": income - expense}
