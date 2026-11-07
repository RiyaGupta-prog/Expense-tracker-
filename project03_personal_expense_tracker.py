"""
Project 03: Personal Expense Tracker with CSV
Features:
- Add expenses
- View all expenses
- Filter expenses by category
- Save and load expenses using the csv module
- Display category-wise summary statistics

Run: python project03_personal_expense_tracker.py
"""

import csv
from pathlib import Path
from datetime import datetime

CSV_FILE = Path("expenses.csv")
FIELDNAMES = ["date", "category", "description", "amount"]


def load_expenses():
    """Load saved expenses from the CSV file."""
    if not CSV_FILE.exists():
        return []

    try:
        with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except (OSError, csv.Error) as error:
        print(f"Could not read expense file: {error}")
        return []


def save_expenses(expenses):
    """Write all expenses to the CSV file."""
    try:
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(expenses)
        return True
    except (OSError, csv.Error) as error:
        print(f"Could not save expenses: {error}")
        return False


def add_expense(expenses):
    """Get expense details from the user and save them."""
    print("\n--- Add New Expense ---")
    date = input("Date (YYYY-MM-DD, press Enter for today): ").strip()

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")
            return

    category = input("Category (Food/Travel/Shopping/Bills/Other): ").strip()
    if not category:
        print("Category cannot be empty.")
        return

    description = input("Description: ").strip()

    try:
        amount = float(input("Amount (₹): ").strip())
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid amount.")
        return

    expense = {
        "date": date,
        "category": category.title(),
        "description": description,
        "amount": f"{amount:.2f}"
    }

    expenses.append(expense)
    if save_expenses(expenses):
        print("Expense added and saved successfully!")


def view_expenses(expenses):
    """Display all recorded expenses."""
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"{'Date':<12} {'Category':<14} {'Description':<22} {'Amount (₹)':>12}")
    print("-" * 64)
    for item in expenses:
        print(
            f"{item['date']:<12} {item['category']:<14} "
            f"{item['description'][:21]:<22} {float(item['amount']):>12.2f}"
        )

    total = sum(float(item["amount"]) for item in expenses)
    print("-" * 64)
    print(f"Total expenses: ₹{total:.2f}")


def filter_expenses(expenses):
    """Show expenses matching a category."""
    print("\n--- Filter Expenses by Category ---")
    category = input("Enter category to search: ").strip().casefold()

    matches = [
        item for item in expenses
        if item["category"].casefold() == category
    ]

    if not matches:
        print("No expenses found in this category.")
        return

    print(f"\nExpenses in {category.title()}:")
    for item in matches:
        print(
            f"{item['date']} | {item['description']} | "
            f"₹{float(item['amount']):.2f}"
        )

    total = sum(float(item["amount"]) for item in matches)
    print(f"Category total: ₹{total:.2f}")


def category_summary(expenses):
    """Calculate and display category-wise totals and counts."""
    print("\n--- Category Summary ---")
    if not expenses:
        print("No expenses available for summary.")
        return

    summary = {}
    for item in expenses:
        category = item["category"]
        amount = float(item["amount"])

        if category not in summary:
            summary[category] = {"count": 0, "total": 0.0}

        summary[category]["count"] += 1
        summary[category]["total"] += amount

    print(f"{'Category':<18} {'Number of expenses':>18} {'Total (₹)':>14}")
    print("-" * 54)

    for category, data in sorted(summary.items()):
        print(
            f"{category:<18} {data['count']:>18} "
            f"{data['total']:>14.2f}"
        )

    grand_total = sum(data["total"] for data in summary.values())
    print("-" * 54)
    print(f"{'Grand Total':<18} {'':>18} {grand_total:>14.2f}")


def main():
    """Main menu of the Personal Expense Tracker."""
    expenses = load_expenses()

    while True:
        print("\n" + "=" * 42)
        print("        PERSONAL EXPENSE TRACKER")
        print("=" * 42)
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses by Category")
        print("4. Category Summary Statistics")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            filter_expenses(expenses)
        elif choice == "4":
            category_summary(expenses)
        elif choice == "5":
            print("Your expenses are stored in expenses.csv. Goodbye!")
            break
        else:
            print("Invalid choice. Please select from 1 to 5.")


if __name__ == "__main__":
    main()
