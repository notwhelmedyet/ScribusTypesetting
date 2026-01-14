# © 2014.07.06 Gregory Pittman
# © 2023 ale riomldi
# modified in 2026 by Lynn
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
"""
A Modified version of images-to-layer
Move all objects that have a Fill or Line set to any color except "Black", "White" or "None" to another layer
Not guaranteed to work on all objects, will not move text frames based on the color of text within the frame
Will move all objects that have hatch or gradient fills/lines regardless of color (for some reason they're all coming up as "aquamarine")
Will not move items on master pages
The idea being that you can show/hide, print-export/not as desired.

You need an open document.
"""
 
def main():
	try:
		import scribus

		if not scribus.haveDoc():
			return
	except ImportError:
		print('This script must be run from inside Scribus')
		return

	current_layer = scribus.getActiveLayer()

	layers = scribus.getLayers()
	try:
		target_layer = scribus.itemDialog('Choose a layer', 'Choose one of the layers or type the name of the layer to be created:', layers, True)
	except:
		# scribus.itemDialog() has been created for this script and might not yet be in your scribus
		target_layer = scribus.valueDialog('Choose a layer', 'Choose one of the layers or type the name of the layer to be created:')
	if target_layer == '':
		return
	if not target_layer in layers:	
		scribus.createLayer(target_layer)
		scribus.setActiveLayer(current_layer)

	for page in range(scribus.pageCount()):
		scribus.gotoPage(page + 1)	
		for item in scribus.getPageItems():
			fill_color = scribus.getFillColor(item[0])
			line_color = scribus.getLineColor(item[0])
			if fill_color == "None" or fill_color == "White" or fill_color == "Black":
				pass
			else:
				scribus.sendToLayer(target_layer, item[0])
			if line_color == "None" or line_color == "White" or line_color == "Black":
				pass
			else:
				scribus.sendToLayer(target_layer, item[0])
		
	scribus.deselectAll()
	scribus.setRedraw(True)
	scribus.docChanged(True)
	 
if __name__ == '__main__':
   main()
