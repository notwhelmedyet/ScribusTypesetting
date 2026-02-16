#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
try:
	import scribus
except ImportError:
	print ("Unable to import the 'scribus' module. This script will only run within")
	print ("the Python interpreter embedded in Scribus. Try Script->Execute Script.")
	sys.exit(1)

def main(argv):
	"""This script resizes text frames and moves them to align with the page margins
	and is intended to be used on book-style documents with automatic text frames after
	the size of the page or margins has been changed. The script was only tested with facing
	page layouts where the first page is on the right hand side and all pages have the same margins.
	Based on initial code by Blaze (thank you!)"""
	#resizeAllFrames, when toggled, will resize ALL frames, not just ones the program thinks are the 'main' text frames
	#which it checks against the size of the objects on the first page
	resizeAllFrames = False
	
	if not scribus.haveDoc():
		scribus.messageBox('Scribus -Script Error', "No document open",
		scribus.ICON_WARNING, scribus.BUTTON_OK)
		sys.exit(1)
	
	#ask if we want to resize ALL frames
	optionSelector = scribus.valueDialog( "Resize text frames" , "This script can either resize all text frames to the size of the margins \nor only resize text frames that were previously margin-sized\n(which it will guess off the size of the text frame on page)\nIt will also attempt to move headers and footers to align with the new text frames,\nbut it is only smart enough to move ones that were previously margin-sized\nPrefix the name of any master page item 'Exempt' to stop this script from moving it\n\nEnter 1 to resize ALL text frames on pages, or any other input\nto skip smaller frames (you'll have to resize/move those manually)." , "" )
	if optionSelector == str(1):
		resizeAllFrames = True
	
	#the size of our pages will be page size - margins
	margins = scribus.getPageMargins()
	size = scribus.getPageSize()
	width = size[0]-(margins[1]+margins[2])
	height = size[1]-(margins[0]+margins[3])
	#the location of the frames should be (x,y) where
	#x is the INSIDE margin on right hand pages (aka the right margin on page 1)
	#x is the OUTSIDE margin on left hand pages (aka the left margin on page 1)
	#y is the TOP margin
	rightX = margins[2]
	leftX = margins[1]
	y = margins[0]
	content = []
		
		
	#finds the size of our main text frames by checking the size of objects on page 1. won't work if here's multiple text frames on page 1!
	scribus.gotoPage(1)
	pageOneItems = scribus.getAllObjects()
	for item in pageOneItems:
		mainFrameSize = scribus.getSize(item) #width,height
		rightFramePosition = scribus.getPosition(item) #x,y
	
	
	rightDisplacement = rightFramePosition[0]-rightX
	verticalDisplacement = y-rightFramePosition[1]	
	bottomMarginMeasurement = size[1]-margins[3]
	

	#repositions all headers/footers on master pages that don't start with the name Exempt to align with the new text frames
	master_pages = {}
	for master_page in scribus.masterPageNames():
		scribus.editMasterPage(master_page)
		for item in (item[0] for item in scribus.getPageItems() if item[1] == 4): #fetches the names of all objects that are text frames			
			if not item.startswith('Exempt'):
				FRAMESIZE = scribus.getSize(item)
				POSITION = scribus.getPosition(item)
				if master_page.find('ight') > 0:
					if scribus.getPosition(item)[1]<2:
						scribus.moveObject(0, verticalDisplacement, item)
					else:
						scribus.moveObjectAbs(leftX, bottomMarginMeasurement, item)
					if FRAMESIZE[0]==mainFrameSize[0]:
						scribus.sizeObject(width, FRAMESIZE[1], item)
						POSITION = scribus.getPosition(item)
						scribus.moveObjectAbs(leftX, POSITION[1], item)
				if master_page.find('eft') > 0:						
					if scribus.getPosition(item)[1]<2:
						scribus.moveObject(0, verticalDisplacement, item)
					else:
						scribus.moveObjectAbs(rightX, bottomMarginMeasurement, item)
					if FRAMESIZE[0]==mainFrameSize[0]:
						scribus.sizeObject(width, FRAMESIZE[1], item)
						POSITION = scribus.getPosition(item)
						scribus.moveObjectAbs(rightX, POSITION[1], item)

	scribus.closeMasterPage()
   


	
	#iterate through all pages and move text boxes		
	for page in range(1, scribus.pageCount() + 1):
		scribus.gotoPage(page)
		x = 0
		if (page%2 == 0):
			x = rightX
		else:
			x = leftX
		allItems = scribus.getAllObjects()
		for item in allItems:
			if scribus.getObjectType(item)=='TextFrame':
				size = scribus.getSize(item)
				if resizeAllFrames:
					scribus.sizeObject(width, height, item)
					scribus.moveObjectAbs(x, y, item)
				elif mainFrameSize == size:
					scribus.sizeObject(width, height, item)
					scribus.moveObjectAbs(x, y, item)
			

   

def main_wrapper(argv):
	"""The main_wrapper() function disables redrawing, sets a sensible generic
	status bar message, and optionally sets up the progress bar. It then runs
	the main() function. Once everything finishes it cleans up after the main()
	function, making sure everything is sane before the script terminates."""


	try:
		scribus.statusMessage("Running script...")
		scribus.progressReset()
		main(argv)
	finally:
		# Exit neatly even if the script terminated with an exception,
		# so we leave the progress bar and status bar blank and make sure
		# drawing is enabled.
		if scribus.haveDoc():
			scribus.setRedraw(True)
		scribus.statusMessage("")
		scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
	main_wrapper(sys.argv)

