import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('workouts')

# Pull exercises from google spreadsheet
sheet_exercises = SHEET.worksheet("exercises")
exercises_data = sheet_exercises.get_all_records()

# Save new workouts to spreadsheet
sheet_saved_workouts = SHEET.worksheet("saved_workouts")
workout_to_save = []
sheet_saved_workouts.append_row(workout_to_save)
# print("Workout successfully saved")

def main_menu():
    print("Welcome to the Workout Generator")
    print("1. Create a new workout")
    print("2. Show saved workouts")

    choice = input("Please choose an option (1 or 2): ")

    if choice == "1":
        create_workout()
    elif choice == "2":
        show_saved_workouts()
    else:
        print("Invalid input, please choose 1 or 2.")
        main_menu()

main_menu()