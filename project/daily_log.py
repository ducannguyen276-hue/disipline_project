import csv
import tkinter as tk

from tkinter import ttk
from tkinter import filedialog

from data_management import (
    get_daily_log
)


def show_activities_histories():
    rows = get_daily_log()

     # Create a pop-up window
    popup = tk.Toplevel()
    popup.title("Activity History")
    popup.geometry("600x350")

    # Create a table with three columns
    table = ttk.Treeview(
        popup,
        columns=("date", "category", "activity"),
        show="headings"
    )

    table.heading("date", text="Date")
    table.heading("category", text="Category")
    table.heading("activity", text="Activity")

    table.pack(fill="both", expand=True, padx=10, pady=10)

    # Add each result to the table
    for row in rows:
        table.insert("", "end", values=row)


def export_activity_history():
    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(
        title="Save activity history",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )

    # If the user clicks Cancel, stop the function
    if not file_path:
        return

    # Get the rows from the backend
    rows = get_daily_log()

    # Create and write the CSV file
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        # Write the column headings
        writer.writerow(["Date", "Category", "Activity"])

        # Write all the data rows
        writer.writerows(rows)

    print(f"Activity history saved to: {file_path}")