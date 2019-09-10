#Import Necessary Packages
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.image as mpimg
from PIL import Image
import pandas as pd
import tkinter as tk
from tkinter import filedialog
#Import Corresponding Scripts
import GlobalFunctions as gf
########################################################################################################################
## List of constant variables to be called 

# String used to detect which column is used in plotting
input_substring = "m_"

# String used to detect which column is used for sorting labels in plots
sort_substring = "s_"

# A list of marker styles to be used for scatter plotting - To make Better
marker_styles = ['s', 'o', 'o','x', '+', 'v', '^', '<', '>', '.', 'd']

# A list of colour styles to be used for scatter plotting - get best styling over time
color_styles = ["midnightblue", "red", "darkgreen", "darkviolet", "magenta", "darkorange", "royalblue", "maroon", "limegreen", "violet", "orange", "slateblue", "tomato", "lime", "palevioletred", "gold"]

# A bool that determines if the plot should contain a trend line **Simple Linear regression only at the moment. 
AddTrendLine = False

# WaterMark Image for the plot backgrounds
watermark = Image.open(r"C:\Users\Gursaanj\Documents\Coop\CBDV\Master Sheet Reader\CBDV_logo_linear_45.png")
watermark.thumbnail((512,512), Image.ANTIALIAS)

########################################################################################################################

# Get the list of all open Windows, so it can be destroyed by the end of the script run 
ListOfWindows = []

# Create Main Window with given title and background
root= tk.Tk()
root.title("CBDV Data analysis tool")

StartCanvas = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
StartCanvas.pack()

#Set Logo icon
root.iconbitmap(r"C:\Users\Gursaanj\Documents\Coop\CBDV\Master Sheet Reader\CBDV_logo_linear_45.ico")

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
    
## Decide whether or not to plot in 3d or 2d
def ChoosePlotType():

    root.title("Plot Choices")
    
    # Get a list of all column labels that are deemed plottable 
    PlotOptions = gf.GetUsuableColumns(data.columns, input_substring)
    
    # Get a list of all column labels used to marginalize (legend) the data
    SortOptions = gf.GetUsuableColumns(data.columns, sort_substring)
    
    
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
    PlotButton = tk.Button(root, text="Make Plots", command= lambda: MakePlots3D(XPlots.get(), YPlots.get(), ZPlots.get(), SortingLabels.get(), CustomTitle.get("1.0", "end-1c")))
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
## The Actual Plotting Methods

## Creates 2d plots with the give specs   
def MakePlots2D(xplot, yplot, sorting, CustomTitle):
    
    fig = plt.figure(figsize=[20,15])
    
    ## Ensure the plot is maximised right away - Might need to remove when it comes to making tool external
#    plt.switch_backend('QT5Agg')
#    mng = plt.get_current_fig_manager()
#    mng.window.showMaximized()
    
    #mng.full_screen_toggle()


    for i in range(len(gf.GetLabels(data[gf.GetActualLabel(sorting, sort_substring)]))):
        plt.scatter(gf.GetArrays(data[gf.GetActualLabel(xplot, input_substring)], data[gf.GetActualLabel(sorting, sort_substring)], i), gf.GetArrays(data[gf.GetActualLabel(yplot, input_substring)], data[gf.GetActualLabel(sorting, sort_substring)], i), marker = marker_styles[i%len(marker_styles)] , s=30, c= color_styles[i%len(color_styles)], label = gf.GetLabels(data[gf.GetActualLabel(sorting, sort_substring)])[i])
    
    #Plot Additional Data as well
    for j in range(len(AddData)):
        if j == 0:
            plt.scatter(AddData[j][gf.GetActualLabel(xplot, input_substring)], AddData[j][gf.GetActualLabel(yplot, input_substring)], c='lightgray', s=30, label = "Additional Data")
        else:
            plt.scatter(AddData[j][gf.GetActualLabel(xplot, input_substring)], AddData[j][gf.GetActualLabel(yplot, input_substring)], c='lightgray', s=30, label = None)
    
    if CustomTitle  != "":
        plt.title(CustomTitle, fontsize=20)
    else:
        plt.title("{} as a function of {}".format(yplot, xplot), fontsize=20)
    
    #Add trendLine,Should convert this to be an opptional effect that works with a button press
    if AddTrendLine: 
        # get the xplot values that dont have null values (cant be understood for polyfit)
        xplot_trendline = data[data[gf.GetActualLabel(xplot, input_substring)].notnull() & data[gf.GetActualLabel(yplot, input_substring)].notnull()][gf.GetActualLabel(xplot, input_substring)]
        # get the yplot values that dont have null values (cant be understood for polyfit)
        yplot_trendline = data[data[gf.GetActualLabel(xplot, input_substring)].notnull() & data[gf.GetActualLabel(yplot, input_substring)].notnull()][gf.GetActualLabel(yplot, input_substring)]
        # Create linear regression model 
        pfit2D = np.polyfit(xplot_trendline, yplot_trendline, 1)
        # Get coefficients for linear regression model
        pfit2D_plot = np.poly1d(pfit2D)
        # Plot trend line based on made linear regression
        plt.plot(xplot_trendline, pfit2D_plot(xplot_trendline), "r--", label="BestFit (Linear)")
        
    ## Decide location and fontsize of labels and legend based on how many entries there are in the legend
    if len(gf.GetLabels(data[gf.GetActualLabel(sorting, sort_substring)])) > 5: #5 is Arbritrary, any better approach??
        plt.legend(loc="center left", bbox_to_anchor=(1,0.5), fontsize="small", title = "{}".format(sorting))
    else:
        plt.legend(loc="best", fontsize="large", title="{}".format(sorting))
    
    # Place Labels onto the the main figure
    plt.xlabel(xplot, fontsize=18)
    plt.ylabel(yplot, fontsize=18)
    
    #Get the assigned figure width and height in pixels
    figure_width = int(fig.get_figwidth()*fig.dpi)
    figure_height = int(fig.get_figheight()*fig.dpi)
    
    #Get the assigned axes width and height in pixes
    axes_width = fig.get_axes()[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted()).width*fig.dpi
    axes_height = fig.get_axes()[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted()).height*fig.dpi    
    
    #The offset for the watermark, for it to be place in the centre of the plot, regardless of the plot data
    x_offset = (axes_width/2) + ((figure_width-axes_width)/2) - watermark.size[0]/2
    y_offset = (axes_height/3) + ((figure_height-axes_height)/3)- watermark.size[1]/2
    
    #Plot the image with appropriate layering and desired alpha channel
    plt.figimage(watermark, x_offset, y_offset, zorder=1, alpha = 0.05)
    
    plt.show()    
    
    destroywindows()
    
