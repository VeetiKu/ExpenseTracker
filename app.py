import json

BUDGET_FILE = "monthly_budget.txt"


def main():
    options()
    
def options():
    print("\nWhat Would you like to do?")
    modules = ["1-Add new expense","2-Modify monthly budget","3-EXIT"]
    while True:
        for option in modules:
            print(option)
        choice = int(input("Enter the Module you want to use: "))
        if 1 <= choice <= 3:
            break
        else:
            print("Entered number must be between 1-3")
    if choice == 1:
        get_expense()
    elif choice == 2:
        monthly_budget()
    elif choice == 3:
        print("Exiting the app")
        quit()
        
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
            
    new_expense = {"Name":expense,
                   "Price":price,
                   "category":category_options[category-1]}        
    expenses.append(new_expense)
    save_expenses(expenses)
    
    print(f"Saved a New expense: {expense} {price}€ Category:{category_options[category-1]}")

    main()
            
def monthly_budget():
    budget = load_budget() 
    if budget > 0:
        print(f"\nYour current monthly budget is {budget}€")
    else:
        print("You haven't set a budget yet.")
    
    budget = float(input("Enter your new monthly budget: "))
    save_budget(budget)
    print(f"Your new budget is {budget}€ every month")
    main()

def save_budget(budget):
    with open(BUDGET_FILE, "w") as f:
        f.write(str(budget))

def load_budget():
    try:
        with open(BUDGET_FILE, "r") as f:
            return float(f.read())
    except (FileNotFoundError, ValueError):
        return 0
    
def save_expenses(expenses, filename="expenses.json"):
    with open(filename,"w") as f:
        json.dump(expenses, f, indent=4)

def load_expenses(filename="expenses.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    main()
