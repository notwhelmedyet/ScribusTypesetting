#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  chapNumCommandLine.py
#  a program for adding chapter numbers to fics processed with my importCleaner.py script for faster import into scribus.
#  
#  Made in 2025 by Lynn Whelmed
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
#  
#  
import string
import re

def main(args):
	#types of numerals
	ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI', 'XXII', 'XXIII', 'XXIV', 'XXV', 'XXVI', 'XXVII', 'XXVIII', 'XXIX', 'XXX', 'XXXI', 'XXXII', 'XXXIII', 'XXXIV', 'XXXV', 'XXXVI', 'XXXVII', 'XXXVIII', 'XXXIX', 'XL', 'XLI', 'XLII', 'XLIII', 'XLIV', 'XLV', 'XLVI', 'XLVII', 'XLVIII', 'XLIX', 'L', 'LI', 'LII', 'LIII', 'LIV', 'LV', 'LVI', 'LVII', 'LVIII', 'LIX', 'LX', 'LXI', 'LXII', 'LXIII', 'LXIV', 'LXV', 'LXVI', 'LXVII', 'LXVIII', 'LXIX', 'LXX', 'LXXI', 'LXXII', 'LXXIII', 'LXXIV', 'LXXV', 'LXXVI', 'LXXVII', 'LXXVIII', 'LXXIX', 'LXXX', 'LXXXI', 'LXXXII', 'LXXXIII', 'LXXXIV', 'LXXXV', 'LXXXVI', 'LXXXVII', 'LXXXVIII', 'LXXXIX', 'XC', 'XCI', 'XCII', 'XCIII', 'XCIV', 'XCV', 'XCVI', 'XCVII', 'XCVIII', 'XCIX', 'C']
	LROMAN = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx', 'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii', 'xxix', 'xxx', 'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi', 'xxxvii', 'xxxviii', 'xxxix', 'xl', 'xli', 'xlii', 'xliii', 'xliv', 'xlv', 'xlvi', 'xlvii', 'xlviii', 'xlix', 'l', 'li', 'lii', 'liii', 'liv', 'lv', 'lvi', 'lvii', 'lviii', 'lix', 'lx', 'lxi', 'lxii', 'lxiii', 'lxiv', 'lxv', 'lxvi', 'lxvii', 'lxviii', 'lxix', 'lxx', 'lxxi', 'lxxii', 'lxxiii', 'lxxiv', 'lxxv', 'lxxvi', 'lxxvii', 'lxxviii', 'lxxix', 'lxxx', 'lxxxi', 'lxxxii', 'lxxxiii', 'lxxxiv', 'lxxxv', 'lxxxvi', 'lxxxvii', 'lxxxviii', 'lxxxix', 'xc', 'xci', 'xcii', 'xciii', 'xciv', 'xcv', 'xcvi', 'xcvii', 'xcviii', 'xcix', 'c']
	NAME = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty-one', 'twenty-two', 'twenty-three', 'twenty-four', 'twenty-five', 'twenty-six', 'twenty-seven', 'twenty-eight', 'twenty-nine', 'thirty', 'thirty-one', 'thirty-two', 'thirty-three', 'thirty-four', 'thirty-five', 'thirty-six', 'thirty-seven', 'thirty-eight', 'thirty-nine', 'forty', 'forty-one', 'forty-two', 'forty-three', 'forty-four', 'forty-five', 'forty-six', 'forty-seven', 'forty-eight', 'forty-nine', 'fifty', 'fifty-one', 'fifty-two', 'fifty-three', 'fifty-four', 'fifty-five', 'fifty-six', 'fifty-seven', 'fifty-eight', 'fifty-nine', 'sixty', 'sixty-one', 'sixty-two', 'sixty-three', 'sixty-four', 'sixty-five', 'sixty-six', 'sixty-seven', 'sixty-eight', 'sixty-nine', 'seventy', 'seventy-one', 'seventy-two', 'seventy-three', 'seventy-four', 'seventy-five', 'seventy-six', 'seventy-seven', 'seventy-eight', 'seventy-nine', 'eighty', 'eighty-one', 'eighty-two', 'eighty-three', 'eighty-four', 'eighty-five', 'eighty-six', 'eighty-seven', 'eighty-eight', 'eighty-nine', 'ninety', 'ninety-one', 'ninety-two', 'ninety-three', 'ninety-four', 'ninety-five', 'ninety-six', 'ninety-seven', 'ninety-eight', 'ninety-nine', 'one hundred']
	CAPNAME = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty', 'Twenty-One', 'Twenty-Two', 'Twenty-Three', 'Twenty-Four', 'Twenty-Five', 'Twenty-Six', 'Twenty-Seven', 'Twenty-Eight', 'Twenty-Nine', 'Thirty', 'Thirty-One', 'Thirty-Two', 'Thirty-Three', 'Thirty-Four', 'Thirty-Five', 'Thirty-Six', 'Thirty-Seven', 'Thirty-Eight', 'Thirty-Nine', 'Forty', 'Forty-One', 'Forty-Two', 'Forty-Three', 'Forty-Four', 'Forty-Five', 'Forty-Six', 'Forty-Seven', 'Forty-Eight', 'Forty-Nine', 'Fifty', 'Fifty-One', 'Fifty-Two', 'Fifty-Three', 'Fifty-Four', 'Fifty-Five', 'Fifty-Six', 'Fifty-Seven', 'Fifty-Eight', 'Fifty-Nine', 'Sixty', 'Sixty-One', 'Sixty-Two', 'Sixty-Three', 'Sixty-Four', 'Sixty-Five', 'Sixty-Six', 'Sixty-Seven', 'Sixty-Eight', 'Sixty-Nine', 'Seventy', 'Seventy-One', 'Seventy-Two', 'Seventy-Three', 'Seventy-Four', 'Seventy-Five', 'Seventy-Six', 'Seventy-Seven', 'Seventy-Eight', 'Seventy-Nine', 'Eighty', 'Eighty-One', 'Eighty-Two', 'Eighty-Three', 'Eighty-Four', 'Eighty-Five', 'Eighty-Six', 'Eighty-Seven', 'Eighty-Eight', 'Eighty-Nine', 'Ninety', 'Ninety-One', 'Ninety-Two', 'Ninety-Three', 'Ninety-Four', 'Ninety-Five', 'Ninety-Six', 'Ninety-Seven', 'Ninety-Eight', 'Ninety-Nine', 'One Hundred']
	ACAPNAME = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN', 'FIFTEEN', 'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN', 'NINETEEN', 'TWENTY', 'TWENTY-ONE', 'TWENTY-TWO', 'TWENTY-THREE', 'TWENTY-FOUR', 'TWENTY-FIVE', 'TWENTY-SIX', 'TWENTY-SEVEN', 'TWENTY-EIGHT', 'TWENTY-NINE', 'THIRTY', 'THIRTY-ONE', 'THIRTY-TWO', 'THIRTY-THREE', 'THIRTY-FOUR', 'THIRTY-FIVE', 'THIRTY-SIX', 'THIRTY-SEVEN', 'THIRTY-EIGHT', 'THIRTY-NINE', 'FORTY', 'FORTY-ONE', 'FORTY-TWO', 'FORTY-THREE', 'FORTY-FOUR', 'FORTY-FIVE', 'FORTY-SIX', 'FORTY-SEVEN', 'FORTY-EIGHT', 'FORTY-NINE', 'FIFTY', 'FIFTY-ONE', 'FIFTY-TWO', 'FIFTY-THREE', 'FIFTY-FOUR', 'FIFTY-FIVE', 'FIFTY-SIX', 'FIFTY-SEVEN', 'FIFTY-EIGHT', 'FIFTY-NINE', 'SIXTY', 'SIXTY-ONE', 'SIXTY-TWO', 'SIXTY-THREE', 'SIXTY-FOUR', 'SIXTY-FIVE', 'SIXTY-SIX', 'SIXTY-SEVEN', 'SIXTY-EIGHT', 'SIXTY-NINE', 'SEVENTY', 'SEVENTY-ONE', 'SEVENTY-TWO', 'SEVENTY-THREE', 'SEVENTY-FOUR', 'SEVENTY-FIVE', 'SEVENTY-SIX', 'SEVENTY-SEVEN', 'SEVENTY-EIGHT', 'SEVENTY-NINE', 'EIGHTY', 'EIGHTY-ONE', 'EIGHTY-TWO', 'EIGHTY-THREE', 'EIGHTY-FOUR', 'EIGHTY-FIVE', 'EIGHTY-SIX', 'EIGHTY-SEVEN', 'EIGHTY-EIGHT', 'EIGHTY-NINE', 'NINETY', 'NINETY-ONE', 'NINETY-TWO', 'NINETY-THREE', 'NINETY-FOUR', 'NINETY-FIVE', 'NINETY-SIX', 'NINETY-SEVEN', 'NINETY-EIGHT', 'NINETY-NINE', 'ONE HUNDRED']
	PREFIXES = ['Chapter ', 'chapter ']
	STYLES = [[], ROMAN, LROMAN, NAME, CAPNAME, ACAPNAME]
	
	#FIC SPECIFIC VARIABLES, edit as needed	
	FILENAME = 'The_Claws_of_Frontiers_ProcessedInput.html'	
	ORNAMENT = 'X'
	SUFFIX = '.'
	LIST = STYLES[1]
	PREFIX = PREFIXES[1]
	usePREFIX = False #if true, prefix numbers with 'chapter: ' or some other prefix
	useDIGIT = False #if true, use digits 1,2,3. Otherwise use the names or roman numerals from the list
	useSUFFIX = False #if true, put a suffix after the number (like : or .)
	oneLine = False #if true, merge the number and title in a single line
	replaceNums = True #if we have chapter numbers and we want to replace them
	ornamentAFTER = True
	ornamentBETWEEN = False
	OFFSET = 2 #set offset >1 if we want to skip prologue chapter

	# the code! the code itself!! 
	# Opening our text file in read only
	# mode using the open() function
	with open(FILENAME, 'r') as file:
	  
		# Reading the content of the file
		# using the read() function and storing
		# them in a new variable
		if oneLine==True and replaceNums==True:
			print("invalid menu options, cannot both combine the title & number into a single line AND delete the title")
			exit()
		if oneLine==True and ornamentBetween==True:
			print("invalid menu options, cannot both combine the title & number into a single line AND add a separate style ornament between them")
			exit()
		data = file.read()
		data = data.replace('\t', '')
		data = data.replace('\n', '')
		chapters = data.split('<h2>')
		cNum = 0
		dataMod = ''
		for c in chapters:
			#print(cNum, '<-num c->', c)
			if cNum==0:
				pass
			elif cNum<OFFSET:
				dataMod += '<h2>'
			else:
				if oneLine == True: #if we want it all on one line, keep using h2
					dataMod += '<h2>'
				elif replaceNums == True:
					if ornamentBETWEEN == True:
						dataMod += '<h1>'+ORNAMENT+'</h1>'
					dataMod += '<h2>'
				else: #otherwise use h6 for the chapter number
					dataMod += '<h6>'
				if replaceNums == True: #if we are deleting the chapter title to put in our number instead, delete everything before the </h2>
					c = re.sub('.*?</h2>', '</h2>', c)
				if usePREFIX == True: #if we're adding a prefix, add a prefix
					dataMod += PREFIX
				if useDIGIT == False: #if we're not using digits, fetch the list item
					dataMod += LIST[cNum-OFFSET]
				else: #otherwise use the digit
					dataMod += str(cNum)
				if useSUFFIX == True: #if we're using a suffix, add the suffix
					dataMod += SUFFIX
				if replaceNums == False: #if we aren't replacing the chapter title either close out the h6 for our number OR put a space (if all on one line)
					if oneLine == False: 
						dataMod += '</h6>'
						if ornamentBETWEEN == True:
							dataMod += '<h1>'+ORNAMENT+'</h1>'
						dataMod += '<h2>'
					if oneLine == True:
						dataMod += ' '
				if ornamentAFTER == True:
					dataMod += '</h2>'
					dataMod += '<h1>'+ORNAMENT+'</h1>'
			dataMod += c
			cNum += 1
		data = dataMod
		data = re.sub('</h2></h2>', '</h2>', data)
		data = re.sub('</h1></h2>', '</h2>', data)
		
		
		#put all the line breaks back
		#log.write("Replacing line breaks: ")
		data = data.replace('</p>', '</p>\n')
		data = data.replace('</h1>', '</h1>\n')
		data = data.replace('</h2>', '</h2>\n')
		data = data.replace('</h3>', '</h3>\n')
		data = data.replace('</h4>', '</h4>\n')
		data = data.replace('</h5>', '</h5>\n')
		data = data.replace('</h6>', '</h6>\n')		
		data = data.replace('</blockquote>', '</blockquote>\n')
		
	# Opening our text file in write only
	# mode to write the replaced content
	with open('ProcessedInput_'+FILENAME, 'w') as file:
	  
		# Writing the replaced data in our
		# text file
		file.write(data)
	
	  
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))



