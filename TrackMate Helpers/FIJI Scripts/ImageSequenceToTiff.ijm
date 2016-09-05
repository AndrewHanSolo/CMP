//This script saves subdirectories containing image sequences to tiff files in a new tiff file in the parent directory

dir = getDirectory("Choose a directory")
fileList = getFileList(dir);
tiffDir = dir + "/tiffs";
File.makeDirectory(tiffDir);
for (i=0; i<fileList.length-1; i++) {
	file = fileList[i];

	if (file != "readme.txt")
		subdirectory = dir + "/" + file;
		subFileList = getFileList(subdirectory);
		startingImagePath = subdirectory + subFileList[0];
		
		run("Image Sequence...", "open=[" + startingImagePath + "] convert sort");
		saveAs("Tiff", tiffDir + "/" + i + ".tif");
		run("Close");
}
