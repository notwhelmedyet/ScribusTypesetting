# go through all text items in the document, check for designated heading style and create matching attributes for the table of contents
#
# some coding borrowed from ale rimoldi's 2023 table-of-contents.py


import scribus

def main():
	if not scribus.haveDoc():
		return


	heading = ''
	attribute_name = 'TOC'

    #get name of document style to use in TOC
	HeadingStyle = scribus.valueDialog( "Set Up TOC" , "Enter the paragraph style to search for the TOC entries (or type 1 to leave as default, ChapterTitle)\n\nNote: this is case sensitive!" , "" )
	if HeadingStyle == str(1):
		heading = 'ChapterTitle'
	else:
		heading = HeadingStyle
		if HeadingStyle not in scribus.getParagraphStyles():
			scribus.setRedraw(True)
			scribus.messageBox(
				'Error',
				f'No style found with the name {HeadingStyle}',
				icon=scribus.ICON_CRITICAL)
			return
	
    #get the name of the TOC attribute to attribute to each entry
	attribute = scribus.valueDialog( "Set Up TOC" , "Enter the name of the TOC Attribute you've created (or type 1 to leave as default, TOC)\n\nNote: this is case sensitive! If you forgot to make the attribute, enter 2 to quit" , "" )
	if attribute == str(1):
		pass
	elif attribute == str(2):
		return
	else:
		attribute_name = attribute
	
    #iterate through all pages
	for page in range(1, scribus.pageCount() + 1):
		scribus.gotoPage(page)
		# get the text and linked frames, sorted by the position on the page
		page_text_frames = [(item[0], scribus.getPosition(item[0])) for item in scribus.getPageItems()
			if item[1] == 4]
		page_text_frames.sort(key= lambda item: (item[1][1], item[1][0]))
        #iterate through all text frames
		for item, _ in page_text_frames:
			scribus.deselectAll()
			scribus.selectObject(item)
			paragraphs = scribus.getFrameText().split('\r')
			start = 0
			toc_attributes = []
			for p in paragraphs:
				scribus.selectFrameText(start, len(p))
				p_style = scribus.getParagraphStyle()
				if p_style == heading and len(p)>2: #len check avoids adding blank line entries. might be better to go >1
					toc_attributes.append({
							'Name': attribute_name,
							'Type': 'none',
							'Value': p,
							'Parameter': 'none',
							'Relationship': 'none',
							'RelationshipTo': '',
							'AutoAddTo': 'none'
						})
				start += len(p) + 1
			if toc_attributes:
					attributes = [a for a in scribus.getObjectAttributes() if a['Name'] != attribute_name]
					scribus.setObjectAttributes(attributes + toc_attributes)
			
		scribus.deselectAll()

main()
