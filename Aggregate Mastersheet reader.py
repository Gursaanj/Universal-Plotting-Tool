#Import Necessary Packages
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import tkinter as tk
from tkinter import filedialog
#########################
## List of constant variables to be called 

# String used to distinctify which column is used for plotting
input_substring = "m_"

# String used to distinctify which column is used for sorting labels in plots
sort_substring = "s_"

# A list of marker styles to be used for scatter plotting - To make Better
marker_styles = ['s', 'o', 'o','x', '+', 'v', '^', '<', '>', '.', 'd']

# A list of colour styles to be used for scatter plotting - get best styling over time
color_styles = ["midnightblue", "red", "darkgreen", "darkviolet", "magenta", "darkorange", "royalblue", "maroon", "limegreen", "violet", "orange", "slateblue", "tomato", "lime", "palevioletred", "gold"]

# A bool that determines if the plot should contain a trend line **Simple Linear regression only at the moment. 
AddTrendLine = True
#########################

# Get the list of all open Windows, so it can be destroyed by the end of the script run 
ListOfWindows = []

# Create Main Window with given title and background
root= tk.Tk()
root.title("CBDV Data analysis tool")

StartCanvas = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
StartCanvas.pack()

#Set Logo icon
root.iconbitmap(r"C:\Users\Gursaanj\Documents\Coop\CBDV\Master Sheet Reader\CBDV_logo_linear_45.ico")

ListOfWindows.append(root)

### Creating a box of global Functions that can be used by any window

# Gets all unique titles in a column and store it in its own list
def GetLabels(StringArray):
    LabelList = []
    for i in range(len(StringArray)):
        if StringArray[i] not in LabelList:
            LabelList.append(StringArray[i])
    return LabelList
    
# Get the array that corresponds with the wanted label
def GetArrays(array1, conditionarray, WhichCondition):
    y = array1.where(conditionarray == GetLabels(conditionarray)[WhichCondition])
    return y

# Finds Columns headers that are meant to be used for plotting and displays them for user
def GetUsuableColumns(array, substring):
    ListOfTitles = []
    for i in range(len(array)):
        if substring in array[i]:
            Label = array[i][len(substring):]
            ListOfTitles.append(Label)
    return ListOfTitles

# Get the column label of data from the actual columns of labelist
def GetActualLabel(truncated_label, sub_string):
    y = sub_string + truncated_label
    return y


#Create list to hold Additional Data if need be
AddData = []

###############################################################################
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
    
    print(len(AddData))
    
## Decide whether or not to plot in 3d or 2d
def ChoosePlotType():
    
    root.title("Plot Choices")
    
    # Get a list of all column labels that are deemed plottable 
    PlotOptions = GetUsuableColumns(data.columns, input_substring)
    
    # Get a list of all column labels used to marginalize (legend) the data
    SortOptions = GetUsuableColumns(data.columns, sort_substring)
    
    
    plot2d = tk.Button(root, text = "2D Plot", command = lambda: ChoosePlotTitles2D(PlotOptions, SortOptions))
    plot2d.pack()
    
    plot3d = tk.Button(root, text = "3D Plot", command = lambda:ChoosePlotTitles3D(PlotOptions, SortOptions))
    plot3d.pack()

    
## Allow users to choose which columns of data to use
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
    PlotButton = tk.Button(root, text="Make Plots", command= lambda: MakePlots2D(XPlots.get(), YPlots.get(), SortingLabels.get(), CustomTitle.get("1.0", "end-1c")))
    PlotButton.pack()
    Window2D.append(PlotButton)
    
    # Create a list of x axs coordinates for all widgets in the window
    Canvas2D_xcord = [50,270,50,270,50,270,225,225,225]
    
    # Create a list of x axs coordinates for all widgets in the window
    Canvas2D_ycord = [40,40,80,80,150,150, 220,245,290]
    
    #Place everything on Canvas
