import pymongo
from pymongo import MongoClient
from datetime import date

cluster = MongoClient("mongodb+srv://bluerayman23:PVxcsqhGrQtUDXY1@cluster0.0dnk4zo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["Bank"]
collection = db["user_accounts"]

def sign_up():
    username = input("Type in a username")
    password = input("Type in a password")

    if collection.find_one({"username": username}):
        print("Sorry username is already taken")
        return 
    
    last_user = collection.find_one(sort=[("_id", -1)])
    new_id = last_user["_id"] + 1 if last_user else 1

    user_doc = { "_id": new_id, "username": username, "password": password}

    collection.insert_one(user_doc)
    print(f"Congrats!")

def update(username, password, new_checkings, new_savings):

    result = collection.update_one({"username":username, "password":password},{"$set":{"checkings":new_checkings,"savings":new_savings}})

    if result.matched_count > 0:
        print("Update successful!")
    else:
        print("no Matching user found!")

def check_account(username,password):
    query = {"username": username, "password": password}
    results = collection.find(query)

    for x in results:
        print(x)
    

def budget_planner(username,password):
    print( "Hello welcome to the budget planner. The goal of this is to establish how much you should save everyday to attain a goal. \n")
    goal = input("Now what are you saving for? \n")
    monetary_goal = int(input("How much will that cost? \n"))
    collection.update_one({"username":username, "password":password},{"$set":{f"{goal}": monetary_goal}})

    weekly_income = int(input("How much do you make a week?\n"))

    if input("Do you have a date you're working towards? Y/N \n").lower() == "y":

        end_year = int(input("input full year (2025,2024) \n"))
        end_month = int(input("input month (08, 09, 10) \n"))
        end_day = int(input("input day (01, 20, 31) \n"))
        end_date = date(end_year, end_month, end_day)

        current_date = date.today()

        difference = end_date - current_date

        weeks = difference.days//7


        weekly_savings_amount = monetary_goal / weeks

        if weekly_savings_amount > weekly_income:
             print("Goal not achievable: you need to save more than you earn each week. Consider going at a later date.")

        else:
            print(f"You need to save ${weekly_savings_amount:.2f} per week.")

    else:
        print("That's alright we'll just figure out a different way")
        choice = input("Would you like to save a percentage aside? Y/N \n").lower()

        if choice == "y":
            weekly_percentage = int(input("What percent would you like to set aside? (1%, 25%, 100% without the percent symbol) \n"))

            savings_amount = (weekly_percentage/100)* weekly_income
            week_amount = monetary_goal/savings_amount
            
            print(f"To achieve your goal you should be saving {savings_amount} or {weekly_percentage} for {week_amount} weeks.")

        elif choice == "n":
            savings_amount = int(input("How much do you plan to save a week?"))
            week_amount = monetary_goal/savings_amount
            print(f"To achieve your goal you should be saving {savings_amount} for {week_amount} weeks.")
        else:
            print("ERROR: existing plan.")
            return
            

def main():
    
    action = input("login or signup \n").strip().lower()
    if action == "login":
        username = input("username: \n")
        password = input("password: \n")

        user = collection.find_one({"username": username,"password":password})
        if not user:
            print("Invalid. Try again")
        else:
            print(f"Welcome back {username}")
            while True:
                print("\nWhat would you like to do?")
                print("1. Update account")
                print("2. Try the budget planner")
                print("3. Check Account")
                print("4. Log out")

                choice = input("Enter the number of your choice: ").strip()

                if choice == "1":
                    print("Redirecting to account update...")
                    # Call update_account() or similar
                    try:
                        new_checkings = float(input("What is your total checkings? "))
                        new_savings = float(input("What is your total savings? "))
                        update(username, password, new_checkings, new_savings)
                    except ValueError:
                        print("Please enter valid numbers.")

                elif choice == "2":
                    print("Launching the budget planner...")
                    budget_planner(username,password)
                    # Call budget_planner() or similax
                elif choice == "3":
                    print("Account info:")
                    check_account(username, password)

                elif choice == "4":
                    print("Logging out...")
                    break  # Exit the loop to log out

                else:
                    print("Invalid option. Please try again.")
    elif action == "signup":
        sign_up()
    else:
        print("Invalid action. Please type 'login' or 'signup'.")

if __name__ == "__main__":
    main()