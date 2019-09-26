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
listOfWindows = []

# Create Main Window with given title and background
root= tk.Tk()
root.title("CBDV Data analysis tool")

# Create starting Canvas interface
startCanvas = tk.Canvas(root, width = 300, height = 300, bg ='lightsteelblue2', relief ='raised')
startCanvas.pack()

# Set Logo icon
root.iconbitmap("CBDV_logo_linear_45.ico")

# Create list to hold Additional Data if need be
additionalData = []

listOfWindows.append(root)
########################################################################################################################
# Starter Methods to be called before choosing plot styles

## Choose the CSV file wanted
def GetPrimaryCSV():
    importedFilePath = filedialog.askopenfilename()
    global data # Make Data accessible outside of Function
    data = pd.read_csv (importedFilePath, engine="python", skiprows=2)
    startCanvas.create_window(150, 220, window=additionalCSVButton)

    ChoosePlotType()

## Store Additional datasets if needed
def GetAdditionalCSV():
    importedFilePath = filedialog.askopenfilename()
    data = pd.read_csv(importedFilePath, engine="python", skiprows=2)
    additionalData.append(data)

## Main buttons to import CSV
primaryCSVButton = tk.Button(text="      Import CSV File     ", command=GetPrimaryCSV, bg='green', fg='white', font=('verdana', 12, 'bold'))
additionalCSVButton = tk.Button(text=" Add Additional Datasets ", command=GetAdditionalCSV, bg="green", fg="white", font = ("verdana", 12, "bold"))

startCanvas.create_window(150, 150, window=primaryCSVButton)

## Decide whether or not to plot in 3d or 2d
def ChoosePlotType():

    root.title("Plot Choices")

    # Get a list of all column labels that are deemed plottable
    plotOptions = gf.GetUsuableColumns(data.columns, gf.inputSubstring)

    # Get a list of all column labels used to marginalize (legend) the data
    sortOptions = gf.GetUsuableColumns(data.columns, gf.sortSubstring)

    # Direct to 2D Plot Settings Page
    plotButton2D = tk.Button(root, text = "2D Plot", command = lambda: HandCraftPlot2D(plotOptions, sortOptions))
    plotButton2D.pack()

    # Direct to 3D Plot Settings page
    plotButton3D = tk.Button(root, text = "3D Plot", command = lambda:HandCraftPlo3D(plotOptions, sortOptions))
    plotButton3D.pack()

    # A radio Button system to let the user to choose either between making a 2D or 3D plot
    # The variable assigned via the variable
    typeOfPlot = tk.StringVar()

    # Selection for 2D Plot
    radioButton2DPlot = tk.Radiobutton(root, text = "2D Plot", value = ps.PlotDimensions.TwoDimensions, variable = typeOfPlot)
    radioButton2DPlot.pack()
    # Selection for 3D Plot
    radioButton3DPlot = tk.Radiobutton(root, text = "3D Plot", value = ps.PlotDimensions.ThreeDimensions, variable = typeOfPlot)
    radioButton3DPlot.pack()

    # A button to let Users move onto the next window and start specifying the plot details
    plotButton = tk.Button(root, text = "Make Plot", command = lambda : HandCraftPlot(plotOptions,sortOptions,typeOfPlot.get()))
    plotButton.pack()

########################################################################################################################
## Allow users to decide what data to plot and in what manner