## Makes 3D plots with given specs 
def MakePlots3D(xplot, yplot, zplot, sorting, CustomTitle):
       
   figure = plt.figure(figsize=[20,15])

   ## Ensure the plot is maximised right away - Might need to remove when it comes to making tool external
   #    plt.switch_backend('QT5Agg')
   #    mng = plt.get_current_fig_manager()
   #    mng.window.showMaximized()

   # mng.full_screen_toggle()

   ax = figure.add_subplot(111, projection="3d")
   for i in range(len(gf.GetLabels(data[gf.GetActualLabel(sorting, sort_substring)]))):
       ax.scatter(gf.GetArrays(data[gf.GetActualLabel(xplot, input_substring)], data[gf.GetActualLabel(sorting, sort_substring)], i), gf.GetArrays(data[gf.GetActualLabel(yplot, input_substring)], data[gf.GetActualLabel(sorting, sort_substring)], i), gf.GetArrays(data[gf.GetActualLabel(zplot, input_substring)], data[gf.GetActualLabel(sorting, sort_substring)], i),  marker = marker_styles[i%len(marker_styles)] , s=30, c= color_styles[i%len(color_styles)], label = gf.GetLabels(data[gf.GetActualLabel(sorting, sort_substring)])[i])

       # Plot Additional Data as well
   for j in range(len(AddData)):
       if j == 0:
           ax.scatter(AddData[j][gf.GetActualLabel(xplot, input_substring)], AddData[j][gf.GetActualLabel(yplot, input_substring)], AddData[j][gf.GetActualLabel(zplot, input_substring)], c='lightgray', s=30, label="Additional Data")
       else:
           plt.scatter(AddData[j][gf.GetActualLabel(xplot, input_substring)],AddData[j][gf.GetActualLabel(yplot, input_substring)], AddData[j][gf.GetActualLabel(zplot, input_substring)], c='lightgray', s=30, label=None)

   if CustomTitle  != "":
        ax.set_title(CustomTitle, fontsize=20)
   else:
        ax.set_title("{} as a function of {} and {}".format(zplot, xplot, yplot), fontsize=20)
    
    ## Decide location and fontsize of labels and legend based on how many entries there are in the legend
   if len(gf.GetLabels(data[gf.GetActualLabel(sorting, sort_substring)])) > 5: #5 is Arbritrary, any better approach??
       ax.legend(loc="center left", bbox_to_anchor=(1,0.5), fontsize="small", title = "{}".format(sorting))
   else:
       ax.legend(loc="best", fontsize="large", title="{}".format(sorting))
        
   ax.set_xlabel(xplot, fontsize=18)
   ax.set_ylabel(yplot, fontsize=18)
   ax.set_zlabel(zplot, fontsize=18)

   plt.show()
    
   destroywindows()
########################################################################################################################

## To be called when the application needs to be closed and all plotting has been completed

# Destroy all windows attached to the run
def destroywindows():
    for i in range(len(ListOfWindows)):
        ListOfWindows[i].destroy()
    

## Main buttons to import CSV
browseButton_CSV = tk.Button(text="      Import CSV File     ", command=getCSV, bg='green', fg='white', font=('verdana', 12, 'bold'))
AdditionalData_CSV = tk.Button(text=" Add Additional Datasets ", command=AdditionalData, bg="green", fg="white", font = ("verdana", 12, "bold"))

StartCanvas.create_window(150, 150, window=browseButton_CSV)

root.mainloop()