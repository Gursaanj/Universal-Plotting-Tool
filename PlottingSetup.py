#Script to handle all the plotting for both 2D and 3D Plots

#Import All Necessary Packages
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
#Import Corresponding Scripts
import GlobalFunctions as gf

########################################################################################################################
# WaterMark Image for the plot backgrounds
watermark = Image.open("CBDV_logo_linear_45.png")
watermark.thumbnail((512,512), Image.ANTIALIAS)


# Setting the Booleans related to the outlook of the plotting
initialLegendCheck = True
initialTrendLineCheck = False


########################################################################################################################
## Creates 2d plots with the give specs
#PARAMS: CSV Datasheet, Additional CSV Datasheet, Xaxis, Yaxis, Marker Size, List of Legend Labels, Custom Title, Check for Legend, Check for Trendline
def MakePlots2D(data, AddData, xplot, yplot, msize, sorting, CustomTitle, legendCheck, trendLineCheck):
    fig = plt.figure(figsize=[20, 15])

    ## Ensure the plot is maximised right away - Might need to remove when it comes to making tool external
    #    plt.switch_backend('QT5Agg')
    #    mng = plt.get_current_fig_manager()
    #    mng.window.showMaximized()

    # mng.full_screen_toggle()

    for i in range(len(gf.GetLabels(data[gf.GetActualLabel(sorting, gf.sortSubstring)]))):
        plt.scatter(gf.GetArrays(data[gf.GetActualLabel(xplot, gf.inputSubstring)],
                                 data[gf.GetActualLabel(sorting, gf.sortSubstring)], i),
                    gf.GetArrays(data[gf.GetActualLabel(yplot, gf.inputSubstring)],
                                 data[gf.GetActualLabel(sorting, gf.sortSubstring)], i),
                    marker=gf.markerStyles[i % len(gf.markerStyles)], s=msize, c=gf.colorStyles[i % len(gf.colorStyles)],
                    label=gf.GetLabels(data[gf.GetActualLabel(sorting, gf.sortSubstring)])[i])

    # Plot Additional Data as well
    for j in range(len(AddData)):
        plt.scatter(AddData[j][gf.GetActualLabel(xplot, gf.inputSubstring)],
                    AddData[j][gf.GetActualLabel(yplot, gf.inputSubstring)], c='lightgray', s=msize,
                    label="Additional Data" if j == 0 else None)

    plt.title(CustomTitle if CustomTitle != "" else "{} as a function of {}".format(yplot, xplot), fontsize = 20)

    # Add trendLine,Should convert this to be an opptional effect that works with a button press
    if trendLineCheck:
        # get the xplot values that dont have null values (cant be understood for polyfit)
        trendlineXaxis = data[data[gf.GetActualLabel(xplot, gf.inputSubstring)].notnull() & data[
            gf.GetActualLabel(yplot, gf.inputSubstring)].notnull()][gf.GetActualLabel(xplot, gf.inputSubstring)]
        # get the yplot values that dont have null values (cant be understood for polyfit)
        trendlineYaxis = data[data[gf.GetActualLabel(xplot, gf.inputSubstring)].notnull() & data[
            gf.GetActualLabel(yplot, gf.inputSubstring)].notnull()][gf.GetActualLabel(yplot, gf.inputSubstring)]
        # Create linear regression model
        linearFit = np.polyfit(trendlineXaxis, trendlineYaxis, 1)
        # Get coefficients for linear regression model
        linearFitCoefficients = np.poly1d(linearFit)
        # Plot trend line based on made linear regression
        plt.plot(trendlineXaxis, linearFitCoefficients(trendlineXaxis), "r--", label="BestFit (Linear)")

    ## Decide location and fontsize of labels and legend based on how many entries there are in the legend
    if legendCheck:
        if len(gf.GetLabels(data[gf.GetActualLabel(sorting, gf.sortSubstring)])) > 5:  # 5 is Arbritrary, any better approach??
            plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small", title="{}".format(sorting))
        else:
            plt.legend(loc="best", fontsize="large", title="{}".format(sorting))

    # Place Labels onto the the main figure
    plt.xlabel(xplot, fontsize=18)
    plt.ylabel(yplot, fontsize=18)

    # Get the assigned figure width and height in pixels
    figureWidth = int(fig.get_figwidth() * fig.dpi)
    figureHeight = int(fig.get_figheight() * fig.dpi)

    # Get the assigned axes width and height in pixes
    axesWidth = fig.get_axes()[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted()).width * fig.dpi
    axesHeight = fig.get_axes()[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted()).height * fig.dpi

    # The offset for the watermark, for it to be place in the centre of the plot, regardless of the plot data
    xAxisOffset = (axesWidth / 2) + ((figureWidth - axesWidth) / 2) - watermark.size[0] / 2
    yAxisOffset = (axesHeight / 3) + ((figureHeight - axesHeight) / 3) - watermark.size[1] / 2

    # Plot the image with appropriate layering and desired alpha channel
    plt.figimage(watermark, xAxisOffset, yAxisOffset, zorder=1, alpha=0.05)

    plt.show()

