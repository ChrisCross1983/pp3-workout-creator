import gspread
from google.oauth2.service_account import Credentials
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('workouts')


def main_menu():
    print("Welcome to the Workout Generator")
    print("-----------------------")
    print("1. Create a new workout")
    print("2. Show saved workouts")
    print("-----------------------")

    choice = input("Please choose an option (1 or 2): ")

    if choice == "1":
        create_workout()
    elif choice == "2":
        show_saved_workouts()
    else:
        print("Invalid input, please choose 1 or 2.")
        main_menu()


def create_workout():
    # Ask user for the desired training time
    workout_duration = int(
        input(
            "How many minutes would you like to workout? "
            "Please enter a number between 10 and 90 minutes: "
        )
    )

    # Pull exercises from spreadsheet
    sheet_exercises = SHEET.worksheet("exercises")
    exercises_data = sheet_exercises.get_all_records()

    workout_plan = generate_workout(exercises_data, workout_duration)

    print("Your workout plan: ")
    for exercise in workout_plan:
        print(exercise)


def generate_workout(exercises_data, workout_duration):
    total_time = 0
    workout_plan = []

    while total_time < workout_duration:
        random_exercise = random.choice(exercises_data)
        print(random_exercise)
        exercise_time = (
            random_exercise.get("Repetitions/Duration", 0)
            * random_exercise.get("Time per Rep (Sec)", 0) / 60
        )

        if total_time + exercise_time <= workout_duration:
            workout_plan.append(random_exercise)
            total_time += exercise_time
        else:
            break
    return workout_plan


def show_saved_workouts():
    # Get saved workouts from spreadsheet
    sheet_saved_workouts = SHEET.worksheet("saved_workouts")
    saved_workouts_data = sheet_saved_workouts.get_all_records()
    if saved_workouts_data:
        for workout in saved_workouts_data:
            print(workout)
    else:
        print("No saved workouts found.")


main_menu()
