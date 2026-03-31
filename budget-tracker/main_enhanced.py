import tkinter as tk
from tkinter import ttk, messagebox
from tracker import BudgetTracker
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class ModernButton(tk.Canvas):
    """Custom modern button with hover effects."""
    def __init__(self, parent, text, command, bg_color, hover_color, width=150, height=50, **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent['bg'], highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.current_color = bg_color
        self.text = text
        
        self.bind("<Button-1>", lambda e: command() if command else None)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.draw()
    
    def draw(self):
        self.delete("all")
        self.create_rectangle(5, 5, self.winfo_width()-5, self.winfo_height()-5, 
                            fill=self.current_color, outline=self.current_color, width=2)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, 
                        text=self.text, font=('Segoe UI', 11, 'bold'), fill='white')
    
    def on_enter(self, e):
        self.current_color = self.hover_color
        self.draw()
    
    def on_leave(self, e):
        self.current_color = self.bg_color
        self.draw()

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 PREMIUM Budget Tracker")
        self.root.geometry("1500x950")
        self.root.configure(bg="#0a0e27")
        
        # Initialize tracker
        self.tracker = BudgetTracker()
        
        # Premium Color Scheme (Neon + Dark)
        self.bg_dark = "#0a0e27"
        self.bg_card = "#1a1f3a"
        self.accent_cyan = "#00d9ff"
        self.accent_purple = "#00a8ff"
        self.accent_pink = "#ff006e"
        self.accent_gold = "#ffd700"
        self.success_green = "#00ff88"
        self.danger_red = "#ff6b6b"
        self.text_light = "#e2e8f0"
        self.text_dim = "#94a3b8"
        
        self.setup_enhanced_styles()
        self.create_widgets()
        self.refresh_data()
    
    def setup_enhanced_styles(self):
        """Enhanced modern styling with neon colors."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.bg_dark)
        style.configure('TLabel', background=self.bg_dark, font=('Segoe UI', 10), foreground=self.text_light)
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), background=self.accent_cyan, foreground='#000')
        style.configure('TNotebook', background=self.bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[25, 12])
        
        style.configure('Treeview', background=self.bg_card, foreground=self.text_light, 
                       fieldbackground=self.bg_card, borderwidth=0, font=('Segoe UI', 9))
        style.configure('Treeview.Heading', background=self.bg_card, foreground=self.accent_cyan, 
                       font=('Segoe UI', 10, 'bold'), borderwidth=0)
        style.map('Treeview', background=[('selected', self.accent_cyan)], foreground=[('selected', '#000')])
    
    def create_widgets(self):
        """Create the complete UI layout."""
        # Header with gradient effect
        header_frame = tk.Frame(self.root, bg=self.bg_card, height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with gradient-like effect using multiple labels
        title_main = tk.Label(header_frame, text="💰 PREMIUM BUDGET TRACKER", 
                            font=('Segoe UI', 28, 'bold'), bg=self.bg_card, fg=self.accent_cyan)
        title_main.pack(pady=10)
        
        subtitle = tk.Label(header_frame, text="💎 Master Your Finances with Style 💎", 
                           font=('Segoe UI', 11), bg=self.bg_card, fg=self.accent_gold)
        subtitle.pack()
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tabs
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="📊 Dashboard")
        self.create_dashboard_tab()
        
        self.add_transaction_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_transaction_tab, text="➕ Add Transaction")
        self.create_add_transaction_tab()
        
        self.view_transaction_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.view_transaction_tab, text="📋 History")
        self.create_view_transactions_tab()
        
        self.analytics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analytics_tab, text="📈 Analytics")
        self.create_analytics_tab()
        
        self.insights_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.insights_tab, text="✨ Insights")
        self.create_insights_tab()
    
    def create_premium_card(self, parent, title, value, icon="", color=None, width=None):
        """Create a premium-styled card."""
        card = tk.Frame(parent, bg=self.bg_card, relief=tk.FLAT, bd=0)
        card.configure(highlightthickness=2, highlightbackground=color or self.accent_cyan, highlightcolor=color or self.accent_cyan)
        
        if width:
            card.configure(width=width)
            card.pack_propagate(False)
        
        # Top bar with color
        top_bar = tk.Frame(card, bg=color or self.accent_cyan, height=4)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Title and icon
        title_frame = tk.Frame(card, bg=self.bg_card)
        title_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
        
        title_label = tk.Label(title_frame, text=f"{icon} {title}", font=('Segoe UI', 11, 'bold'), 
                              bg=self.bg_card, fg=color or self.accent_cyan)
        title_label.pack(anchor=tk.W)
        
        # Value
        value_label = tk.Label(card, text=value, font=('Segoe UI', 24, 'bold'), 
                              bg=self.bg_card, fg=self.text_light)
        value_label.pack(pady=10)
        
        return card, value_label
    
    def create_dashboard_tab(self):
        """Create stunning dashboard."""
        # Top cards container
        cards_container = ttk.Frame(self.dashboard_tab)
        cards_container.pack(fill=tk.X, padx=15, pady=15)
        
        # Balance Card (Large - takes 2 columns)
        balance_frame = tk.Frame(cards_container, bg=self.bg_dark)
        balance_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5, ipady=20)
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)
        
        self.balance_card, self.balance_label = self.create_premium_card(
            balance_frame, "TOTAL BALANCE", "₹0", "💰", self.accent_cyan, width=600
        )
        self.balance_card.pack(fill=tk.BOTH, expand=True)
        
        # Income Card
        income_frame = tk.Frame(cards_container, bg=self.bg_dark)
        income_frame.grid(row=0, column=2, sticky="ew", padx=5, pady=5, ipady=20)
        cards_container.grid_columnconfigure(2, weight=1)
        
        self.income_card, self.income_label = self.create_premium_card(
            income_frame, "INCOME", "₹0", "📈", self.success_green
        )
        self.income_card.pack(fill=tk.BOTH, expand=True)
        
        # Expense Card
        expense_frame = tk.Frame(cards_container, bg=self.bg_dark)
        expense_frame.grid(row=0, column=3, sticky="ew", padx=5, pady=5, ipady=20)
        cards_container.grid_columnconfigure(3, weight=1)
        
        self.expense_card, self.expense_label = self.create_premium_card(
            expense_frame, "EXPENSES", "₹0", "📉", self.danger_red
        )
        self.expense_card.pack(fill=tk.BOTH, expand=True)
        
        # Statistics and Recent Transactions
        content_frame = ttk.Frame(self.dashboard_tab)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Recent transactions
        recent_frame = tk.Frame(content_frame, bg=self.bg_card, relief=tk.FLAT, bd=0)
        recent_frame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 10), ipady=10)
        recent_frame.configure(highlightthickness=2, highlightbackground=self.accent_purple, highlightcolor=self.accent_purple)
        
        recent_label = tk.Label(recent_frame, text="📝 Recent Transactions", 
                               font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_purple)
        recent_label.pack(padx=10, pady=10, anchor=tk.W)
        
        columns = ('Date', 'Description', 'Category', 'Type', 'Amount')
        self.recent_tree = ttk.Treeview(recent_frame, columns=columns, height=12, show='headings')
        
        col_widths = {'Date': 120, 'Description': 130, 'Category': 100, 'Type': 60, 'Amount': 80}
        for col in columns:
            self.recent_tree.column(col, width=col_widths.get(col, 100))
            self.recent_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, command=self.recent_tree.yview)
        self.recent_tree.configure(yscroll=scrollbar.set)
        
        self.recent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        
        # Mini chart on the right
        chart_frame = tk.Frame(content_frame, bg=self.bg_card, relief=tk.FLAT, bd=0)
        chart_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, ipady=10)
        chart_frame.configure(highlightthickness=2, highlightbackground=self.accent_pink, highlightcolor=self.accent_pink)
        
        chart_label = tk.Label(chart_frame, text="💹 Spending Trend", 
                              font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_pink)
        chart_label.pack(padx=10, pady=10, anchor=tk.W)
        
        self.mini_chart_canvas = tk.Frame(chart_frame, bg=self.bg_card)
        self.mini_chart_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def create_add_transaction_tab(self):
        """Create transaction form tab."""
        form_frame = tk.Frame(self.add_transaction_tab, bg=self.bg_dark)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(form_frame, text="✨ Add New Transaction ✨", 
                        font=('Segoe UI', 18, 'bold'), bg=self.bg_dark, fg=self.accent_gold)
        title.pack(pady=20)
        
        # Form container
        input_frame = tk.Frame(form_frame, bg=self.bg_card, relief=tk.FLAT, bd=0)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20, ipady=30)
        input_frame.configure(highlightthickness=2, highlightbackground=self.accent_purple)
        
        # Type selection
        type_frame = tk.Frame(input_frame, bg=self.bg_card)
        type_frame.pack(fill=tk.X, padx=20, pady=15)
        
        type_label = tk.Label(type_frame, text="Transaction Type:", 
                             font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan)
        type_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.type_var = tk.StringVar(value="expense")
        radio_frame = tk.Frame(type_frame, bg=self.bg_card)
        radio_frame.pack(fill=tk.X)
        
        income_btn = tk.Radiobutton(radio_frame, text="💰 Income", variable=self.type_var, value="income",
                                    bg=self.bg_card, fg=self.success_green, selectcolor=self.bg_card,
                                    font=('Segoe UI', 11), activebackground=self.bg_card, activeforeground=self.success_green)
        income_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        expense_btn = tk.Radiobutton(radio_frame, text="💸 Expense", variable=self.type_var, value="expense",
                                     bg=self.bg_card, fg=self.danger_red, selectcolor=self.bg_card,
                                     font=('Segoe UI', 11), activebackground=self.bg_card, activeforeground=self.danger_red)
        expense_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Amount
        amount_label = tk.Label(input_frame, text="Amount (₹):", 
                               font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan)
        amount_label.pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.amount_entry = tk.Entry(input_frame, font=('Segoe UI', 12), bg=self.bg_dark, 
                                     fg=self.text_light, insertbackground=self.accent_cyan, 
                                     width=40, bd=2, relief=tk.FLAT)
        self.amount_entry.pack(padx=20, pady=(0, 15), ipady=8)
        self.amount_entry.bind('<Return>', lambda e: None)
        
        # Category
        category_label = tk.Label(input_frame, text="Category:", 
                                 font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan)
        category_label.pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.category_var = tk.StringVar(value="Food")
        categories = ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Education", "Other"]
        category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories, 
                                     state="readonly", width=37, font=('Segoe UI', 11))
        category_combo.pack(padx=20, pady=(0, 15), ipady=6)
        
        # Description
        desc_label = tk.Label(input_frame, text="Description:", 
                             font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan)
        desc_label.pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        self.description_entry = tk.Entry(input_frame, font=('Segoe UI', 12), bg=self.bg_dark, 
                                          fg=self.text_light, insertbackground=self.accent_cyan, 
                                          width=40, bd=2, relief=tk.FLAT)
        self.description_entry.pack(padx=20, pady=(0, 25), ipady=8)
        
        # Submit button
        submit_btn = tk.Button(input_frame, text="🚀 ADD TRANSACTION 🚀", 
                             font=('Segoe UI', 13, 'bold'), bg=self.accent_gold, fg='#000',
                             activebackground=self.accent_cyan, activeforeground='#000',
                             padx=30, pady=12, relief=tk.FLAT, bd=0, cursor="hand2",
                             command=self.add_transaction)
        submit_btn.pack(pady=20)
    
    def create_view_transactions_tab(self):
        """Create transaction history view."""
        # Filter section
        filter_frame = tk.Frame(self.view_transaction_tab, bg=self.bg_card, relief=tk.FLAT, bd=0)
        filter_frame.pack(fill=tk.X, padx=15, pady=15)
        filter_frame.configure(highlightthickness=2, highlightbackground=self.accent_cyan)
        
        filter_label = tk.Label(filter_frame, text="🔍 Filter by Category:", 
                               font=('Segoe UI', 11, 'bold'), bg=self.bg_card, fg=self.accent_cyan)
        filter_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.filter_category_var = tk.StringVar(value="All")
        categories = ["All", "Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Education", "Other"]
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var, values=categories, 
                                   state="readonly", width=18, font=('Segoe UI', 10))
        filter_combo.pack(side=tk.LEFT, padx=10, pady=10)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_transactions_list())
        
        # Transactions list
        tree_frame = tk.Frame(self.view_transaction_tab, bg=self.bg_card, relief=tk.FLAT, bd=0)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        tree_frame.configure(highlightthickness=2, highlightbackground=self.accent_purple)
        
        columns = ('ID', 'Date', 'Description', 'Category', 'Type', 'Amount')
        self.transactions_tree = ttk.Treeview(tree_frame, columns=columns, height=20, show='headings')
        
        col_widths = {'ID': 30, 'Date': 130, 'Description': 150, 'Category': 80, 'Type': 70, 'Amount': 100}
        for col in columns:
            self.transactions_tree.column(col, width=col_widths.get(col, 100))
            self.transactions_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscroll=scrollbar.set)
        
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        
        # Delete button
        btn_frame = tk.Frame(self.view_transaction_tab, bg=self.bg_dark)
        btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        delete_btn = tk.Button(btn_frame, text="🗑️ DELETE SELECTED 🗑️", 
                             font=('Segoe UI', 11, 'bold'), bg=self.danger_red, fg='white',
                             activebackground=self.accent_cyan, activeforeground='#000',
                             padx=20, pady=10, relief=tk.FLAT, bd=0, cursor="hand2",
                             command=self.delete_selected)
        delete_btn.pack(side=tk.LEFT)
    
    def create_analytics_tab(self):
        """Create stunning analytics."""
        self.analytics_container = ttk.Frame(self.analytics_tab)
        self.analytics_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def create_insights_tab(self):
        """Create insights and statistics."""
        insights_frame = tk.Frame(self.insights_tab, bg=self.bg_dark)
        insights_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Title
        title = tk.Label(insights_frame, text="📊 SMART INSIGHTS & STATISTICS", 
                        font=('Segoe UI', 18, 'bold'), bg=self.bg_dark, fg=self.accent_gold)
        title.pack(pady=15)
        
        # Insights container
        self.insights_content = tk.Frame(insights_frame, bg=self.bg_dark)
        self.insights_content.pack(fill=tk.BOTH, expand=True)
    
    def add_transaction(self):
        """Add new transaction."""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_var.get()
            description = self.description_entry.get()
            trans_type = self.type_var.get()
            
            if amount <= 0:
                messagebox.showerror("❌ Error", "Amount must be greater than 0!")
                return
            
            if not description:
                messagebox.showerror("❌ Error", "Please enter a description!")
                return
            
            self.tracker.add_transaction(amount, category, description, trans_type)
            messagebox.showinfo("✅ Success", "Transaction added successfully!")
            
            self.amount_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.category_var.set("Food")
            self.type_var.set("expense")
            
            self.refresh_data()
        
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid amount!")
    
    def delete_selected(self):
        """Delete selected transaction."""
        selected = self.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Warning", "Please select a transaction to delete!")
            return
        
        if messagebox.askyesno("🗑️ Confirm", "Delete this transaction?"):
            trans_id = int(self.transactions_tree.item(selected[0])['values'][0])
            self.tracker.delete_transaction(trans_id)
            messagebox.showinfo("✅ Success", "Transaction deleted!")
            self.refresh_data()
    
    def refresh_transactions_list(self):
        """Refresh transaction list with filter."""
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        filter_category = self.filter_category_var.get()
        
        if filter_category == "All":
            transactions = self.tracker.get_all_transactions()
        else:
            transactions = self.tracker.get_transactions_by_category(filter_category)
        
        for trans in reversed(transactions):
            color = '' if trans['type'] == 'income' else ''
            values = (
                trans['id'],
                trans['date'],
                trans['description'][:30],
                trans['category'],
                trans['type'].upper(),
                f"₹{trans['amount']:.2f}"
            )
            self.transactions_tree.insert('', 0, values=values)
    
    def refresh_data(self):
        """Refresh all UI data."""
        balance = self.tracker.get_balance()
        income = self.tracker.get_income_total()
        expense = self.tracker.get_expense_total()
        
        # Update cards with animation effect
        balance_color = self.success_green if balance >= 0 else self.danger_red
        self.balance_card.configure(highlightbackground=balance_color, highlightcolor=balance_color)
        self.balance_label.config(text=f"₹{balance:,.2f}", fg=balance_color)
        self.income_label.config(text=f"₹{income:,.2f}")
        self.expense_label.config(text=f"₹{expense:,.2f}")
        
        # Update recent transactions
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        
        transactions = self.tracker.get_all_transactions()[-8:]
        for trans in reversed(transactions):
            values = (
                trans['date'][:10],
                trans['description'][:20],
                trans['category'],
                trans['type'].upper(),
                f"₹{trans['amount']:.2f}"
            )
            self.recent_tree.insert('', 0, values=values)
        
        self.refresh_transactions_list()
        self.update_analytics()
        self.update_insights()
    
    def update_analytics(self):
        """Create beautiful analytics charts."""
        for widget in self.analytics_container.winfo_children():
            widget.destroy()
        
        breakdown = self.tracker.get_category_breakdown()
        transactions = self.tracker.get_all_transactions()
        
        if not breakdown:
            empty = tk.Label(self.analytics_container, text="No data to display yet!", 
                            font=('Segoe UI', 14), bg=self.bg_dark, fg=self.text_dim)
            empty.pack(pady=50)
            return
        
        # Create multiple charts
        fig = Figure(figsize=(14, 6), dpi=100, facecolor=self.bg_dark, edgecolor='none')
        fig.patch.set_alpha(0.0)
        
        # Chart 1: Pie chart
        ax1 = fig.add_subplot(121)
        categories = list(breakdown.keys())
        amounts = list(breakdown.values())
        colors_list = [self.accent_cyan, self.danger_red, self.success_green, self.accent_gold, 
                      self.accent_pink, self.accent_purple, '#00ff88', '#ff006e']
        
        wedges, texts, autotexts = ax1.pie(amounts, labels=categories, autopct='%1.1f%%', 
                                            colors=colors_list[:len(categories)], startangle=90,
                                            textprops={'color': self.text_light, 'fontsize': 10, 'weight': 'bold'})
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        ax1.set_title('💸 Expense Breakdown by Category', fontsize=13, color=self.accent_cyan, weight='bold', pad=20)
        ax1.set_facecolor(self.bg_dark)
        
        # Chart 2: Income vs Expense bar chart
        ax2 = fig.add_subplot(122)
        income_total = self.tracker.get_income_total()
        expense_total = self.tracker.get_expense_total()
        
        bars = ax2.bar(['Revenue', 'Expenses'], [income_total, expense_total], 
                      color=[self.success_green, self.danger_red], width=0.6, edgecolor='none')
        ax2.set_ylabel('Amount (₹)', color=self.text_light, fontsize=11, weight='bold')
        ax2.set_title('💰 Income vs Expenses', fontsize=13, color=self.accent_cyan, weight='bold', pad=20)
        ax2.set_facecolor(self.bg_dark)
        ax2.tick_params(colors=self.text_light)
        ax2.spines['bottom'].set_color(self.text_dim)
        ax2.spines['left'].set_color(self.text_dim)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'₹{height:,.0f}', ha='center', va='bottom', color=self.text_light, fontweight='bold')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.analytics_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_insights(self):
        """Update insights and statistics."""
        for widget in self.insights_content.winfo_children():
            widget.destroy()
        
        breakdown = self.tracker.get_category_breakdown()
        transactions = self.tracker.get_all_transactions()
        balance = self.tracker.get_balance()
        
        if not transactions:
            msg = tk.Label(self.insights_content, text="Start adding transactions to see insights!", 
                          font=('Segoe UI', 14), bg=self.bg_dark, fg=self.text_dim)
            msg.pack(pady=50)
            return
        
        # Create insight cards
        insights_grid = tk.Frame(self.insights_content, bg=self.bg_dark)
        insights_grid.pack(fill=tk.BOTH, expand=True)
        
        insights = [
            {
                "title": "💡 Highest Spending Category",
                "value": max(breakdown, key=breakdown.get) if breakdown else "N/A",
                "subvalue": f"₹{max(breakdown.values()):,.2f}" if breakdown else "₹0",
                "color": self.accent_pink
            },
            {
                "title": "📊 Total Transactions",
                "value": str(len(transactions)),
                "subvalue": f"{'Mostly Expenses' if self.tracker.get_expense_total() > self.tracker.get_income_total() else 'Mostly Income'}",
                "color": self.accent_purple
            },
            {
                "title": "🎯 Average Transaction",
                "value": f"₹{sum(t['amount'] for t in transactions) / len(transactions):,.2f}" if transactions else "₹0",
                "subvalue": f"Based on {len(transactions)} transactions",
                "color": self.accent_gold
            },
            {
                "title": "📈 Financial Health",
                "value": "Healthy ✓" if balance > 0 else "Critical ⚠️",
                "subvalue": f"Balance: ₹{balance:,.2f}",
                "color": self.success_green if balance >= 0 else self.danger_red
            }
        ]
        
        for idx, insight in enumerate(insights):
            col = idx % 2
            row = idx // 2
            
            card = tk.Frame(insights_grid, bg=self.bg_card, relief=tk.FLAT, bd=0)
            card.grid(row=row, column=col, sticky="ew", padx=10, pady=10, ipady=15)
            card.configure(highlightthickness=2, highlightbackground=insight['color'], highlightcolor=insight['color'])
            insights_grid.grid_columnconfigure(col, weight=1)
            
            title = tk.Label(card, text=insight['title'], font=('Segoe UI', 11, 'bold'), 
                           bg=self.bg_card, fg=insight['color'])
            title.pack(anchor=tk.W, padx=15, pady=(10, 5))
            
            value = tk.Label(card, text=insight['value'], font=('Segoe UI', 18, 'bold'), 
                           bg=self.bg_card, fg=self.text_light)
            value.pack(anchor=tk.W, padx=15)
            
            subvalue = tk.Label(card, text=insight['subvalue'], font=('Segoe UI', 10), 
                              bg=self.bg_card, fg=self.text_dim)
            subvalue.pack(anchor=tk.W, padx=15, pady=(5, 10))

def main():
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
