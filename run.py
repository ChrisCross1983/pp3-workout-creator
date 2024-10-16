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
                    "(Please enter a number between 10 and 60): "
                    )
                )
            if 10 <= workout_duration <= 60:
                print("Workout will be created for you. Please wait...")
                time.sleep(2)
                break
            else:
                print("Invalid input. Please enter a number "
                      "between 10 and 60.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Ask user for the difficulty level
    while True:
        difficulty = input(
            "Please choose your difficulty level (easy, medium, hard): "
            ).lower()
        if difficulty in ["easy", "medium", "hard"]:
            print(
                f"Workout will be created with difficulty"
                f" '{difficulty}'. Please wait..."
            )
            time.sleep(2)
            break
        else:
            print("Invalid input. Please enter 'easy', 'medium', or 'hard'.")

    # Pull warm up, cooldown and exercises from spreadsheet
    sheet_exercises = SHEET.worksheet("exercises")
    exercises_data = sheet_exercises.get_all_records()

    # Filter exercises based on selected level
    filtered_exercises = [
        exercise for exercise in exercises_data
        if exercise['Difficulty Level'].lower() == difficulty
    ]

    sheet_warm_up = SHEET.worksheet("warm_up")
    warm_up_data = sheet_warm_up.get_all_records()
    sheet_cool_down = SHEET.worksheet("cool_down")
    cool_down_data = sheet_cool_down.get_all_records()

    # Generate main workout
    workout_plan = generate_workout(
        filtered_exercises, workout_duration, difficulty)

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


def generate_workout(exercises_data, workout_duration, difficulty_level):
    total_time = 0
    workout_plan = []
    used_exercises = []

    # Defining muscle groups
    muscle_groups = set(
        exercise['Muscle Group'] for exercise in exercises_data
        if exercise['Difficulty Level'] == difficulty_level
    )

    # Step 1: Choose minimum one exercise of each muscle group
    for muscle_group in muscle_groups:
        muscle_exercises = [
            exercise for exercise in exercises_data
            if exercise['Muscle Group'] == muscle_group and
            exercise['Difficulty Level'] == difficulty_level
        ]
        if muscle_exercises:
            random_exercise = random.choice(muscle_exercises)
            sets = random_exercise.get('Sets', 3)

            # Check if the exercise is static or dynamic
            if isinstance(random_exercise['Repetitions/Duration'], str) and random_exercise['Repetitions/Duration'].lower() == 'static':
                # Static exercise
                exercise_time = math.ceil(
                    int(random_exercise['Time per Rep (Sec)']) * sets / 60
                )
            else:
                # Dynamic exercise
                exercise_time = math.ceil(
                    int(random_exercise['Repetitions/Duration']) *
                    int(random_exercise['Time per Rep (Sec)']) * sets / 60
                )

            if total_time + exercise_time <= workout_duration:
                random_exercise['Sets'] = sets
                workout_plan.append(random_exercise)
                used_exercises.append(random_exercise)
                total_time += exercise_time

    # Step 2: Fill the remaining time with random exercises
    while total_time < workout_duration:
        remaining_exercises = [
            exercise for exercise in exercises_data
            if exercise not in used_exercises and
            exercise['Difficulty Level'] == difficulty_level
        ]
        if remaining_exercises:
            random_exercise = random.choice(remaining_exercises)
            sets = random_exercise.get('Sets', 3)

            repetitions = random_exercise['Repetitions/Duration']
            if isinstance(repetitions, str) and repetitions.lower() == 'static':
                # Static exercise
                exercise_time = math.ceil(
                    int(random_exercise['Time per Rep (Sec)']) * sets / 60
                )
            else:
                # Dynamic exercise
                exercise_time = math.ceil(
                    int(repetitions) *
                    int(random_exercise['Time per Rep (Sec)']) * sets / 60
                )
            if total_time + exercise_time <= workout_duration:
                random_exercise['Sets'] = sets
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
                sets = exercise.get('Sets', 1)
                repetitions = exercise['Repetitions/Duration']

                if isinstance(repetitions, str) and repetitions.lower() == 'static':
                    # Static exercise - use the time value
                    time_per_rep = exercise['Time per Rep (Sec)']
                    print(
                        f"{exercise['Exercise']} ({exercise['Muscle Group']}): "
                        f"Hold for {time_per_rep} seconds x {sets} sets"
                    )
                else:
                    # Dynamic exercise - use repetitions value
                    print(
                        f"{exercise['Exercise']} ({exercise['Muscle Group']}): "
                        f"{repetitions} reps x {sets} sets"
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
                # Check, if exercise is static or dynamic
                repetitions = exercise['Repetitions/Duration']
                sets = exercise.get('Sets', 3)
                if isinstance(repetitions, str) and repetitions.lower() == 'static':
                    # Static exercise - calculate total hold time
                    total_time = int(exercise['Time per Rep (Sec)']) * sets
                    reps_duration = f"Hold for {total_time} seconds"
                else:
                    # Dynamic exercise - use repetitons value
                    reps_duration = f"{repetitions} reps x {sets} sets"

                row = [
                    today, "Main Workout",
                    exercise['Muscle Group'],
                    exercise['Exercise'],
                    reps_duration,
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

    # Group workouts by date
    grouped_workouts = {}

    for workout in saved_workouts_data:
        date = workout['Date']
        if date not in grouped_workouts:
            grouped_workouts[date] = []
        grouped_workouts[date].append(workout)

    for date, workouts in grouped_workouts.items():
        print(f"\nWorkout for: {date}")
        print("-------------------------")
        print(
            f"| {'Muscle Group':<12} | {'Exercise':<18} |"
            f" {'Reps/Duration':<14} | {'Difficulty':<10} |")
        print("-------------------------")

        # Sort workouts by muscle groups and order
        sorted_workouts = sorted(workouts, key=lambda x: x['Muscle Group'])

        for workout in sorted_workouts:
            # show the time correct for static exercises
            reps_duration = workout['Reps/Duration']
            if reps_duration == 'static':
                reps_duration = f"Hold for {workout['Time per Rep (Sec)']} seconds"

            print(
                f"| {workout['Muscle Group']:<12} | {workout['Exercise']:<18}"
                f"| {reps_duration:<14} | {workout['Difficulty Level']:<10} |"
            )
        print("-------------------------")

    if not saved_workouts_data:
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
