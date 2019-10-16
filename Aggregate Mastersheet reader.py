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

    # A radio Button system to let the user to choose either between making a 2D or 3D plot
    # The variable assigned via the variable
    typeOfPlot = tk.StringVar()

    # Selection for 2D Plot
    radioButton2DPlot = tk.Radiobutton(root, text = "2D Plot", value = ps.PlotDimensions.TwoDimensions.name, variable = typeOfPlot)
    radioButton2DPlot.pack()
    radioButton2DPlot.select()

    # Selection for 3D Plot
    radioButton3DPlot = tk.Radiobutton(root, text = "3D Plot", value = ps.PlotDimensions.ThreeDimensions.name, variable = typeOfPlot)
    radioButton3DPlot.pack()

    # A button to let Users move onto the next window and start specifying the plot details
    plotButton = tk.Button(root, text = "Make Plot", command = lambda : HandCraftPlot(plotOptions,sortOptions,typeOfPlot.get()))
    plotButton.pack()

########################################################################################################################
## Allow users to decide what data to plot and in what manner

def HandCraftPlot(plottingOptions, sortingOptions, plottingStyle):

    #region Initialise GUI
    # Reset current window for new inputs
    for widget in root.winfo_children():
        widget.destroy()

    # Reset Canvas
    handCraftPlotCanvas = tk.Canvas(root, width = 450, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    handCraftPlotCanvas.pack()

    # Rebase the title of the window
    root.title("Plot Customization")

    # Create a list of widgets for easier placement on the Canvas
    windowOfWidgets = []

    # maintain a list of data taken from the GUI widgets and pass them to the appropriate plots
    widgetData = []
    #endregion

    # region Plotting Data for X axis
    # Create Label for Xaxis plot options
    xAxisPlotLabel = tk.Label(root, text="X axis Plot", width=10)
    xAxisPlotLabel.pack()
    windowOfWidgets.append(xAxisPlotLabel)

    # Create Options for Xaxis in plots - Dropdown
    xAxisPlotData = tk.StringVar(root)
    xAxisPlotData.set(plottingOptions[0])
    widgetData.append(xAxisPlotData)

    xAxisPlotDataOptions = tk.OptionMenu(root, xAxisPlotData, *plottingOptions)
    xAxisPlotDataOptions.pack()
    windowOfWidgets.append(xAxisPlotDataOptions)
    # endregion

    # region Plotting Data for Y axis
    # Create Label for Yaxis plot options
    yAxisPlotLabel = tk.Label(root, text="Y axis Plot", width=10)
    yAxisPlotLabel.pack()
    windowOfWidgets.append(yAxisPlotLabel)

    # Create Options for Yaxis in plots - Dropdown
    yAxisPlotData = tk.StringVar(root)
    yAxisPlotData.set(plottingOptions[0])
    widgetData.append(yAxisPlotData)

    yAxisPlotDataOptions = tk.OptionMenu(root, yAxisPlotData, *plottingOptions)
    yAxisPlotDataOptions.pack()
    windowOfWidgets.append(yAxisPlotDataOptions)
    # endregion

    # region Plotting Data for Z axis
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

    if plottingStyle == ps.PlotDimensions.ThreeDimensions.name:
        widgetData.append(zAxisPlotData)
    else:
        zAxisPlotDataOptions.configure(state = "disabled")
    # endregion

    # region Marker Size choices
    # Create label for changing Marker Size
    markerSizeLabel = tk.Label(root, text="Marker Size", width=8)
    markerSizeLabel.pack()
    windowOfWidgets.append(markerSizeLabel)

    # Let users decide the size of the markers used in plotting
    markerSizes = tk.IntVar(root)
    markerSizes.set(gf.markerSizes[0])
    widgetData.append(markerSizes)

    markerSizeOptions = tk.OptionMenu(root, markerSizes, *gf.markerSizes)
    markerSizeOptions.pack()
    windowOfWidgets.append(markerSizeOptions)
    # endregion

    # region Sorting Options
    # Create label for sorting options
    sortByLabel = tk.Label(root, text="Sort By", width=8)
    sortByLabel.pack()
    windowOfWidgets.append(sortByLabel)

    # Let users decide how they which to sort through the aggregate data (decide what to use to determine legend in plots)
    sortingByLabels = tk.StringVar(root)
    sortingByLabels.set(sortingOptions[0])
    widgetData.append(sortingByLabels)

    sortingByLabelOptions = tk.OptionMenu(root, sortingByLabels, *sortingOptions)
    sortingByLabelOptions.pack()
    windowOfWidgets.append(sortingByLabelOptions)
    # endregion

    # region Custom Title Input
    # Label fo Custom Title
    customTitleLabel = tk.Label(root, text="Custom Title", width=10)
    customTitleLabel.pack()
    windowOfWidgets.append(customTitleLabel)

    # Let users decide custom title, if not filled, using "Zplots as a function of Yplots and Xplots"
    customTitle = tk.Entry(root, width = 50)
    customTitle.pack()
    customTitle.focus() # Sets the cursor to initially be on the Enrtry text box
    windowOfWidgets.append(customTitle)
    widgetData.append(customTitle)
    # endregion

    # region Adding Legend Option
    # Let users decide if they would like to display a legend on the plot : Set by PlottingSetup.py
    addLegendOption = tk.BooleanVar()
    addLegendOption.set(ps.initialLegendCheck)
    widgetData.append(addLegendOption)

    addLegendCheckbox = tk.Checkbutton(root, text="Add Legend", variable=addLegendOption)
    addLegendCheckbox.pack()
    windowOfWidgets.append(addLegendCheckbox)
    # endregion

    # region Adding Trendline Option
    # Let Users decide if they would like a trendline in their plot via a CheckBox
    addTrendLineOption = tk.BooleanVar()
    addTrendLineOption.set(ps.initialTrendLineCheck)

    addTrendLineCheckbox = tk.Checkbutton(root, text = "Add Trendline", variable = addTrendLineOption)
    addTrendLineCheckbox.pack()
    windowOfWidgets.append(addTrendLineCheckbox)

    if plottingStyle == ps.PlotDimensions.ThreeDimensions.name:
        addTrendLineCheckbox.configure(state = "disabled")
    else:
        widgetData.append(addLegendOption)
    # endregion

    # region Adding Documentation Option
    # Allow users to decide to create a document to correspond with the plot
    addDocumentationOption = tk.BooleanVar()
    addDocumentationOption.set(ps.initialDocumentationCheck)
    widgetData.append(addDocumentationOption)

    addDocumentationCheckbox = tk.Checkbutton(root, text = "Create Documentation", variable = addDocumentationOption)
    addDocumentationCheckbox.pack()
    windowOfWidgets.append(addDocumentationCheckbox)
    # endregion

    # region Plotting Button
    # Make Plots with given data
    plotGraphButton = tk.Button(root, text="Make Plot", command = lambda: ps.MakePlot(plottingStyle, data, additionalData, *widgetData))
    plotGraphButton.pack()
    windowOfWidgets.append(plotGraphButton)
    # endregion

    # region End Process Button
    # End Plotting Process
    quitApplicationButton = tk.Button(root, text="End Process", command = lambda: gf.DestroyWindows(listOfWindows))
    quitApplicationButton.pack()
    windowOfWidgets.append(quitApplicationButton)
    # endregion

    # region Plotting GUI Coordinates
    # Create a list of x axs coordinates for all widgets in the window
    plottingCanvasXCoordinates = [50, 270, 50, 270, 50, 270, 50, 270, 50, 270, 225, 225, 335, 115, 80, 225, 320]

    # Create a list of x axs coordinates for all widgets in the window
    plottingCanvasYCoordinates = [40, 40, 80, 80, 120, 120, 160, 160, 205, 205, 235, 265, 235, 235, 290, 290, 290]

    # Arrange 3D Canvas
    for i in range(len(windowOfWidgets)):
        handCraftPlotCanvas.create_window(plottingCanvasXCoordinates[i], plottingCanvasYCoordinates[i], window=windowOfWidgets[i])
    # endregion
########################################################################################################################

root.mainloop()