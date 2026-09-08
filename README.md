# Scribus Resources for Book Typesetting
To accompany my tutorial on using Scribus to typeset (primarily fanfiction sourced from AO3) books for home bookbinding. This repo contains scripts I have authored or edited, links to other important scripts you might use & Scribus files you can use as templates to start your own book project.

![diagram listing the main scripts in this repo and their uses, described below](https://github.com/notwhelmedyet/ScribusTypesetting/blob/main/ReferenceDocs/Flier.png)

### Things I am Not: 
* A professional programmer
	* (I took a python class in college a decade ago)
	* I am aware that manually processing html with regex, which is how the importCleaner program runs, is a bad idea that will break if the html isn't formatted the way I expect. However, I do not plan to learn html parsing. The script works on current ao3 outputted HTML files and that is all it needs to do.
* Capable of offering immediate tech support if you cannot make a script work.
	* Sometimes I may be able to figure out why a script isn't doing what it should. Sometimes I might not. Debugging and kludging together scripts are two very different skills.
* Scripts are not offered with any guarantee to their usefulness, code efficiency, etc. Always save a **copy** of your typeset before running any script. (The exception being the html processing scripts and the renumberSplitPages script, all of which create copies of the files they edit rather than work int he actual file)


## The Core Scripts
1. importCleanerScribus.py
	>These scripts read a html file downloaded from ao3 and apply header styles to various sections of the document so they can be easily converted to Scribus paragraph styles upon import. It saves a edited copy of the file as well as a log output that tracks potential issues.

	>The script will assign the following html headers for parts of the fic:
	>* \<h1> Fic Title
	>* \<h2> Chapter Titles
	>* \<h3> Chapter Start - first paragraph after chapter title
	>* \<h4> Scene Start - first paragraph after a scene break
	>* \<h5> Scene Break/Ornaments
2. chapterNumScribus.py
	>These scripts take a already-processed html file created by ImportCleaner and apply one of several changes:
	>* Add chapter numbers (in chosen format) prior to chapter title
	>* Replace chapter title with chapter numbers. If the chapters were not given titles within AO3 the default title will be 'Chapter One' etc.
	>* Add a separate-style ornament either above or below chapter titles/numbers
	
	>The script will assign html headers as follows:
    >* \<h1> Chapter title ornaments
    >* \<h6> Chapter number
3. boldItalicsToStyle.py
    > When importing HTML, Scribus hardcodes your substitution fonts as manual overrides wherever it found bold, italic, bold italic etc. This guides you in replacing those with character styles, if you prefer. If you already have char styles Italic, Bold and BoldItalic, it will use those. Otherwise it will create them.
    > It also addresses a bug: if you import HTML, realize you messed up and then import the text again Scribus will hard code the substitution fonts for all of your html header styles. You can avoid that bug by closing the document without saving and reimporting (or deleting the HTML header styles before importing). You can also use this script to fix it. It will only address that bug if you haven't swapped the html header styles to your document styles yet.
3. runtsAndStuff.py
	> This preprocesses a hyphenated Scribus file to prevent lots of manual dehyphenation work, stub line endings, automatically add frame breaks between paragraphs and optionally style the beginning of a paragraph style. It should be run after importing, applying styles & hyphenation. It will:
    >* Insert a nonbreaking space in front of all short words (default 6 characters) at the end of paragraphs
    >* Remove soft hyphens from the last X characters of paragraph endings (can turn off or set character count, default 50) 
    >* Remove soft hyphens in all normally hyphenated words
    >* Remove soft hyphens in last word of paragraph
    >* Insert a frame break before instances of X style (can turn off, default ChapterTitle)
    >* Apply a character style X to first Y of paragraph style Z (can turn off, options to apply to first Y characters, words, or up to a delimiter.)
	> This script must be run within scribus. You need to open the scribus file you're editing with the file picker, but it must also be open within Scribus for the style verification to work correctly. You must hyphenate the whole text prior to running this script for dehyphenation to work - the script does not prevent hyphenating, it simply removes hyphenation from the situations descirbed above.
4. textToFramesScribus.py
	>Move certain text elements on the main margin-sized text frame into separate frames for the currently selected page.
	>Will only work if you have text on the page using the styles ChapterTitle, ChapterNumber. Will move the first paragraph of text in the main frame (assumed to be the size of the page-margins) using those styles into text frames that contain the style name if they exist. If no matching text frame exists, the text is not moved.
	>The script will also move the first letter of the style ChapterStart if there is a frame containing the name DropCap. If the chapter starts with a quotation mark and a character style named DropQuote exists, the initial quotation mark will be styled with the DropQuote style.
5. runningHeadersScribus.py
	>This was built on [Ale's headers_with_chapter_titles script](https://github.com/aoloe/scribus-script-repository/tree/master/headers_with_chapter_titles). It finds text in a selected style (Author name, chapter title, chapter number etc.) and, for all pages assigned master page templates that have a frame name containing the word "Header", copies that frame to the page and places the author name, chapter title etc. in the frame. It continues to place that text until it encounters a new instance of the chosen style. Basically, it can automatically apply any per-chapter or per-work field to headers/footers/wherever you want to put these frames.

	>I added in dialogue options within Scribus to set a number of extra variables: whether the script should delete previously created headers, whether the script should apply to left/right/both pages, the source style to search for the header text, a destination style to apply to the headers and whether to append text from the master page to the header.
6. autoMasters.py
    > This script will automatically apply master pages for the pages that begin chapters & blank facing pages by searching for a chosen heading style that appears at the start of chapters. You would use this script at the very end (around the same time as runningHeaders)

## Situational Scripts
1. ResizeMarginsAndHeadersScribus.py
	>Resizes text frames and moves them to align with the page margins. This script is intended to be used on book-style documents with automatic text frames after the size of the page or margins has been changed. The script was only tested with facing page layouts where the first page is on the right hand side and all pages have the same margins. Based on initial code by Blaze.
2. move-to-layer-colors.py & move-to-layer-name-match.py
	>Two variants of [Ale's images-to-layer script](https://github.com/aoloe/scribus-script-repository/tree/master/images-to-layer) These scripts (in addition to the images-to-layer script) are useful for a highly specialized task: you did not use layers when making your file but then realize you want to export the text and images/colored elements/specific items in different files. Maybe you want to print text and images on separate printers to save color ink or to optimize quality by using a b&w laserjet for text. Maybe you want to offer someone an image-free version to save on printing costs. Either way, this will make it easier.

	>* images-to-layer moves all images to a layer of your choice.
	>* move-to-layer-colors moves all objects that have a fill or line color which is anything besides black, white or none. It is greedy and also moves anything with a gradient or hatch fill, because for some reason the script thinks those things are aquamarine. It does not notice colored text.
	>* move-to-layer-name-match looks at the currently selected object and moves all objects that have a name containing that object's name to a layer. This will really only work if you gave the object a unique name prior to copy and pasting it many times. But in that specific use-case it is very handy.
3. renumberSplitPages.py
    > Sometimes you have to split a book into multiple scribus files because it starts lagging. This is a script to adjust the page numbers of all those files so they count up sequentially file-to-file.  It also checks to make sure you have correct alternating left-right pages across files.

    > This script should be run prior to renumbering any epilogues/appendix back-matter sections to your final document - the will correctly ignore any front-matter sections in document 1, but it assumes all subsequent documents have only 1 section. Other than that, run right before your final PDF export!
4. setUpTOC.py
    > This is a variant built on [Ale's table_of_contents script](https://github.com/aoloe/scribus-script-repository/tree/master/table_of_contents). It allows you to add attributes to the document listing all instances of your selected style, which Scribus can then use to generate a TOC.
5. styleTOC.py
    > The default Scribus Table of Contents generator applies the same paragraph style to the whole TOC. But what if you want the numbers (or chapter titles) to be styled differently? Or what if you want to insert a special character between the title and number?
    > This script styles any section of each line in a chosen character style. It also inserts the character of your choice in the middle of the line or an initial tab upon request.
6. pasteInlineImages.py
    > This script can be used to insert an image, line or shape object scene break wherever you currently have a placeholder character. The placeholder must be in an ornament style that's styled the way you want the image (centered, baseline grid alignment, etc.) The script can only run in Scribus 1.6 and later, due to missing scripter commands in earlier versions. I highly recommend converting your object to a scribus symbol prior to running the script so all instances can be edited en-masse if necessary
    > Select the object you want to place (already correctly sized) prior to running the script. Please run this script on a copy of your file. Runtime will be long on large files.
6. CommandLine-chapNum.py and CommandLine-importCleaner.py
    > Variants of the ChapNumScribus and importCleanerScribus scripts that run in the terminal with python 3, if you have that available. Allows you to set your default variables and keep using them without messing around with all the dialogues. Intended for users comfortable with the command line and ediitng scripts manually.

## Experimental Scripts (need further testing)
1. anthologyCleaner.py
    > A variant of importCleanerScribus.py which can process a group of works sequentially and append them together into a combined Anthology.html document. This script must be run twice and all the source html files must be in the same directory. The first run will generate the list of works in a directory. The user then must manually open that list and put the works in the desired order. You can then run again to generate the anthology source document. Some differences from the regular importCleanerScribus.py:
    >* Will separate metadata into its own file (AnthologyMeta.html)
    >* Cannot handle source documents that are double spaced throughout, since that logic would have to then be applied to all the source documents

    > This script is experimental. I have not tested all variable combinations and it might give weird results. Please let me know if you find any bugs. The script will work best on single-author anthologies, because they're less likely to have substantial formatting differences between the works

## The Templates
Needs to be Filled Out, tldr they're shortcuts to set up some of the many styles you need to typeset a book with some sane default values.