## Makes 3D plots with given specs
#PARAMS: CSV Datasheet, Additional CSV Datasheet, Xaxis, Yaxis, Zazis, Marker Size, List of Legend Labels, Custom Title, Check for Legend
def MakePlots3D(data, AddData, xplot, yplot, zplot, msize, sorting, CustomTitle, legendCheck):
    figure = plt.figure(figsize=[20, 15])

    ## Ensure the plot is maximised right away - Might need to remove when it comes to making tool external
    #    plt.switch_backend('QT5Agg')
    #    mng = plt.get_current_fig_manager()
    #    mng.window.showMaximized()

    # mng.full_screen_toggle()

    ax = figure.add_subplot(111, projection="3d")
    for i in range(len(gf.GetLabels(data[gf.GetActualLabel(sorting, gf.sortSubstring)]))):
        ax.scatter(gf.GetArrays(data[gf.GetActualLabel(xplot, gf.inputSubstring)],
                                data[gf.GetActualLabel(sorting, gf.sortSubstring)], i),
                   gf.GetArrays(data[gf.GetActualLabel(yplot, gf.inputSubstring)],
                                data[gf.GetActualLabel(sorting, gf.sortSubstring)], i),
                   gf.GetArrays(data[gf.GetActualLabel(zplot, gf.inputSubstring)],
                                data[gf.GetActualLabel(sorting, gf.sortSubstring)], i),
                   marker=gf.markerStyles[i % len(gf.markerStyles)], s=msize, c=gf.colorStyles[i % len(gf.colorStyles)],
                   label=gf.GetLabels(data[gf.GetActualLabel(sorting, gf.sortSubstring)])[i])

    # Plot Additional Data as well
    for j in range(len(AddData)):
         ax.scatter(AddData[j][gf.GetActualLabel(xplot, gf.inputSubstring)],
                    AddData[j][gf.GetActualLabel(yplot, gf.inputSubstring)],
                    AddData[j][gf.GetActualLabel(zplot, gf.inputSubstring)], c='lightgray', s=msize,
                    label= "Additional Data" if j == 0 else None)

    ax.set_title(CustomTitle if CustomTitle != "" else "{} as a function of {} and {}".format(zplot, xplot, yplot), fontsize = 20)

    ## Decide location and fontsize of labels and legend based on how many entries there are in the legend
    if initialLegendCheck:
        if len(gf.GetLabels(data[gf.GetActualLabel(sorting, gf.sortSubstring)])) > 5:  # 5 is Arbitrary, any better approach??
            ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small", title="{}".format(sorting))
        else:
            ax.legend(loc="best", fontsize="large", title="{}".format(sorting))

    ax.set_xlabel(xplot, fontsize=18)
    ax.set_ylabel(yplot, fontsize=18)
    ax.set_zlabel(zplot, fontsize=18)

    plt.show()

########################################################################################################################