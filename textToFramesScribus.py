"""move certain text elements on a page into separate frames.
Will only work if you have text on the page using the styles ChapterTitle, ChapterNumber, and/or ChapterStart
Will move the first instance of text in the main frame (assumed to be the size of the page-margins) using those styles
into text frames that contain the style name if they exist. If no matching text frame exists, the text is not moved.

For ChapterTitle and ChapterNumber, the entire paragraph is moved. 

For DropCap, the first letter (or first two characters if the line begins with a quote) is moved to the DropCap text frame
If a text frame DropQuote exists, any beginning quote mark will be moved to DropQuote
If a character style DropQutoe exists, the quote will be styled in that character style (using the drop cap style in superscript seems to work well)


"""

try:
	import scribus
except ImportError:
	pass

def main():
	replaceCAP = False
	replaceTITLE = False
	replaceNUMBER = False
	replaceQUOTE = False
	foundTITLE = False
	foundNUMBER = False
	foundBOXTITLE = False
	foundBOXNUMBER = False
	foundCAP = False
	foundQUOTE = False
	TITLE = ''
	NUMBER = ''
	BOXTITLE = ''
	BOXNUMBER = ''
	CAPITAL = ''
	deleteLIST = []
	QUOTELIST = ["“","”",'"',"‘","’","'"] 

	try:
		scribus # pylint: disable=pointless-statement
	except NameError:
		return

	scribus.setRedraw(False)
	scribus.closeMasterPage()
	current_page = scribus.currentPage()

	#figure out size of the full margin text frame so we can look for it later
	margins = scribus.getPageMargins() 
	size = scribus.getPageSize()
	width = size[0]-(margins[1]+margins[2])
	height = size[1]-(margins[0]+margins[3])
	
	#get all text frame names
	page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
		if item[1] == 4]
	page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))
	
	#if text frames matching chosen styles exist, set flag to move them
	for item, _ in page_text_frames:
		if item.find('DropCap')>=0:
			replaceCAP = True
		elif item.find('ChapterTitle')>=0:
			replaceTITLE = True
		elif item.find('ChapterNumber')>=0:
			replaceNUMBER = True
		elif item.find('DropQuote')>=0:
			replaceQUOTE = True		

	for item, _ in page_text_frames:
		scribus.deselectAll()
		scribus.selectObject(item)
		#check the size of the text frame. Only apply script if text frame size = page size-margin
		frameSize = scribus.getSize(item)
		ratioHEIGHT = frameSize[1] / height
		ratioWIDTH = frameSize[0] / width
		if ratioHEIGHT > 0.9 and ratioWIDTH > 0.9: #only look for chapter title and chapter number within the main text frame
			#split text on frame into paragraphs
			paragraphs = scribus.getFrameText().split('\r')
			#iterate through paragraphs
			start = 0
			for p in paragraphs:
				coordinates = (start, len(p)+1)
				scribus.selectFrameText(start, len(p)) #select the text so we can get the style
				p_style = scribus.getParagraphStyle()
				if len(p)<1: #skip blank paragraphs
					pass
				else:
					if replaceTITLE == True: #if we're replacing the title
						if foundTITLE == False: #only move the FIRST (non-blank) entry
							if p_style == 'ChapterTitle': #if current paragraph has the Chapter Title style
								foundTITLE = True	#flag it as found, save the text, mark the coordinates for deletion			
								TITLE = p
								deleteLIST.insert(0, coordinates)
					if replaceNUMBER == True:
						if foundNUMBER == False:
							if p_style == 'ChapterNumber':
								foundNUMBER = True
								NUMBER = p
								deleteLIST.insert(0, coordinates)
					if replaceCAP == True:
						if foundCAP == False:
							if p_style == 'ChapterStart':
								foundCAP = True
								#result = scribus.messageBox ('Error', 'found chapter start p0 is'+str(p[0]),scribus.BUTTON_OK)
								if p[0] in QUOTELIST:
									foundQUOTE = True
									QUOTE = p[0]
									CAPITAL = p[1]
									coordinates = (start, 2)
								else:
									#result = scribus.messageBox ('Error', 'did not find quote',scribus.BUTTON_OK)
									CAPITAL = p[0]
									coordinates = (start, 1)
								#result = scribus.messageBox ('Error', 'Capital is'+CAPITAL,scribus.BUTTON_OK)
								deleteLIST.insert(0, coordinates)
				start += len(p) + 1 #set start to the start of the next paragraph
			#after we find all, go through the page from bottom to top and delete marked text
			for c in deleteLIST:
				scribus.selectFrameText(c[0], c[1])
				scribus.deleteText()
				
	for item, _ in page_text_frames:
		#for our three styles, there is a matching text frame & we found text, insert it into the frame & set the appropriate paragraph style.
		if item.find('ChapterTitle')>=0:
			if foundTITLE == True:
				scribus.insertText(TITLE, 0, item)
				scribus.setParagraphStyle("ChapterTitle", item)
		elif item.find('ChapterNumber')>=0:
			if foundNUMBER == True:
				scribus.insertText(NUMBER, 0, item)
				scribus.setParagraphStyle("ChapterNumber", item)
		elif item.find('DropCap')>=0:
			if foundCAP == True:
				scribus.insertText(CAPITAL, 0, item)
				scribus.setParagraphStyle("DropCap", item)	
				if foundQUOTE == True: #if we found a leading quote, AND the char style DropQuote exists, style the leading quote in that style
					scribus.insertText(QUOTE, 0, item)
					if "DropQuote" in scribus.getCharStyles():
						scribus.layoutText(item) #you need to layout the text so Scribus can select it
						scribus.selectFrameText(0, 1, item)
						scribus.setCharacterStyle("DropQuote")
		elif item.find('DropQuote')>=0:
			if foundQUOTE == True:
				scribus.insertText(QUOTE, 0, item)
				scribus.setParagraphStyle("DropCap", item)
				if "DropQuote" in scribus.getCharStyles():
					scribus.setCharacterStyle("DropQuote", item)
		scribus.layoutText(item)
		
	scribus.deselectAll()
	scribus.gotoPage(current_page)
	scribus.setRedraw(True)

if __name__ == '__main__':
	main()
