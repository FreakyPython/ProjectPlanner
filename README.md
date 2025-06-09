# 🛠 Project Planner (Tkinter Gantt Chart)

A beginner-friendly Python desktop application that displays project tasks using a visual Gantt chart. Load tasks from a CSV or JSON file and automatically schedule them based on prerequisites.

---

## ✅ Features

- 📂 Load tasks from **CSV** or **JSON** files
- 📊 Draws a **dynamic Gantt chart**
- 🧠 Automatically calculates task order and start times
- 🖱 Hover to view tooltips with task info
- 🌙 Optional **Dark Mode** toggle
- 🖼 Export chart as **PostScript (.ps)** image
- 💾 Save or load full projects using **JSON**

---

## 🏗 How It Works

- The app reads your CSV/JSON file and builds a list of tasks.
- Each task has a `title`, `duration`, and optional prerequisites.
- It uses a simple scheduling algorithm:
  - Tasks can’t begin until all their prerequisites are completed.
- The chart is drawn using `tkinter.Canvas`, with time represented in **days**.
- Every task is displayed as a **horizontal bar** on the timeline.

---

## 📁 File Structure
project_planner/
├── project_planner.py # Main application script
├── example_project.csv # Sample CSV input
├── example_project.json # Sample JSON input/output
└── README.md # This file

---

## 📥 CSV Format

Each line in the CSV should follow this format:

```csv
ID,Title,Duration,Prerequisites
1,Plan Project,3,
2,Design,2,1
3,Develop,5,1 2
4,Test,2,3
5,Deploy,1,4
ID: Unique task number

Title: Short description

Duration: How long the task takes (in days)

Prerequisites: Space-separated list of task IDs this task depends on (optional)

{
  "tasks": [
    { "id": 1, "title": "Plan Project", "duration": 3, "prerequisites": [] },
    { "id": 2, "title": "Design", "duration": 2, "prerequisites": [1] },
    { "id": 3, "title": "Develop", "duration": 5, "prerequisites": [1, 2] },
    { "id": 4, "title": "Test", "duration": 2, "prerequisites": [3] },
    { "id": 5, "title": "Deploy", "duration": 1, "prerequisites": [4] }
  ]
}
🚀 How to Run
Install Python 3 (if not already installed).

Open a terminal in the project directory.

🚀 How to Run
Install Python 3 (if not already installed).

Open a terminal in the project directory.

Run the app:
python planner.py

🎮 How to Use the App
Click "Open Project..." to select a .csv file.

The Gantt chart is drawn automatically.

Hover over a bar to view task info.

Click "Clear" to reset the canvas.

If available:

Use "Load JSON" or "Save JSON" to load/save full projects.

Click "Export Image" to save the chart as .ps.

👶 Who This Is For
This project is perfect if you're learning:
Python file handling (CSV/JSON)
Tkinter GUI development
Scheduling logic and basic algorithms
Making tools that are actually useful
You can use this to:
Learn
Customize
Share
Impress others with your GUI skills 🧠🎨

🙌 License
MIT License — feel free to use, share, and modify.