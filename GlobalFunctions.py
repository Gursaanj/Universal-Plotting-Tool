# This Script will be used for Global Functions in the Aggregate Master Reader

# A List of Global variables/Functions  to be used outside of the respective windows

########################################################################################################################
## List of Global variables to be called

# String used to detect which column is used in plotting
inputSubstring = "m_"

# String used to detect which column is used for sorting labels in plots
sortSubstring = "s_"

# A list of marker styles to be used for scatter plotting - To make Better
markerStyles = ['s', 'o', 'o', 'x', '+', 'v', '^', '<', '>', '.', 'd']

# A list of possible marker sizes, for users to scale the size of the images as the please
markerSizes = [30, 40, 50, 60, 70, 80, 90, 100]

# A list of colour styles to be used for scatter plotting - get best styling over time
colorStyles = ["midnightblue", "red", "darkgreen", "darkviolet", "magenta", "darkorange", "royalblue", "maroon", "limegreen", "violet", "orange", "slateblue", "tomato", "lime", "palevioletred", "gold"]

########################################################################################################################
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

# Destroy all windows attached to the run
def destroywindows(listOfWindows):
    for i in range(len(listOfWindows)):
        listOfWindows[i].destroy()

########################################################################################################################
