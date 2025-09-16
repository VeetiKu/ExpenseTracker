import json
import datetime
import calendar

BUDGET_FILE = "monthly_budget.json"
EXPENSE_FILE_CURRENT = "expenses.json"
EXPENSE_FILE_PAST = "pastexpenses.json"
RECURRING_EXPENSE_FILE = "recurring.json"

class BudgetManager:
    BUDGET_FILE = "monthly_budget.json"

    def __init__(self):
        self.budget, self.saved_month = self.load_budget()

    def load_budget(self):
        try:
            with open(self.BUDGET_FILE, "r") as f:
                data = json.load(f)
                return data.get("budget", 0), data.get("month", "")
        except (FileNotFoundError, ValueError, json.JSONDecodeError):
            return 0, ""

    def save_budget(self, budget, month):
        data = {"budget": budget, "month": month}
        with open(self.BUDGET_FILE, "w") as f:
            json.dump(data, f)
        self.budget = budget
        self.saved_month = month

    def set_budget(self):
        if self.budget > 0:
            print(f"\nYour current monthly budget is {self.budget}€")
        else:
            print("You haven't set a budget yet.")

        while True:
            try:
                budget = float(input("Enter your new monthly budget: "))
                if budget < 0:
                    raise ValueError
                break
            except ValueError:
                print("Enter a valid positive number for the budget.")

        current_month = datetime.date.today().strftime("%Y-%m")
        self.save_budget(budget, current_month)
        print(f"Your new budget is {budget}€ every month")

def main():
    budget_manager = BudgetManager()
    while True:
        budget, saved_month = budget_manager.budget, budget_manager.saved_month
        current_month = datetime.date.today().strftime("%Y-%m")

        # Reset if new month
        if saved_month != current_month:
            print("\n--- New Month Detected ---")
            print("Archiving last month’s expenses and resetting for this month.")
            last_expenses = load_expenses()
            save_expenses(last_expenses, EXPENSE_FILE_PAST)
            recurring_expenses = load_recurring_expenses()
            save_expenses(recurring_expenses)  
            budget_manager.save_budget(budget, current_month)

        if budget == 0:
            budget_manager.set_budget()
        choice = options()
        if choice == 1:
            get_expense()
        elif choice == 2:
            budget_manager.set_budget()
        elif choice == 3:
            show_expenses(budget_manager)
        elif choice == 4:
            delete_expense()
        elif choice == 5:
            print("Exiting the app")
            break

def options():
    print("\nWhat Would you like to do?")
    modules = ["1-Add new expense","2-Modify monthly budget","3-Display your expenses","4-Delete an expense","5-EXIT"]
    for option in modules:
            print(option)
    while True:
        user_input = input("Enter the Module you want to use: ")
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= 5:
                return choice
        print("Error: Entered number must be between 1-5.")

def get_expense():
    expenses = load_expenses()
    expense = input("\nEnter your expense: ")
    while True:
        try:
            price = float(input("Cost: "))
            if price < 0:
                raise ValueError
            break
        except ValueError:
            print("Enter a valid positive number for the cost.")
    category_options = ["Food","Housing","Transportation","Entertainment","Misc"]
    while True:
        print("Category:")
        for i,option in enumerate(category_options):
            print(f"{i+1}-{option}")
        category = int(input("Enter the Category number: "))

        if 1 <= category <= 5:
            break
        else:
            print("Entered number must be between 1-5")

    new_expense = {
        "Name": expense,
        "Price": price,
        "category": category_options[category - 1],
        "Date":datetime.date.today().isoformat()
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Saved a New expense: {expense} {price:.2f}€ Category:{category_options[category-1]}")
    
    recurring = input("Is this a recurring monthly expense? (y/n): ").strip().lower()
    if recurring == "y":
        recurring_expenses = load_recurring_expenses()
        recurring_expenses.append(new_expense)
        save_recurring_expenses(recurring_expenses)
        print("Recurring expense saved.")

def save_expenses(expenses, filename=EXPENSE_FILE_CURRENT):
    with open(filename, "w") as f:
        json.dump(expenses, f, indent=4)

def load_expenses(filename=EXPENSE_FILE_CURRENT):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_recurring_expenses(expenses):
    with open(RECURRING_EXPENSE_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

def load_recurring_expenses():
    try:
        with open(RECURRING_EXPENSE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def show_expenses(budget_manager):
    expenses = load_expenses()
    today = datetime.date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    days_left = last_day - today.day
    category_options = ["Food","Housing","Transportation","Entertainment","Misc"]
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    
    print("\nYour Expenses:")
    print("-" * 50)
    total = 0
    category_totals = {category: 0 for category in category_options}
    
    for i, expense in enumerate(expenses, start=1):
        name = expense["Name"]
        price = expense["Price"]
        category = expense["category"]
        print(f"{i}. {name:<15} {price:>7.2f}€  ({category})")
        total += price
        if category in category_totals:
            category_totals[category] += price
        
    print("-" * 50)

    print("Spending by Category:")
    for category, amount in category_totals.items():
        print(f"{category:<15}: {amount:.2f}€")
    print(f"\nTotal Spent: \033[31m{total:.2f}€\033[0m")
    if budget_manager.budget > 0:
        remaining = budget_manager.budget - total
        remaining_per_day = remaining/days_left
        remaining_percentage = (remaining/budget_manager.budget)*100
        
        if remaining >= 0.0:
            print(f"\nRemaining Budget: \033[32m{remaining:.2f}€\033[0m ({remaining_percentage}% left)")
            print(f"Remaining Budget Per Day: \033[32m{remaining_per_day:.2f}€\033[0m")
        elif remaining < 0.0:
            print(f"Remaining Budget: \033[31m{remaining:.2f}€\033[0m")
            print(f"Remaining Budget Per Day: \033[31m{remaining_per_day:.2f}€\033[0m")

def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return []

    print("\nYour Expenses:")
    print("-" * 50)
    for i, expense in enumerate(expenses, start=1):
        print(f"{i}. {expense['Name']} - {expense['Price']:.2f}€ ({expense['category']})")
    print("-" * 50)
    
    cancel_index = len(expenses) + 1
    print(f"{cancel_index}. Cancel")
    print("-" * 50)
    
    return expenses

def delete_expense():
    expenses = list_expenses()
    if not expenses:
        return
    
    cancel_index = len(expenses) + 1
    
    while True:
        user_input = input("\nEnter the number of the expense you want to delete (or choose Cancel): ")
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(expenses):
                removed = expenses.pop(choice - 1)
                save_expenses(expenses)
                print(f"Removed expense: {removed['Name']} ({removed['Price']:.2f}€)")
                break
            elif choice == cancel_index:
                print("Deletion canceled.")
                break
            else:
                print(f"Enter a number between 1 and {cancel_index}.")
        else:
            print("Invalid input! Please enter a number.")


if __name__ == "__main__":
    main()
