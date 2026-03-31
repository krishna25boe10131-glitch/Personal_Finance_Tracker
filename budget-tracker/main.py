import tkinter as tk
from tkinter import ttk, messagebox
from tracker import BudgetTracker
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 PREMIUM Budget Tracker")
        self.root.geometry("1500x950")
        self.root.configure(bg="#0a0e27")
        
        self.tracker = BudgetTracker()
        
        # Premium Neon Color Palette
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
        
        self.setup_styles()
        self.create_widgets()
        self.refresh_data()
    
    def setup_styles(self):
        """Premium modern styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.bg_dark)
        style.configure('TLabel', background=self.bg_dark, font=('Segoe UI', 10), foreground=self.text_light)
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('TNotebook', background=self.bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[25, 12])
        
        style.configure('Treeview', background=self.bg_card, foreground=self.text_light, 
                       fieldbackground=self.bg_card, borderwidth=0, font=('Segoe UI', 9))
        style.configure('Treeview.Heading', background=self.bg_card, foreground=self.accent_cyan, 
                       font=('Segoe UI', 10, 'bold'))
        style.map('Treeview', background=[('selected', self.accent_cyan)], foreground=[('selected', '#000')])
    
    def create_widgets(self):
        """Create complete UI layout"""
        # Header
        header = tk.Frame(self.root, bg=self.bg_card, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(header, text="💰 PREMIUM BUDGET TRACKER", 
                font=('Segoe UI', 28, 'bold'), bg=self.bg_card, fg=self.accent_cyan).pack(pady=10)
        tk.Label(header, text="💎 Master Your Finances with Style 💎", 
                font=('Segoe UI', 11), bg=self.bg_card, fg=self.accent_gold).pack()
        
        # Tabs
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True)
        
        nb = ttk.Notebook(main)
        nb.pack(fill=tk.BOTH, expand=True)
        
        self.dashboard_tab = ttk.Frame(nb)
        nb.add(self.dashboard_tab, text="📊 Dashboard")
        self.create_dashboard()
        
        self.add_tab = ttk.Frame(nb)
        nb.add(self.add_tab, text="➕ Add Transaction")
        self.create_add_tab()
        
        self.history_tab = ttk.Frame(nb)
        nb.add(self.history_tab, text="📋 History")
        self.create_history()
        
        self.analytics_tab = ttk.Frame(nb)
        nb.add(self.analytics_tab, text="📈 Analytics")
        self.create_analytics()
        
        self.insights_tab = ttk.Frame(nb)
        nb.add(self.insights_tab, text="✨ Insights")
        self.create_insights()
    
    def create_card(self, parent, title, value, icon, color):
        """Create premium card"""
        card = tk.Frame(parent, bg=self.bg_card)
        card.configure(highlightthickness=2, highlightbackground=color, highlightcolor=color)
        
        tk.Frame(card, bg=color, height=3).pack(fill=tk.X)
        tk.Label(card, text=f"{icon} {title}", font=('Segoe UI', 11, 'bold'), 
                bg=self.bg_card, fg=color).pack(anchor=tk.W, padx=15, pady=(10, 0))
        
        value_label = tk.Label(card, text=value, font=('Segoe UI', 24, 'bold'), 
                              bg=self.bg_card, fg=self.text_light)
        value_label.pack(pady=10)
        
        return card, value_label
    
    def create_dashboard(self):
        """Dashboard tab"""
        cards = ttk.Frame(self.dashboard_tab)
        cards.pack(fill=tk.X, padx=15, pady=15)
        
        # Balance card (large)
        bal_frame = tk.Frame(cards, bg=self.bg_dark)
        bal_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        cards.grid_columnconfigure(0, weight=1)
        cards.grid_columnconfigure(1, weight=1)
        cards.grid_columnconfigure(2, weight=1)
        cards.grid_columnconfigure(3, weight=1)
        
        self.balance_card, self.balance_label = self.create_card(bal_frame, "TOTAL BALANCE", "₹0", "💰", self.accent_cyan)
        self.balance_card.pack(fill=tk.BOTH, expand=True)
        
        # Income card
        inc_frame = tk.Frame(cards, bg=self.bg_dark)
        inc_frame.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.income_card, self.income_label = self.create_card(inc_frame, "INCOME", "₹0", "📈", self.success_green)
        self.income_card.pack(fill=tk.BOTH, expand=True)
        
        # Expense card
        exp_frame = tk.Frame(cards, bg=self.bg_dark)
        exp_frame.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
        self.expense_card, self.expense_label = self.create_card(exp_frame, "EXPENSES", "₹0", "📉", self.danger_red)
        self.expense_card.pack(fill=tk.BOTH, expand=True)
        
        # Content
        content = ttk.Frame(self.dashboard_tab)
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Recent transactions
        recent = tk.Frame(content, bg=self.bg_card)
        recent.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=(0, 10))
        recent.configure(highlightthickness=2, highlightbackground=self.accent_purple, highlightcolor=self.accent_purple)
        
        tk.Label(recent, text="📝 Recent Transactions", font=('Segoe UI', 12, 'bold'), 
                bg=self.bg_card, fg=self.accent_purple).pack(anchor=tk.W, padx=10, pady=10)
        
        cols = ('Date', 'Description', 'Category', 'Type', 'Amount')
        self.recent_tree = ttk.Treeview(recent, columns=cols, height=12, show='headings')
        for col in cols:
            self.recent_tree.column(col, width=120)
            self.recent_tree.heading(col, text=col)
        
        sb = ttk.Scrollbar(recent, orient=tk.VERTICAL, command=self.recent_tree.yview)
        self.recent_tree.configure(yscroll=sb.set)
        self.recent_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        sb.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_add_tab(self):
        """Add transaction tab"""
        form = tk.Frame(self.add_tab, bg=self.bg_dark)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(form, text="✨ Add New Transaction ✨", 
                font=('Segoe UI', 18, 'bold'), bg=self.bg_dark, fg=self.accent_gold).pack(pady=20)
        
        input_f = tk.Frame(form, bg=self.bg_card)
        input_f.pack(fill=tk.BOTH, expand=True, padx=30, pady=20, ipady=30)
        input_f.configure(highlightthickness=2, highlightbackground=self.accent_purple)
        
        # Type
        type_f = tk.Frame(input_f, bg=self.bg_card)
        type_f.pack(fill=tk.X, padx=20, pady=15)
        tk.Label(type_f, text="Type:", font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan).pack(anchor=tk.W, pady=(0, 10))
        
        self.type_var = tk.StringVar(value="expense")
        radio_f = tk.Frame(type_f, bg=self.bg_card)
        radio_f.pack(fill=tk.X)
        tk.Radiobutton(radio_f, text="💰 Income", variable=self.type_var, value="income",
                      bg=self.bg_card, fg=self.success_green, selectcolor=self.bg_card).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(radio_f, text="💸 Expense", variable=self.type_var, value="expense",
                      bg=self.bg_card, fg=self.danger_red, selectcolor=self.bg_card).pack(side=tk.LEFT, padx=10)
        
        # Amount
        tk.Label(input_f, text="Amount (₹):", font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan).pack(anchor=tk.W, padx=20, pady=(15, 5))
        self.amount_entry = tk.Entry(input_f, font=('Segoe UI', 12), bg=self.bg_dark, fg=self.text_light, width=40)
        self.amount_entry.pack(padx=20, pady=(0, 15), ipady=8)
        
        # Category
        tk.Label(input_f, text="Category:", font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan).pack(anchor=tk.W, padx=20, pady=(15, 5))
        self.category_var = tk.StringVar(value="Food")
        cats = ["Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Education", "Other"]
        ttk.Combobox(input_f, textvariable=self.category_var, values=cats, state="readonly", width=37).pack(padx=20, pady=(0, 15), ipady=6)
        
        # Description
        tk.Label(input_f, text="Description:", font=('Segoe UI', 12, 'bold'), bg=self.bg_card, fg=self.accent_cyan).pack(anchor=tk.W, padx=20, pady=(15, 5))
        self.desc_entry = tk.Entry(input_f, font=('Segoe UI', 12), bg=self.bg_dark, fg=self.text_light, width=40)
        self.desc_entry.pack(padx=20, pady=(0, 25), ipady=8)
        
        tk.Button(input_f, text="🚀 ADD TRANSACTION 🚀", font=('Segoe UI', 13, 'bold'),
                 bg=self.accent_gold, fg='#000', padx=30, pady=12, relief=tk.FLAT,
                 command=self.add_trans).pack(pady=20)
    
    def create_history(self):
        """History tab"""
        filt = tk.Frame(self.history_tab, bg=self.bg_card)
        filt.pack(fill=tk.X, padx=15, pady=15)
        filt.configure(highlightthickness=2, highlightbackground=self.accent_cyan)
        
        tk.Label(filt, text="🔍 Filter:", font=('Segoe UI', 11, 'bold'), bg=self.bg_card, fg=self.accent_cyan).pack(side=tk.LEFT, padx=15, pady=10)
        
        self.filter_var = tk.StringVar(value="All")
        cats = ["All", "Food", "Transport", "Entertainment", "Utilities", "Shopping", "Health", "Education", "Other"]
        ttk.Combobox(filt, textvariable=self.filter_var, values=cats, state="readonly", width=18).pack(side=tk.LEFT, padx=10, pady=10)
        self.filter_var.trace('w', lambda *x: self.refresh_history())
        
        tree_f = tk.Frame(self.history_tab, bg=self.bg_card)
        tree_f.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        tree_f.configure(highlightthickness=2, highlightbackground=self.accent_purple)
        
        cols = ('ID', 'Date', 'Description', 'Category', 'Type', 'Amount')
        self.tree = ttk.Treeview(tree_f, columns=cols, height=20, show='headings')
        
        for col in cols:
            self.tree.column(col, width=120)
            self.tree.heading(col, text=col)
        
        sb = ttk.Scrollbar(tree_f, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        
        btn = tk.Frame(self.history_tab, bg=self.bg_dark)
        btn.pack(fill=tk.X, padx=15, pady=(0, 15))
        tk.Button(btn, text="🗑️ DELETE SELECTED 🗑️", font=('Segoe UI', 11, 'bold'),
                 bg=self.danger_red, fg='white', padx=20, pady=10, relief=tk.FLAT,
                 command=self.delete_trans).pack(side=tk.LEFT)
    
    def create_analytics(self):
        """Analytics tab"""
        self.analytics_f = ttk.Frame(self.analytics_tab)
        self.analytics_f.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def create_insights(self):
        """Insights tab"""
        title = tk.Label(self.insights_tab, text="📊 SMART INSIGHTS & STATISTICS", 
                        font=('Segoe UI', 18, 'bold'), bg=self.bg_dark, fg=self.accent_gold)
        title.pack(pady=15)
        
        self.insights_f = tk.Frame(self.insights_tab, bg=self.bg_dark)
        self.insights_f.pack(fill=tk.BOTH, expand=True)
    
    def add_trans(self):
        """Add transaction"""
        try:
            amt = float(self.amount_entry.get())
            cat = self.category_var.get()
            desc = self.desc_entry.get()
            typ = self.type_var.get()
            
            if amt <= 0:
                messagebox.showerror("❌ Error", "Amount must be > 0!")
                return
            if not desc:
                messagebox.showerror("❌ Error", "Add description!")
                return
            
            self.tracker.add_transaction(amt, cat, desc, typ)
            messagebox.showinfo("✅ Success", "Transaction added!")
            
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.category_var.set("Food")
            self.type_var.set("expense")
            
            self.refresh_data()
        except ValueError:
            messagebox.showerror("❌ Error", "Invalid amount!")
    
    def delete_trans(self):
        """Delete transaction"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("⚠️ Warning", "Select transaction!")
            return
        
        if messagebox.askyesno("🗑️ Confirm", "Delete?"):
            tid = int(self.tree.item(sel[0])['values'][0])
            self.tracker.delete_transaction(tid)
            messagebox.showinfo("✅ Success", "Deleted!")
            self.refresh_data()
    
    def refresh_history(self):
        """Refresh history list"""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        filt = self.filter_var.get()
        trans = self.tracker.get_all_transactions()
        
        if filt != "All":
            trans = [t for t in trans if t['category'] == filt]
        
        for t in reversed(trans):
            vals = (t['id'], t['date'][:10], t['description'][:20], t['category'], t['type'].upper(), f"₹{t['amount']:.2f}")
            self.tree.insert('', 0, values=vals)
    
    def refresh_data(self):
        """Refresh all data"""
        bal = self.tracker.get_balance()
        inc = self.tracker.get_income_total()
        exp = self.tracker.get_expense_total()
        
        bal_color = self.success_green if bal >= 0 else self.danger_red
        self.balance_card.configure(highlightbackground=bal_color, highlightcolor=bal_color)
        self.balance_label.config(text=f"₹{bal:,.2f}", fg=bal_color)
        self.income_label.config(text=f"₹{inc:,.2f}")
        self.expense_label.config(text=f"₹{exp:,.2f}")
        
        # Recent
        for i in self.recent_tree.get_children():
            self.recent_tree.delete(i)
        
        trans = self.tracker.get_all_transactions()[-8:]
        for t in reversed(trans):
            vals = (t['date'][:10], t['description'][:20], t['category'], t['type'].upper(), f"₹{t['amount']:.2f}")
            self.recent_tree.insert('', 0, values=vals)
        
        self.refresh_history()
        self.update_analytics()
        self.update_insights()
    
    def update_analytics(self):
        """Update analytics"""
        for w in self.analytics_f.winfo_children():
            w.destroy()
        
        breakdown = self.tracker.get_category_breakdown()
        
        if not breakdown:
            tk.Label(self.analytics_f, text="No data yet!", font=('Segoe UI', 14), bg=self.bg_dark, fg=self.text_dim).pack(pady=50)
            return
        
        fig = Figure(figsize=(14, 6), dpi=100, facecolor=self.bg_dark)
        
        ax1 = fig.add_subplot(121)
        cats = list(breakdown.keys())
        amts = list(breakdown.values())
        colors = [self.accent_cyan, self.danger_red, self.success_green, self.accent_gold, 
                 self.accent_pink, self.accent_purple, '#00ff88', '#ff006e']
        
        ax1.pie(amts, labels=cats, autopct='%1.1f%%', colors=colors[:len(cats)], startangle=90,
               textprops={'color': self.text_light, 'weight': 'bold'})
        for at in ax1.texts[len(cats):]:
            at.set_color('black')
        ax1.set_title('💸 Expense Breakdown', fontsize=13, color=self.accent_cyan, weight='bold')
        ax1.set_facecolor(self.bg_dark)
        
        ax2 = fig.add_subplot(122)
        inc_t = self.tracker.get_income_total()
        exp_t = self.tracker.get_expense_total()
        bars = ax2.bar(['Income', 'Expenses'], [inc_t, exp_t], color=[self.success_green, self.danger_red])
        ax2.set_ylabel('₹', color=self.text_light, weight='bold')
        ax2.set_title('💰 Income vs Expenses', fontsize=13, color=self.accent_cyan, weight='bold')
        ax2.set_facecolor(self.bg_dark)
        ax2.tick_params(colors=self.text_light)
        for sp in ['top', 'right']:
            ax2.spines[sp].set_visible(False)
        ax2.spines['bottom'].set_color(self.text_dim)
        ax2.spines['left'].set_color(self.text_dim)
        
        for bar in bars:
            h = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., h, f'₹{h:,.0f}', 
                    ha='center', va='bottom', color=self.text_light, weight='bold')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.analytics_f)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def update_insights(self):
        """Update insights"""
        for w in self.insights_f.winfo_children():
            w.destroy()
        
        bd = self.tracker.get_category_breakdown()
        trans = self.tracker.get_all_transactions()
        bal = self.tracker.get_balance()
        
        if not trans:
            tk.Label(self.insights_f, text="Add transactions to see insights!", 
                    font=('Segoe UI', 14), bg=self.bg_dark, fg=self.text_dim).pack(pady=50)
            return
        
        grid = tk.Frame(self.insights_f, bg=self.bg_dark)
        grid.pack(fill=tk.BOTH, expand=True)
        
        insights = [
            {"title": "💡 Top Category", "val": max(bd, key=bd.get) if bd else "N/A", 
             "sub": f"₹{max(bd.values()):,.0f}" if bd else "₹0", "color": self.accent_pink},
            {"title": "📊 Total Trans", "val": str(len(trans)), 
             "sub": "Expenses" if self.tracker.get_expense_total() > self.tracker.get_income_total() else "Income", 
             "color": self.accent_purple},
            {"title": "🎯 Avg Amount", "val": f"₹{sum(t['amount'] for t in trans) / len(trans):,.0f}", 
             "sub": f"{len(trans)} transactions", "color": self.accent_gold},
            {"title": "📈 Status", "val": "Healthy ✓" if bal >= 0 else "Low ⚠️", 
             "sub": f"₹{bal:,.0f}", "color": self.success_green if bal >= 0 else self.danger_red}
        ]
        
        for idx, ins in enumerate(insights):
            card = tk.Frame(grid, bg=self.bg_card)
            card.grid(row=idx%2, column=idx//2, sticky="ew", padx=10, pady=10, ipady=15)
            card.configure(highlightthickness=2, highlightbackground=ins['color'])
            grid.grid_columnconfigure(idx//2, weight=1)
            
            tk.Label(card, text=ins['title'], font=('Segoe UI', 11, 'bold'), bg=self.bg_card, fg=ins['color']).pack(anchor=tk.W, padx=15, pady=(10, 5))
            tk.Label(card, text=ins['val'], font=('Segoe UI', 18, 'bold'), bg=self.bg_card, fg=self.text_light).pack(anchor=tk.W, padx=15)
            tk.Label(card, text=ins['sub'], font=('Segoe UI', 10), bg=self.bg_card, fg=self.text_dim).pack(anchor=tk.W, padx=15, pady=(5, 10))

def main():
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