def HandCraftPlot(plottingOptions, sortingOptions, plottingStyle):

    # Reset current window for new inputs
    for widget in root.winfo_children():
        widget.destroy()

    # Reset Canvas
    handCraftPlotCanvas = tk.Canvas(root, width = 450, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    handCraftPlotCanvas.pack()

    # Rebase the title of the window
    root.title("Plot Choices")

    # Create a list of widgets for easier placement on the Canvas
    windowOfWidgets = []

    # Create Label for Xaxis plot options
    xAxisPlotLabel = tk.Label(root, text="X axis Plot", width=10)
    xAxisPlotLabel.pack()
    windowOfWidgets.append(xAxisPlotLabel)

    # Create Options for Xaxis in plots - Dropdown
    xAxisPlotData = tk.StringVar(root)
    xAxisPlotData.set(plottingOptions[0])

    xAxisPlotDataOptions = tk.OptionMenu(root, xAxisPlotData, *plottingOptions)
    xAxisPlotDataOptions.pack()
    windowOfWidgets.append(xAxisPlotDataOptions)

    # Create Label for Yaxis plot options
    yAxisPlotLabel = tk.Label(root, text="Y axis Plot", width=10)
    yAxisPlotLabel.pack()
    windowOfWidgets.append(yAxisPlotLabel)

    # Create Options for Yaxis in plots - Dropdown
    yAxisPlotData = tk.StringVar(root)
    yAxisPlotData.set(plottingOptions[0])

    yAxisPlotDataOptions = tk.OptionMenu(root, yAxisPlotData, *plottingOptions)
    yAxisPlotDataOptions.pack()
    windowOfWidgets.append(yAxisPlotDataOptions)

    # Create Label for Zaxis plot options
    zAxisPlotLabel = tk.Label(root, text="Z axis Plot", width=10)
    zAxisPlotLabel.pack()
    windowOfWidgets.append(zAxisPlotLabel)

    # Create Options for Zaxis in plots - Dropdown
    zAxisPlotData = tk.StringVar(root)
    zAxisPlotData.set(plottingOptions[0])

    zAxisPlotDataOptions = tk.OptionMenu(root, zAxisPlotData, *plottingOptions)
    zAxisPlotDataOptions.pack()
    windowOfWidgets.append(zAxisPlotDataOptions)

    # Create label for changing Marker Size
    markerSizeLabel = tk.Label(root, text="Marker Size", width=8)
    markerSizeLabel.pack()
    windowOfWidgets.append(markerSizeLabel)

    # Let users decide the size of the markers used in plotting
    markerSizes = tk.IntVar(root)
    markerSizes.set(gf.markerSizes[0])

    markerSizeOptions = tk.OptionMenu(root, markerSizes, *gf.markerSizes)
    markerSizeOptions.pack()
    windowOfWidgets.append(markerSizeOptions)

    # Create label for sorting options
    sortByLabel = tk.Label(root, text="Sort By", width=8)
    sortByLabel.pack()
    windowOfWidgets.append(sortByLabel)

    # Let users decide how they which to sort through the aggregate data (decide what to use to determine legend in plots)
    sortingByLabels = tk.StringVar(root)
    sortingByLabels.set(sortingOptions[0])

    sortingByLabelOptions = tk.OptionMenu(root, sortingByLabels, *sortingOptions)
    sortingByLabelOptions.pack()
    windowOfWidgets.append(sortingByLabelOptions)

    # Label fo Custom Title
    customTitleLabel = tk.Label(root, text="Custom Title", width=10)
    customTitleLabel.pack()
    windowOfWidgets.append(customTitleLabel)

    # Let users decide custom title, if not filled, using "Zplots as a function of Yplots and Xplots"
    customTitle = tk.Text(root, heigh=1, width=50)
    customTitle.pack()
    windowOfWidgets.append(customTitle)

    # Let users decide if they would like to display a legend on the plot : Set by PlottingSetup.py
    addLegendOption = tk.BooleanVar()
    addLegendOption.set(ps.initialLegendCheck)
    addLegendCheckbox = tk.Checkbutton(root, text="Add Legend", variable=addLegendOption)
    addLegendCheckbox.pack()
    windowOfWidgets.append(addLegendCheckbox)

    # Let Users decide if they would like a trendline in their plot via a CheckBox
    addTrendLineOption = tk.BooleanVar()
    addTrendLineOption.set(ps.initialTrendLineCheck)
    addTrendLineCheckbox = tk.Checkbutton(root, text = "Add Trendline", variable = addTrendLineOption)
    addTrendLineCheckbox.pack()
    windowOfWidgets.append(addTrendLineCheckbox)

    # Let users decide if they would like to display a TrendLine on the plot : Set by PlottingSetup.py

    # Make Plots with given data
    plotGraphButton = tk.Button(root, text="Make Plots",
                                command=lambda: ps.MakePlots3D(data, additionalData, xAxisPlotData.get(),
                                                               yAxisPlotData.get(), zAxisPlotData.get(),
                                                               markerSizes.get(), sortingByLabels.get(),
                                                               customTitle.get("1.0", "end-1c"), addLegendOption.get()))
    plotGraphButton.pack()
    windowOfWidgets.append(plotGraphButton)

    # End Plotting Process
    quitApplicationButton = tk.Button(root, text="End Process", command=lambda: gf.destroywindows(listOfWindows))
    quitApplicationButton.pack()
    windowOfWidgets.append(quitApplicationButton)

    # Create a list of x axs coordinates for all widgets in the window
    plottingCanvasXCoordinates = [50, 270, 50, 270, 50, 270, 50, 270, 50, 270, 225, 225, 335, 115, 225, 320]

    # Create a list of x axs coordinates for all widgets in the window
    plottingCanvasYCoordinates = [40, 40, 80, 80, 120, 120, 160, 160, 205, 205, 235, 265, 235, 235, 290, 290]

    # Arrange 3D Canvas
    for i in range(len(windowOfWidgets)):
        handCraftPlotCanvas.create_window(plottingCanvasXCoordinates[i], plottingCanvasYCoordinates[i], window=windowOfWidgets[i])

#Decide Specifications for plotting in 2D
def HandCraftPlot2D(plottingOptions, sortingOptions):

    #Reset current window for new inputs
    for widget in root.winfo_children():
        widget.destroy()

    #Reset Canvas
    plotChoices2DCanvas = tk.Canvas(root, width = 450, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    plotChoices2DCanvas.pack()

    #Create a list of widgets so that it can be used to on canvas windows
    window2D = []

    root.title("Plot Choices")

    #Create Label for Xaxis plot options
    xAxisPlotLabel = tk.Label(root, text = "X axis Plot", width = 10)
    xAxisPlotLabel.pack()
    window2D.append(xAxisPlotLabel)

    #Create Options for Xaxis in plots - Dropdown
    xAxisPlotData = tk.StringVar(root)
    xAxisPlotData.set(plottingOptions[0])

    xAxisPlotDataOptions = tk.OptionMenu(root, xAxisPlotData, *plottingOptions)
    xAxisPlotDataOptions.pack()
    window2D.append(xAxisPlotDataOptions)

    # Create Label for Yaxis plot options
    yAxisPlotLabel = tk.Label(root, text = "Y axis Plot", width = 10)
    yAxisPlotLabel.pack()
    window2D.append(yAxisPlotLabel)

    # Create Options for Yaxis in plots - Dropdown
    yAxisPlotData = tk.StringVar(root)
    yAxisPlotData.set(plottingOptions[0])

    yAxisPlotDataOptions = tk.OptionMenu(root, yAxisPlotData, *plottingOptions)
    yAxisPlotDataOptions.pack()
    window2D.append(yAxisPlotDataOptions)

    # Create label for changing Marker Size
    markerSizeLabel = tk.Label(root, text = "Marker Size", width = 8)
    markerSizeLabel.pack()
    window2D.append(markerSizeLabel)

    # Let users decide the size of the markers used in plotting
    markerSizes = tk.IntVar(root)
    markerSizes.set(gf.markerSizes[0])

    markerSizeOptions = tk.OptionMenu(root, markerSizes, *gf.markerSizes)
    markerSizeOptions.pack()
    window2D.append(markerSizeOptions)

    # Create label for sorting options
    sortByLabel = tk.Label(root, text = "Sort By", width = 8)
    sortByLabel.pack()
    window2D.append(sortByLabel)

    # Let users decide how they which to sort through the aggregate data (decide what to use to determine legend in plots)
    sortingByLabels = tk.StringVar(root)
    sortingByLabels.set(sortingOptions[0])

    sortingByOptions = tk.OptionMenu(root, sortingByLabels, *sortingOptions)
    sortingByOptions.pack()
    window2D.append(sortingByOptions)

    # Label fo Custom Title
    customTitleLabel = tk.Label(root, text = "Custom Title", width = 10)
    customTitleLabel.pack()
    window2D.append(customTitleLabel)

    # Let users decide custom title, if not filled, using "Yplots as a function of Xplots"
    customTitle = tk.Text(root, height = 1, width = 50)
    customTitle.pack()
    window2D.append(customTitle)

    # Let users decide if they would like to display a legend on the plot : Set by PlottingSetup.py
    addLegendOption = tk.BooleanVar()
    addLegendOption.set(ps.initialLegendCheck)
    addLegendCheckbox = tk.Checkbutton(root, text = "Add Legend", variable = addLegendOption)
    addLegendCheckbox.pack()
    window2D.append(addLegendCheckbox)

    # Let Users decide if they would like a trendline in their plot via a CheckBox
    addTrendLineOption = tk.BooleanVar()
    addTrendLineOption.set(ps.initialTrendLineCheck)
    addTrendLineCheckbox = tk.Checkbutton(root, text = "Add Trendline", variable = addTrendLineOption)
    addTrendLineCheckbox.pack()
    window2D.append(addTrendLineCheckbox)

    # Make Plots with given data
    plotGraphButton = tk.Button(root, text="Make Plots", command = lambda: ps.MakePlots2D(data, additionalData, xAxisPlotData.get(), yAxisPlotData.get(), markerSizes.get(), sortingByLabels.get(), customTitle.get("1.0", "end-1c"), addLegendOption.get(), addTrendLineOption.get()))
    plotGraphButton.pack()
    window2D.append(plotGraphButton)

    # End Plotting Process
    quitApplicationButton = tk.Button(root, text= "End Process", command = lambda: gf.destroywindows(listOfWindows))
    quitApplicationButton.pack()
    window2D.append(quitApplicationButton)

    # Create a list of x axs coordinates for all widgets in the window
    canvas2DXCoordinates = [50 ,270 ,50 ,270 ,50 ,270 ,50 ,270 ,225 ,225 ,335 ,60 ,225 ,320]

    # Create a list of x axs coordinates for all widgets in the window
    canvas2DYCoordinates = [40 ,40 ,80 ,80 ,120 ,120 ,170 ,170 ,220 ,255 ,220 ,220 ,290 ,290]

    #Place everything on Canvas
    for i in range(len(window2D)):
        plotChoices2DCanvas.create_window(canvas2DXCoordinates[i], canvas2DYCoordinates[i], window = window2D[i])

#Decide Specifications for plotting in 3D
def HandCraftPlo3D(PlotOptions, SortOptions):

     #Reset current window for new inputs
    for widget in root.winfo_children():
        widget.destroy()

    # Reset Canvas
    plotChoices3DCanvas = tk.Canvas(root, width=450, height=300, bg='lightsteelblue2', relief='raised')
    plotChoices3DCanvas.pack()

    # Create a list of widgets so that it can be used to on canvas windows
    window3D = []

    root.title("Plot Choices")

    # Create Label for Xaxis plot options
    xAxisPlotLabel = tk.Label(root, text="X axis Plot", width=10)
    xAxisPlotLabel.pack()
    window3D.append(xAxisPlotLabel)

    #Create Options for Xaxis in plots - Dropdown
    xAxisPlotData = tk.StringVar(root)
    xAxisPlotData.set(PlotOptions[0])

    xAxisPlotDataOptions = tk.OptionMenu(root, xAxisPlotData, *PlotOptions)
    xAxisPlotDataOptions.pack()
    window3D.append(xAxisPlotDataOptions)

    # Create Label for Yaxis plot options
    yAxisPlotLabel = tk.Label(root, text="Y axis Plot", width=10)
    yAxisPlotLabel.pack()
    window3D.append(yAxisPlotLabel)

    #Create Options for Yaxis in plots - Dropdown
    yAxisPlotData = tk.StringVar(root)
    yAxisPlotData.set(PlotOptions[0])

    yAxisPlotDataOptions = tk.OptionMenu(root, yAxisPlotData, *PlotOptions)
    yAxisPlotDataOptions.pack()
    window3D.append(yAxisPlotDataOptions)

    # Create Label for Zaxis plot options
    zAxisPlotLabel = tk.Label(root, text="Z axis Plot", width=10)
    zAxisPlotLabel.pack()
    window3D.append(zAxisPlotLabel)

    #Create Options for Zaxis in plots - Dropdown
    zAxisPlotData = tk.StringVar(root)
    zAxisPlotData.set(PlotOptions[0])

    zAxisPlotDataOptions = tk.OptionMenu(root, zAxisPlotData, *PlotOptions)
    zAxisPlotDataOptions.pack()
    window3D.append(zAxisPlotDataOptions)

    # Create label for changing Marker Size
    markerSizeLabel = tk.Label(root, text="Marker Size", width=8)
    markerSizeLabel.pack()
    window3D.append(markerSizeLabel)

    # Let users decide the size of the markers used in plotting
    markerSizes = tk.IntVar(root)
    markerSizes.set(gf.markerSizes[0])

    markerSizeOptions = tk.OptionMenu(root, markerSizes, *gf.markerSizes)
    markerSizeOptions.pack()
    window3D.append(markerSizeOptions)

    # Create label for sorting options
    sortByLabel = tk.Label(root, text="Sort By", width=8)
    sortByLabel.pack()
    window3D.append(sortByLabel)

    # Let users decide how they which to sort through the aggregate data (decide what to use to determine legend in plots)
    sortingByLabels = tk.StringVar(root)
    sortingByLabels.set(SortOptions[0])

    sortingByLabelOptions = tk.OptionMenu(root, sortingByLabels, *SortOptions)
    sortingByLabelOptions.pack()
    window3D.append(sortingByLabelOptions)

    # Label fo Custom Title
    customTitleLabel = tk.Label(root, text = "Custom Title", width = 10)
    customTitleLabel.pack()
    window3D.append(customTitleLabel)

    # Let users decide custom title, if not filled, using "Zplots as a function of Yplots and Xplots"
    customTitle = tk.Text(root, heigh = 1, width = 50)
    customTitle.pack()
    window3D.append(customTitle)

     # Let users decide if they would like to display a legend on the plot : Set by PlottingSetup.py
    addLegendOption = tk.BooleanVar()
    addLegendOption.set(ps.initialLegendCheck)
    addLegendCheckbox = tk.Checkbutton(root, text="Add Legend", variable=addLegendOption)
    addLegendCheckbox.pack()
    window3D.append(addLegendCheckbox)

    # Make Plots with given data
    plotGraphButton = tk.Button(root, text="Make Plots", command = lambda: ps.MakePlots3D(data, additionalData, xAxisPlotData.get(), yAxisPlotData.get(), zAxisPlotData.get(), markerSizes.get(), sortingByLabels.get(), customTitle.get("1.0", "end-1c"), addLegendOption.get()))
    plotGraphButton.pack()
    window3D.append(plotGraphButton)

    # End Plotting Process
    quitApplicationButton = tk.Button(root, text= "End Process", command = lambda: gf.destroywindows(listOfWindows))
    quitApplicationButton.pack()
    window3D.append(quitApplicationButton)

    # Create a list of x axs coordinates for all widgets in the window
    canvas3DXCoordinates = [50, 270, 50, 270, 50, 270, 50, 270, 50, 270, 225, 225, 335, 225, 320]

    # Create a list of x axs coordinates for all widgets in the window
    canvas3DYCoordinates = [40, 40, 80, 80, 120, 120, 160, 160, 205, 205, 235, 265, 235, 290, 290]

    # Arrange 3D Canvas
    for i in range(len(window3D)):
        plotChoices3DCanvas.create_window(canvas3DXCoordinates[i], canvas3DYCoordinates[i], window = window3D[i])
########################################################################################################################

root.mainloop()
