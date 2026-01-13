"""create running titles, based on master pages and text styles

For more details see the README.md

Original (c) MIT 2024, ale rimoldi <ale@graphicslab.org>
https://github.com/aoloe/scribus-script-repository/tree/master/headers_with_chapter_titles

Edited by Lynn notwhelmedyet@gmail.com in 2025 to add paragraph style to the header, toggle header deletion & give dialogue options to set variables on run
"""

try:
	import scribus
except ImportError:
	pass


HEADING_STYLE = 'AuthorName'
HEADING_ITEM_PREFIX = 'Header'
NEW_HEADING_STYLE = 'RunningHeader2' 
DELETE = True
PLACEMENT = 0

def get_master_pages_with_running_titles():
	"""get the names of the master page with a running title
	   and the name of the text frame for it"""
	master_pages = {}
	for master_page in scribus.masterPageNames():
		scribus.editMasterPage(master_page)
		for item in (item[0] for item in scribus.getPageItems() if item[1] == 4):
			if item.startswith(HEADING_ITEM_PREFIX):
				master_pages[master_page] = item
				break
	scribus.closeMasterPage()
	return master_pages

def delete_all_heading_frames():
	for page in range(1, scribus.pageCount() + 1):
		scribus.gotoPage(page)
		if page % 2 == 0:
			for item in (item[0] for item in scribus.getPageItems() if item[1] == 4):
				if item.startswith(HEADING_ITEM_PREFIX):
					scribus.deleteObject(item)


def get_first_h1_in_page(page):
	"""go through all paragraphs in all frames in page
		and if there is an h1 paragraph style return its text."""
	scribus.gotoPage(page)

	# get the text and linked frames, sorted by the position on the page
	page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
		if item[1] == 4]
	page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))

	for item, _ in page_text_frames:
		scribus.deselectAll()
		scribus.selectObject(item)

		paragraphs = scribus.getFrameText().split('\r')

		start = 0
		for p in paragraphs:
			scribus.selectFrameText(start, len(p))
			p_style = scribus.getParagraphStyle()
			if p_style == HEADING_STYLE:
				return p
			start += len(p) + 1
	return None

