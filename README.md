# Scribus Resources for Book Typesetting
To accompany my tutorial on using Scribus to typeset (primarily fanfiction sourced from AO3) books for home bookbinding. This repo contains scripts I have authored or edited, links to other important scripts you might use & Scribus files you can use as templates to start your own book project.

Finally moving off Google docs.

## The Scripts
1. importCleaner.py and importCleanerScribus.py
	>These scripts read a html file downloaded from ao3 and apply header styles to various sections of the document so they can be easily converted to Scribus paragraph styles upon import. It saves a edited copy of the file as well as a log output that tracks potential issues. The script with the 'Scribus' suffix will run within Scribus, and allows you to set a number of variables at run-time. The other version runs on your command line using Python3.

	>The script will assign the following html headers for parts of the fic:
	>* \<h1> Fic Title
	>* \<h2> Chapter Titles
	>* \<h3> Chapter Start - first paragraph after chapter title
	>* \<h4> Scene Start - first paragraph after a scene break
	>* \<h5> Scene Break/Ornaments
2. chapterNum.py & chapterNumScribus.py
	>These scripts take a already-processed html file created by ImportCleaner and apply one of several changes:
	>* Add chapter numbers (in chosen format) prior to chapter title
	>* Replace chapter title with chapter numbers. If the chapters were not given titles within AO3 the default title will be 'Chapter One' etc.
	>* Add a separate-style ornament either above or below chapter titles/numbers

	> As with the ImportCleaner, the script with the Scribus suffix runs within Scribus and offers prompts to set variables at run-time.
	
	>The script will assign html headers as follows:
    >* \<h1> Chapter title ornaments
    >* \<h6> Chapter number

3. ResizeMarginsAndHeadersScribus.py
	>Resizes text frames and moves them to align with the page margins. This script is intended to be used on book-style documents with automatic text frames after the size of the page or margins has been changed. The script was only tested with facing page layouts where the first page is on the right hand side and all pages have the same margins. Based on initial code by Blaze.
4. textToFramesScribus.py
	>Move certain text elements on the main margin-sized text frame into separate frames for the currently selected page.
	>Will only work if you have text on the page using the styles ChapterTitle, ChapterNumber. Will move the first paragraph of text in the main frame (assumed to be the size of the page-margins) using those styles into text frames that contain the style name if they exist. If no matching text frame exists, the text is not moved.
	>The script will also move the first letter of the style ChapterStart if there is a frame containing the name DropCap.
5. runningHeadersScribus.py
	>This was built on [Ale's headers_with_chapter_titles script](https://github.com/aoloe/scribus-script-repository/tree/master/headers_with_chapter_titles). It finds text in a selected style (Author name, chapter title, chapter number etc.) and, for all pages assigned master page templates that have a frame name containing the word "Header", copies that frame to the page and places the author name, chapter title etc. in the frame. It continues to place that text until it encounters a new instance of the chosen style. Basically, it can automatically apply any per-chapter or per-work field to headers/footers/wherever you want to put these frames.

	>I added in dialogue options within Scribus to set a number of extra variables: whether the script should delete previously created headers, whether the script should apply to left/right/both pages, the source style to search for the header text, a destination style to apply to the headers and whether to append text from the master page to the header.
6. colors-to-layer.py & name-match-move-to-layer.py
	>Two variants of [Ale's images-to-layer script](https://github.com/aoloe/scribus-script-repository/tree/master/images-to-layer) These scripts (in addition to the images-to-layer script) are useful for a highly specialized task: you did not use layers when making your file but then realize you want to export the text and images/colored elements/specific items in different files. Maybe you want to print text and images on separate printers to save color ink or to optimize quality by using a b&w laserjet for text. Maybe you want to offer someone an image-free version to save on printing costs. Either way, this will make it easier.

	>* images-to-layer moves all images to a layer of your choice.
	>* colors-to-layer moves all objects that have a fill or line color which is anything besides black, white or none. It is greedy and also moves anything with a gradient or hatch fill, because for some reason the script thinks those things are aquamarine. It does not notice colored text.
	>* name-match-move-to-layer looks at the currently selected object and moves all objects that have a name containing that object's name to a layer. This will really only work if you gave the object a unique name prior to copy and pasting it many times. But in that specific use-case it is very handy.

### Things I am Not: 
* A professional programmer
	* (I took a python class in college a decade ago)
	* I am aware that manually processing html with regex, which is how the importCleaner program runs, is a bad idea that will break if the html isn't formatted the way I expect. However, I do not plan to learn html parsing. The script works on current ao3 outputted HTML files and that is all it needs to do.
* Capable of offering immediate tech support if you cannot make a script work.
	* Sometimes I may be able to figure out why a script isn't doing what it should. Sometimes I might not. Debugging and kludging together scripts are two very different skills.
* Scripts are not offered with any guarantee to their usefulness, code efficiency, etc. Always save a **copy** of your typeset before running any script. (The exception being the html processing scripts, which don't edit any Scribus file and don't make any edits to the source html)

## The Templates
Needs to be Filled Out, tldr they're shortcuts to set up some of the many styles you need to typeset a book with some sane default values.
