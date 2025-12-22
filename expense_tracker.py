import sqlite3
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

console = Console()
DB_NAME = "expenses.db"

# -----------------------------
# Database Setup
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)",
        (category, amount, date)
    )
    conn.commit()
    conn.close()
    console.print(f"✅ [bold green]Expense Added:[/bold green] {category} - ₹{amount}")

# -----------------------------
# View Expenses
# -----------------------------
def view_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("❌ No expenses found.")
        return

    table = Table(title="💸 All Expenses")
    table.add_column("ID")
    table.add_column("Category")
    table.add_column("Amount")
    table.add_column("Date")

    for row in rows:
        table.add_row(str(row[0]), row[1], f"₹{row[2]}", row[3])

    console.print(table)

# -----------------------------
# Summary by Category
# -----------------------------
def summary_by_category():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("❌ No data to summarize.")
        return

    table = Table(title="📊 Category Summary")
    table.add_column("Category")
    table.add_column("Total Spent")

    for row in rows:
        table.add_row(row[0], f"₹{row[1]}")

    console.print(table)

# -----------------------------
# Monthly Summary
# -----------------------------
def monthly_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', date), SUM(amount)
        FROM expenses
        GROUP BY strftime('%Y-%m', date)
    """)
    rows = cursor.fetchall()
    conn.close()

    table = Table(title="📅 Monthly Summary")
    table.add_column("Month")
    table.add_column("Total Spent")

    for row in rows:
        table.add_row(row[0], f"₹{row[1]}")

    console.print(table)

# -----------------------------
# Expense Chart
# -----------------------------
def show_chart():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses GROUP BY category"
    )
    data = cursor.fetchall()
    conn.close()

    if not data:
        console.print("❌ No data for chart.")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()

# -----------------------------
# Export to CSV
# -----------------------------
def export_to_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Category", "Amount", "Date"])
        writer.writerows(rows)

    console.print("📁 [bold green]Exported to expenses.csv[/bold green]")

# -----------------------------
# Main Menu
# -----------------------------
def main():
    init_db()

    while True:
        console.print("\n[bold cyan]Expense Tracker Menu[/bold cyan]")
        console.print("1️⃣ Add Expense")
        console.print("2️⃣ View Expenses")
        console.print("3️⃣ Category Summary")
        console.print("4️⃣ Monthly Summary")
        console.print("5️⃣ Show Chart")
        console.print("6️⃣ Export to CSV")
        console.print("7️⃣ Exit")

        choice = input("\nEnter choice (1-7): ")

        if choice == "1":
            category = input("Category: ")
            try:
                amount = float(input("Amount: "))
                add_expense(category, amount)
            except ValueError:
                console.print("❌ Invalid amount")

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            summary_by_category()

        elif choice == "4":
            monthly_summary()

        elif choice == "5":
            show_chart()

        elif choice == "6":
            export_to_csv()

        elif choice == "7":
            console.print("👋 Goodbye!")
            break

        else:
            console.print("❌ Invalid choice")

if __name__ == "__main__":
    main()