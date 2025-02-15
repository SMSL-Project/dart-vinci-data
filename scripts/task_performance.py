#!/usr/bin/env python3
"""
This script collects performance data for a series of tasks, each with a 2-minute duration.
At the start, the user is prompted to specify the CSV file name. The file will be saved to a folder
named 'data' located in the parent directory of the current working directory.
Before each task, the user selects a task by entering its enumerated ID. To exit data collection,
the user can type 'exit' when prompted for a task ID. After each task's timer expires,
the user is prompted to enter the total number of successes and attempts.
The success rate is computed as total_success / total_attempt.
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
    print("-" * 60)
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
    csv_filename = input(
        "Enter Subject Codename (without extension or with '.csv'): "
    ).strip()
    if not csv_filename.lower().endswith(".csv"):
        csv_filename += ".csv"

    parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    data_dir = os.path.join(parent_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    csv_filepath = os.path.join(data_dir, csv_filename)

    return csv_filepath


def select_task(tasks):
    """
    Display a list of tasks with their corresponding IDs and prompt the user to select a task.
    The user can type 'exit' to finish data collection.

    Parameters:
        tasks (list): List of available tasks.

    Returns:
        str or None: The selected task name, or None if the user types 'exit'.
    """
    print("\nAvailable tasks:")
    for idx, task in enumerate(tasks, start=1):
        print(f"{idx}. {task}")
    selection = input(
        f"Enter task id (1-{len(tasks)}) or type 'exit' to finish: "
    ).strip()
    if selection.lower() == "exit":
        return None
    try:
        task_id = int(selection)
        if 1 <= task_id <= len(tasks):
            return tasks[task_id - 1]
        else:
            print(f"Invalid task id. Please enter a number between 1 and {len(tasks)}.")
            return select_task(tasks)
    except ValueError:
        print("Invalid input. Please enter a valid task id or 'exit'.")
        return select_task(tasks)


def main():
    csv_filepath = prepare_csv_filepath()

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

    task_duration_seconds = 5  # Set duration to 2 minutes (120 seconds)

    data = []

    print("\nPerformance Data Collection for Tasks\n")

    while True:
        selected_task = select_task(tasks)
        if selected_task is None:
            # User chose to exit data collection.
            break

        print(f"\nTask: {selected_task}")
        input("Press Enter to start the 2-minute timer for this task...")
        start_timer(task_duration_seconds)

        total_success = get_integer_input("  Enter total number of successes: ")
        total_attempt = get_integer_input("  Enter total number of attempts: ")

        if total_attempt > 0:
            success_rate = total_success / total_attempt
        else:
            success_rate = 0

        print()  # Blank line for readability.

        data.append(
            {
                "Task": selected_task,
                "Total Success": total_success,
                "Total attempt": total_attempt,
                "Success Rate": success_rate,
                "Task Duration (secs)": task_duration_seconds,
            }
        )

    # Define the header fields for the CSV.
    fieldnames = [
        "Task",
        "Total Success",
        "Total attempt",
        "Success Rate",
        "Task Duration (secs)",
    ]

    try:
        with open(csv_filepath, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Write the header row.
            writer.writerows(data)  # Write all collected task data.
        print(f"\nData has been successfully saved to '{csv_filepath}'.")
    except Exception as e:
        print("An error occurred while writing to the CSV file:", e)


if __name__ == "__main__":
    main()
