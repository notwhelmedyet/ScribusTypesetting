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
	INSERT_CHAR = False
	STYLE_TEXT =  True
	STYLE_FIRST = False
	STYLE_CHAR = False
	STYLE_LAST = False
	
	scribus.setRedraw(False)
	scribus.closeMasterPage()
	current_page = scribus.currentPage()

	#Set the style we want to use to generate the running header content
	CHARACTER = scribus.valueDialog( "Style TOC" , "This script will only work on the currently selected page.\n\nIf you want to insert a character between the page number and chapter title, enter it here\n(or type 0 to not insert anything)\n\nNote: this is case sensitive!" , "" )
	if CHARACTER == str(0):
		RANGE = scribus.valueDialog( "Style TOC" , "Do you want to style part of each line with a character style?\n\nEnter 1 to style text before the tab\nEnter 2 to style text after the tab\nEnter 0 to not style any text", "")
		if RANGE.find("0")>=0:
			STYLE_TEXT = False
			scribus.messageBox('Style', "Range == 0, style text = "+str(STYLE_TEXT))
		if RANGE.find("1")>=0:
			STYLE_FIRST = True
		if RANGE.find("2")>=0:
			STYLE_LAST = True
	else:
		CHARACTER = "	"+CHARACTER
		INSERT_CHAR = True
		#Set the style we want to use to generate the running header content
		RANGE = scribus.valueDialog( "Style TOC" , "If you want to style part of each line with a character style, select the components to be styled here:\n\n0: [First Text is 1] TAB [Insert Char is 2] TAB [Second Text is 3]. \n\n for instance, to style the first text and the inserted character type 12.\nto style only the second text type 3.\nto style no text type 0", "")
		if RANGE.find("0")>=0:
			STYLE_TEXT = False
			scribus.messageBox('Style', "Range == 0, style text = "+str(STYLE_TEXT))
		if RANGE.find("1")>=0:
			STYLE_FIRST = True
		if RANGE.find("2")>=0:
			STYLE_CHAR = True
		if RANGE.find("3")>=0:
			STYLE_LAST = True

	#Set the style we want to use
	if STYLE_TEXT == True:
		CharacterStyle = scribus.valueDialog( "Style TOC" , "This script will only work on the currently selected page.\n\nEnter the character style to apply to the selected slice of each line\n(or type 0 to leave as default, FancyTOC)\n\nNote: this is case sensitive!" , "" )
		if CharacterStyle == str(0):
			STYLE = 'FancyTOC'
		else:
			STYLE = CharacterStyle
		if STYLE not in scribus.getCharStyles():
			scribus.setRedraw(True)
			scribus.messageBox(
				'Error',
				f'No style found with the name {STYLE}',
				icon=scribus.ICON_CRITICAL)
			return

	MODE = scribus.valueDialog( "Style TOC" , "Enter a 1 to insert a tab at the start of each line,\nor enter 0 to leave TOC spacing as-is" , "" )
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
	
	#scribus.messageBox('Style', "Settings: \nAdd Char: "+str(INSERT_CHAR)+"\nStyle Text: "+str(STYLE_TEXT)+"\nStyle first half: "+str(STYLE_FIRST)+"\nStyle second half: "+str(STYLE_LAST)+"\nSelected style: "+str(STYLE))
	
	
	for item, _ in page_text_frames:
		scribus.deselectAll()
		scribus.selectObject(item)
		#check the size of the text frame. Only apply script if text frame size = page size-margin
		frameSize = scribus.getSize(item)
		ratioHEIGHT = frameSize[1] / height
		if ratioHEIGHT > 0.9: #only look for chapter title and chapter number within the main text frame
			#split text on frame into paragraphs
			FULL_PAGE = scribus.getFrameText()
			paragraphs = FULL_PAGE.split('\r')
			#iterate through paragraphs
			start = 0
			insertList = []
			for p in paragraphs:
				line_end = len(p)+1
				tab_start = p.find("	")
				second_start = tab_start+1
				if len(p)<1: #skip blank paragraphs
					pass
				elif tab_start>=0:
					if TAB == True:
						entry = ("	", start, item)
						insertList.insert(0, entry)
					if INSERT_CHAR == True:
						entry = (CHARACTER, start+tab_start, item)
						insertList.insert(0, entry)
					if STYLE_TEXT == True:
						if STYLE_FIRST == True:
							scribus.selectFrameText(start, tab_start)
							scribus.setCharacterStyle(STYLE)
						if STYLE_LAST == True:
							scribus.selectFrameText(start+tab_start+1, line_end-tab_start-2)
							scribus.setCharacterStyle(STYLE)
				start += line_end #set start to the start of the next paragraph
			for x in insertList:
				#scribus.messageBox('Style', "inserting text "+str(x[0])+" at "+str(x[1])+" in "+str(x[2]))
				scribus.insertText(x[0], x[1], x[2])
				if STYLE_CHAR == True:
					if x[0] == CHARACTER:
						#scribus.messageBox('Style', "style "+str(x[1])+" to "+str(len(CHARACTER)))
						scribus.selectFrameText(x[1]+1, len(CHARACTER)-1)
						scribus.setCharacterStyle(STYLE)

			scribus.layoutText(item)
			
	scribus.deselectAll()
	scribus.gotoPage(current_page)
	scribus.setRedraw(True)

if __name__ == '__main__':
	main()
