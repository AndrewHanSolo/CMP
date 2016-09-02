import xlsxwriter


def writeHistogram(workbook, worksheetName, counts, bincenters):
	worksheet = workbook.add_worksheet(workSheetName)

	worksheet.write(0, 0, "binCenters")
	worksheet.write(0, 1, "counts")

	for row in range(1, len(wAvgs)):
		worksheet.write(row, 0, binCenters[row])
		worksheet.write(row, 1, counts[row])


	return

def writeBinData(workbook, workSheetName, wAvgs, stdDevs, stdErrs, trackCounts, countPercents, binCenters):
	worksheet = workbook.add_worksheet(workSheetName)

	worksheet.write(0, 0, "binCenters")
	worksheet.write(0, 1, "wAvgs")
	worksheet.write(0, 2, "stdDevs")
	worksheet.write(0, 3, "stdErrs")
	worksheet.write(0, 4, "trackCounts")
	worksheet.write(0, 5, "countPercents")

	for row in range(1, len(wAvgs)):
		worksheet.write(row, 0, binCenters[row])
		worksheet.write(row, 1, wAvgs[row])
		worksheet.write(row, 2, stdDevs[row])
		worksheet.write(row, 3, stdErrs[row])
		worksheet.write(row, 4, trackCounts[row])
		worksheet.write(row, 5, countPercents[row])

	return