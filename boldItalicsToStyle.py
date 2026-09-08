#  swapItalics.py
#  This script transforms the html import manual bold/italic/bold italics into character styles
#  If bold/italic/bold italic char styles don't exist before you run the script it will create them
#  
#  Additionally, if you imported html into the same document twice and Scribus responded by manually applying your 
#  substitution fonts to all the html header styles, this font will fix those (as long as you haven't replaced the html styles yet)
#  You can always avoid that bug by only imporitng your html once and, if you mess up the import, closing the document without saving and reloading
#  But this script will fix it for you, if you forget.
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
	
	scribus.messageBox("Script settings", "This script is designed to take the currently open Scribus file, open the source XML document and edit a copy swapping italic, bold and/or bold italic local styles to corresponding character styles.\n\nIt will save a separate copy of your file named [FILENAME]_SWAPPED.sla. If you don't have existing character styles named Bold, Italic and BoldItalic, it will create them at runtime.\n\nAdditionally, it will fix the bug where duplicate imports hard code bold styles to html headers.")
	fileName = scribus.getDocName()
	entry = fileName.rsplit('.sla', 1)[0]
	writeName = entry+"_SWAPPED.sla"
	
	
	with open(fileName, mode='r', encoding='utf8') as f:
		data = f.read()
		if data.find('<SCRIBUSUTF8NEW Version="1.6')>1 or data.find('<SCRIBUSUTF8NEW Version="1.5')>1 or data.find('<SCRIBUSUTF8NEW Version="1.7.0')>1:		
			#remove auto bold for html headers
			numSwaps = len(re.findall(r'<ITEXT FONT=.* (CH.*/>\s*)(<para PARENT=\"HTML_h)', data))
			data = re.sub('<ITEXT FONT=.* (CH.*/>\s*)(<para PARENT=\"HTML_h)', r'<ITEXT \1\2', data)
			
			#swap bold, italic and bold italic to char styles
			fonts = re.findall(r'<ITEXT FONT=\"(.+?)\" ', data)
			fonts = list(set(fonts))
			if len(fonts)>=1:
				scribus.messageBox(
						'Fonts Used',
						f'fonts applied locally to text in the document are\n{fonts}\nTake note of these fonts so you can tell the script which ones you want to sub in the next dialogue.',
						icon=scribus.ICON_INFORMATION)
				fonts.append("None")

				#check if bold, italic and bold italic styles exist. if not, create them as clones of the default style
				testBold = re.search('CHARSTYLE CNAME=\"Bold\"', data)
				if not testBold:
					data = re.sub(r'(<CHARSTYLE CNAME=\"Default Character Style\".+/>)(\s*)<', r'\1\2<CHARSTYLE CNAME="Bold" CPARENT="Default Character Style"/>\2<', data)
				
				testItalic = re.search('CHARSTYLE CNAME=\"Italic\"', data)
				if not testItalic:
					data = re.sub(r'(<CHARSTYLE CNAME=\"Default Character Style\".+/>)(\s*)<', r'\1\2<CHARSTYLE CNAME="Italic" CPARENT="Default Character Style"/>\2<', data)
				
				testBItalic	=  re.search('CHARSTYLE CNAME=\"BoldItalic\"', data)
				if not testBItalic:
					data = re.sub(r'(<CHARSTYLE CNAME=\"Default Character Style\".+/>)(\s*)<', r'\1\2<CHARSTYLE CNAME="BoldItalic" CPARENT="Default Character Style"/>\2<', data)

				
				#substitute bold font
				try:
					boldFont = scribus.itemDialog( "Bold font search" , "Enter the name of the font currently applied to bold text", fonts)
				except:		
					boldFont = scribus.valueDialog( "Apply char style" , f"Enter the name of the font currently applied to bold text. Script will substitute the Bold character style. To skip, enter 0\n\nAvailable fonts are {fonts}" , "" )
				if boldFont!="0" and boldFont != "None":
					test = re.search(boldFont, data)
					if test:
						data = re.sub(fr'<ITEXT FONT=\"{boldFont}\" (CH.*/>)', r'<ITEXT CPARENT="Bold" \1', data)
						if boldFont in fonts:
							fonts.remove(boldFont)
					else:
						scribus.messageBox(
							'Error',
							f'The document does not use font {boldFont}, no replacements were made',
							icon=scribus.ICON_CRITICAL)
						
				#substitute italic font
				try:
					italicFont = scribus.itemDialog( "italic font search" , "Enter the name of the font currently applied to italic text", fonts)
				except:		
					italicFont = scribus.valueDialog( "italic font search" , f"Enter the name of the font currently applied to italic text. Script will substitute the italic character style. To skip, enter 0\n\nAvailable fonts are {fonts}" , "" )
				if italicFont!="0" and italicFont != "None":
					test = re.search(italicFont, data)
					if test:
						data = re.sub(fr'<ITEXT FONT=\"{italicFont}\" (CH.*/>)', r'<ITEXT CPARENT="Italic" \1', data)
						if italicFont in fonts:
							fonts.remove(italicFont)
					else:
						scribus.messageBox(
							'Error',
							f'The document does not use font {italicFont}, no replacements were made',
							icon=scribus.ICON_CRITICAL)
				
				#substitute BItalic		
				try:
					BItalicFont = scribus.itemDialog( "BItalic font search" , "Enter the name of the font currently applied to bold italic text", fonts)
				except:		
					BItalicFont = scribus.valueDialog( "BItalic font search" , f"Enter the name of the font currently applied to bold italic text. Script will substitute the BoldItalic character style. To skip, enter 0\n\nAvailable fonts are {fonts}" , "" )
				if italicFont!="0" and italicFont != "None":
					test = re.search(BItalicFont, data)
					if test:
						data = re.sub(fr'<ITEXT FONT=\"{BItalicFont}\" (CH.*/>)', r'<ITEXT CPARENT="BItalic" \1', data)
						if BItalicFont in fonts:
							fonts.remove(BItalicFont)
					else:
						scribus.messageBox(
							'Error',
							f'The document does not use font {BItalicFont}, no replacements were made',
							icon=scribus.ICON_CRITICAL)		
			if len(fonts)<1:
				scribus.messageBox(
					'Error',
					f'{numSwaps} hardcoded header styles were fixed. The document did not use any other bold, italic or bold italic substitution fonts.',
					icon=scribus.ICON_CRITICAL)

		else:
			#version of script for Scribus 1.7.1+
			numSwaps = len(re.findall(r'<Content Font=.* (Ch.*/>\s*)(<para Parent=\"HTML_h)', data))
			data = re.sub('<Content Font=.* (Ch.*/>\s*)(<para Parent=\"HTML_h)', r'<Content \1\2', data)
			fonts = re.findall(r'Content Font=\"(.+?)\" ', data)
			fonts = list(set(fonts))
			if len(fonts)>=1:
				fonts.append("None")

				#check if bold, italic and bold italic styles exist. if not, create them as clones of the default style
				testBold = re.search('CharacterStyle Name=\"Bold\"', data)
				if not testBold:
					data = re.sub(r'(<CharacterStyle Name=\"Default Character Style\".+/>)(\s*)<', r'\1\2<CharacterStyle Name="Bold" CParent="Default Character Style"/>\2<', data)
				
				testItalic = re.search('CharacterStyle Name=\"Italic\"', data)
				if not testItalic:
					data = re.sub(r'(<CharacterStyle Name=\"Default Character Style\".+/>)(\s*)<', r'\1\2<CharacterStyle Name="Italic" CParent="Default Character Style"/>\2<', data)
				
				testBItalic	=  re.search('CharacterStyle Name=\"BoldItalic\"', data)
				if not testBItalic:
					data = re.sub(r'(<CharacterStyle Name=\"Default Character Style\".+/>)(\s*)<', r'\1\2<CharacterStyle Name="BoldItalic" CParent="Default Character Style"/>\2<', data)

				'''
						scribus.messageBox(
					'Fonts Used',
					f'got to 1',
					icon=scribus.ICON_INFORMATION)	'''	
				#substitute bold font
				try:
					boldFont = scribus.itemDialog( "Bold font search" , "Enter the name of the font currently applied to bold text", fonts)
				except:		
					boldFont = scribus.valueDialog( "Apply char style" , "Enter the name of the font currently applied to bold text. Script will substitute the Bold character style. To skip, enter 0" , "" )
				if boldFont!="0" and boldFont != "None":
					test = re.search(boldFont, data)
					data = re.sub(fr'<Content Font=\"{boldFont}\" (Ch.*/>)', r'<Content CParent="Bold" \1', data)
				elif boldFont == "None":
					pass 
				else:
					scribus.messageBox(
						'Error',
						f'The document does not use font {boldFont}, no replacements were made',
						icon=scribus.ICON_CRITICAL)
					
				#substitute italic font
				try:
					ItalicFont = scribus.itemDialog( "Italic font search" , "Enter the name of the font currently applied to italic text", fonts)
				except:		
					ItalicFont = scribus.valueDialog( "Apply char style" , "Enter the name of the font currently applied to Italic text. Script will substitute the Italic character style. To skip, enter 0" , "" )
				if ItalicFont!="0" and ItalicFont != "None":
					data = re.sub(fr'<Content Font=\"{ItalicFont}\" (Ch.*/>)', r'<Content CParent="Italic" \1', data)
				elif ItalicFont == "None":
					pass 
				else:
					scribus.messageBox(
						'Error',
						f'The document does not use font {ItalicFont}, no replacements were made',
						icon=scribus.ICON_CRITICAL)
				
				#substitute BItalic		
				try:
					bItalicFont = scribus.itemDialog( "BItalic font search" , "Enter the name of the font currently applied to bold italic text", fonts)
				except:		
					bItalicFont = scribus.valueDialog( "Apply char style" , "Enter the name of the font currently applied to bold italic text. Script will substitute the BItalic character style. To skip, enter 0" , "" )
				if bItalicFont!="0" and bItalicFont != "None":	
					test = re.search(bItalicFont, data)
					data = re.sub(fr'<Content Font=\"{bItalicFont}\" (Ch.*/>)', r'<Content CParent="BoldItalic" \1', data)
				elif bItalicFont == "None":
					pass 
				else:
					scribus.messageBox(
						'Error',
						f'The document does not use font {bItalicFont}, no replacements were made',
						icon=scribus.ICON_CRITICAL)
			
			if len(fonts)<1:
				scribus.messageBox(
					'Error',
					f'{numSwaps} hardcoded header styles were fixed. The document did not use any other bold, italic or bold italic substitution fonts.',
					icon=scribus.ICON_CRITICAL)

					
		with open(writeName, mode='w', encoding='utf8') as w:
			w.write(data)
		


if __name__ == '__main__':
	main()