#    PlotChoices2DCanvas.create_window(50, 40, window=XPlotLabel)
#    PlotChoices2DCanvas.create_window(270,40, window=w)
#    PlotChoices2DCanvas.create_window(50, 80, window=YPlotLabel)
#    PlotChoices2DCanvas.create_window(270, 80, window=v)
#    PlotChoices2DCanvas.create_window(50, 150, window = SortByLabel)
#    PlotChoices2DCanvas.create_window(270, 150, window = sortList)
#    PlotChoices2DCanvas.create_window(225,220,window=CustomTitleLabel)
#    PlotChoices2DCanvas.create_window(225, 260, window = CustomTitle)
#    PlotChoices2DCanvas.create_window(225, 290, window = PlotButton)
    
    for i in range(len(Window2D)):
        PlotChoices2DCanvas.create_window(Canvas2D_xcord[i], Canvas2D_ycord[i], window = Window2D[i])
    
# Title choice for 3D plots 
def ChoosePlotTitles3D(PlotOptions, SortOptions):
    
     #Reset current window for new inputs
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("Plot Choices")
    
    #Create Options for Xaxis in plots - Dropdown
    XPlots = tk.StringVar(root)
    XPlots.set(PlotOptions[0])
    
    w = tk.OptionMenu(root, XPlots, *PlotOptions)
    w.pack()
    
    #Create Options for Yaxis in plots - Dropdown 
    YPlots = tk.StringVar(root)
    YPlots.set(PlotOptions[0])
    
    v = tk.OptionMenu(root, YPlots, *PlotOptions)
    v.pack()
    
    #Create Options for Zaxis in plots - Dropdown
    ZPlots = tk.StringVar(root)
    ZPlots.set(PlotOptions[0])
    
    q = tk.OptionMenu(root, ZPlots, *PlotOptions)
    q.pack()
    
    # Label fo Custom Title
    CustomTitleLabel = tk.Label(root, text = "Custom Title", width = 10)
    CustomTitleLabel.pack()
    
    # Let users decide custom title, if not filled, using "Zplots as a function of Yplots and Xplots"
    CustomTitle = tk.Text(root, heigh = 1, width = 50)
    CustomTitle.pack()
    
    # Let users decide how they which to sort through the aggregate data (decide what to use to determine legend in plots)
    SortingLabels = tk.StringVar(root)
    SortingLabels.set(SortOptions[0])
    
    sortList = tk.OptionMenu(root, SortingLabels, *SortOptions)
    sortList.pack()
    
    #Make Plots with given data
    PlotButton = tk.Button(root, text="Make Plots", command= lambda: MakePlots3D(XPlots.get(), YPlots.get(), ZPlots.get(), SortingLabels.get(), CustomTitle.get("1.0", "end-1c")))
    PlotButton.pack()
    
