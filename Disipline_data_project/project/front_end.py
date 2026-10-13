import tkinter as tk

from tkinter import ttk
from tkinter import simpledialog

from datetime import date

from data_management import (
    create_table,
    add_category,
    add_info,
    get_data_storage,
    close_database,
    reset_table
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
    # Get activities belonging to category
    # ------------------------------------------------

    def get_category_activities(category_id):

        activities = get_data_storage("activities")

        if not activities:
            return None

        result = []

        for activity in activities:

            # activity:
            # (id, date, category_id, activity_name)

            if activity[2] == category_id:

                activity_name = activity[3]

                if activity_name not in result:
                    result.append(activity_name)

        return result

    # ------------------------------------------------
    # Create category row
    # ------------------------------------------------

    def create_category_row(category_id, category_name):

        row = len(category_widgets)

        checked = tk.BooleanVar(value=False)

        selected_activity = tk.StringVar()

        activities = get_category_activities(category_id)

        # -----------------------
        # Checkbox
        # -----------------------

        checkbox = tk.Checkbutton(
            category_frame,
            text=category_name,
            variable=checked
        )

        checkbox.grid(
            row=row,
            column=0,
            sticky="w",
            padx=5,
            pady=5
        )

        # -----------------------
        # Dropdown
        # -----------------------

        dropdown = ttk.Combobox(
            category_frame,
            textvariable=selected_activity,
            values=activities,
            state="readonly",
            width=25
        )

        dropdown.grid(
            row=row,
            column=1,
            padx=5
        )

        # Select first activity automatically
        if activities:
            selected_activity.set(activities[0])

        # -----------------------
        # Add activity function
        # -----------------------

        def add_new_activity():

            activity_name = simpledialog.askstring(
                "New Activity",
                f"Add an activity to {category_name}:"
            )

            if not activity_name:
                return

            current_date = date_entry.get()

            add_info(
                current_date,
                category_id,
                activity_name
            )

            # Reload activities from database
            new_activities = get_category_activities(category_id)

            dropdown["values"] = new_activities

            selected_activity.set(activity_name)

        # -----------------------
        # Add activity button
        # -----------------------

        add_activity_button = tk.Button(
            category_frame,
            text="+ Activity",
            command=add_new_activity
        )

        add_activity_button.grid(
            row=row,
            column=2,
            padx=5
        )

        # Store everything for this category
        category_widgets[category_id] = {

            "name": category_name,

            "checked": checked,

            "selected_activity": selected_activity,

            "dropdown": dropdown
        }

    # ------------------------------------------------
    # Load categories from database
    # ------------------------------------------------

    def load_categories():

        # Remove old GUI rows
        for widget in category_frame.winfo_children():
            widget.destroy()

        category_widgets.clear()

        categories = get_data_storage("categories")

        for category in categories:

            category_id = category[0]
            category_name = category[1]

            create_category_row(
                category_id,
                category_name
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
            category_name
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


    def delete_all():
        reset_table("categories")
        reset_table("activities")
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