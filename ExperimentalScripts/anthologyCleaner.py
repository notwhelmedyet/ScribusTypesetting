#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  anthologyCleaner.py
#  a program for cleaning up various spacing/italics/typographic quote issues in ao3 downloads for faster import into scribus. This script works on a directory of files which are intended to be appended together and typeset as an anthology. This script must be run within scribus.
#  #  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
"""

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

	htmlHeader = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"><head> <meta charset="utf-8" /> <meta http-equiv="x-ua-compatible" content="ie=edge" /></head><body>'
	#FIC SPECIFIC VARIABLES, edit as needed.
	scenebreakList = ['<hr>', '<p>—</p>', '<p align="center">~*~</p>', '<p align="center">*</p>', '<p align="center">***</p>']
	breakcharacter = '*' #what character do you want breaks to be in your chosen ornament font?
	newDash = '—' #replace with your preferred dash. UK Standard: spaced en dash, US Standard: unspaced em dash.
	#if set to True, the fic will turn multiple empty paragraphs used as a break
	#into the same scenebreak as used for ornamented breaks
	#if set to false they will be turned into a single space (still using our ornament style to give us spacing above & below)	
	ornamentAllBreaks = False 
	#if you don't want the script to try and replace dashes, set this to True
	LeaveDashesAlone = True
	#if you don't want the script to try and swap straight quotes for typographic quotes, set this to true
	LeaveQuotesAlone = True
	#if you want to keep the tags in the document (will be left unformatted at the top of the document), set this to True
	#if set to False all metadata except the fic title and author will be removed
	KeepTags = True
	#if set to false, any br spaces used in the fic will be discarded
	#if set to true, they'll be kept, but won't be converted or processed
	keepBr = True
	workCount = 1
	multiAuthor = True

	# the code! the code itself!! 
	# Opening our text file in read only
	# mode using the open() function
	mode = scribus.valueDialog( "Script settings" , "This script is designed to take a folder of AO3-formatted html works and make a combined copy formatted for Scribus importing in your chosen order.\nThe script must be run twice: once to make the list of works and once to process those works.\n\nEnter 1 or 2:\n1: Initial run, generate list of works in folder\n2: Second run, make combined anthology document" , "")

	if mode==str(1):
		basehtml = scribus.fileDialog('Select a source folder that contains your anthology works', isdir=True)
		list_files = os.listdir(basehtml)
		scribus.messageBox("message", "The selected directory is: "+str(list_files))
		writeName = basehtml+'/AnthologyEntries.txt'
		
		with open(writeName, mode='w', encoding='utf8') as f:
			for entry in list_files:
				if entry.endswith('.html') or entry.endswith('.HTML'):
					f.write(entry+'\n')
		
		scribus.messageBox("message", "List made! Before running script again, open the file AnthologyEntries.txt and reorder the works (each on its own line) to the order you want them in the typeset version")
	if mode==str(2):
		scribus.messageBox("message", "Processing Mode: in the next dialogue, select a source folder that contains your anthology works and the AnthologyEntries.txt list of works in your chosen order.")
		basehtml = scribus.fileDialog('Select a source folder that contains your anthology works & AnthologyEntries file', isdir=True)
		
		#use anthologyEntries.txt file to make the list of files we will process
		list_files = []
		with open(basehtml+'/AnthologyEntries.txt', mode='r', encoding='utf8') as f:
			list_files = f.read().split('\n')
			for entry in list_files:
				if len(entry)<4:
					list_files.remove(entry)
				elif entry.endswith('.html') or entry.endswith('.HTML'):
					pass
				else:
					scribus.messageBox("error", "All works in list MUST be html files contained within the folder. Exiting...")
					return 0
	else:
		return 0
		
	#Uses the Scribus ValueDialog to set the values for the above-defined importing variables.
	breakcharacter = scribus.valueDialog( "Script settings" , "This script is designed to take AO3-formatted html and make a copy formatted for Scribus importing.\n\nPlease enter the character(s) from your chosen ornament font glyph that will be used as a scene break" , "" )
	defaults = scribus.valueDialog( "More settings?", "By DEFAULT the script will do the following:\n - Include the author name after each work title\n - look for horizontal rules as the fics' scene breaks to swap for our break ornament\n - not swap any dashes to em/en dashes \n - treat consecutive multiple paragraph breaks as a scene break (and insert a blank line in the ornament style)\n - not change any straight quotes to typographic quotes.\n - send (unformatted) tags and metadocs to a separate file called AnthologyMeta.html\n\nTo accept these settings type 1 and enter. To edit these settings type any other character", "")
	if defaults != str(1):
		authorSelector = scribus.valueDialog( "Author selector" , "Enter 1 or 2.\n1: This is a multi-author anthology, include the author name with each entry \n2: This is a single-author anthology, only include the author name with the first entry" , "" )
		if authorSelector != str(1):
			multiAuthor = False
			
		scribus.messageBox("message", "Currently the script is looking for the following scene breaks in the files being processed: horizontal rules, centered em dash, centered *, centered ***, centered ~*~")
		addBreaks = scribus.valueDialog( "Current breaks" , "Please paste the HTML for any additional breaks used in the works being processed. Separate multiple entries with commas (NO SPACE) " , "" )
		if len(addBreaks)>2:
			breakBreaks = addBreaks.split(",")
			for b in breakBreaks:
				scenebreakList.append(b)
	
		dashSelector = scribus.valueDialog( "Dash selector" , "Enter 1, 2, or 3.\n1: Do not edit any dashes \n2: Replace dashes with un-spaced em dash \n3: Replace dashes with spaced en dash" , "" )
		if dashSelector == str(1):
			LeaveDashesAlone = True
		elif dashSelector == str(2):
			newDash = '—'
		elif dashSelector == str(3):
			newDash = ' – '
		breakSelector = scribus.valueDialog( "Break selector" , "Enter 1 or 2.\n1: Treat multiple paragraph breaks as a break (don't add ornament) \n2: Treat multiple paragraph breaks as a break (use usual ornament)", "1" )
		if breakSelector == str(1):
			OrnamentAllBreaks = False
		elif breakSelector == str(2):
			OrnamentAllBreaks = True
		quoteSelector = scribus.valueDialog("Change typographic quotes", "Enter 1 to swap straight quotes to typographic quotes (English-style quotes only), enter any other character to leave quotes unchanged", "")
		if quoteSelector == str(1):
			LeaveQuotesAlone = False
		
	if defaults == str(1):
		result = scribus.messageBox ('Script Settings','Default settings selected! breakcharacter: '+breakcharacter+'\n\nThe output will be saved as Anthology.html, metadata will be saved in AnthologyMeta.html, processing notes will be logged in AnthologyLog.txt. These files will be overwritten when you next run this script! Please check your file before importing into Scribus & save a copy if needed',scribus.BUTTON_OK)		
	elif LeaveDashesAlone:
		result = scribus.messageBox ('Script Settings','Settings selected:\nmulti author: '+str(multiAuthor)+'\nornamentAllBreaks: '+str(ornamentAllBreaks)+'\nLeaveDashesAlone: '+str(LeaveDashesAlone)+'\nLeaveQuotesAlone: '+str(LeaveQuotesAlone)+'\n\nThe output will be saved as Anthology.html, metadata will be saved in AnthologyMeta.html, processing notes will be logged in AnthologyLog.txt.\nThese files will be overwritten when you next run this script!\nPlease check your file before importing into Scribus & save a copy if needed',scribus.BUTTON_OK)
	else:
		result = scribus.messageBox ('Script Settings','Settings selected:\n\nmulti author: '+str(multiAuthor)+'\nbreakcharacter: '+breakcharacter+'\nnewDash: '+newDash+'\nornamentAllBreaks: '+str(ornamentAllBreaks)+'\nLeaveDashesAlone: '+str(LeaveDashesAlone)+'\nLeaveQuotesAlone: '+str(LeaveQuotesAlone)+'\n\nThe output will be saved as Anthology.html, metadata will be saved in AnthologyMeta.html, processing notes will be logged in AnthologyLog.txt.\nThese files will be overwritten when you next run this script!\nPlease check your file before importing into Scribus & save a copy if needed',scribus.BUTTON_OK)
		
	newbreak = '<h5>'+breakcharacter+'</h5>' #our break set in the ornament style
	minibreak = '<h5>MINIBREAK</h5>'
	minispacebreak = '<h5> </h5>'
	log = ''

	logName = basehtml+'/AnthologyLog.txt'
	metaName = basehtml+'/AnthologyMeta.html'
	writeName = basehtml+'/Anthology.html'
	
	with open(logName, mode='w', encoding='utf8') as log, open(metaName, mode='w', encoding='utf8') as meta, open(writeName, mode='w', encoding='utf8') as anthology:
		log.write('Processing files into a combined anthology source document: '+str(list_files))
		log.write('\nIn Directory: '+str(basehtml))
		log.write('\nSettings selected:\multi author: '+str(multiAuthor)+'\nscenebreak: '+str(scenebreakList)+'\nbreakcharacters: '+str(breakcharacter)+'\nnewDash: '+newDash+'\nornamentAllBreaks: '+str(ornamentAllBreaks)+'\nLeaveDashesAlone: '+str(LeaveDashesAlone)+'\nLeaveQuotesAlone: '+str(LeaveQuotesAlone)+'\n\nThe output will be saved as Anthology.html. These files will be overwritten when you next run this script!\nPlease check your file before importing into Scribus & save a copy if needed')
		
		anthology.write(htmlHeader)
		meta.write(htmlHeader)
		
		for entry in list_files:
			with open(basehtml+'/'+entry, mode='r', encoding='utf8') as f:
				data = f.read()
				#scribus.messageBox("message", "Running for file: "+str(entry)+" work count is: "+str(workCount))
				log.write('\n\nProcessing file: '+str(entry))
				
				#remove all tabs, newlines and duplicate spaces
				#log.write("Removing all linebreaks for processing....")
				data = data.replace('\t', '')
				data = data.replace('\n', '')
				
				#sometimes our scene break is surrounded by <span></span>. We need to axe those so we can get rid of the sdans, which otherwise mess up our italic spacing correction
				#EDIT POINT
				for b in scenebreakList:
					if b.find('<span>')>1:
						nospanbreak = b.replace('span>', 'p>')
						data = data.replace(b, nospanbreak)
						scenebreakList.remove(b)
						scenebreakList.append(nospanbreak)
				data = data.replace('<span>', '')
				data = data.replace('</span>', '')
				
				data = re.sub(r'\s{2,}', ' ', data)	
				data = data.replace('/p> <p>', '/p><p>')
				data = data.replace('<p>\s<p>', '<p></p>')
				
				# swapping italics and bold to a single method for consistency
				log.write("\n\nSwapping italics and bolds to a single format for processing...")
				log.write("\nSwapping italic to emphasis: "+str(data.count('i>')))
				data = data.replace('i>', 'em>')
				log.write("\nSwapping b to strong: "+str(data.count('<b>')))
				data = data.replace("<b>", "<strong>")
				data = data.replace("</b>", "</strong>")
								
				log.write("\n\nRemoving/reordering extra spaces...")
				log.write("\nwhere italic bracketed by spaces: "+str(data.count(' <em> ')))		
				data = data.replace(' <em> ', ' <em>')
				log.write("\nwhere italic start has internal space: "+str(data.count('<em> ')))
				data = data.replace('<em> ', ' <em>')
				log.write("\nwhere end italic bracketed by spaces: "+str(data.count(' </em> ')))
				data = data.replace(' </em> ', '</em> ')
				#italic separated from punctuation by space
				data = re.sub(' (</em>[,.?!])', r'\1', data)
				data = re.sub('</em> ([,.?!])', '</em>'+r'\1', data)
				data = re.sub('(["“”]) <em>', r'\1'+'<em>', data)
				log.write("\nwhere end italic preceeded by spaces: "+str(data.count(' </em>')))
				data = data.replace(' </em>', '</em> ')		
				log.write("\nend of paragraphs: "+str(data.count(' </p>')))
				data = data.replace(' </p>', '</p>')
				log.write("\nwhere bold bracketed by spaces: "+str(data.count(' <strong> ')))
				data = data.replace(' <strong> ', ' <strong>')
				log.write("\nwhere bold start has internal space: "+str(data.count('<strong> ')))
				data = data.replace('<strong> ', ' <strong>')
				log.write("\nwhere end bold bracketed by spaces: "+str(data.count(' </strong> ')))
				data = data.replace(' </strong> ', '</strong> ')
				#bold separated from punctuation by space
				data = re.sub(' (</strong>[,.?!])', r'\1', data)
				data = re.sub('(</strong> [,.?!])', r'\1', data)
				data = re.sub('(["“”]) <strong>', r'\1'+'<strong>', data)
				log.write("\nwhere end bold preceeded by spaces: "+str(data.count(' </strong>')))
				data = data.replace(' </strong>', '</strong> ')	
				
				#now that we've reordered the italic and bold we might have errant spaces, fix those
				#log.write("start of paragraphs: ", data.count('<p> <'))
				data = re.sub('<p>\s<', '<p><', data)	
				#log.write("end of paragraphs: ", data.count(' </p>'))
				data = re.sub('\s</p>', '</p>', data)

				#only useful if the fic had used headers for something and we're going to fuck it up via formatting whooops
				log.write("\n\nThese headers will be replaced by the script to use to mark chapters, chapter breaks, and scene breaks.\nIf these headers were already in use you may lose formatting from the author. Check if count>0")
				log.write("\nh3: "+str(data.count('</h3>')))
				log.write("\nh4: "+str(data.count('</h4>')))
				log.write("\nh5: "+str(data.count('</h5>')))		

				#Removing chapter notes
				data = re.sub('(<h2 class="heading">.*?</h2>).*?<!--chapter content-->', r'\1', data)
				data = re.sub('</div><!--/chapter content-->.*?<h2 class="heading">', '<h2 class="heading">', data)
				data = re.sub('<div id="afterword">.*?</body>', '</body>', data)
				data = re.sub('</div><!--/chapter content-->.*?</body>', '</body>', data)
				data = re.sub('<h2.*?>', '<h2>', data)

				#remove more top matter
				#keep tags version
				title = data[data.find('<h1>')+4:data.find('</h1>')]
				data = re.sub('<div class="byline">by <a.*?href=".*?>', '<BYLINE>', data)
				data = re.sub('<BYLINE>(.*?)</a>', r'<BYLINE>\1</BYLINE>', data)
				author = data[data.find('<BYLINE>')+8:data.find('</BYLINE>')]
				 
				
				data = data.replace('<dt>', '<p>')
				data = data.replace('</dd>', '</p>')
				data = data.replace("<dd>", "")
				data = data.replace("</dt>", "")	
				data = data.replace("</dl>", "")
				data = re.sub('<p>Notes</p>.*?<div class="meta group">', "", data)
				data = data.replace('<div class="meta"> <dl class="tags">', "")
				data = re.sub('(<p>Summary</p>.*?)</blockquote>', r'\1', data)
				data = data.replace('<blockquote class="userstuff">', "")
				data = data.replace('<div class="userstuff">', "")
				data = re.sub('<BYLINE>(.*?)</div>', r'<h1>\1</h1>', data)
				data = re.sub('<div id="preface">.*?</h2>', "", data)
				data = data.replace('<p class="message">', '<p>')

				#remove links from tags
				data = re.sub('<a.*?href=".*?>', '', data)
				data = data.replace('</a>, ', ', ')
				data = data.replace('</a>', '')
				data = data.replace('&#39;', "’")

				#save topmatter before messing with dashes/quotation marks
				topmatter_index = data.find('<h2>')
				tagdata = data[:topmatter_index]
				tagdata = re.sub('<!DOCTYPE.*?<p>Rating:', '<p>Rating:', tagdata)
				tagdata = tagdata[:tagdata.find('<h1>')]
				tagdata = tagdata.replace(' <p>Stats:  Published: ', ' <p>First Published: ')
				tagdata = tagdata.replace(' Updated: ', '</p> <p>Last Updated: ')
				tagdata = tagdata.replace(' Words: ', '</p> <p>Words: ')
				tagdata = tagdata.replace(' Chapters: ', '</p> <p>Chapters: ')
				tagdata = re.sub('Chapters: .*?/', 'Chapters: ', tagdata)
				tagdata = re.sub('Series: Part (\d*) of', r'Series: Part \1 of ', tagdata)
				tagdata = tagdata.replace('</p> <p>', '</p>\n<p>')
				meta.write('<p>'+title+'</p>\n')
				if multiAuthor == True:
					meta.write('<p>'+author+'</p>\n')
				elif workCount < 2:
					meta.write('<p>'+author+'</p>\n')
				#meta.write(author+'\n')
				meta.write(tagdata)
				data = data[topmatter_index:]

						
				
				#swap all dashes in fic for the selected dash newDash
				if not LeaveDashesAlone:
					log.write('\nAutomatically converting dashes to'+newDash)
					log.write('\nAuthor used the following dashes:')
					log.write("\nEm dash: "+str(data.count('—')))
					log.write("\nSpaced em dash: "+str(data.count(' — ')))
					log.write("\nEn dash: "+str(data.count('–')))
					log.write("\nSpaced en dash: "+str(data.count(' – ')))
					log.write("\nSpaced hyphens: "+str(data.count(' - ')))
					log.write("\nDoubled hyphens: "+str(data.count('--')))
					data = data.replace('--', newDash)
					data = data.replace(' — ', newDash)
					data = data.replace('—', newDash)
					data = data.replace('<strong>–</strong>', '–')
					data = data.replace(' - ', newDash)
					data = data.replace(' -', newDash)
					data = data.replace('- ', newDash)
					data = data.replace(' – ', newDash)
					data = data.replace(' –', newDash)
					data = data.replace('– ', newDash)
					data = data.replace('–', newDash)
				
				#swap ... to elipsis
				data = data.replace('...', '…')
				data = data.replace('. . .', '…')

				#One more shot at removing bonus spaces
				data = data.replace(' </p>', '</p>') 
				data = data.replace('<p> ', '<p>')
				data = data.replace('<h3> ', '<h3>')
				data = data.replace('<h4> ', '<h4>')
				
				#remove all breaks. If the author is using them as scene breaks, this will...break things. Otherwise this clears out extra unneeded spaces
				if not keepBr:
					data = re.sub('<br.*?>', '', data)
					data = data.replace('<br>', '')

				#find and replace multiple paragraph breaks in a row, either deleting them if the fic is double spaced or treating them as scene breaks
				data = re.sub('(<p></p>){2,}', minibreak, data) #if double spaces are used as extra breaks, replace. This will not work for authors with double spaces between every line, or who have extra spaces above and below normal breaks
				data = data.replace('</p><p></p><p>', '</p>'+minibreak+'<p>')
				data = data.replace('<p></p>', '')
				
				#replace scene breaks and make scene starts <h5>		
				log.write("\n\nReplacing fic scene breaks with selected breakCharacter: "+breakcharacter)
				data = re.sub('<hr.*?>', '<hr>', data)
				for b in scenebreakList:
					data = data.replace(b, newbreak)
				data = data.replace( newbreak+minibreak, newbreak) #if they've double spaced before or after their breaks fix
				data = data.replace( minibreak+newbreak, newbreak) #if they've double spaced before or after their breaks fix
				data = data.replace('</h5><p>', '</h5><h4>')
				data = re.sub('(<h4>.*?)</p>', r'\1</h4>', data)
				log.write("\nTurning the first paragraph after each scene break to <h4>")
				if ornamentAllBreaks:
					data = data.replace(minibreak, newbreak)
					log.write("\nBecause OrnamentAllBreaks=True, double paragraph spaces swapped to our ornament symbol glyph")
				else:
					data = data.replace(minibreak, minispacebreak)
					log.write("\nBecause OrnamentAllBreaks=False, double paragraph spaces swapped to a ornament-styled blank line")

				#Making chapter start paragraphs <h3>
				log.write("\nTurning the first paragraph after each chapter to <h3>")
				data = data.replace('</h2> <p>', '</h2><h3>')
				data = re.sub('(<h3>.*?)</p>', r'\1</h3>', data)

				
				#for text that doesn't have typographic quotes
				if not LeaveQuotesAlone:
					log.write("\nAutomatically correcting typographic quotes - keep alert for quotation mark errors in typeset")
					data = data.replace('&ldquo;', '"') #swap out any errant html code formats instead of glyphs
					data = data.replace('&rdquo;', '"')
					data = data.replace('&quot;', '"')
					data = data.replace('&apos;', "'")
					data = data.replace('&lsquo;', "'")
					data = data.replace('&rsquo;', "'")
					data = data.replace('"', "”")
					data = data.replace('"', "”")
					data = data.replace('<p>”', '<p>“') #quote at start of paragraph is opener
					data = data.replace('<em>”', '<em>“') #quote after em is opener
					data = data.replace('<strong>”', '<strong>“') #quote after bold is opener
					data = re.sub('(\s)”', r'\1“', data) #quote after space is opener
					data = data.replace("'", "’")
					data = data.replace("<p>’", "<p>‘") #quote at start of paragraph is opener
					data = data.replace("<em>’", "<em>‘") #quote at start of paragraph is opener
					data = data.replace("<strong>’", "<strong>‘") #quote at start of paragraph is opener
					data = re.sub("(\s)’", r"\1‘", data) #quote after space is opener
					#apostrophe exceptions
					data = re.sub("‘([e,E]m\W)", r"’\1", data) #'em
					data = re.sub("‘([t,T]is\W)", r"’\1", data) #'tis
					data = re.sub("‘([t,T]was\W)", r"’\1", data) #'twas		
					data = re.sub("‘([t,T]wixt\W)", r"’\1", data) #'twixt
					data = re.sub("‘([t,T]il\W)", r"’\1", data) #'til
					data = re.sub("‘([s,S]cuse\W)", r"’\1", data) #'scuse
					data = re.sub("‘([r,R]ound\W)", r"’\1", data) #'round
					data = re.sub("‘([c,C]ause\W)", r"’\1", data)	
					data = re.sub("‘([m,M]\W)", r"’\1", data)	
					data = re.sub("‘(\d)", r"’\1", data) #year abbreviations
					
				
				#put all the line breaks back
				#log.write("Replacing line breaks: ")
				data = data.replace('</p>', '</p>\n')
				data = data.replace('<h1>', '\n\n<h1>') #spaces above fic title to make them easier to see (in case you combine documents for an anthology later)
				data = data.replace('</h1>', '</h1>\n')
				data = data.replace('<h2>', '\n\n<h2>') #spaces above chapters to make them easier to see
				data = data.replace('</h2>', '</h2>\n')
				data = data.replace('</h3>', '</h3>\n')
				data = data.replace('</h4>', '</h4>\n')
				data = data.replace('</h5>', '</h5>\n')
				data = data.replace('</blockquote>', '</blockquote>\n')
				
				#remove /body/html at end of each work
				data = data[:data.find('</body></html>')]
				
				log.write("\n\nChecking for one and two character italics")
				log.write("\nthese may be errors that need correcting:")
				emlist = set(re.findall(r'<em>.{1,2}</em>', data))
				for i in emlist:
					log.write('\n')
					log.write(i)


				log.write("\n\nChecking for one and two character bolds")
				log.write("\nthese may be errors that need correcting:")
				stronglist = set(re.findall(r'<strong>.{1,2}</strong>', data))
				for i in stronglist:
					log.write('\n')
					log.write(i)
			
				#TEST NOT WORKING?
				title = '<h1>'+title+'<h1>'
				author = '<h6>'+author+'</h6>'
				anthology.write(title+'\n')
				if multiAuthor == True:
					anthology.write(author+'\n')
				elif workCount < 2:
					anthology.write(author+'\n')
				#anthology.write(author+'\n')
				anthology.write(data)
				meta.write('\n\n')
				workCount += 1
			
		anthology.write('</body></html>')
		meta.write('</body></html>')	
	
	return 0
	 
if __name__ == '__main__':
	main()
