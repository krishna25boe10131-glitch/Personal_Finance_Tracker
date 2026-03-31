# 💰 Personal Budget Tracker

A modern, feature-rich budget tracker built with Python and Tkinter. Track your income and expenses with an intuitive GUI, categorize transactions, and visualize your spending patterns.

## Features

✨ **Dashboard** - Overview of your total balance, income, and expenses with recent transactions  
➕ **Add Transactions** - Easily add income or expense transactions with categories  
📋 **Transaction History** - View all transactions with filtering by category  
📈 **Analytics** - Visual expense breakdown by category with pie charts  
💾 **Data Persistence** - All data is automatically saved to JSON  
🎨 **Modern UI** - Clean, professional design with dark theme  

## Project Structure

```
budget-tracker/
├── main.py                 # Main GUI application
├── tracker.py              # Budget tracking logic and data management
├── requirements.txt        # Project dependencies
├── README.md               # This file
└── data/
    └── budget_data.json    # Transaction data (auto-created)
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**
```bash
cd budget-tracker
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python main.py
```

## Usage

### Dashboard Tab
- View your total balance, income, and expenses
- See recent transactions at a glance

### Add Transaction Tab
1. Select transaction type (Income or Expense)
2. Enter the amount (in ₹)
3. Choose a category from the dropdown
4. Add a description (e.g., "Lunch at restaurant")
5. Click "Add Transaction"

### Transactions Tab
- View all your transactions in a detailed list
- Filter by category to see specific spending
- Select and delete transactions as needed

### Analytics Tab
- View a pie chart showing your expense breakdown
- See which categories you spend the most on
- Charts update automatically with new transactions

## Categories

- **Food** - Groceries, restaurants, dining
- **Transport** - Gas, public transport, taxi
- **Entertainment** - Movies, games, hobbies
- **Utilities** - Electricity, water, internet
- **Shopping** - Clothes, accessories
- **Health** - Medicine, gym, doctor visits
- **Education** - Books, courses, tuition
- **Other** - Miscellaneous expenses

## Data Storage

All transactions are automatically saved to `data/budget_data.json`. The app loads this data on startup, so your data persists between sessions.

## Technical Details

### Built With
- **Tkinter** - GUI framework (built-in Python)
- **Matplotlib** - Data visualization
- **JSON** - Data persistence

### Key Classes

**BudgetTracker** (`tracker.py`)
- `add_transaction()` - Add new income/expense
- `delete_transaction()` - Remove a transaction
- `get_balance()` - Calculate current balance
- `get_category_breakdown()` - Get expenses by category
- `save_data()` / `load_data()` - Persist data

**BudgetTrackerApp** (`main.py`)
- GUI application class
- Manages all UI components and interactions

## Future Enhancements

- 📅 Monthly/yearly reports
- 💳 Budget limits and alerts
- 📊 Advanced charts (line graphs, bar charts)
- 🔍 Search functionality
- 📤 Export to CSV/PDF
- 📱 Mobile version

## Troubleshooting

**Issue:** "No module named 'matplotlib'"  
**Solution:** Run `pip install -r requirements.txt`

**Issue:** App crashes on startup  
**Solution:** Ensure you have Python 3.7+ installed: `python --version`

**Issue:** Data not saving  
**Solution:** Ensure the `data/` folder has write permissions

## Author

Created as a personal finance management tool for bioengineering students.

## License

MIT License - Feel free to use and modify!

---

**Happy budgeting! 💰**
