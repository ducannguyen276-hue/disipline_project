from data_management import create_table, close_database
from front_end import create_gui
# pull

create_table()

root = create_gui()


def close_app():
    close_database()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)

root.mainloop()