def main():
	try:
		scribus # pylint: disable=pointless-statement
	except NameError:
		return

	scribus.setRedraw(False)

	scribus.closeMasterPage()
	current_page = scribus.currentPage()

	master_pages = get_master_pages_with_running_titles()	

	if len(master_pages) == 0:
		scribus.setRedraw(True)
		scribus.messageBox(
			'Error',
			f'No master page found, with a text item starting with {HEADING_ITEM_PREFIX}',
			icon=scribus.ICON_CRITICAL)
		return


	#Delete old headers? Turn this off to set both left and right running headers
	HeadingStyle = scribus.valueDialog( "Set Up Running Headers" , "Enter 1 to keep any headers made previously by this script,\n2 to delete old headers and exit\nany other character to delete headers made by previous runs and make new headers" , "" )
	if HeadingStyle != str(1):
		delete_all_heading_frames()
	if HeadingStyle == str(2):
		delete_all_heading_frames()		
		scribus.deselectAll()
		scribus.gotoPage(current_page)
		scribus.setRedraw(True)
		return

	#Set the style we want to use to generate the running header content
	HeadingStyle = scribus.valueDialog( "Set Up Running Headers" , "Enter the paragraph style to search for the running header content (or type 1 to leave as default, ChapterTitle)\n\nNote: this is case sensitive!" , "" )
	if HeadingStyle == str(1):
		HEADING_STYLE = 'ChapterTitle'
	else:
		HEADING_STYLE = HeadingStyle
	if HEADING_STYLE not in scribus.getParagraphStyles():
		scribus.setRedraw(True)
		scribus.messageBox(
			'Error',
			f'No style found with the name {HEADING_STYLE}',
			icon=scribus.ICON_CRITICAL)
		return
	#Set the style we want to use to style the running header content
	NewHeadingStyle = scribus.valueDialog( "Set Up Running Headers" , "Enter the paragraph style to use for the new running headers (or type 1 to leave as default, RunningHeader)\n\nNote: this is case sensitive!" , "" )
	if NewHeadingStyle == str(1):
		NEW_HEADING_STYLE = 'RunningHeader2'
	else:
		NEW_HEADING_STYLE = NewHeadingStyle
	if NEW_HEADING_STYLE not in scribus.getParagraphStyles():
		scribus.setRedraw(True)
		scribus.messageBox(
			'Error',
			f'No style found with the name {NEW_HEADING_STYLE}',
			icon=scribus.ICON_CRITICAL)
		return 
	#Set if this applies to left, right, or all pages    
	HeadingStyle = scribus.valueDialog( "Set Up Running Headers" , "Enter 1, 2, or 3:\n1: Apply Running Headers to left-hand pages only\n2: Apply Running Headers to right-hand pages only\n3: Apply Running Headers to all applicable pages", "")
	if HeadingStyle == str(1):
		Sides = 0
		PLACEMENT = -1
	elif HeadingStyle == str(2): 
		Sides = 2
		PLACEMENT = 0
	elif HeadingStyle == str(3):
		Sides = 3
		PLACEMENT = 1 #1 is code for alternating, place to outside
	#If there's text in the header (likely a page number), should we replace it, or put the new running header to the right or left?
	HeadingStyle = scribus.valueDialog( "Set Up Running Headers" , "Enter 1, 2, or 3:\n1: Put running headers on the inside of the page relative to any text in the master page text frame \n2: Put running headers to the outside of the page relative to any text \n3: Ignore any text on the master page text frames", "")
	if HeadingStyle == str(2): 
		if Sides == 0:
			PLACEMENT = 0
		elif Sides == 2:
			PLACEMENT = -1
		else:
			PLACEMENT = 2 #2 is code for alternating, but place to inside
	elif HeadingStyle == str(3):
		PLACEMENT = 3 #code for ignore placement

	current_h1 = None
	# TODO: it might be better to get both the first and last h1 on the page.
	# the first for this page, the last (if different) for the following ones
	for page in range(1, scribus.pageCount() + 1):
		h1 = get_first_h1_in_page(page)
		if h1 is not None:
			current_h1 = h1
		if current_h1 is None:
			continue
		#test if we're on the same side page as we selected for headers, only apply new header if so
		if (Sides == 3) or (Sides == scribus.getPageType(page)): 
			master_page = scribus.getMasterPage(page)
			if master_page not in master_pages:
				continue
			scribus.editMasterPage(master_page)
			scribus.copyObjects([master_pages[master_page]])
			scribus.closeMasterPage()
			scribus.gotoPage(page)
			new_frame = scribus.pasteObjects()[0]
			if PLACEMENT == 3:
				scribus.setText(current_h1, new_frame)
			elif (PLACEMENT == -1) or (PLACEMENT == 0):
				scribus.insertText(current_h1, PLACEMENT, new_frame)
			elif PLACEMENT == 1:
				if scribus.getPageType(page) == 0:
					scribus.insertText(current_h1, -1, new_frame)
				if scribus.getPageType(page) == 2:
					scribus.insertText(current_h1, 0, new_frame)	
			else:
				if scribus.getPageType(page) == 0:
					scribus.insertText(current_h1, 0, new_frame)
				if scribus.getPageType(page) == 2:
					scribus.insertText(current_h1, -1, new_frame)	
			scribus.setProperty(new_frame, 'printEnabled', True)
			scribus.setParagraphStyle(NEW_HEADING_STYLE, new_frame)
			scribus.setItemName(HEADING_ITEM_PREFIX + str(page), new_frame)
	scribus.deselectAll()
	scribus.gotoPage(current_page)
	scribus.setRedraw(True)

if __name__ == '__main__':
	main()
