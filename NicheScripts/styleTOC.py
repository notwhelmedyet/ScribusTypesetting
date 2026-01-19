"""apply character style to the text in your TOC prior to the tab (whether number or letter)

Will run on the currently selected page. Default style to apply is FancyTOC, gives a selector to apply something else
You can also add an additional tab at the start of each line to allow for tab left/tab right combos
Will only work on text frames the full height of the page minus margins (skips small frames so we don't restyle headers etc)

"""

try:
	import scribus
except ImportError:
	pass

def main():
	try:
		scribus # pylint: disable=pointless-statement
	except NameError:
		return

	STYLE = 'FancyTOC'
	TAB = False
	
	scribus.setRedraw(False)
	scribus.closeMasterPage()
	current_page = scribus.currentPage()

	#Set the style we want to use to generate the running header content
	CharacterStyle = scribus.valueDialog( "Style TOC" , "This script will only work on the currently selected page.\n\nEnter the character style to apply to the first word(s) on each line, prior to the tab\n(or type 1 to leave as default, FancyTOC)\n\nNote: this is case sensitive!" , "" )
	if CharacterStyle == str(1):
		STYLE = 'FancyTOC'
		scribus.messageBox('Style', "Style FancyTOC")
	else:
		STYLE = CharacterStyle
		scribus.messageBox('Style', "Style "+str(CharacterStyle))
	if STYLE not in scribus.getCharStyles():
		scribus.setRedraw(True)
		scribus.messageBox(
			'Error',
			f'No style found with the name {STYLE}',
			icon=scribus.ICON_CRITICAL)
		return

	MODE = scribus.valueDialog( "Style TOC" , "Enter a 1 to insert a tab at the start of each line,\nor enter any other character to leave TOC spacing as-is" , "" )
	if MODE == str(1):
		TAB = True
	else:
		TAB = False
	
	#get all text frame names
	page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
		if item[1] == 4]
	page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))
	
	#figure out size of the full margin text frame so we can look for it later
	margins = scribus.getPageMargins() 
	size = scribus.getPageSize()
	height = size[1]-(margins[0]+margins[3])
	
	for item, _ in page_text_frames:
		scribus.deselectAll()
		scribus.selectObject(item)
		#check the size of the text frame. Only apply script if text frame size = page size-margin
		frameSize = scribus.getSize(item)
		ratioHEIGHT = frameSize[1] / height
		if ratioHEIGHT > 0.9: #only look for chapter title and chapter number within the main text frame
			#split text on frame into paragraphs
			paragraphs = scribus.getFrameText().split('\r')
			#iterate through paragraphs
			start = 0
			for p in paragraphs:
				coordinates = (start, len(p)+1)
				scribus.selectFrameText(start, len(p)) #select the text so we can get the style
				tab_start = p.find("	")
				p_style = scribus.getParagraphStyle()
				if len(p)<1: #skip blank paragraphs
					pass
				else:
					if tab_start > 0:
						scribus.selectFrameText(start, tab_start)
						scribus.setCharacterStyle(STYLE)
				start += len(p) + 1 #set start to the start of the next paragraph
			start = 0
			if TAB == True:
				for p in paragraphs:
					scribus.insertText("	", start, item)
					start += len(p) + 2
			
	
	scribus.deselectAll()
	scribus.gotoPage(current_page)
	scribus.setRedraw(True)

if __name__ == '__main__':
	main()
