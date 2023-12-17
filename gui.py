import os
import random
import subprocess
import threading
import time
import traceback

import PySimpleGUI as sg

from exceptions import InternalException

script_running = False
colors = ["orange", "lightblue", "yellow", "purple"]


def run_script_in_thread(values, window):
    """
    Run the script in a separate thread.

    Parameters:
    values (dict): The values from the GUI.
    window (sg.Window): The PySimpleGUI window.
    """
    global script_running
    script_running = True
    url = values["-URL-"]
    folder = values["-FOLDER-"]
    headless = values["-HEADLESS-"]
    command = ["python", "summary.py", "-u", url]
    if folder:
        command = ["python", "summary.py", "-u", url, "-f", folder]
    if headless:
        command.append("--headless")
    try:
        subprocess.run(command, check=True)
        window.write_event_value("UpdateStatus", "File created successfully!")
        os.system("afplay /System/Library/Sounds/Glass.aiff -v 8")
        print("File created successfully!")
    except InternalException as err:
        window.write_event_value("UpdateStatus", "An error occurred")
        os.system("afplay /System/Library/Sounds/Sosumi.aiff -v 8")
        os.system("afplay /System/Library/Sounds/Sosumi.aiff -v 8")
        print(f"Internal Exception: {err}")
    except Exception as err:
        window.write_event_value(
            "UpdateStatus",
            "An error occurred",
        )
        os.system("afplay /System/Library/Sounds/Sosumi.aiff -v 8")
        os.system("afplay /System/Library/Sounds/Sosumi.aiff -v 8")
        print(
            f"An unexpected error occurred: {err}. Traceback:\n{traceback.format_exc()}"
        )
    script_running = False


def run_script(values, window):
    """
    Run the script and update the status message.

    Parameters:
    values (dict): The values from the GUI.
    window (sg.Window): The PySimpleGUI window.
    """
    global script_running
    status_message = "Running... Please wait..."
    threading.Thread(
        target=run_script_in_thread, args=(values, window), daemon=True
    ).start()
    while script_running:
        color = random.choice(colors)
        for i in range(len(status_message) + 1):
            window["-STATUS-"].update(status_message[:i], text_color=color)
            window.refresh()
            time.sleep(0.2)


def view_file():
    """
    Open a file and display its contents in a popup window.
    """
    file = sg.popup_get_file("Open File", no_window=True)
    if file is not None:
        with open(file, "r") as f:
            content = f.read()
        sg.popup_scrolled(content, title="File content")


def main():
    """
    The main function of the GUI.
    It creates the window, handles events, and runs the script.
    """
    sg.theme("SystemDefaultForReal")
    layout = [
        [
            sg.Text("         URL"),
            sg.Input(key="-URL-"),
            sg.Button("Clear URL"),
        ],
        [
            sg.Text("      Folder"),
            sg.Input(default_text="./sumarios", key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Column(
                [
                    [
                        sg.Checkbox("Headless", key="-HEADLESS-", default=True),
                        sg.Text("(enable to hide browser)"),
                    ]
                ],
                justification="center",
            )
        ],
        [
            sg.Column(
                [
                    [
                        sg.Button("Run Script", bind_return_key=True),
                        sg.Button("View File"),
                    ]
                ],
                justification="center",
            )
        ],
        [
            sg.Text(" ", expand_x=True),
            sg.Text(
                "",
                key="-STATUS-",
                size=(50, 1),
                justification="center",
                text_color="orange",
            ),
            sg.Text(" ", expand_x=True),
        ],
    ]

    # Get screen size
    screen_width, screen_height = sg.Window.get_screen_size()

    # Define window size
    window_width = 800
    window_height = 200

    # Calculate position for bottom right
    position = (screen_width - window_width - 50, screen_height - window_height - 50)
    window = sg.Window(
        "IAFD Scraper GUI",
        layout,
        # size=(800, 200),
        font=("Helvetica", 18),
        icon="app_icon.png",
        location=position,
    )

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Run Script":
            run_script(values, window)
        elif event == "View File":
            view_file()
        elif event == "Clear URL":
            window["-URL-"].update("")
        elif event == "UpdateStatus":
            window["-STATUS-"].update(
                values["UpdateStatus"],
                text_color="red"
                if "An error occurred" in values["UpdateStatus"]
                else "green",
            )
            window.refresh()

    window.close()


if __name__ == "__main__":
    main()
