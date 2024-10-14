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

# connect with the google sheet
sheet_exercises = SHEET.worksheet("exercises")
exercises_data = sheet_exercises.get_all_records()

for exercise in exercises_data:
    print(exercise)

sheet_saved_workouts = SHEET.worksheet("saved_workouts")
workout_to_save = [
    "2024-10-15",
    "Workout",
    "Chest",
    "Push-Ups",
    15,
    60,
    "medium"
]

sheet_saved_workouts.append_row(workout_to_save)
print("Workout successfully saved")
