# Workout Creator

The Workout Creator is a Python program designed to help users create personalized workout routines based on their preferences. It runs in the terminal, offering a convenient way to generate full-body workouts that include warm-up, main workout, and cool-down exercises.

Here is the live version of my project: [Link to the Workout Creator Program](https://workout-creator-228871cd4fa2.herokuapp.com/)

![Screenshot of App on different screens](docs/responsive_pp3.png)

## How to use

The Workout Creator is designed to be simple and user-friendly. Users can specify their desired workout duration and select a difficulty level (easy, medium, hard). Based on these inputs, the program generates a complete workout plan.

1. Start the Program: Run the program in your terminal to be greeted by the main menu.
2. Create a Workout: Choose the workout duration (between 10 and 60 minutes) and the difficulty level (easy, medium, hard).
   The program will generate exercises targeting different muscle groups.
3. Save and View Workouts: You can save generated workout and access them later.
4. Warm-Up and Cool-Down: Every workout includes fixed warm-up and cool-down to help prevent injury.

## Briefing

**Workout Creator Program**

- The Workout Generator Program is designed for users who want to create personalized full-body workouts based on their preferences, such as duration and difficulty level. This project was created to help individuals train more efficiently and balance their exercise routines. Users can generate full-body workouts that include a warm-up, main workout, and cool-down session.

### Planning

- The Workout Generator aims to simplify the process of creating and planning workout routines. It considers user input, including training time and preferred difficulty level, to generate a balanced training plan that targets major muscle groups. The program is intended for anyone interested in at-home or gym workouts, with a focus on bodyweight exercises to ensure accessibility.

- The main elements of the workout include:

  - **Warm-Up**: Suggested exercises to prepare the body for the workout.
  - **Main Workout**: Focused on full-body exercises tailored to the selected difficulty level and duration.
  - **Cool-Down**: Recommended exercises to stretch and relax muscles post-training.

- The program ensures that the exercises selected fit the duration entered by the user and adapt based on the difficulty level. Warm-up and cool-down sessions are fixed at approximately 5 minutes each to avoid injury and promote muscle recovery.

## User Experience

### Ease of Use and Guidance

- The Workout Generator is easy to use, with simple prompts guiding the user through each step of generating a workout. Users are welcomed with a menu to either create a new workout, view saved workouts, or exit the program. Upon choosing to create a workout, users are prompted to enter the desired workout duration, select a difficulty level, and generate their workout.

- The user-friendly interface and informative messages ensure that even beginners can effectively use the program, with input validation helping avoid mistakes during the process.

## **Features**

### Existing Features

- **User-Friendly Menus**: The main menu allows users to create a new workout, view saved workouts, or exit the program.

![Screenshot of Main Menu](docs\features\main_menu_pp3.png)

- **Workout Customization**: Users can enter a desired workout duration (between 10 and 60 minutes) and select their preferred difficulty level (easy, medium, or hard). The workout is then created based on these inputs, including a warm-up, main workout, and cool-down.

![Screenshot of Workout Customization](docs\features\workout_customization_pp3.png)

- **Random Exercise Selection**: Exercises are selected randomly from predefined categories, ensuring variety.
- **Warm-Up and Cool-Down**: The program always includes a warm-up and cool-down to ensure the user is well-prepared and can safely recover. Each takes approximately 5 minutes and consists of basic stretching and mobility exercises.

![Screenshot of Random Workout](docs\features\random_workout_pp3.png)

- **Input Validation**: Ensures users enter valid numbers and choices throughout the program.

![Screenshot of Input Validation](docs\features\input_validation_pp3.png)

- **Save and View previous Workouts**: Users can save workouts and view them later for tracking progress.

![Screenshot of Input Validation](docs\features\saved_workouts_pp3.png)

### Future Features

- **Exercise Customization**: Allow users to choose specific exercises or muscle groups
- **Difficulty Progression**: Track user progress and recommend gradually increasing workout intensity.
- **Integrated Timer**: Add a timer to help users keep track of workout sets and rest periods.
- **Workout Analytics**: Provide insights and analysis of saved workout sessions to help users track their fitness journey.

## Structuring

**Flowchart Structure**:

- The structure of the Workout Generator Program is laid out through basic flowcharts that demonstrate the flow from input to output, ensuring clear visualization of user interaction and program decisions.

![Screenshot of the Flowchart](docs\flowchart_pp3.png)

## Technologies

### Python

- Python was used to create the program's logic

### Google Sheets API (gspread)

- Used to store and access workout data, including exercises and user-generated workouts.

### Flake8

- The Flake8 extension of Visual Studio Code was used to get a constant feedback about pythonic style.

### gspread

- The Python module used to interact with Google Sheets.

### datetime

- datetime was imported to get the current date and insert it to the export data file.

### Colorama

- Used to display text in color to enhance the user experience and readability.

### Visual Studio Code

- Visual Studio was used to write, debug, and test the Python code.

### GitHub

- GitHub was used for version control and project repository management.

## Data Model

The workout data is stored in a Google Sheet using the gspread libary. The Google Sheet maintains information
on exercises, difficulty levels, sets, repetitions and saved workouts. Each entry is time-stamped to allow users
to keep track of their workout history.

The program retrieves exercises from separate worksheets for warm-up, main exercises and cool-down. Depending on
the difficulty level, the program selects different exercises to generate a balanced routine.

## Testing

### General Testing

|       General Testing       |                        Testing Method                        |                      Expected result                      | Actual result |
| :-------------------------: | :----------------------------------------------------------: | :-------------------------------------------------------: | :-----------: |
|    User Input Validation    | Entering invalid input values (e.g., text in numeric fields) | Programm should prompt the user to re-enter correct input |     Pass      |
| Workout Duration Validation | Entering a workout duration less than 10 or greater than 60  | Program should prompt the user to enter a valid duration  |     Pass      |

### Manual Testing

I have manually tested this project by doing the following:

- Entered valid and invalid inputs to ensure the program handles errors correctly.
- Created workouts of different durations and difficulty levels to ensure the generated plans fit the specified parameters.
- Saved multiple workouts and checked if they were stored correctly in the Goolge Sheet.
- Verified that the static exercises (e.g., holds) display the correct duration in the saved workouts.

### Bugs

### Solved Bugs

### Remeining Bugs

- No known bugs.

### Validator Testing

### Flake8

- The code was checked for errors using the Flake8 extension for Visual Studio Code as a PEP8 control tool. No errors occurred while testing the final product.

![Screenshot of terminal flake8 results](docs\flake8_testing_pp3.png)

### CI Python Linter

- The code was checked for errors using the Code Institute Python Linter. No errors occurred while testing the final product.

![Screenshot of terminal flake8 results](docs\ci_python_linter_pp3.png)

## Deployment
