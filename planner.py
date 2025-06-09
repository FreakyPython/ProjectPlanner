import csv
import json
from collections import namedtuple
import tkinter
from tkinter import filedialog, messagebox

# ------------------------
# Task Definition
# ------------------------

# We define a Task as a namedtuple with three fields: 'title', 'duration', and 'prerequisites'.
# The 'prerequisites' is a set of task IDs that need to be completed before the current task can begin.
Task = namedtuple("Task", ["title", "duration", "prerequisites"])

# The 'tasks' dictionary will store task data, where the key is the task ID and the value is the Task namedtuple.
tasks = {}

# ------------------------
# File Reading & Writing
# ------------------------

# This function reads a CSV file and returns a dictionary of tasks.
# Each row in the CSV contains the task data:
#   - First column: Task ID (integer)
#   - Second column: Task Title (string)
#   - Third column: Task Duration (float)
#   - Fourth column (optional): Prerequisites (space-separated task IDs)
def read_tasks_csv(filepath):
    result = {}  # Store tasks in this dictionary
    with open(filepath, newline='') as file:
        for row in csv.reader(file):  # Read each row in the CSV file
            if len(row) < 3:  # Skip rows with less than 3 columns (invalid data)
                continue
            try:
                task_id = int(row[0])  # Convert the task ID to an integer
                title = row[1]  # Task title
                duration = float(row[2])  # Task duration in days
                # Parse prerequisites if they exist (split by space and convert to integers)
                prereqs = set(map(int, row[3].split())) if len(row) > 3 and row[3] else set()
                # Add the task to the result dictionary
                result[task_id] = Task(title, duration, prereqs)
            except:
                continue  # Skip rows with invalid data (e.g., missing or non-numeric values)
    return result

# This function saves the tasks to a JSON file.
# The tasks are serialized into a list of dictionaries with keys: 'id', 'title', 'duration', and 'prerequisites'.
def save_tasks_json(filepath):
    data = [{"id": i, "title": t.title, "duration": t.duration, "prerequisites": list(t.prerequisites)} for i, t in tasks.items()]
    with open(filepath, 'w') as f:
        json.dump({"tasks": data}, f, indent=2)  # Write the tasks data as a JSON object

# This function loads tasks from a JSON file.
# It expects a JSON file with a structure like:
# {"tasks": [{"id": 1, "title": "Task A", "duration": 2.5, "prerequisites": [2, 3]}, ...]}
def load_tasks_json(filepath):
    with open(filepath) as f:
        data = json.load(f)  # Parse the JSON file into a Python dictionary
    result = {}
    for t in data["tasks"]:
        # For each task, create a Task namedtuple and store it in the result dictionary
        result[t["id"]] = Task(t["title"], t["duration"], set(t["prerequisites"]))
    return result

# ------------------------
# Task Scheduling
# ------------------------

# This function orders the tasks based on their prerequisites.
# It creates a schedule where tasks are arranged based on the prerequisite dependencies.
def order_tasks(tasks):
    incomplete = set(tasks)  # Set of tasks that still need to be scheduled
    completed = set()  # Set of tasks that have been completed
    start_days = {}  # Dictionary to store the start days for each task

    while incomplete:
        progress = False
        for task_number in list(incomplete):
            task = tasks[task_number]
            # If all prerequisites for the task are completed, it can be scheduled
            if task.prerequisites.issubset(completed):
                # Calculate the earliest possible start day by finding the maximum completion day of its prerequisites
                earliest_start = max(
                    (start_days[p] + tasks[p].duration for p in task.prerequisites),
                    default=0  # If there are no prerequisites, start on day 0
                )
                start_days[task_number] = earliest_start  # Set the start day for the task
                completed.add(task_number)  # Mark the task as completed
                incomplete.remove(task_number)  # Remove the task from the incomplete list
                progress = True
        if not progress:  # If no progress was made, it means there is a circular dependency
            raise Exception("Circular dependency detected")
    return start_days  # Return the start days for each task

# ------------------------
# Drawing
# ------------------------

