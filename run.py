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
            "(Please enter a number between 10 and 90): "
        )
    )

    # Pull warm up, cooldown and exercises from spreadsheet
    sheet_exercises = SHEET.worksheet("exercises")
    exercises_data = sheet_exercises.get_all_records()
    sheet_warm_up = SHEET.worksheet("warm_up")
    warm_up_data = sheet_warm_up.get_all_records()
    sheet_cool_down = SHEET.worksheet("cool_down")
    cool_down_data = sheet_cool_down.get_all_records()

    # Fixed warm-up exercises
    print("Warm-Up:")
    print("--------")
    for warm_up_exercise in warm_up_data:
        print(
            f"{warm_up_exercise['Exercise']}: "
            f"{warm_up_exercise['Repetitions/Duration']} reps"
        )

    print("\nStarting Main Workout...\n")

    # Generate main workout
    workout_plan = generate_workout(exercises_data, workout_duration)

    print("Your workout plan:")
    print("------------------")
    for exercise in workout_plan:
        print(
            f"{exercise['Exercise']} ({exercise['Muscle Group']}): "
            f"{exercise['Repetitions/Duration']} reps"
        )

    # Fixed cool-down exercises
    print("\nCool-Down:")
    print("----------")
    for cool_down_exercise in cool_down_data:
        print(
            f"{cool_down_exercise['Exercise']}: "
            f"{cool_down_exercise['Repetitions/Duration']} reps"
        )


def generate_workout(exercises_data, workout_duration):
    total_time = 0
    workout_plan = []
    used_exercises = []

    # Calculate average exercising time per set
    average_exercise_time = sum([
        (exercise['Repetitions/Duration'] * exercise['Time per Rep (Sec)'] / 60)
        for exercise in exercises_data
    ]) / len(exercises_data)

    # Limit max sets per exercise
    max_sets_per_exercise = 3

    # Estimate total number of sets possible within workout duration
    estimated_total_sets = int(workout_duration / average_exercise_time)
    print(f"Total estimated sets for the workout: {estimated_total_sets}")

    # Generate Workout
    while total_time < workout_duration:
        random_exercise = random.choice(exercises_data)

        if random_exercise not in used_exercises:
            exercise_time = (
                random_exercise['Repetitions/Duration'] * random_exercise['Time per Rep (Sec)'] / 60
            )
            # Dynamically calculate how many sets for this exercise
            sets_for_this_exercise = min(max_sets_per_exercise, int((workout_duration - total_time) / exercise_time))

            for _ in range(sets_for_this_exercise):
                if total_time + exercise_time <= workout_duration:
                    workout_plan.append(random_exercise)
                    total_time += exercise_time
                else:
                    break
            used_exercises.append(random_exercise)
            
        if total_time >= workout_duration:
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
