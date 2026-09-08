#  runtsAndStuff.py
#  This preprocesses a hyphenated Scribus file to prevent lots of manual dehyphenation work. It will:
#	- Insert a nonbreaking space in front of all short words (default 6 characters) at the end of paragraphs
#	- Remove soft hyphens from the last X characters of paragraph endings (can turn off or set character count, default 50) 
#	- Remove soft hyphens in all normally hyphenated words
#	- Remove soft hyphens in last word of paragraph
#	- Insert a frame break before instances of X style (can turn off, default ChapterTitle)
#	- Apply a character style X to first Y of paragraph style Z (can turn off, options to apply to first Y characters, words, or up to a delimiter.)
#  This script must be run within scribus. You need to open the scribus file you're editing with the file picker, but it must also be open within Scribus for the style verification to work correctly. You must hyphenate the whole text prior to running this script for dehyphenation to work - the script does not prevent hyphenating, it simply removes hyphenation from the situations descirbed above.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.


import os.path
import string
import re
import sys

try:
	import scribus
except ImportError:
	pass

def main():
	try:
		scribus # pylint: disable=pointless-statement
	except NameError:
		return
	
	FrameBreaks = False
	RUNT = 6
	heading = 'ChapterTitle'
	headingF = 'ChapterTitle'
	styleChar = 'CharStart'
	charStyle = 'CharStart'
	wordCount = 0
	charCount = 0
	useDelimiter = False
	toDelimiter = False
	delimiter = ":"
	LastLine = True
	LLLength = 50

		
	mode = scribus.valueDialog("Script settings", "This script is designed to take the currently open Scribus file, open the source XML document\nand edit a copy so paragraphs don't end in hyphenated words or stubs on a newline.\nIt will save a separate copy of your file named [FILENAME]_Runts.sla.\nIf you want it to fix hyphenaton you must have your document hyphenated before continuing.\n\nEnter 0 to exit the script without running or any other character to continue", "")
	if mode == str(0):
		return 0
	else:
		fileName = scribus.getDocName()
		entry = fileName.rsplit('.sla', 1)[0]
		writeName = entry+"_Runts.sla"
	
	#Default settings to skip most of menus
	mode = scribus.valueDialog( "Default settings?" , "By default, the script will:\nPrevent runts shorter than 6 characters\nUnhyphenate all words within the last 50 characters of paragraph endings\nInsert a frame break at instances of the style ChapterTitle\nNot apply any character styles.\n\nEnter 1 to accept the default or any other character to edit the settings", "")
	if mode == str(1):
		FrameBreaks = True
	elif mode != str(1):
		#Set the minimum stub paragraph length
		RUNT = scribus.valueDialog( "Prevent stub paragraph endings" , "This script will insert a nonbreaking space before the last word of every paragraph\nif that word is shorter than the allowable length you set.\nEnter the minimum length word you want Scribus to allow to break onto a new line.", "")
		if RUNT.isdigit():
			RUNT = int(RUNT)
		else:
			scribus.messageBox(
				'Error', "You must enter a number. Exiting...", icon=scribus.ICON_CRITICAL)
			return
			
		#Unhyphenation options
		LLLength = scribus.valueDialog( "Dehyphenate paragraph paragraph endings" , "This script will dehyphenate the last word of each paragraph.\nIf you also want it to ALSO dehyphenate words within the last X characters of the paragraph ending\nenter your desired character count.\nEnter 0 to only dehyphenate the last word.", "")
		if LLLength.isdigit():
			LLLength = int(LLLength)
			if LLLength == 0: 
				LastLine = False
		else:
			scribus.messageBox(
				'Error', "You must enter a number. Exiting...", icon=scribus.ICON_CRITICAL)
			return

		#Optionally insert frame break between start of each chapter
		mode = scribus.valueDialog( "Insert frame break for new chapters" , "Do you want the script to insert a frame break at the start of each chapter? Enter 1 to insert breaks or any other character to skip.", "")
		if mode == str(1):
			FrameBreaks = True
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

		#Optionally style first X (or up to a delimiter) of selected paragraph style
		mode = scribus.valueDialog( "Apply char style" , "Do you want the script to apply a character style to the beginning of a chosen paragraph style?\n\nEnter 1 to skip styling\nEnter 2 to style first X words\nEnter 3 to style first X characters\nEnter 4 to apply style up to a chosen delimiter (comma, colon, etc)\nEnter 5 to style up to and including a chosen delimiter", "")
		if mode == str(1):
			charStyle = False
		else:
			charStyle = True
			try:
				HeadingStyle = scribus.itemDialog( "Apply char style" , "Select the paragraph style you want to apply the char style to", scribus.getParagraphStyles())
			except:		
				HeadingStyle = scribus.valueDialog( "Apply char style" , "Enter the paragraph style you want to apply the char style to (or type 1 to leave as default, ChapterStart)\n\nNote: this is case sensitive!" , "" )
			if HeadingStyle == str(1):
				headingF = 'ChapterStart'
			else:
				headingF = HeadingStyle
				if HeadingStyle not in scribus.getParagraphStyles():
					scribus.messageBox(
						'Error',
						f'No style found with the name {HeadingStyle}',
						icon=scribus.ICON_CRITICAL)
					return
			try:
				styleChar = scribus.itemDialog( "Apply char style" , "Select the character style you want to apply", scribus.getCharStyles())
			except:		
				styleChar = scribus.valueDialog( "Apply char style" , "Enter the character style you want to apply (or type 1 to leave as default, CharStart)\n\nNote: this is case sensitive!" , "" )
			if styleChar == str(1):
				styleChar = 'CharStart'
			else:
				if styleChar not in scribus.getCharStyles():
					scribus.messageBox(
						'Error',
						f'No style found with the name {styleChar}',
						icon=scribus.ICON_CRITICAL)
					return
					
			if mode == str(2):
				wordCount = scribus.valueDialog( "Apply char style" , "How many starting words do you want to apply the style to?" , "" )
				if wordCount.isdigit():
					wordCount = int(wordCount)
				else:
					scribus.messageBox(
						'Error', 'Must be a number', icon=scribus.ICON_CRITICAL)
					return
			elif mode == str(3):
				charCount = scribus.valueDialog( "Apply char style" , "How many starting characters do you want to apply the style to?" , "" )
				if charCount.isdigit():
					charCount = int(charCount)
				else:
					scribus.messageBox(
						'Error', 'Must be a number', icon=scribus.ICON_CRITICAL)
					return
			elif mode == str(4):
				toDelimiter = True
				delimiter = scribus.valueDialog( "Apply char style" , "What delimiter do you want to apply the style up until?" , "" )
				if len(delimiter)<1:
					scribus.messageBox(
						'Error', 'Delimiter cannot be empty string', icon=scribus.ICON_CRITICAL)
					return
			elif mode == str(5):
				useDelimiter = True
				delimiter = scribus.valueDialog( "Apply char style" , "What delimiter do you want to apply the style up to and including?" , "" )
				if len(delimiter)<1:
					scribus.messageBox(
						'Error', 'Delimiter cannot be empty string', icon=scribus.ICON_CRITICAL)
					return
			#we need to escape delimiter if it is a period
			if delimiter == ".":
				delimiter = "\."




	with open(fileName, mode='r', encoding='utf8') as f:
		data = f.read()
		#remove soft hyphen in hyphenated words, my nemesis
		data = re.sub('(\w*)\u00AD(\w*-\w*)', r'\1\2', data)
		data = re.sub('(\w*-\w*)\u00AD(\w*)', r'\1\2', data)
		
		#remove soft hyphen in last word before paragraph break
		data = re.sub('(\w*)\u00AD(\w*)\u00AD(\w*)\u00AD(\w*.{,3}/>)', r'\1\2\3\4', data)
		data = re.sub('(\w*)\u00AD(\w*)\u00AD(\w*.{,3}/>)', r'\1\2\3', data)
		data = re.sub('(\w*)\u00AD(\w*.{,3}/>)', r'\1\2', data)
		
		#remove soft hyphen all words up to X characters from the paragraph break
		if LastLine == True:
			NUM = "{,"+str(LLLength)+"}"
			data = re.sub(f'(\w*)\u00AD(\w*)\u00AD(\w*)\u00AD(.{NUM}/>)', r'\1\2\3\4', data)
			data = re.sub(f'(\w*)\u00AD(\w*)\u00AD(.{NUM}/>)', r'\1\2\3', data)
			data = re.sub(f'(\w*)\u00AD(.{NUM}/>)', r'\1\2', data)

		
		#insert nonbreaking space before last X characters
		nonbreak = '\u00A0'
		#data = re.sub('[ ](\S{,10}/>\s*<para/>)', fr'{nonbreak}\1', data)
		NUM = "{1,"+str(RUNT)+"}"
		if data.find('<SCRIBUSUTF8NEW Version="1.6')>1 or data.find('<SCRIBUSUTF8NEW Version="1.5')>1 or data.find('<SCRIBUSUTF8NEW Version="1.7.0')>1:
			data = re.sub(f'(CH=".*)[ ](\S{NUM}/>\s*<para)', fr'\1{nonbreak}\2', data)
		else:
			data = re.sub(f'(Chars=".*)[ ](\S{NUM}/>\s*<para)', fr'\1{nonbreak}\2', data)
			
			
		#insert nonbreaking space before last X characters
		nonbreak = '\u00A0'
		if data.find('<SCRIBUSUTF8NEW Version="1.6')>1 or data.find('<SCRIBUSUTF8NEW Version="1.5')>1 or data.find('<SCRIBUSUTF8NEW Version="1.7.0')>1:
			data = re.sub(f'—', fr'"/>\n                <zwnbspace CPARENT="Default Character Style"/>\n                <ITEXT CH="—', data)
		else:
			data = re.sub(f'(Chars=".*)[ ](\S{NUM}/>\s*<para)', fr'\1{nonbreak}\2', data)
		

		#insert frame break where selected style found
		#paragraph formatting changed in Scribus 1.7.1 so we need an alt replacement for those files
		if FrameBreaks == True:
			if data.find('<SCRIBUSUTF8NEW Version="1.6')>1 or data.find('<SCRIBUSUTF8NEW Version="1.5')>1 or data.find('<SCRIBUSUTF8NEW Version="1.7.0')>1:
				data = re.sub(f'(\s*)(<ITEXT.*/>\s*<para PARENT=\"{heading}\"/>)', r'\1<para/>\1<breakframe/>\1\2', data)
			else:
				data = re.sub(f'(\s*)(<Content Chars.*/>\s*<para Parent=\"{heading}\"/>)', r'\1<para/>\1<breakframe/>\n                \2', data)
			

		#apply character style to first X of selected paragraph style
		if charStyle == True:
			if data.find('<SCRIBUSUTF8NEW Version="1.6')>1 or data.find('<SCRIBUSUTF8NEW Version="1.5')>1 or data.find('<SCRIBUSUTF8NEW Version="1.7.0')>1:
				if wordCount > 0:
					NUM = "{"+str(wordCount)+"}"
					data = re.sub(f'(\s*)(<ITEXT CH=\")((\S+\s){NUM})(.*/>)(\s*<para PARENT=\"{headingF}\"/>)', fr'\1<ITEXT CPARENT="{styleChar}" CH="\3"/>\1\2\5\1<para PARENT="{headingF}"/>', data)
				elif charCount > 0:
					NUM = "{"+str(charCount)+"}"
					data = re.sub(f'(\s*)(<ITEXT CH=\")(.{NUM})(.*/>)(\s*<para PARENT=\"{headingF}\"/>)', fr'\1<ITEXT CPARENT="{styleChar}" CH="\3"/>\1\2\4\1<para PARENT="{headingF}"/>', data)
				elif useDelimiter == True: 
					data = re.sub(f'(\s*)(<ITEXT CH=\")(.*?{delimiter})(.*/>)(\s*<para PARENT=\"{headingF}\"/>)', fr'\1<ITEXT CPARENT="{styleChar}" CH="\3"/>\1\2\4\1<para PARENT="{headingF}"/>', data)
				elif toDelimiter == True: 
					data = re.sub(f'(\s*)(<ITEXT CH=\")(.*?){delimiter}(.*/>)(\s*<para PARENT=\"{headingF}\"/>)', fr'\1<ITEXT CPARENT="{styleChar}" CH="\3"/>\1\2{delimiter}\4\1<para PARENT="{headingF}"/>', data)
			#if Scribus 1.7.1 or later. If they change the dang XML formatting again this will break in the future but is tested to work on 1.7.2		
			else:
				if wordCount > 0:
					NUM = "{"+str(wordCount)+"}"
					data = re.sub(f'(\s*)(<Content Chars=\")((\S+\s){NUM})(.*/>)(\s*<para Parent=\"{headingF}\"/>)', fr'\1\1<Content CParent="{styleChar}" Chars="\3"/>\1<Content Chars="\5\6', data)
				elif charCount > 0:
					NUM = "{"+str(charCount)+"}"
					data = re.sub(f'(\s*)(<Content Chars=\")(.{NUM})(.*/>)(\s*<para Parent=\"{headingF}\"/>)', fr'\1<Content CParent="{styleChar}" Chars="\3"/>\1<Content Chars="\4\5', data)
				elif useDelimiter == True: 
					data = re.sub(f'(\s*)(<Content Chars=\")(.*?{delimiter})(.*/>)(\s*<para Parent=\"{headingF}\"/>)', fr'\1<Content CParent="{styleChar}" Chars="\3"/>\1<Content Chars="\4\5', data)
				elif toDelimiter == True: 
					data = re.sub(f'(\s*)(<Content Chars=\")(.*?){delimiter}(.*/>)(\s*<para Parent=\"{headingF}\"/>)', fr'\1<Content CParent="{styleChar}" Chars="\3"/>\1<Content Chars="{delimiter}\4\5', data)
					
					
					
		with open(writeName, mode='w', encoding='utf8') as w:
			w.write(data)
		


if __name__ == '__main__':
	main()
