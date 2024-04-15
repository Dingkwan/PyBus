import PySimpleGUI as sg
import pandas as pd

# All the stuff inside your window.
layout = [  [sg.Text("Some bus route", font = ('Arial', 30))],
            [sg.Button("Bus 1", size = (50,1), font = ("Arial", 20))],
            [sg.Button("Bus 2", size = (50,1), font = ("Arial", 20))],
            [sg.Button("Bus 3", size = (50,1), font = ("Arial", 20))],
            [sg.Button("Bus 4", size = (50,1), font = ("Arial", 20))],
            [sg.Button("Bus 5", size = (50,1), font = ("Arial", 20))],
            [sg.Text("Or you can choose a GPS data file to analyse:", font = ("Arial", 15)), sg.Button("File...", font = ("Arial",15))],
            [sg.Text(key = "open", font = ("Arial", 13))]
        ]

# Create the Window
window = sg.Window('PyBus', layout, element_justification = 'centre', size = (600, 500))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    
    if event == "File...":
        file = sg.PopupGetFile("Select file", no_window = True)
        window["open"].update(file)
        print(file)

window.close()