## Creates 2d plots with the give specs   
def MakePlots2D(xplot, yplot, sorting, CustomTitle):
           
    plt.figure(figsize=[18,14])
    for i in range(len(GetLabels(data[GetActualLabel(sorting, sort_substring)]))):
        plt.scatter(GetArrays(data[GetActualLabel(xplot, input_substring)], data[GetActualLabel(sorting, sort_substring)], i), GetArrays(data[GetActualLabel(yplot, input_substring)], data[GetActualLabel(sorting, sort_substring)], i), marker = marker_styles[i%len(marker_styles)] , s=20, c= color_styles[i%len(color_styles)], label = GetLabels(data[GetActualLabel(sorting, sort_substring)])[i])
    
    #Plot Additional Data as well
    for j in range(len(AddData)):
        if j == 0:
            plt.scatter(AddData[j][GetActualLabel(xplot, input_substring)], AddData[j][GetActualLabel(yplot, input_substring)], c='lightgray', s=20, label = "Additional Data")
        else:
            plt.scatter(AddData[j][GetActualLabel(xplot, input_substring)], AddData[j][GetActualLabel(yplot, input_substring)], c='lightgray', s=20, label = None)
    
    if CustomTitle  != "":
        plt.title(CustomTitle, fontsize=20)
    else:
        plt.title("{} as a function of {}".format(yplot, xplot), fontsize=20)

    #Add trendLine,Should convert this to be an opptional effect that works with a button press
    if AddTrendLine: 
        # get the xplot values that dont have null values (cant be understood for polyfit)
        xplot_trendline = data[data[GetActualLabel(xplot, input_substring)].notnull() & data[GetActualLabel(yplot, input_substring)].notnull()][GetActualLabel(xplot, input_substring)]
        # get the yplot values that dont have null values (cant be understood for polyfit)
        yplot_trendline = data[data[GetActualLabel(xplot, input_substring)].notnull() & data[GetActualLabel(yplot, input_substring)].notnull()][GetActualLabel(yplot, input_substring)]   
        # Create linear regression model 
        pfit2D = np.polyfit(xplot_trendline, yplot_trendline, 1)
        # Get coefficients for linear regression model
        pfit2D_plot = np.poly1d(pfit2D)
        # Plot trendline based on made linear regression
        plt.plot(xplot_trendline, pfit2D_plot(xplot_trendline), "r--", label="BestFit (Linear)")
        
    ## Decide location and fontsize of labels and legend based on how many entries there are in the legend
    if len(GetLabels(data[GetActualLabel(sorting, sort_substring)])) > 5: #5 is Arbritrary, any better approach??
        plt.legend(loc="center left", bbox_to_anchor=(1,0.5), fontsize="small", title = "{}".format(sorting))
    else:
        plt.legend(loc="best", fontsize="large", title="{}".format(sorting))
    
    
    plt.xlabel(xplot, fontsize=18)
    plt.ylabel(yplot, fontsize=18)


    plt.show()    
    DestroyWindows()
    
## Makes 3D plots with given specs 
def MakePlots3D(xplot, yplot, zplot, sorting, CustomTitle):
       
   figure = plt.figure(figsize=[30,20])
   ax = figure.add_subplot(111, projection="3d")
   for i in range(len(GetLabels(data[GetActualLabel(sorting, sort_substring)]))):
       ax.scatter(GetArrays(data[GetActualLabel(xplot, input_substring)], data[GetActualLabel(sorting, sort_substring)], i), GetArrays(data[GetActualLabel(yplot, input_substring)], data[GetActualLabel(sorting, sort_substring)], i), GetArrays(data[GetActualLabel(zplot, input_substring)], data[GetActualLabel(sorting, sort_substring)], i),  marker = marker_styles[i%len(marker_styles)] , s=12, label = GetLabels(data[GetActualLabel(sorting, sort_substring)])[i])
   
   if CustomTitle  != "":
        ax.set_title(CustomTitle, fontsize=20)
   else:
        ax.set_title("{} as a function of {} and {}".format(zplot, xplot, yplot), fontsize=20)
    
    ## Decide location and fontsize of labels and legend based on how many entries there are in the legend
   if len(GetLabels(data[GetActualLabel(sorting, sort_substring)])) > 5: #5 is Arbritrary, any better approach??
       ax.legend(loc="center left", bbox_to_anchor=(1,0.5), fontsize="small", title = "{}".format(sorting))
   else:
       ax.legend(loc="best", fontsize="large", title="{}".format(sorting))
        
   ax.set_xlabel(xplot, fontsize=18)
   ax.set_ylabel(yplot, fontsize=18)
   ax.set_zlabel(zplot, fontsize=18)

   plt.show()
    
   DestroyWindows()



## Destroy all windows attached to the run  
def DestroyWindows():
    for i in range(len(ListOfWindows)):
        ListOfWindows[i].destroy()
    

## Main buttons to import CSV
browseButton_CSV = tk.Button(text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('verdana', 12, 'bold'))
AdditionalData_CSV = tk.Button(text=" Add Additional Datasets ", command=AdditionalData, bg="green", fg="white", font = ("verdana", 12, "bold"))

StartCanvas.create_window(150, 150, window=browseButton_CSV)


root.mainloop()


####### Tool that might be used - Destroy Current Widgets
## This is so that data would not get overiden 
#for widget in root.winfo_children():
#    widget.destroy()