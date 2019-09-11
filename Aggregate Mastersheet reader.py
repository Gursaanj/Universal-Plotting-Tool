#Import Necessary Packages
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
#Import Corresponding Scripts
import GlobalFunctions as gf
import PlottingSetup as ps
########################################################################################################################
# Get the list of all open Windows, so it can be destroyed by the end of the script run
ListOfWindows = []

# Create Main Window with given title and background
root= tk.Tk()
root.title("CBDV Data analysis tool")

StartCanvas = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
StartCanvas.pack()

#Set Logo icon
root.iconbitmap("CBDV_logo_linear_45.ico")

#Create list to hold Additional Data if need be
AddData = []

ListOfWindows.append(root)
########################################################################################################################
# Starter Methods to be called before choosing plot styles

## Choose the CSV file wanted
def getCSV():
    import_file_path = filedialog.askopenfilename()

    # Import data
    global data
    data = pd.read_csv (import_file_path, engine="python", skiprows=2)

    StartCanvas.create_window(150, 220, window=AdditionalData_CSV)

    ChoosePlotType()

## Store Additional datasets if needed
def AdditionalData():
    import_file_path = filedialog.askopenfilename()

    data = pd.read_csv(import_file_path, engine="python", skiprows=2)

    AddData.append(data)

## Main buttons to import CSV
browseButton_CSV = tk.Button(text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('verdana', 12, 'bold'))
AdditionalData_CSV = tk.Button(text=" Add Additional Datasets ", command=AdditionalData, bg="green", fg="white", font = ("verdana", 12, "bold"))

StartCanvas.create_window(150, 150, window=browseButton_CSV)

## Decide whether or not to plot in 3d or 2d
def ChoosePlotType():

    root.title("Plot Choices")

    # Get a list of all column labels that are deemed plottable
    PlotOptions = gf.GetUsuableColumns(data.columns, gf.input_substring)

    # Get a list of all column labels used to marginalize (legend) the data
    SortOptions = gf.GetUsuableColumns(data.columns, gf.sort_substring)


    plot2d = tk.Button(root, text = "2D Plot", command = lambda: ChoosePlotTitles2D(PlotOptions, SortOptions))
    plot2d.pack()

    plot3d = tk.Button(root, text = "3D Plot", command = lambda:ChoosePlotTitles3D(PlotOptions, SortOptions))
    plot3d.pack()

########################################################################################################################
## Allow users to decide what data to plot and in what manner

