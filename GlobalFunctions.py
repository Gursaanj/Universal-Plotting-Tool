# This Script will be used for Global Functions in the Aggregate Master Reader
# A List of Global functions to be used outside of the respective windows

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
########################################################################################################################