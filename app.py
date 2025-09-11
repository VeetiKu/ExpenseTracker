def main():
    print("App running!")
    options()
    
def options():
    print("What Would you like to do?")
    modules = ["1-Add new expense","2-modify monthly budget"]
    while True:
        for option in modules:
            print(option)
        choice = int(input("Enter the Module you want to use: "))
        if 1<= choice <= 5:
            break
        else:
            print("Entered Number must be between 1-5")
    if choice == 1:
        get_expense()
    if choice == 2:
        monthly_budget()
        
            

        
def get_expense():
    expense = input(str("Enter your expense:"))
    price = int(input("Cost:"))
    category_options=["1-Food","2-Housing","3-Transportation","4-Entertainment","5-Misc",""]
    while True:
        print("Category:")
        for option in category_options:
            print(option)
        category = int(input("Enter the Category: "))
        if 1<= category <= 5:
            break
        else:
            print("Entered Number must be between 1-5")
    main()
            
def monthly_budget():
    print("EYY")
    main()
    
        
    
    
    
if __name__ == "__main__":
    main()