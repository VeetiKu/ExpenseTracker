BUDGET_FILE = "monthly_budget.txt"

def main():
    options()
    
def options():
    print("What Would you like to do?")
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
    expense = input("Enter your expense: ")
    price = float(input("Cost: "))
    category_options = ["1-Food","2-Housing","3-Transportation","4-Entertainment","5-Misc"]
    while True:
        print("Category:")
        for option in category_options:
            print(option)
        category = int(input("Enter the Category: "))

        if 1 <= category <= 5:
            break
        else:
            print("Entered number must be between 1-5")
    print(f"Saved a New expense:{expense} {price}€ Category:{category_options[category-1]}")
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

if __name__ == "__main__":
    main()
