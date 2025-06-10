The provided code is a Python application that creates a Gantt chart for project planning using Tkinter. It allows users to load tasks from CSV or JSON files, schedule them based on prerequisites, display a Gantt chart, and save or export the results. Below, I’ll simplify the documentation to make it easier to understand, similar to the approach taken with the Budget Manager documentation. This will include an overview, features, usage instructions, and key details about the code structure, while keeping it concise and clear.

---

# Project Planner

A Python application for creating Gantt charts to visualize task schedules using a Tkinter-based GUI. The app reads tasks from CSV or JSON files, schedules them based on prerequisites, and displays a Gantt chart on a Tkinter canvas. Tasks can be saved as JSON or exported as PostScript images.

## Features
- **Load Tasks**: Import tasks from CSV or JSON files, including task ID, title, duration, and prerequisites.
- **Schedule Tasks**: Automatically schedules tasks based on their prerequisites, detecting circular dependencies.
- **Gantt Chart**: Displays tasks as bars on a canvas, with weeks marked and tooltips showing task details on hover.
- **Dark Mode**: Toggle between light and dark themes for the chart.
- **Export Options**: Save tasks as JSON or export the Gantt chart as a PostScript (.ps) file.
- **User-Friendly GUI**: Buttons for loading/saving files and a checkbox for dark mode, with an interactive canvas.

## Prerequisites
- Python 3.x
- Tkinter (included with Python)
- Standard libraries: `csv`, `json`, `collections`

## Installation
1. Ensure Python 3.x is installed.
2. Save the code in a file named `project_planner.py`.
3. No additional packages are required (uses Python standard libraries).

## Usage

### Running the GUI
Run the script to launch the GUI:
```bash
python project_planner.py
```

**Using the GUI**:
- **Open CSV**: Load tasks from a CSV file (format: `task_id,title,duration,prerequisites`).
- **Load JSON**: Load tasks from a JSON file.
- **Save JSON**: Save current tasks to a JSON file.
- **Export Image**: Save the Gantt chart as a PostScript (.ps) file.
- **Dark Mode**: Toggle the checkbox to switch between light and dark themes.
- **Gantt Chart**: Tasks are displayed as bars with:
  - Task ID and title on the left.
  - Bars showing duration and start time, with tooltips on hover.
  - Light blue headers (in light mode) or dark background (in dark mode).

### Example CSV File Format
```csv
1,Design,3,
2,Development,5,1
3,Testing,2,2
```
- Columns: Task ID (integer), Title (string), Duration (float, in days), Prerequisites (space-separated task IDs, optional).
- Example: Task 2 (Development) depends on Task 1 (Design) being completed.

### Example JSON File Format
```json
{
  "tasks": [
    {"id": 1, "title": "Design", "duration": 3.0, "prerequisites": []},
    {"id": 2, "title": "Development", "duration": 5.0, "prerequisites": [1]},
    {"id": 3, "title": "Testing", "duration": 2.0, "prerequisites": [2]}
  ]
}
```

## Code Structure

### Key Components
- **Task Namedtuple**:
  - Defined as `Task(title, duration, prerequisites)` to store task data.
  - `prerequisites` is a set of task IDs that must be completed first.
- **Tasks Dictionary**:
  - Stores tasks with task ID as the key and `Task` namedtuple as the value.

### Functions
- **File Handling**:
  - `read_tasks_csv(filepath)`: Reads tasks from a CSV file into a dictionary.
  - `load_tasks_json(filepath)`: Loads tasks from a JSON file.
  - `save_tasks_json(filepath)`: Saves tasks to a JSON file.
- **Task Scheduling**:
  - `order_tasks(tasks)`: Schedules tasks based on prerequisites, returning start days. Raises an error for circular dependencies.
- **Gantt Chart**:
  - `draw_chart(tasks, canvas, dark_mode)`: Draws the Gantt chart on a Tkinter canvas with task bars, week markers, and tooltips.
- **Tooltip Functions**:
  - `show_tooltip(event, text)`: Shows task details when hovering over a task bar.
  - `hide_tooltip()`: Hides the tooltip when the mouse leaves.
- **File Dialogs**:
  - `open_csv()`, `load_json()`, `save_json()`, `export_image()`: Handle file operations via Tkinter file dialogs.

### GUI Setup
- **Main Window**: Tkinter window (`root`) with title "Project Planner" and size 1000x600.
- **Top Frame**: Contains buttons (`Open CSV`, `Load JSON`, `Save JSON`, `Export Image`) and a `Dark Mode` checkbox.
- **Canvas**: Displays the Gantt chart with task IDs, titles, and bars representing task durations.

## Example Output
For the example CSV above:
- **GUI Gantt Chart**:
  - Task 1 (Design): Starts at day 0, lasts 3 days.
  - Task 2 (Development): Starts at day 3, lasts 5 days.
  - Task 3 (Testing): Starts at day 8, lasts 2 days.
  - Chart shows task bars aligned by start days, with week markers (Week 1, Week 2, etc.).
  - Hovering over a bar shows a tooltip (e.g., "Design (3 days)").
- **Console**: No direct console output; all visualization is in the GUI.

## Limitations
- No programmatic interface for adding/modifying tasks (GUI-only input via files).
- CSV files require valid data (integer ID, float duration, optional prerequisites).
- No support for editing tasks directly in the GUI.
- PostScript export is limited to `.ps` format, which may require conversion for common use.
- Circular dependencies cause an error and prevent chart rendering.

## Contributing
Submit pull requests or open issues for bugs, improvements, or feature requests.

## License
MIT License

---

### Notes
- The code assumes a 5-day workweek for week markers in the Gantt chart.
- Task bars are colored red (`#f75d59`) with black outlines.
- The GUI is fixed at 1000x600 pixels but could be made resizable.
- To enhance readability, I avoided technical jargon where possible and focused on practical usage instructions.
- If you want a specific section expanded (e.g., adding programmatic task creation or modifying the GUI), let me know!


