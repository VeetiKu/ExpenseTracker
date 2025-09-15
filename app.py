import json
import datetime
import calendar


BUDGET_FILE = "monthly_budget.json"
EXPENSE_FILE_CURRENT = "expenses.json"
EXPENSE_FILE_PAST = "pastexpenses.json"


def main():
    while True:
        budget, saved_month = load_budget()
        current_month = datetime.date.today().strftime("%Y-%m")

        # Reset if new month
        if saved_month != current_month:
            print("\n--- New Month Detected ---")
            print("Archiving last month’s expenses and resetting for this month.")
            last_expenses = load_expenses()
            save_expenses(last_expenses, EXPENSE_FILE_PAST)
            save_expenses([])
            save_budget(budget, current_month)

        if budget == 0:
            monthly_budget()
        choice = options()
        if choice == 1:
            get_expense()
        elif choice == 2:
            monthly_budget()
        elif choice == 3:
            show_expenses()
        elif choice == 4:
            print("Exiting the app")
            break
        
def options():
    print("\nWhat Would you like to do?")
    modules = ["1-Add new expense","2-Modify monthly budget","3-Display your expenses","4-EXIT"]
    while True:
        for option in modules:
            print(option)
        user_input = input("Enter the Module you want to use: ")
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= 4:
                return choice
        print("Error: Entered number must be between 1-3.")
        
def get_expense():
    expenses = load_expenses()
    expense = input("\nEnter your expense: ")
    price = float(input("Cost: "))
    category_options = ["Food","Housing","Transportation","Entertainment","Misc"]
    while True:
        print("Category:")
        for i,option in enumerate(category_options):
            print(f"{i+1}-{option}")
        category = int(input("Enter the Category: "))

        if 1 <= category <= 5:
            break
        else:
            print("Entered number must be between 1-5")

    new_expense = {
        "Name": expense,
        "Price": price,
        "category": category_options[category - 1],
    }
    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"Saved a New expense: {expense} {price}€ Category:{category_options[category-1]}")
    
def monthly_budget():
    budget, _ = load_budget()
    if budget > 0:
        print(f"\nYour current monthly budget is {budget}€")
    else:
        print("You haven't set a budget yet.")

    budget = float(input("Enter your new monthly budget: "))
    current_month = datetime.date.today().strftime("%Y-%m")
    save_budget(budget, current_month)
    print(f"Your new budget is {budget}€ every month")


def save_budget(budget, month):
    data = {"budget": budget, "month": month}
    with open(BUDGET_FILE, "w") as f:
        json.dump(data, f)

def load_budget():
    try:
        with open(BUDGET_FILE, "r") as f:
            data = json.load(f)
            return data.get("budget", 0), data.get("month", "")
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return 0, ""
    
def save_expenses(expenses, filename=EXPENSE_FILE_CURRENT):
    with open(filename, "w") as f:
        json.dump(expenses, f, indent=4)


def load_expenses(filename=EXPENSE_FILE_CURRENT):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def show_expenses():
    expenses = load_expenses()
    today = datetime.date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    days_left = last_day - today.day
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\nYour Expenses:")
    print("-" * 50)
    total = 0
    for i, expense in enumerate(expenses, start=1):
        name = expense["Name"]
        price = expense["Price"]
        category = expense["category"]
        print(f"{i}. {name:<15} {price:>7.2f}€  ({category})")
        total += price
    print("-" * 50)
    print(f"Total Spent: \033[31m{total:.2f}€\033[0m")
    budget, _ = load_budget()
    if budget > 0:
        remaining = budget - total
        remaining_per_day = remaining/days_left
        if remaining >= 0.0:
            print(f"Remaining Budget: \033[32m{remaining:.2f}€\033[0m")
            print(f"Remaining Budget Per Day: \033[32m{remaining_per_day:.2f}€\033[0m")
        elif remaining < 0.0:
            print(f"Remaining Budget: \033[31m{remaining:.2f}€\033[0m")
            print(f"Remaining Budget Per Day: \033[31m{remaining_per_day:.2f}€\033[0m")
            


if __name__ == "__main__":
    main()

# ADD EXPENSES SHOW SUMMARY PER CATEGORY LIKE FOOD TOTAL:50€
#SHOW HOW MUCH YOU CAN SPEND PER DAY TO STAY ON BUDGET FOR THE MONTH