#  RenumberSplitPages.py
#  Sometimes you have to split a book into multiple scribus files because it starts lagging. This is a script to then go back and adjust the page numbers of all those files so they count up sequentially file-to-file. It also checks to make sure you have correct alternating left-right pages across files.
#
#  This script must be run within scribus. The files to renumber must all be in the same directory.
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
	
	START_RIGHT = False
	LAST_SIDE_RIGHT = False
	LAST_COUNT = 0
		
	scribus.messageBox("Script settings", 'This script is designed to take a folder of Scribus docs which have been separated for size reasons and align the page numbers so the outputted PDFs can be combined.\n\nIt will work if you start "page one" of the book on a later document page for the FIRST document (ex: you have un-numbered front matter) but will not work if you have multiple sections in subsequent documents. Your files must all be in the same folder.')
	
	mode = scribus.valueDialog( "Script settings" , "There are two methods for sorting works - a user-sorted list or prefix based. \n\nEnter 1, 2, or 3:\n1: Generate List mode (Scribus will copy all file names into a .txt document, you must\nthen open that list, order the works correctly and save before continuing)\n2: Continue using previously generated list using mode 1\n3: Use all .sla files in the folder in alphanumeric order (Will only work correctly if\nyou've given all filenames prefixes so they sort correctly)" , "")
	
	if mode == str(1):
		basehtml = scribus.fileDialog('Select a source folder that contains your files', isdir=True)
		list_files = os.listdir(basehtml)
		writeName = basehtml+'/RenumberOrder.txt'
		with open(writeName, mode='w', encoding='utf8') as f:
			for entry in list_files:
				if entry.endswith('.sla') or entry.endswith('.SLA'):
					f.write(entry+'\n')
		return 0
		scribus.messageBox("message", "List made! Before running script again, open the file RenumberOrder.txt and reorder the works (each on its own line) to the correct order. The first work should be on the first line.")
	elif mode == str(2):
		scribus.messageBox("message", "Processing Mode: in the next dialogue, select a source folder that contains your files and the RenumberOrder.txt list of works in your chosen order.")
		basehtml = scribus.fileDialog('Select a source folder that contains your files and the RenumberOrder file', isdir=True)
		
		#use anthologyEntries.txt file to make the list of files we will process
		list_files = []
		with open(basehtml+'/RenumberOrder.txt', mode='r', encoding='utf8') as f:
			list_files = f.read().split('\n')
			for entry in list_files:
				if len(entry)<3:
					list_files.remove(entry)
				elif entry.endswith('.sla') or entry.endswith('.SLA'):
					pass
				else:
					scribus.messageBox("error", "All works in list MUST be .sla files contained within the folder. Exiting...")
					return 0
	elif mode == str(3):
		basehtml = scribus.fileDialog('Select a source folder that contains your files', isdir=True)
		list_files = os.listdir(basehtml)
		for entry in list_files:
				if len(entry)<3:
					list_files.remove(entry)
				elif entry.endswith('.sla') or entry.endswith('.SLA'):
					pass
				else:
					list_files.remove(entry)
		list_files.sort()
	else:
		scribus.messageBox("error", "Select mode 1, 2, or 3 to run the script. Exiting...")
		return 0
		
	scribus.messageBox("message", "The selected file order for the files in the chosen directory are: "+str(list_files))
	
	count = 1
	for entry in list_files:
		fileName = basehtml+'/'+entry
		writeName = basehtml+'/Renumbered_'+entry
		
		with open(fileName, mode='r', encoding='utf8') as f:
			data = f.read()
			#get what side we start on
			if data.find('<Set Name="Facing Pages" FirstPage="1"')>0:
				START_RIGHT = True
			elif data.find('<Set Name="Facing Pages" FirstPage="0"')>0:
				pass
			else:
				scribus.messageBox("message", "Improper file formatting, exiting...")
				return 0
			#get number of pages
			index = data.find('DOCUMENT ANZPAGES="')
			if index>0:
				index += len('DOCUMENT ANZPAGES="')
				CURRENT_PAGES = int(data[index:data.find('"', index)])
			else:
				scribus.messageBox("message", "Improper file formatting, exiting...")
				return 0
			#get what side last page is
			if CURRENT_PAGES % 2 == 0:
				if START_RIGHT == True:
					END_RIGHT = False
				else:
					END_RIGHT = True
			else:
				if START_RIGHT == True:
					END_RIGHT = True
				else:
					END_RIGHT = False
			#check if starts on right side
			if count>1:
				if START_RIGHT == PREV_RIGHT:
					scribus.messageBox("message", "File "+entry+"first page starts on the wrong side. Exiting")
					return 0
			index = data.rfind('<Section Number=')
			index = data.find('From="', index)
			index += len('From="')
			FROM = int(data[index:data.find('"', index)])
			index = data.find('Start="', index)
			index += len('Start="')
			START = int(data[index:data.find('"', index)])
			if count == 1:
				LAST_PAGE = CURRENT_PAGES - FROM
				scribus.messageBox("message", str(entry)+"! is the first work. This document has "+str(CURRENT_PAGES)+" pages. FROM is " +str(FROM)+" and START is "+str(START)+". The last page is "+str(LAST_PAGE)+" so the starting page number for the next doc will be "+str(LAST_PAGE+1))
			else:
				#LAST_PAGE = CURRENT_PAGES+LAST_COUNT
				index = data.find('Type="Type_1_2_3" Start="')+len('Type="Type_1_2_3" Start="')
				index2 = data.find('"', index)
				data = data[:index]+str(LAST_COUNT+1)+data[index2:]
				scribus.messageBox("message", str(entry)+"! this document has "+str(CURRENT_PAGES)+" pages. The previous last page was "+str(LAST_COUNT)+" so the starting page number for the current will be "+str(LAST_COUNT+1)+". Last page for the this will be "+str(LAST_COUNT+CURRENT_PAGES))
				LAST_PAGE += CURRENT_PAGES
			LAST_COUNT = LAST_PAGE
			PREV_RIGHT = END_RIGHT
			count += 1
			
			with open(writeName, mode='w', encoding='utf8') as w:
				w.write(data)
		

	
"""
if <Set Name="Facing Pages" FirstPage="1"
then first page right

if <Set Name="Facing Pages" FirstPage="0"
then first page left

# of pages found at
DOCUMENT ANZPAGES="11"

#section numbers, want last item starting with <Section Number>
<Section Number="1" Name="1" From="11" To="11" Type="Type_1_2_3" Start="10" 

open doc 1
get starting page side
get ending page side
get ending page number (to-from+start)

for doc in list:
	open doc
	get starting page side
		if page side not different than ending page side, exit program
	set section Start = EPN+1
	else get ending page number (start+pages)


"""
	




if __name__ == '__main__':
	main()