## for the needed plot
def ChoosePlotTitles2D(PlotOptions, SortOptions):

    #Reset current window for new inputs
    for widget in root.winfo_children():
        widget.destroy()

    #Reset Canvas
    PlotChoices2DCanvas = tk.Canvas(root, width = 450, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    PlotChoices2DCanvas.pack()

    #Create a list of widgets so that it can be used to on canvas windows
    Window2D = []

    root.title("Plot Choices")

    #Create Label for Xaxis plot options
    XPlotLabel = tk.Label(root, text = "X axis Plot", width = 10)
    XPlotLabel.pack()
    Window2D.append(XPlotLabel)

    #Create Options for Xaxis in plots - Dropdown
    XPlots = tk.StringVar(root)
    XPlots.set(PlotOptions[0])

    w = tk.OptionMenu(root, XPlots, *PlotOptions)
    w.pack()
    Window2D.append(w)

    # Create Label for Yaxis plot options
    YPlotLabel = tk.Label(root, text = "Y axis Plot", width = 10)
    YPlotLabel.pack()
    Window2D.append(YPlotLabel)

    # Create Options for Yaxis in plots - Dropdown
    YPlots = tk.StringVar(root)
    YPlots.set(PlotOptions[0])

    v = tk.OptionMenu(root, YPlots, *PlotOptions)
    v.pack()
    Window2D.append(v)

    # Create label for sorting options
    SortByLabel = tk.Label(root, text = "Sort By", width = 8)
    SortByLabel.pack()
    Window2D.append(SortByLabel)


    # Let users decide how they which to sort through the aggregate data (decide what to use to determine legend in plots)
    SortingLabels = tk.StringVar(root)
    SortingLabels.set(SortOptions[0])

    sortList = tk.OptionMenu(root, SortingLabels, *SortOptions)
    sortList.pack()
    Window2D.append(sortList)

    # Label fo Custom Title
    CustomTitleLabel = tk.Label(root, text = "Custom Title", width = 10)
    CustomTitleLabel.pack()
    Window2D.append(CustomTitleLabel)

    # Let users decide custom title, if not filled, using "Yplots as a function of Xplots"
    CustomTitle = tk.Text(root, height = 1, width = 50)
    CustomTitle.pack()
    Window2D.append(CustomTitle)

    #Make Plots with given data
    PlotButton = tk.Button(root, text="Make Plots", command= lambda: ps.MakePlots2D(data, AddData, XPlots.get(), YPlots.get(), SortingLabels.get(), CustomTitle.get("1.0", "end-1c")))
    PlotButton.pack()
    Window2D.append(PlotButton)

    # Create a list of x axs coordinates for all widgets in the window
    Canvas2D_xcord = [50,270,50,270,50,270,225,225,225]

    # Create a list of x axs coordinates for all widgets in the window
    Canvas2D_ycord = [40,40,80,80,150,150, 220,245,290]

    #Place everything on Canvas
    for i in range(len(Window2D)):
        PlotChoices2DCanvas.create_window(Canvas2D_xcord[i], Canvas2D_ycord[i], window = Window2D[i])

# Title choice for 3D plots
def ChoosePlotTitles3D(PlotOptions, SortOptions):

     #Reset current window for new inputs
    for widget in root.winfo_children():
        widget.destroy()

    # Reset Canvas
    PlotChoices3DCanvas = tk.Canvas(root, width=450, height=300, bg='lightsteelblue2', relief='raised')
    PlotChoices3DCanvas.pack()

    # Create a list of widgets so that it can be used to on canvas windows
    Window3D = []

    root.title("Plot Choices")

    # Create Label for Xaxis plot options
    XPlotLabel = tk.Label(root, text="X axis Plot", width=10)
    XPlotLabel.pack()
    Window3D.append(XPlotLabel)

    #Create Options for Xaxis in plots - Dropdown
    XPlots = tk.StringVar(root)
    XPlots.set(PlotOptions[0])

    w = tk.OptionMenu(root, XPlots, *PlotOptions)
    w.pack()
    Window3D.append(w)

    # Create Label for Yaxis plot options
    YPlotLabel = tk.Label(root, text="Y axis Plot", width=10)
    YPlotLabel.pack()
    Window3D.append(YPlotLabel)

    #Create Options for Yaxis in plots - Dropdown
    YPlots = tk.StringVar(root)
    YPlots.set(PlotOptions[0])

    v = tk.OptionMenu(root, YPlots, *PlotOptions)
    v.pack()
    Window3D.append(v)

    # Create Label for Zaxis plot options
    ZPlotLabel = tk.Label(root, text="Z axis Plot", width=10)
    ZPlotLabel.pack()
    Window3D.append(ZPlotLabel)

    #Create Options for Zaxis in plots - Dropdown
    ZPlots = tk.StringVar(root)
    ZPlots.set(PlotOptions[0])

    q = tk.OptionMenu(root, ZPlots, *PlotOptions)
    q.pack()
    Window3D.append(q)

    # Create label for sorting options
    SortByLabel = tk.Label(root, text="Sort By", width=8)
    SortByLabel.pack()
    Window3D.append(SortByLabel)

    # Let users decide how they which to sort through the aggregate data (decide what to use to determine legend in plots)
    SortingLabels = tk.StringVar(root)
    SortingLabels.set(SortOptions[0])

    sortList = tk.OptionMenu(root, SortingLabels, *SortOptions)
    sortList.pack()
    Window3D.append(sortList)

    # Label fo Custom Title
    CustomTitleLabel = tk.Label(root, text = "Custom Title", width = 10)
    CustomTitleLabel.pack()
    Window3D.append(CustomTitleLabel)

    # Let users decide custom title, if not filled, using "Zplots as a function of Yplots and Xplots"
    CustomTitle = tk.Text(root, heigh = 1, width = 50)
    CustomTitle.pack()
    Window3D.append(CustomTitle)

    #Make Plots with given data
    PlotButton = tk.Button(root, text="Make Plots", command= lambda: ps.MakePlots3D(data, AddData, XPlots.get(), YPlots.get(), ZPlots.get(), SortingLabels.get(), CustomTitle.get("1.0", "end-1c")))
    PlotButton.pack()
    Window3D.append(PlotButton)

    # Create a list of x axs coordinates for all widgets in the window
    Canvas3D_xcord = [50, 270, 50, 270, 50, 270, 50, 270, 225, 225, 225]

    # Create a list of x axs coordinates for all widgets in the window
    Canvas3D_ycord = [40, 40, 80, 80, 120, 120, 180, 180, 220, 245, 290]

    # Arrange 3D Canvas
    for i in range(len(Window3D)):
        PlotChoices3DCanvas.create_window(Canvas3D_xcord[i], Canvas3D_ycord[i], window = Window3D[i])
########################################################################################################################

root.mainloop()
