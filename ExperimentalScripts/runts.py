"""Replaces the last space in a paragraph with a nonbreaking space if the last word of the paragraph is shorter than the entered acceptable minimum length.

A decent default value might be 3 or 4 characters. Common typesetting advice is to make sure the allowable stub words are wider than the indentation used in the text.

"""

def main():
	try:
		import scribus

		if not scribus.haveDoc():
			return
	except ImportError:
		print('This script must be run from inside Scribus')
		return
		
	scribus.setRedraw(False)
	scribus.closeMasterPage()
	current_page = scribus.currentPage()

	
	margins = scribus.getPageMargins() 
	size = scribus.getPageSize()
	height = size[1]-(margins[0]+margins[3])

	#Set the style we want to use to generate the running header content
	RUNT = scribus.valueDialog( "Prevent stub paragraph endings" , "This script will insert a nonbreaking space before the last word of every paragraph\nif that word is shorter than the allowable length you set.\nEnter the minimum length word you want Scribus to allow to break onto a new line.", "")
	if RUNT.isdigit():
		RUNT = int(RUNT)
	else:
		scribus.messageBox(
			'Error', 'Invalid input, must be a number. Exiting...',
			icon=scribus.ICON_CRITICAL)
		scribus.deselectAll()
		scribus.gotoPage(current_page)
		scribus.setRedraw(True)
		return
	
	for page in range(1, scribus.pageCount() + 1):
		page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
		if item[1] == 4]
		page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))
		for item, _ in page_text_frames:
			frameSize = scribus.getSize(item)
			ratioHEIGHT = frameSize[1] / height
			start = 0
			if ratioHEIGHT > 0.9: #only look at main text frame
				paragraphs = scribus.getFrameText(item).split('\r')
				for p in paragraphs:
					length = len(p)
					x = p.rfind(" ")
					lastLength = length - (x+2)
					if lastLength < RUNT and lastLength > 0:
						result = scribus.messageBox('Error', p[x:length]+str(lastLength), scribus.BUTTON_OK)
						scribus.selectObject(item)
						scribus.selectFrameText(start+x, 1)
						scribus.deleteText()
						scribus.insertText("\u00A0", start+x, item)			
					start += len(p) + 1
					scribus.layoutText(item)
	
	scribus.deselectAll()
	scribus.gotoPage(current_page)
	scribus.setRedraw(True)

if __name__ == '__main__':
	main()
