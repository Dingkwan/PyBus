import PySimpleGUI as sg
import pandas as pd
import route_map
import webbrowser
import os
import create_video
import gpxpy
from shutil import rmtree

def cleanCache():
    if os.path.exists("__pycache__"):
        rmtree("__pycache__")
    if os.path.exists("SV_panoramas"):
        rmtree("SV_panoramas")
    if os.path.exists("route_map.html"):
        os.remove("route_map.html")

# Adjust this function if the data structure changes
def dealTXTData(filePath):
    data = pd.read_csv(filePath)
    data.columns = ["datetime","latitude", "longitude"]
    # data.columns = ["id", "datetime","longitude", "latitude"]
    # data = data[["datetime","latitude", "longitude"]]
    return data

def dealGPXData(filePath):
    with open(filePath) as f:
        gpx = gpxpy.parse(f)
    # Convert to a dataframe one point at a time.
    points = []
    for segment in gpx.tracks[0].segments:
        for p in segment.points:
            points.append({
                "datetime": p.time.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": p.latitude,
                "longitude": p.longitude,
            })
    GPXdata = pd.DataFrame.from_records(points)
    return GPXdata



cleanCache()

# All the stuff inside your window.
layout = [  [sg.Text("Some bus route", font = ('Arial', 30))],
            [sg.Button("Bus 1", size = (50,1), font = ("Arial", 20), key = "Bus 1")],
            [sg.Button("Bus 2", size = (50,1), font = ("Arial", 20), key = "Bus 2")],
            [sg.Button("Bus 3", size = (50,1), font = ("Arial", 20), key = "Bus 3")],
            [sg.Button("Bus 4", size = (50,1), font = ("Arial", 20), key = "Bus 4")],
            [sg.Button("Bus 5", size = (50,1), font = ("Arial", 20), key = "Bus 5")],
            [sg.Text("Or you can choose a GPS data file to analyse:", font = ("Arial", 15)), sg.Button("File...", font = ("Arial",15))],
            [sg.Text(key = "open", font = ("Arial", 13))],
            [sg.Button("Show route map", key = "routemap", size = (25,1), font = ("Arial", 15), visible = False), sg.Button("Show route video", key = "routevideo", size = (25,1), font = ("Arial", 15), visible = False)],
            [sg.HorizontalSeparator()],
            [sg.Text("Some bus stops are under maintenance:")]
        ]



# --------------------------Create the Window----------------------------

window = sg.Window('PyBus', layout, element_justification = 'centre', size = (600, 500))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED:
        break
    
    # 点击file按钮之后的动作
    if event == "File...":
        filePath = sg.PopupGetFile("Select file", no_window = True) #无需展示弹窗

        #开始处理文件
        # data = dealTXTData(filePath)
        data = dealGPXData(filePath)
        print(data)

        # 显示剩余功能
        window["open"].update(filePath)
        window["routemap"].update(visible = True)
        window["routevideo"].update(visible = True)
    
    if event == "routemap":
        cleanCache()
        sg.popup_no_titlebar("Createing route map. Please wait. (Another window will pop up at the end of the running time)", font = ("Arial", 15), auto_close = True, auto_close_duration = 5)
        route_map.routeMap(data)
        print("---------Process finished---------")
        htmlPath = "file://"+os.getcwd()+"/" + "route_map.html"
        webbrowser.open(htmlPath)
        sg.popup_no_titlebar("Finished!", font = ("Arial", 15))
    
    if event == "routevideo":
        cleanCache()
        saveVideoFolder = sg.popup_get_folder("Please select the directory where the video will be saved:", font = ("Arial", 15), title = "Save route video")
        sg.popup_no_titlebar("Creating video. Please wait. (Another window will pop up at the end of the running time)", font = ("Arial", 15), auto_close = True, auto_close_duration = 5)
        create_video.create_video(saveVideoFolder, data)
        sg.popup_no_titlebar("Finished!", font = ("Arial", 15))
    
    # ---------------上半部分按钮行为---------------

    if event == "Bus 1":
        bus1GPXPath = "2024-04-12 PM 12_21_41.gpx"
        data = dealGPXData(bus1GPXPath)
        route_map.routeMap(data)
        htmlPath = "file://"+os.getcwd()+"/" + "route_map.html"
        webbrowser.open(htmlPath)


window.close()