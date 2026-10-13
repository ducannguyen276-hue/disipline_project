import tkinter as tk

from tkinter import ttk
from tkinter import simpledialog

from data_management import (
    add_activity,
    add_activity_log,
    get_data_storage,
    delete_activities,
    delete_category
)


# ------------------------------------------------
# Get activities belonging to category
# ------------------------------------------------

def get_category_activities(category_id):

    activities = get_data_storage("activities")

    if not activities:
        return []

    result = []

    for activity in activities:
        result.append(activity)
        

    return result

# ------------------------------------------------
# Create category row
# ------------------------------------------------

def create_category_row(category_id, category_name,
                        category_widgets, category_frame,
                        date_entry, load_categories):

    row = len(category_widgets)

    checked = tk.BooleanVar(value=False)

    selected_activity = tk.StringVar()

    activities = get_category_activities(category_id)
    activity_names = [activity[2] for activity in activities]

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
        values=activity_names,
        state="readonly",
        width=25
    )

    dropdown.grid(
        row=row,
        column=1,
        padx=5
    )

    # Select first activity automatically
    if activity_names:
        selected_activity.set(activity_names[0])

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

        existing_activity = next(
            (
                activity
                for activity in get_category_activities(category_id)
                if activity[2] == activity_name
            ),
            None
        )
        activity_id = (
            existing_activity[0]
            if existing_activity
            else add_activity(category_id, activity_name)
        )
        add_activity_log(date_entry.get(), activity_id)

        # Reload activities from database
        new_activities = get_category_activities(category_id)

        dropdown["values"] = [activity[2] for activity in new_activities]

        selected_activity.set(activity_name)

    def delete_activity():

        activity_name = selected_activity.get()

        if not activity_name:
            return

        delete_activities(
            category_id,
            activity_name
        )

        # Refresh dropdown after deleting
        new_activities = get_category_activities(category_id)

        activity_names = [activity[2] for activity in new_activities]
        dropdown["values"] = activity_names

        if activity_names:
            selected_activity.set(activity_names[0])
        else:
            selected_activity.set("")

    def delete_category_info():
        delete_category(category_id)
        load_categories()



        
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

    # -----------------------
    # Delete activity button
    # -----------------------

    add_delete_act_button = tk.Button(
        category_frame,
        text="- Activity",
        command=delete_activity
    )

    add_delete_act_button.grid(
        row=row,
        column=3,
        padx=5
    )

    # -----------------------
    # Delete category button
    # -----------------------
    
    add_delete_cat_button = tk.Button(
        category_frame,
        text="- Category",
        command=delete_category_info
    )
    
    add_delete_cat_button.grid(
        row=row,
        column=4,
        padx=5
    )
    
    # Store everything for this category
    category_widgets[category_id] = {

        "name": category_name,

        "checked": checked,

        "selected_activity": selected_activity,

        "dropdown": dropdown
    }
