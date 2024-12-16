import sqlite3
from tabulate import tabulate
# Connect to SQLite database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create expenses table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL
    )
''')
conn.commit()
def add_expense(date, category, description, amount):
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    print("Expense added successfully!")
def view_expenses():
    cursor.execute('SELECT * FROM expenses')
    records = cursor.fetchall()
    print(tabulate(records, headers=["ID", "Date", "Category", "Description", "Amount"], tablefmt="grid"))
def delete_expense(expense_id):
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    print("Expense deleted successfully!")
def generate_report_by_category():
    cursor.execute('''
        SELECT category, SUM(amount) AS total 
        FROM expenses 
        GROUP BY category
    ''')
    records = cursor.fetchall()
    print(tabulate(records, headers=["Category", "Total Amount"], tablefmt="grid"))
def main_menu():
    while True:
        print("\nExpense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Generate Report by Category")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            add_expense(date, category, description, amount)
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id)
        elif choice == '4':
            generate_report_by_category()
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main_menu()
    conn.close()
