import PySimpleGUI as sg
import subprocess
import os
import time
import threading
import random

script_running = False
colors = ["orange", "lightblue", "yellow", "purple"]


def run_script_in_thread(values, window):
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
        window.write_event_value("UpdateStatus", f"File created successfully!")
    except Exception:
        window.write_event_value("UpdateStatus", f"An error occurred")
    script_running = False


def run_script(values, window):
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
    file = sg.popup_get_file("Open File", no_window=True)
    if file is not None:
        with open(file, "r") as f:
            content = f.read()
        sg.popup_scrolled(content, title="File content")


def main():
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
                        sg.Checkbox("Headless", key="-HEADLESS-"),
                        sg.Text("(enable to hide browser)"),
                    ]
                ],
                justification="center",
            )
        ],
        [
            sg.Column(
                [[sg.Button("Run Script", bind_return_key=True), sg.Button("View File")]],
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

    window = sg.Window(
        "IAFD Scraper GUI",
        layout,
        size=(800, 200),
        font=("Helvetica", 18),
        icon="app_icon.icns",
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
            if values["UpdateStatus"] == "An error occurred":
                window["-STATUS-"].update(values["UpdateStatus"], text_color="red")
            else:
                window["-STATUS-"].update(values["UpdateStatus"], text_color="green")
            window.refresh()

    window.close()


if __name__ == "__main__":
    main()
