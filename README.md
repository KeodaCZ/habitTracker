# Habit Tracker (CLI)

A simple command-line habit tracker written in Python.  
You can add habits, mark them as completed, view statistics, export data, and see streaks — all from the terminal.

---

## 📦 Features

### ✔ Add and Track Habits
- Add new habits  
- List all habits  
- Record daily check-ins (today or a chosen date)

### 📊 Statistics
- Total number of completions  
- Activity in the last 7 and 30 days  
- Current streak (consecutive days)

### 📄 Export
- Export all entries into a CSV file (`habit,date` format)

### 🧰 Additional Tools
- Show stats for all habits  
- Clean CLI interface using `argparse`  
- JSON-based storage (`data.json`)

---

## 🚀 Usage

Run the script from the command line:

### Add a habit
```bash
python habits.py add reading
```

### List all habits
```bash
python habits.py list
```

### Check in a habit (today)
```bash
python habits.py checkin reading
```

### Check in with a custom date
```bash
python habits.py checkin reading --date 2025-02-15
```

### Show statistics for a habit
```bash
python habits.py stats reading
```

### Show statistics for all habits
```bash
python habits.py stats-all
```

### Export all data to CSV
```bash
python habits.py export --output habits_export.csv
```

---

## 📁 Data Format

The JSON file (`data.json`) uses this structure:

```json
{
  "habits": {
    "reading": [
      "2025-02-14",
      "2025-02-15"
    ]
  }
}
```

---

## 🛠 Requirements

- Python **3.x**
- Standard library only (json, datetime, csv, argparse)

No external dependencies required.

---

## 📅 Roadmap
- 🔁 Refactor into modules (logic.py, storage.py, cli.py) 
- 🧪 Unit tests for streak and check-in
- ⭐ Display TOP 3 most active habits (last 30 days)
- 📥 Import data from CSV 
- 🪟 Simple Tkinter GUI
- 📝 Expanded documentation and more examples

---

## 📄 License
This project is free to use and modify for personal learning.

