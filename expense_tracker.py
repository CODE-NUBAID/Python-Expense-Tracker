import sqlite3
from datetime import datetime

# -----------------------------
# Database Setup
# -----------------------------
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# -----------------------------
# Add Expense
# -----------------------------
def add_expense(category, amount):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
                   (category, amount, date))
    conn.commit()
    conn.close()
    print(f"✅ Added expense: {category} - {amount} on {date}")

# -----------------------------
# View All Expenses
# -----------------------------
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No expenses recorded yet.")
        return

    print("\n--- All Expenses ---")
    for row in rows:
        print(f"ID: {row[0]} | Category: {row[1]} | Amount: {row[2]} | Date: {row[3]}")

# -----------------------------
# Summary by Category
# -----------------------------
def summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No expenses to summarize.")
        return

    print("\n--- Expense Summary ---")
    for row in rows:
        print(f"Category: {row[0]} | Total Spent: {row[1]}")

# -----------------------------
# Main Menu
# -----------------------------
def main():
    init_db()
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summary")
        print("4. Exit")

        choice = input("Enter choice (1-4): ")

        if choice == "1":
            category = input("Enter category: ")
            try:
                amount = float(input("Enter amount: "))
                add_expense(category, amount)
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary()
        elif choice == "4":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
