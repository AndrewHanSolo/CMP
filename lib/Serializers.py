from General import *
import xlsxwriter


def writeTrackData(trackFile, workbook, worksheetName):
	worksheet = workbook.add_worksheet(worksheetName + " All")

	colindex = 0
	rowindex = 0
	#label track ids
	worksheet.write(rowindex, colindex, 'id')
	for trackCount in range(len(trackFile.tracks)):
		rowindex += 1
		worksheet.write(rowindex, colindex, trackCount)
	#list each propertyName value by col
	for propertyName, na in sorted(trackFile.d.items()):
		colindex += 1
		rowindex = 0
		worksheet.write(rowindex, colindex, propertyName)
		propertyValues = trackFile.d[propertyName]
		#write all values of propertyNames to rows
		for value in propertyValues:
			rowindex += 1
			worksheet.write(rowindex, colindex, value)

	return

#helper function for writing current instance of data to exel file
#@param workbookName	Name of the excel file to write to
#@param worksheetName	Name of the new sheet to be added to the file
def writeMetaData(trackFile, workbook, worksheetName):

	#WRITE AVERAGES METADATA
	worksheet = workbook.add_worksheet(worksheetName + " Meta")
	worksheet.write(0, 0, "propertyName")
	worksheet.write(0, 3, "wAvg")
	worksheet.write(0, 4, "stdDev")
	worksheet.write(0, 6, "nAvg")
	worksheet.write(0, 7, "stdDev")
	worksheet.write(0, 8, "stdErr")

	rowIndex = 1
	for propertyName, na in sorted(trackFile.d.items()):
		worksheet.write(rowIndex, 0, (trackFile.fields[propertyName]).axisLabel)

		weightAvgVals = trackFile.getAverage(propertyName, weights = TCG.PlotDefaults["weights"]);
		numAvgVals = trackFile.getAverage(propertyName, weights = False)

		worksheet.write(rowIndex, 3, weightAvgVals[0])
		worksheet.write(rowIndex, 4, weightAvgVals[1])
		worksheet.write(rowIndex, 6, numAvgVals[0])
		worksheet.write(rowIndex, 7, numAvgVals[1])
		worksheet.write(rowIndex, 8, numAvgVals[2])

		rowIndex += 1

	worksheet.write(0, 10, "Data Filters")
	rowIndex = 1
	for propertyName, filters in sorted(trackFile.filters.items()):
		worksheet.write(rowIndex, 10, propertyName)
		worksheet.write(rowIndex, 11, str(filters))
		rowIndex += 1

	worksheet.write(0, 13, "Exp Params")
	rowIndex = 1
	for param, val in sorted(trackFile.expParams.items()):
		worksheet.write(rowIndex, 13, param)
		worksheet.write(rowIndex, 14, str(val))
		rowIndex += 1

	worksheet.write(0, 16, "Project Info")
	worksheet.write(1, 16, "Data Import Time: %s" % (trackFile.importTime))
	worksheet.write(2, 16, "Import Path: %s" % (trackFile.path))

	return

# prints all track measurement data to excel file
# TODO: Add sheet and write metadata for experiment
#
# @param      trackFile      The object
# @param      settings  The settings
#
def writeData(trackFile, workbook, worksheetName = ""):

	writeTrackData(trackFile, workbook, trackFile.fileName + worksheetName)
	writeMetaData(trackFile, workbook, trackFile.fileName + worksheetName)

	return

def writeHistogram(workbook, worksheetName, counts, bincenters):
	worksheet = workbook.add_worksheet(workSheetName)

	worksheet.write(0, 0, "binCenters")
	worksheet.write(0, 1, "counts")

	for row in range(1, len(wAvgs)):
		worksheet.write(row, 0, binCenters[row])
		worksheet.write(row, 1, counts[row])


	return

def writeBinData(workbook, workSheetName, wAvgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters):
	worksheet = workbook.add_worksheet(workSheetName + " binData")

	worksheet.write(0, 0, "binCenters")
	worksheet.write(0, 1, "wAvgs")
	worksheet.write(0, 2, "stdDevs")
	worksheet.write(0, 3, "stdErrs")
	worksheet.write(0, 4, "trackCounts")
	worksheet.write(0, 5, "countPercents")

	for index in range(0, len(wAvgs)):
		row = index + 1
		worksheet.write(row, 0, binCenters[index])
		worksheet.write(row, 1, wAvgs[index])
		worksheet.write(row, 2, stdDevs[index])
		worksheet.write(row, 3, stdErrs[index])
		worksheet.write(row, 4, trackCounts[index])
		worksheet.write(row, 5, countPercents[index])

	return

def writePercentHistogramData(workbook, workSheetName, y, bincenters, labels):
	worksheet = workbook.add_worksheet(workSheetName + " percents")

	worksheet.write(0, 0, "labels")

	arraySize = len(bincenters[0])

	for labelIndex in range(0, len(labels)):
		row = (labelIndex * 3)
		worksheet.write(row, 0, labels[labelIndex])
		worksheet.write(row+1, 1, "bincenters")
		worksheet.write(row+2, 1, "value")

		for index in range(0, arraySize):
			worksheet.write(row+1, 2+index, (bincenters[labelIndex])[index])
			worksheet.write(row+2, 2+index, (y[labelIndex])[index])

	return