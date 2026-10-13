import tkinter as tk

from tkinter import ttk
from tkinter import simpledialog

from datetime import date

from data_management import (
    create_table,
    add_category,
    get_data_storage,
    close_database,
    reset_table,
)

from category_ui import (
    create_category_row
)

def create_gui():

    root = tk.Tk()

    root.title("Student Life Balance")
    root.geometry("700x500")

    # Make sure database tables exist
    create_table()

    # ------------------------------------------------
    # Date
    # ------------------------------------------------

    tk.Label(
        root,
        text="Date:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    date_entry = tk.Entry(root)

    date_entry.grid(
        row=0,
        column=1
    )

    # Automatically put today's date
    date_entry.insert(
        0,
        date.today().isoformat()
    )
    
    # ------------------------------------------------
    # Category area
    # ------------------------------------------------

    category_frame = tk.Frame(root)

    category_frame.grid(
        row=1,
        column=0,
        columnspan=4,
        padx=20,
        pady=20
    )

    # Store GUI information about categories
    category_widgets = {}

    
    # ------------------------------------------------
    # Load categories from database
    # ------------------------------------------------

    def load_categories():

        # Remove old GUI rows
        for widget in category_frame.winfo_children():
            widget.destroy()

        category_widgets.clear()

        categories = get_data_storage("categories")

        if not categories:
            print("No categoty to show")
            return
        for category in categories:
            category_id = category[0]
            category_name = category[1]

            create_category_row(
                category_id,
                category_name,
                category_widgets,
                category_frame,
                date_entry,
                load_categories
            )

    # ------------------------------------------------
    # Create new category
    # ------------------------------------------------

    def create_new_category():

        category_name = simpledialog.askstring(
            "New Category",
            "Enter category name:"
        )

        if not category_name:
            return

        category_id = add_category(category_name)

        if category_id is None:
            return

        create_category_row(
            category_id,
            category_name,
            category_widgets,
            category_frame,
            date_entry,
            load_categories
        )

    # ------------------------------------------------
    # Print selected categories
    # ------------------------------------------------

    def show_selected():

        for category_id, info in category_widgets.items():

            if info["checked"].get():

                print(
                    info["name"],
                    ":",
                    info["selected_activity"].get()
                )

    def print_data():
        print("categories: ",get_data_storage("categories"))
        print("activities: ",get_data_storage("activities"))
        print("activity logs: ",get_data_storage("activities_log"))


    def delete_all():
        reset_table("activities_log")
        reset_table("activities")
        reset_table("categories")
        create_table()
        load_categories()

    
    # ------------------------------------------------
    # Buttons
    # ------------------------------------------------

    add_category_button = tk.Button(
        root,
        text="+ Category",
        command=create_new_category
    )

    add_category_button.grid(
        row=2,
        column=0,
        pady=10
    )

    save_button = tk.Button(
        root,
        text="Show Selected",
        command=show_selected
    )

    save_button.grid(
        row=2,
        column=1
    )

    information_button = tk.Button(
            root,
            text="Show All Information",
            command=print_data
        )

    information_button.grid(
        row = 3,
        column = 1,
        pady = 10
    )

    delete_button = tk.Button(
                    root,
                    text="Delete All Information",
                    command=delete_all
                )

    delete_button.grid(
            row = 3,
            column = 2,
            pady = 10
        )

    # ------------------------------------------------
    # Load saved categories
    # ------------------------------------------------

    try:
        load_categories()
    except:
        print('no catogories had found')

    # ------------------------------------------------
    # Close program correctly
    # ------------------------------------------------

    def close_app():

        close_database()

        root.destroy()

    root.protocol(
        "WM_DELETE_WINDOW",
        close_app
    )

    return root