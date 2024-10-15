import gspread
from google.oauth2.service_account import Credentials
import random
import math
from datetime import datetime
import time

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
    print("--------------------------------")
    print("1. Create a new workout")
    print("2. Show saved workouts")
    print("3. Exit Program")
    print("--------------------------------")

    choice = input("Please choose an option (1, 2 or 3): ")

    if choice == "1":
        create_workout()
    elif choice == "2":
        show_saved_workouts()
    elif choice == "3":
        print("Goodbye! Closing the program.")
        exit()
    else:
        print("Invalid input, please choose 1, 2 or 3.")
        main_menu()


def create_workout():
    # Ask user for the desired training time
    while True:
        try:
            workout_duration = int(
                input(
                    "How many minutes would you like to workout? "
                    "(Please enter a number between 10 and 90): "
                    )
                )
            if 10 <= workout_duration <= 90:
                print("Workout will be created for you. Please wait...")
                time.sleep(2)
                break
            else:
                print("Invalid input. Please enter a number "
                      "between 10 and 90.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Pull warm up, cooldown and exercises from spreadsheet
    sheet_exercises = SHEET.worksheet("exercises")
    exercises_data = sheet_exercises.get_all_records()
    sheet_warm_up = SHEET.worksheet("warm_up")
    warm_up_data = sheet_warm_up.get_all_records()
    sheet_cool_down = SHEET.worksheet("cool_down")
    cool_down_data = sheet_cool_down.get_all_records()

    # Generate main workout
    workout_plan = generate_workout(exercises_data, workout_duration)

    # Display the complete workout (Warm-Up, Main Workout, Cool-Down)
    print_sorted_workout(workout_plan, warm_up_data, cool_down_data)

    # Question if workout should be saved
    while True:
        save_choice = input(
            "\nDo you want to save this workout? (y/n): ").lower()
        if save_choice == 'y':
            print("Please wait, your workout will be saved...")
            time.sleep(2)
            save_workout(workout_plan)
            break
        elif save_choice == 'n':
            print("Workout was not saved.")
            break
        else:
            print("Invalid input, please enter 'y' or 'n'.")

    return_to_menu_or_exit()


def generate_workout(exercises_data, workout_duration):
    total_time = 0
    workout_plan = []
    used_exercises = []

    # Defining muscle groups
    muscle_groups = set(
        exercise['Muscle Group'] for exercise in exercises_data
    )

    # Step 1: Choose minimum one exercise of each muscle group
    for muscle_group in muscle_groups:
        muscle_exercises = [
            exercise for exercise in exercises_data
            if exercise['Muscle Group'] == muscle_group
        ]
        if muscle_exercises:
            random_exercise = random.choice(muscle_exercises)
            exercise_time = math.ceil(
                random_exercise.get('Repetitions/Duration', 0)
                * random_exercise.get('Time per Rep (Sec)', 0) / 60
            )
            if total_time + exercise_time <= workout_duration:
                workout_plan.append(random_exercise)
                used_exercises.append(random_exercise)
                total_time += exercise_time

    # Step 2: Fill the remaining time with random exercises
    while total_time < workout_duration:
        remaining_exercises = [
            exercise for exercise in exercises_data
            if exercise not in used_exercises
        ]
        if remaining_exercises:
            random_exercise = random.choice(remaining_exercises)
            exercise_time = (
                random_exercise.get('Repetitions/Duration')
                * random_exercise.get('Time per Rep (Sec)') / 60
            )
            if total_time + exercise_time <= workout_duration:
                workout_plan.append(random_exercise)
                used_exercises.append(random_exercise)
                total_time += exercise_time
            else:
                break
        else:
            break

    return workout_plan


def print_sorted_workout(workout_plan, warm_up_data, cool_down_data):
    # ANSI color codes
    ORANGE = "\033[33m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

    print("\nYour sorted workout plan:")
    print("------------------------")

    # Display Warm-up
    print(f"\n{ORANGE}Warm-Up:{RESET}")
    print("----------")
    for warm_up_exercise in warm_up_data:
        print(
            f"{warm_up_exercise['Exercise']}: "
            f"{warm_up_exercise['Repetitions/Duration']} reps"
        )

    # Display Main Workout
    categories = ["Legs", "Chest", "Core", "Shoulders", "Back"]
    print(f"\n{GREEN}Main Workout:{RESET}")
    print("---------------")
    for category in categories:
        exercise_in_category = [
            exercise for exercise in workout_plan
            if exercise["Muscle Group"] == category
        ]
        if exercise_in_category:
            print(f"\n{category} exercises:")
            print("------------------------")
            for exercise in exercise_in_category:
                print(
                    f"{exercise['Exercise']} ({exercise['Muscle Group']}): "
                    f"{exercise['Repetitions/Duration']} reps"
                )
    # Display Cool-Down
    print(f"\n{BLUE}Cool-Down:{RESET}")
    print("------------")
    for cool_down_exercise in cool_down_data:
        print(
            f"{cool_down_exercise['Exercise']}: "
            f"{cool_down_exercise['Repetitions/Duration']} reps"
        )


def save_workout(workout_plan):
    # Save the workout to the Spreadsheet 'saved_workouts'
    sheet_saved_workouts = SHEET.worksheet("saved_workouts")

    # Todays date
    today = datetime.now().strftime("%Y-%m-%d")

    # Sort and save categories
    categories = ["Legs", "Chest", "Core", "Shoulders", "Back"]

    for category in categories:
        exercise_in_category = [
            exercise for exercise in workout_plan
            if exercise["Muscle Group"] == category
        ]
        if exercise_in_category:
            for exercise in exercise_in_category:
                row = [
                    today, "Main Workout",
                    exercise['Muscle Group'],
                    exercise['Exercise'],
                    exercise['Repetitions/Duration'],
                    exercise.get('Time per Rep (Sec)', 'N/A'),
                    exercise['Difficulty Level']
                ]
                sheet_saved_workouts.append_row(row)
    print("Workout successfully saved!")


def show_saved_workouts():
    print("Fetching saved workouts... Please wait...")
    time.sleep(2)

    # Get saved workouts from spreadsheet
    sheet_saved_workouts = SHEET.worksheet("saved_workouts")
    saved_workouts_data = sheet_saved_workouts.get_all_records()
    if saved_workouts_data:
        for workout in saved_workouts_data:
            print(workout)
    else:
        print("No saved workouts found.")

    return_to_menu_or_exit()


def return_to_menu_or_exit():
    # Possibility to retrun to the main menu or close the program
    while True:
        choice = input(
            "\nWould you like to back to the "
            "main menu (m) or exit (e)?"
        ).lower()
        if choice == 'm':
            main_menu()
            break
        elif choice == 'e':
            print("Closing the program. Goodbye!")
            exit()
        else:
            print(
                "Invalid input. Please enter 'm' to return"
                " to the main men or 'e' to exit."
            )


main_menu()
