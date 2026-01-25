"""Copies a selected object (image, shape, line) as an inline object everywhere it finds the specified placeholder string
Will only work in Scribus 1.6.1 (I believe) and later, when the scribus.setEditMode() and setNormalModer commands were added to the scripter
Will only work if your chosen placeholder is UNIQUE and not used elsewhere within the document where you don't want an image
For future editability of the inserted object, convert it to a symbol prior to running this script

with thanks to Ale for the code in this discussion https://forums.scribus.net/index.php/topic,4743.0.html

"""

#thank you to AkiRoss on stackoverflow for saving my life here back in 2015
def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i+1)

def main():
	try:
		import scribus

		if not scribus.haveDoc():
			return
	except ImportError:
		print('This script must be run from inside Scribus')
		return
		

	if scribus.selectionCount() != 1:
		scribus.messageBox(
			'Error', 'Script only works if 1 object is selected before run. Please try again',
			icon=scribus.ICON_CRITICAL)
		return
	selected_object = scribus.getSelectedObject()
	scribus.copyObjects(selected_object)
	scribus.setRedraw(False)
	scribus.closeMasterPage()
	current_page = scribus.currentPage()

	
	margins = scribus.getPageMargins() 
	size = scribus.getPageSize()
	height = size[1]-(margins[0]+margins[3])

	
	if scribus.scribus_version_info[1]<6:
		scribus.messageBox(
			'Error', 'You are running Scribus '+str(scribus.scribus_version)+" Script can only run in Scribus 1.6.0 or later. Exiting...",
			icon=scribus.ICON_CRITICAL)
		return

	#Set the style we want to use to generate the running header content
	CHARACTER = scribus.valueDialog( "Inline Image Replacer" , "This script will copy whatever object was selected when you LAUNCHED the script\nand copy it into the program wherever it finds the designated placeholder character.\n\nIf you want to exit the script without running type 0.\nOtherwise type the placeholder character or string and hit enter to find and replace.", "")
	if CHARACTER == str(0):
		scribus.messageBox(
			'Error', 'Exiting...',
			icon=scribus.ICON_CRITICAL)
		scribus.deselectAll()
		scribus.gotoPage(current_page)
		scribus.setRedraw(True)
		return
	else:
		scribus.copyObjects(selected_object)
	
	for page in range(1, scribus.pageCount() + 1):
		page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
		if item[1] == 4]
		page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))
		for item, _ in page_text_frames:
			frameSize = scribus.getSize(item)
			ratioHEIGHT = frameSize[1] / height
			if ratioHEIGHT > 0.9: #only for ornaments within main text frame
				scribus.deselectAll()
				scribus.selectObject(item)
				text = scribus.getAllText(item)
				indexes = []	
				for i in findall(CHARACTER, text):
					indexes.insert(0, i)
				for i in indexes:
					scribus.selectText(i, len(CHARACTER), item)
					scribus.setEditMode() 
					scribus.pasteObjects()
					scribus.setNormalMode()
				scribus.layoutText(item)
	
	scribus.deselectAll()
	scribus.gotoPage(current_page)
	scribus.setRedraw(True)

if __name__ == '__main__':
	main()