# This function draws the Gantt chart on a Tkinter canvas.
# It calculates task start days and creates rectangles for each task on the chart.
def draw_chart(tasks, canvas, dark_mode=False):
    canvas.delete("all")  # Clear the canvas
    try:
        start_days = order_tasks(tasks)  # Order the tasks based on dependencies
    except Exception as e:
        messagebox.showerror("Error", str(e))  # If there is an error (like circular dependency), show an error message
        return

    total_days = max(start_days[t] + tasks[t].duration for t in tasks)  # Total days needed for all tasks
    total_weeks = int(total_days / 5) + 1  # Calculate how many weeks will fit in the total duration (assuming 5 days per week)
    title_width, row_height = 250, 40  # Task title column width and row height
    day_width = (int(canvas["width"]) - title_width) // (total_weeks * 5)  # Calculate the width of each day block
    week_width = 5 * day_width  # Width of a week (5 days)
    bar_height = 20  # Height of the task bars
    font = ("Helvetica", -14)  # Font for labels

    # Set background and foreground colors based on dark mode setting
    bg = "#2c2c2c" if dark_mode else "white"
    fg = "white" if dark_mode else "black"
    canvas.config(bg=bg)  # Set the canvas background color

    # Draw the weeks on the chart
    for week in range(total_weeks):
        x = title_width + week * week_width
        canvas.create_line(x, 0, x, int(canvas["height"]), fill="gray")  # Draw vertical lines for weeks
        canvas.create_text(x + week_width / 2, row_height / 2, text=f"Week {week + 1}", font=font, fill=fg)

    y = row_height
    # Draw each task on the chart
    for task_id in sorted(start_days):
        task = tasks[task_id]
        canvas.create_text(10, y + row_height / 2, text=str(task_id), anchor="w", font=font, fill=fg)  # Draw task ID
        canvas.create_text(40, y + row_height / 2, text=task.title, anchor="w", font=font, fill=fg)  # Draw task title

        # Calculate the position of the task bar on the chart
        bar_x = title_width + start_days[task_id] * day_width
        bar_y = y + (row_height - bar_height) / 2
        bar_width = task.duration * day_width

        # Draw the task bar (rectangle)
        rect = canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                       fill="#f75d59", outline="black")

        # Add a tooltip when the mouse hovers over the task bar
        canvas.tag_bind(rect, "<Enter>", lambda e, text=f"{task.title} ({task.duration} days)": show_tooltip(e, text))
        canvas.tag_bind(rect, "<Leave>", lambda e: hide_tooltip())

        y += row_height  # Move to the next row for the next task

# ------------------------
# Tooltip Functions
# ------------------------

tooltip = None  # Variable to store the tooltip window

# This function displays a tooltip with the task information when the mouse enters the task bar.
def show_tooltip(event, text):
    global tooltip
    x = event.x_root + 10  # Tooltip's x-coordinate (offset from the mouse position)
    y = event.y_root + 10  # Tooltip's y-coordinate (offset from the mouse position)
    tooltip = tkinter.Toplevel()  # Create a new top-level window for the tooltip
    tooltip.wm_overrideredirect(True)  # Remove the window's title bar
    tooltip.wm_geometry(f"+{x}+{y}")  # Position the tooltip at the mouse location
    label = tkinter.Label(tooltip, text=text, background="black", foreground="white", padx=5)
    label.pack()

# This function hides the tooltip when the mouse leaves the task bar.
def hide_tooltip():
    global tooltip
    if tooltip:
        tooltip.destroy()  # Destroy the tooltip window
        tooltip = None

# ------------------------
# File Dialog Handlers
# ------------------------

# This function opens a CSV file and loads the tasks from it.
def open_csv():
    global tasks
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])  # Open a file dialog to select the CSV file
    if filename:
        tasks.clear()  # Clear the current tasks
        tasks.update(read_tasks_csv(filename))  # Read the tasks from the CSV file
        draw_chart(tasks, canvas, dark_mode_var.get())  # Redraw the Gantt chart with the new tasks

# This function loads tasks from a JSON file.
def load_json():
    global tasks
    filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])  # Open a file dialog to select the JSON file
    if filename:
        tasks.clear()  # Clear the current tasks
        tasks.update(load_tasks_json(filename))  # Load the tasks from the JSON file
        draw_chart(tasks, canvas, dark_mode_var.get())  # Redraw the Gantt chart with the new tasks

# This function saves the tasks to a JSON file.
def save_json():
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        save_tasks_json(filename)  # Save the tasks to the selected JSON file

# This function exports the Gantt chart as a PostScript (PS) image.
def export_image():
    filename = filedialog.asksaveasfilename(defaultextension=".ps", filetypes=[("PostScript Files", "*.ps")])
    if filename:
        canvas.postscript(file=filename)  # Save the canvas content as a PostScript file

# ------------------------
# UI Setup
# ------------------------

root = tkinter.Tk()  # Create the main Tkinter window
root.title("Project Planner")  # Set the window title
root.geometry("1000x600")  # Set the window size

# Create a top frame to hold the buttons
top_frame = tkinter.Frame(root)
top_frame.pack(side="top", fill="x", padx=5, pady=5)

# Add buttons for opening CSV, loading JSON, saving JSON, and exporting images
tkinter.Button(top_frame, text="Open CSV", command=open_csv).pack(side="left")
tkinter.Button(top_frame, text="Load JSON", command=load_json).pack(side="left")
tkinter.Button(top_frame, text="Save JSON", command=save_json).pack(side="left")
tkinter.Button(top_frame, text="Export Image", command=export_image).pack(side="left")

# Add a checkbox for toggling dark mode
dark_mode_var = tkinter.BooleanVar()
tkinter.Checkbutton(top_frame, text="Dark Mode", variable=dark_mode_var,
                    command=lambda: draw_chart(tasks, canvas, dark_mode_var.get())).pack(side="right")

# Create a canvas to draw the Gantt chart
canvas = tkinter.Canvas(root, width=1000, height=550, bg="white")
canvas.pack()

root.mainloop()  # Start the Tkinter main event loop
