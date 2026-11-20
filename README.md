
# Student Life Balance

A Python desktop application for recording daily activities across different areas of student life. Create categories and activities, log what you did on a date, view your history, and export it as a CSV file for Excel.

## Features

- Create and delete categories and activities.
- Select activities and save them to a daily log.
- View logged dates, categories, and activities in a separate window.
- Export activity history to a CSV file that can be opened in Excel.
- Store data locally in an SQLite database.

## Requirements

- Python 3.11 (the version used during development).
- Tkinter and SQLite support in your Python installation. The supplied files use Python's standard library; no third-party packages are required.
- The `category_ui.py` file alongside the other Python files. It is imported by `front_end.py` and is needed to start the application.

## Run the application

1. Open a terminal in the folder containing `main.py`, `front_end.py`, `data_management.py`, `daily_log.py`, and `category_ui.py`.
2. On Windows, run:

   ```powershell
   py main.py
   ```

   If `py` is unavailable, try `python main.py`.
3. The application creates its database tables if they do not already exist.

The app opens `data_storage.db` relative to the **terminal's current working directory**, not necessarily the folder containing `main.py`. Run it from the same folder each time to avoid accidentally creating another empty database. Back up an existing database before moving or replacing it.

## Using the app

1. Select **+ Category** and enter a category name.
2. Add activities to your categories using the category controls.
3. Check a category, select an activity, and enter a date. Today's date is filled in automatically in `YYYY-MM-DD` format.
4. Select **Save Selected** to add the selected activities to the log.
5. Select **Show All Log** to view activity history, or **Export Csv** to choose where to save a CSV file. Open the CSV in Excel to view it there.

**Show Selected** and **Show All Information** print information to the terminal. **Delete All Information** drops and recreates all three tables, removing saved categories, activities, and logs. Back up the database first if you want to keep the data.

## Project files

| File | Purpose |
| --- | --- |
| `main.py` | Starts the application and its event loop. |
| `front_end.py` | Creates the main Tkinter window and connects its controls. |
| `category_ui.py` | Provides the category row interface imported by the front end. |
| `data_management.py` | Creates the SQLite tables and reads or changes the data. |
| `daily_log.py` | Displays history in a Treeview and exports it to CSV. |
| `data_storage.db` | SQLite database created or opened in the current working directory. |

## Database structure

- **categories:** `id`, `category_name`
- **activities:** `id`, `category_id`, `activity_name`
- **activities_log:** `id`, `date`, `activity_id`

The history query joins the three tables to show readable category and activity names. The schema declares a foreign key from the log to activities; the provided code does not explicitly enable SQLite foreign-key enforcement. Removing an activity or category can therefore leave log entries that no longer appear in the joined history. Back up your database before deleting data.

## Privacy and backups

The database may contain personal activity information. If the repository is public, avoid committing personal database or exported CSV files. Adding files to `.gitignore` does not remove copies already committed to Git history. Keep a separate backup of the database if you want to preserve your records.
