#!/usr/bin/env python3
"""
This script collects performance data for a series of tasks, each with a 2-minute duration.
At the start, the user is prompted to specify the CSV file name. The file will be saved to a folder
named 'data' located in the parent directory of the current working directory.
For each task, the user initiates a timer by pressing Enter. After the timer expires,
the user is prompted to enter the total number of successes and completions.
The success rate is computed as total_success / total_completion.
All collected data is then saved into the specified CSV file.
"""

import os
import time
import csv


def get_integer_input(prompt):
    """
    Prompt the user until a valid integer is entered.

    Parameters:
        prompt (str): The prompt message to display to the user.

    Returns:
        int: The integer value provided by the user.
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer value.")


def start_timer(duration=120):
    """
    Start a timer for a specified duration in seconds.
    The timer is displayed on the console, counting from 0 to the specified duration.
    Execution is paused until the timer completes.

    Parameters:
        duration (int): Duration of the timer in seconds (default is 120 seconds).
    """
    print("\nTask timer started. Please perform the task.")
    for elapsed in range(duration + 1):
        # Display the elapsed time on the same console line.
        print(f"Elapsed time: {elapsed:3d} seconds", end="\r", flush=True)
        time.sleep(1)
    print("\nTime is up! Please proceed with the input.")


def prepare_csv_filepath():
    """
    Prompt the user for a CSV file name and prepare the full file path.
    The CSV file will be saved in a folder named 'data' under the parent directory.

    Returns:
        str: The full file path for the CSV file.
    """
    # Prompt user to enter the CSV file name.
    csv_filename = input(
        "Enter CSV file name (without extension or with '.csv'): "
    ).strip()
    # Append .csv extension if not provided.
    if not csv_filename.lower().endswith(".csv"):
        csv_filename += ".csv"

    # Get the parent directory of the current working directory.
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    # Define the data folder path.
    data_dir = os.path.join(parent_dir, "data")
    # Create the data folder if it does not exist.
    os.makedirs(data_dir, exist_ok=True)
    # Construct the full CSV file path.
    csv_filepath = os.path.join(data_dir, csv_filename)

    return csv_filepath


def main():
    # Obtain the CSV file path from the user.
    csv_filepath = prepare_csv_filepath()

    # List of tasks for which data will be collected.
    tasks = [
        "Reach",
        "Reach with Obstacle",
        "Dual Arm Reach",
        "Dual Arm Reach with Obstacle",
        "Needle Pick",
        "Needle Handover",
        "Peg Pick",
        "Peg Transfer",
        "Peg Board Pick and Place",
        "Needle through Ring",
    ]

    # Duration for each task in seconds (2 minutes).
    task_duration_seconds = 10

    # List to store the collected data for each task.
    data = []

    print("\nPerformance Data Collection for Tasks\n")

    # Iterate over each task to collect data.
    for task in tasks:
        print(f"Task: {task}")

        # Prompt the user to start the timer.
        input("Press Enter to start the 2-minute timer for this task...")
        start_timer(task_duration_seconds)

        # After the timer, prompt the user for performance data.
        total_success = get_integer_input("  Enter total number of successes: ")
        total_completion = get_integer_input("  Enter total number of completions: ")

        # Compute the success rate (handle division by zero).
        if total_completion > 0:
            success_rate = total_success / total_completion
        else:
            success_rate = 0

        print()  # Blank line for readability.

        # Append the collected data for the current task.
        data.append(
            {
                "Task": task,
                "Total Success": total_success,
                "Total Completion": total_completion,
                "Success Rate": success_rate,
                "Task Duration (secs)": task_duration_seconds,
            }
        )

    # Define the header fields for the CSV.
    fieldnames = [
        "Task",
        "Total Success",
        "Total Completion",
        "Success Rate",
        "Task Duration (secs)",
    ]

    # Write the collected data to the CSV file.
    try:
        with open(csv_filepath, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row.
            writer.writerows(data)  # Write all task data rows.
        print(f"\nData has been successfully saved to '{csv_filepath}'.")
    except Exception as e:
        print("An error occurred while writing to the CSV file:", e)


if __name__ == "__main__":
    main()
