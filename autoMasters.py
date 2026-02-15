"""auto apply master pages to all blank and chapter start pages

For more details see the README.md
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

	scribus.setRedraw(False)
	scribus.closeMasterPage()
	current_page = scribus.currentPage()

	allRight = False
	blankLeft = ""
	chapLeft = ""
	chapRight = ""
	HeadingStyle = "ChapterTitle"
	
	
	
	#Default settings to skip most of menus
	mode = scribus.valueDialog( "Left or Right" , "Are all chapter breaks on the right, or are they on right and left sides? \n\nEnter 1 if all on right, or any other character if they are on both right and left", "")
	if mode == str(1):
		allRight = True
	else:
		#select left chapter page master 
		try:
			chapLeft = scribus.itemDialog( "Select masters" , "Select the master page to assign to LEFT chapter starts", scribus.masterPageNames())
		except:		
			chapLeft = scribus.valueDialog( "Select masters" , "Enter the name of the master page to assign to LEFT chapter starts (or type 1 to leave as default, BottomNum_Left)\n\nNote: this is case sensitive!" , "" )
		if chapLeft == str(1):
			chapLeft = 'BottomNum_Left'
		else:
			if chapLeft not in scribus.masterPageNames():
				scribus.messageBox(
					'Error',
					f'No master page found with the name {chapLeft}',
					icon=scribus.ICON_CRITICAL)
				return
	#assign right chapter starts for all files				
	try:			
		chapRight = scribus.itemDialog( "Select masters" , "Select the master page to assign to RIGHT chapter starts", scribus.masterPageNames())
	except:		
		chapRight = scribus.valueDialog( "Select masters" , "Enter the name of the master page to assign to RIGHT chapter starts (or type 1 to leave as default, BottomNum_Right)\n\nNote: this is case sensitive!" , "" )
	if chapRight == str(1):
		chapRight = 'BottomNum_Right'
	else:
		if chapRight not in scribus.masterPageNames():
			scribus.messageBox(
				'Error',
				f'No master page found with the name {chapRight}',
				icon=scribus.ICON_CRITICAL)
			return
	#if all right we will have blank left pages
	if allRight == True:
		try:			
			blankLeft = scribus.itemDialog( "Select masters" , "Select the master page to assign to blank pages on the left", scribus.masterPageNames())
		except:		
			blankLeft = scribus.valueDialog( "Select masters" , "Enter the name of the master page to blank pages on the left (or type 1 to leave as default, Normal Left)\n\nNote: this is case sensitive!" , "" )
		if blankLeft == str(1):
			blankLeft = 'Normal Left'
		else:
			if blankLeft not in scribus.masterPageNames():
				scribus.messageBox(
					'Error',
					f'No master page found with the name {blankLeft}',
					icon=scribus.ICON_CRITICAL)
				return
	
	#either way, get paragraph style
	try:
		HeadingStyle = scribus.itemDialog( "Frame breaks" , "Enter the paragraph style used at the start of each chapter", scribus.getParagraphStyles())
	except:		
		HeadingStyle = scribus.valueDialog( "Frame breaks" , "Enter the paragraph style used at the start of each chapter (or type 1 to leave as default, ChapterTitle)\n\nNote: this is case sensitive!" , "" )
	if HeadingStyle == str(1):
		heading = 'ChapterTitle'
	else:
		heading = HeadingStyle
		if HeadingStyle not in scribus.getParagraphStyles():
			scribus.messageBox(
				'Error',
				f'No style found with the name {HeadingStyle}',
				icon=scribus.ICON_CRITICAL)
			return

	scribus.messageBox('Settings', f'Looking for chapter pages that include text with the style {HeadingStyle}\nRight chapter page master is {chapRight}\nLeft chapter page master (if applicable) is {chapLeft}, blank left page master is {blankLeft}')
	scribus.messageBox('Settings', 'filename is '+scribus.getDocName())
	
	'''
	applyPage = False
	blankPage = False
	for page in range(1, scribus.pageCount() + 1):
		# get the text and linked frames, sorted by the position on the page
		page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
			if item[1] == 4]
		page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))

		for item, _ in page_text_frames:
			scribus.deselectAll()
			scribus.selectObject(item)

			text = scribus.getFrameText()
			#if there's no text this is a white page
			test = re.search('\W', text)
			if test:
				blankPage = True
			else:
				paragraphs = text.split('\r')

				start = 0
				for p in paragraphs:
					scribus.selectFrameText(start, len(p))
					p_style = scribus.getParagraphStyle()
					if p_style == Heading_Style:
						applyPage = True
					start += len(p) + 1
		if applyPage == True:
			if blankPage = True:
				#apply blank left master page
			else:
				#figure out if page is on the right or left
				#page type 0 is 
				if scribus.getPageType(page) == 0: 
				#page type 2 is
				if scribus.getPageType(page) == 2: 
		blankPage = False
		applyPage = False'''


	scribus.deselectAll()
	scribus.gotoPage(current_page)
	scribus.setRedraw(True)

if __name__ == '__main__':
	main()
