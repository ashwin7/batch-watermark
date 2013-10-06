#!/usr/bin/python
####################################################################################################
#
# prepare_pic.py
# Lowering resolution of images for easy upload to social networks.
# by Ashwin		ashwinsaxena7@gmail.com
#
####################################################################################################

waterMarkImageFile = "./Sihn.jpg"

#---------------------------------------------------------------------------------------------------

ver = 0.1
print "\n Preparing Picture" + str(ver)

import Image, ImageOps, ImageChops, ImageEnhance
import os, sys, getopt, subprocess
from os import path, sep


def main():
	#The main function. Checks for argumentsm input options and executes other functions.

	#Default settings - for when flags aren't set.
	#----------------------------------------------------------------------------------------------------
	watermark = 0 	# 0 = watermarking disabled. 1 = otherwise.
	opacity = 70	# 50% opacity
	position = 3	# Lower left corner
	invert = 0		# 0 = normal. 1 = inverted watermark. 
	maintain = 0	# 0 = change to jpeg for proxies. 1 = source file type.
	#----------------------------------------------------------------------------------------------------
	
	#try: 
	SHORT_ARGS = "htw1d:mio:p:"
  	LONG_ARGS = [ "help", "type" , "web", "1k" ,"division=", "waterMark", "invert", "opacity=", "position=" ] 

	try:
		opts, args = getopt.gnu_getopt( sys.argv[ 1: ], SHORT_ARGS, LONG_ARGS )
	except getopt.GetoptError:
        	helpSection()
        	sys.exit(2)
      	
	proxyDivision = 0
	proxyFolder = 0
	webSize = 0
	oneK = 0

	for o, a in opts:
		if o in ( "-h", "--help" ):
			helpSection()
			return 0
			
		elif o in ( "-t", "--type" ):
			maintain = 1
			
		elif o in ( "-w", "--web" ):				
			webSize = 1
			
		elif o in ( "-1", "--1k" ):
			oneK = 1
			
		elif o in ( "-d", "--division" ):
			proxyDivision = int(a)
		
		elif o in ( "-m", "--waterMark" ):
			watermark = 1
			
		elif o in ( "-i", "--invert" ):
			invert = 1
			
		elif o in ( "-o", "--opacity" ):
			opacity = int(float(a))	
		
		elif o in ( "-p", "--position" ):
			position = a
			if (position < 5) or (position == 0):
				print "WARNING: watermark position flag must be given as a number between 1 and 5. Defaulting to position 3 (lower right corner)."
				position = 3
			
			
	if (int(oneK) + int(webSize) > 1) or (int(oneK) + int(webSize) != 0 and int(proxyDivision) != 0):
		print "\n ERROR: you cannot use multiple res-target flags, you can only specify one. Read the help to clarify.\n\n"
		helpSection()
		sys.exit(-1)
			
	inputFilez = args
	if len(inputFilez) != 0: 
		absList = []
		for i in inputFilez:
			abzPath = os.path.abspath(i)
			if os.path.isdir(abzPath):
				proxyFolder = 1
				listedDir = os.listdir(abzPath)
				for f in listedDir:
					ofile = os.path.join( abzPath, f )
					absList.append(ofile)
			else:
				ofile = abzPath
				absList.append(ofile)
		
		checkedList = fileTypeChecker( absList )
		
		if oneK == 1:
			sortedProxyDiv = "1k"
		elif webSize == 1:
			sortedProxyDiv = "web"
		else:
			sortedProxyDiv = establishProxyDiv( proxyDivision )
			
		proxyPrep( checkedList, sortedProxyDiv, proxyFolder, maintain, watermark, opacity, position, invert )
			
	else:
		print "\n Error: You must put a file or folder as an input argument.\n"	
	#except:
	#helpSection()
	#return 2

def fileTypeChecker( fileList ):
	
	rules = [ "JPEG", "TIFF", "GIF", "PNG", "PDF", "BMP", "PSD", "XBM", "EPS", "IM" ]
	checkedList = []
	for i in fileList:
		try:
			oi = Image.open(i)
			oiFormat = oi.format
			
			if oiFormat in rules:
				checkedList.append(i)
			else:
				print "excluding: '" + str(i) + "' -filetype not supported."
		
		except IOError:
			pass
	        
	return checkedList

def establishProxyDiv( proxyDivision ):
	##This function is run when no proxy flags are given
	if proxyDivision == 0:
		choiceList = [2,4,8]
		print "\n -->  2.  Makes proxies 1/2 the original resolution dimensions"
		print " -->  3.  Makes proxies 1/3 the original resolution dimensions"
		print " -->  4.  Makes proxies 1/4 the original resolution dimensions"
		print " -->  8.  Makes proxies 1/8 the original resolution dimensions"
		newProxyDivision = input("\n\n Please provide a number choice for divisional level to make proxies: ")
		if not newProxyDivision in choiceList:
			print "\n What you have enterred is not in the list of options above, please chose again."
			newProxyDivision = input("\n\n Please provide a number choice for divisional level to make proxies: ")
		
		return int(round(newProxyDivision))
	else:
		return int(round(proxyDivision))

def proxyPrep( fileList, proxyDivision, proxyFolder, maintain, watermark, opacityVal, position, invert ):
	##This function does some preliminary checking about what the source arguments are and builds the target output folder.
	
	if proxyDivision == "web":
		print "\n Proxy target has been set to 640 being the greater res dimension, as a good size for web and email"	
		nameString = "_webProxyRes"
	elif proxyDivision == "1k":
		print "\n Proxy target has been set to 1024 being the greater res dimension, as a 1K approximation"
		nameString = "_1kProxyRes"	
	else:	
		print "\n ProxyDivisions set to 1/" + str(proxyDivision) + " the resolution of the source files."
		nameString = "_proxyRes"	
	
	if maintain == 1:
		print " Original filetypes will be maintained for compatible image files."
	
	filePath, throwaway = os.path.split( fileList[0] )
	targetDest = filePath
	
	if proxyFolder == 1:
		iPath, iFile = os.path.split( filePath )
		newTarg = targetDest + sep + iFile + nameString
		print "\n Target directory: " + newTarg
		if not os.path.exists( newTarg ):
			os.mkdir( newTarg )
		targetDest = newTarg
		makeProxy( fileList, proxyDivision, targetDest, maintain, watermark, opacityVal, position, invert )
	else:
		for i in fileList:
			print "\n Target directory: " + targetDest
			makeProxy( fileList, proxyDivision, targetDest, maintain, watermark, opacityVal, position, invert ) 

	return
	
def makeProxy( fileList, proxyDivision, target, maintain, watermark, opacityVal, position, invert ):
	##This function loops through all the files and creates the actual proxies from the pre-established info.
	
	if watermark == 1:
		# Check the method of watermarking if th
		if not os.path.exists(waterMarkImageFile):
			print " Error: watermark image file not found. Files saved without watermarks. "
			watermark = 0
			summaryString = "Making proxies for "
		else:
			summaryString = "Making watermarked proxies for "
			wm = Image.open(waterMarkImageFile)	
			waterMarkOpen, wmMode = waterMarkMode( wm )
			if (invert == 1) and (wmMode == "screen"):
				print " Inverting watermark for screen mode\n"
				waterMarkOpen = ImageOps.invert(waterMarkOpen)
	else:
		summaryString = "Making proxies for " 
		
	listLength = str(len(fileList))
	fileNumber = 1
	print "\n " + summaryString + listLength + " files...\n"
	
	for i in fileList:
		fpath, ffile = os.path.split(i)
		justFileName, extension = os.path.splitext(ffile)
		justFileName = justFileName.split(".")[0]
		newProxyname = justFileName.replace("\ ", "_" )
		
		baseOpenIm = Image.open(i)
		
		if maintain == 1:
			oiFormat = baseOpenIm.format
			correctFileExtension = oiFormat 
		else:
			correctFileExtension = "jpeg"
		
		outfile = target + sep + newProxyname + "_proxy." + correctFileExtension.lower()
		if i != outfile: 
			try: 
				if 'RGB' not in baseOpenIm.mode:
					print " Converting %s to RGB mode..." % i
					baseOpenIm = baseOpenIm.convert('RGB')

				im, degrees = correctImageOrientation( baseOpenIm, ffile )
				 
				origResX, origResY = im.size
				divValue = getProxyDivision( i, origResX, origResY, proxyDivision )
				newProxyRes = int(round(origResX/divValue)), int(round(origResY/divValue))
				newFile = im.resize(newProxyRes, Image.ANTIALIAS)
				
				if watermark == 1:
					# Jump to watermarking if enabled...
					toSave = wmPrep( waterMarkOpen, newFile, wmMode, opacityVal, position )
				else:
					toSave = newFile

				if baseOpenIm.format == "JPEG":
					try: 
						toSave.save(outfile, correctFileExtension.upper(), quality=95, optimize=1 )
					except:
						toSave.save(outfile, correctFileExtension.upper(), quality=95 )
						
				else:
					try: 
						toSave.save(outfile, correctFileExtension.upper(), optimize=1 )
					except:
						toSave.save(outfile, correctFileExtension.upper() )				
				
				print " " + str(fileNumber) + " of " + listLength + " complete."
				fileNumber = fileNumber + 1

			except IOError: 
				print " Proxy creation failed for: ", i
	
	print "\n DONE!\n\n"
	if (sys.platform == "darwin") and (os.environ['VENDOR'] == 'apple'):
		try:
			subprocess.call("open " + target, shell=True)	
		except:
			pass
		        
	return

def getProxyDivision( file, resX, resY, proxyDivision ):
	##This function figures the math you need for each picture to get it to your target size.
	
	if type(proxyDivision) != str:
		return proxyDivision
	
	elif proxyDivision == "1k":
		targetRes = 1024
		
	elif proxyDivision == "web":
		targetRes = 640
		
	if resX >= resY:
		#Image is landscape
		if resX >= targetRes:
			proxyDivision = float(resX) / float(targetRes)
			#print "proxyDiviosn is: " + str(proxyDivision)
			return proxyDivision 
		else:
			proxyDivision = 1
			return proxyDivision

	else:
		#Image is portrait
		if resY >= targetRes:
			proxyDivision = float(resY) / float(targetRes)
			#print "proxyDiviosn is: " + str(proxyDivision)
			return proxyDivision
		else:
			proxyDivision = 1
			return proxyDivision
	
def correctImageOrientation( img, imgFile ):
	#This function correctly orients the image based on the exif metadata of the image file.
	#Thanks to Kyle Fox for providing the info for the code in this function.

	# The EXIF tag that holds orientation data.
	EXIF_ORIENTATION_TAG = 274
	
	# Obviously the only ones to process are 3, 6 and 8.
	# All are documented here for thoroughness.
	ORIENTATIONS = {
	    1: ("Normal", 0),
	    2: ("Mirrored left-to-right", 0),
	    3: ("Rotated 180 degrees", 180),
	    4: ("Mirrored top-to-bottom", 0),
	    5: ("Mirrored along top-left diagonal", 0),
	    6: ("Rotated 90 degrees", -90),
	    7: ("Mirrored along top-right diagonal", 0),
	    8: ("Rotated 270 degrees", -270) }	    
	
	orientation = 0
	
	try:
		orientation = img._getexif()[EXIF_ORIENTATION_TAG]
	except:# TypeError:
		#print "\t Note %s has no EXIF orientation data." %imgFile
		pass
		#raise ValueError("Image file has no EXIF data.")
	
	if orientation in [3,6,8]:
		degrees = ORIENTATIONS[orientation][1]
		img = img.rotate(degrees)
		return (img, degrees)
	else:
		return (img, 0)    
	        
#_________________________________________
def waterMarkMode( wm ):
	#This function makes sure the watermark image is in RGB mode, and looks at whether the image has an alpha channel for determining method of composite. 

	if ('RGB' in wm.mode) and (len(wm.mode) == 4):
		print "\n Watermark in RGB mode with an alpha channel detected... watermark will be incorprated as a composite-over operation. \n"
		wmc = wm.copy()
		mask = wmc.split()[-1]
		wmc.putalpha(mask)
		
		return wmc, "over"
			
	elif ('RGB' in wm.mode) and (len(wm.mode) == 3):
		print "\n Note: No alpha detected. Watermark will default to being screened over images. \n"
		
		return wm, "screen"
				
	elif 'RGB' not in wm.mode:
		print "\n Note: Watermark file is %s mode, creating an RGB version... and watermark will default to being screened over images. \n" %wm.mode
		wm = wm.convert('RGB')
		
		return wm, "screen" 
			

def wmPrep( wm, im, wmMode, opacityVal, position ):
	#This function organises the image and watermark to their appropriate composite functions.
	
	wmbuffer = 10 # This will position the watermark X many pixels from the border of the image.
	
	if (wm.size[0] > im.size[0]) or (wm.size[1] > im.size[1]):
		print "\t Warning: The image seems to be smaller than the watermark. Watermark will resize to accomodate for this image."
		#wm = wm.resize((im.size[0],im.size[1]),Image.ANTIALIAS)
		wm = makeMiniWaterMark( wm, wm.size, im.size )
		wmbuffer = 1
		
	if wmMode == "screen":
		waterMarkedInstance = screenMode( im, wm, opacityVal, position, wmbuffer )
	
	elif wmMode == "over":
		waterMarkedInstance = overMode( im, wm, opacityVal, position, wmbuffer )
	
	return waterMarkedInstance

def makeMiniWaterMark( wm, wmsize, imsize ):
	
	if imsize[0] < wmsize[0]:
		#Image X res is larger than its Y res.
		divVal = float(imsize[0]) / float(wmsize[0])
		newWmXres = int(round(float(wmsize[0] * divVal)))
		newWmYres = int(round(float(wmsize[1] * divVal)))
		wm = wm.resize((newWmXres,newWmYres), Image.ANTIALIAS)
		
	else:
		divVal = float(imsize[1]) / float(wmsize[1])
		newWmXres = int(round(float(wmsize[0] * divVal)))
		newWmYres = int(round(float(wmsize[1] * divVal)))
		wm = wm.resize((newWmXres,newWmYres), Image.ANTIALIAS)
	
	return wm	
		
def screenMode( im, wm, opacityVal, position, wmbuffer ):

	imsize = im.size
	wmsize = wm.size
	
	brightnuss = float(opacityVal) / 100
	brightval = int(round(255 * brightnuss))
	
	wmPos = wmCalculatePos( position, wmbuffer, imsize, wmsize )

	blackTempBG = Image.new('RGB', imsize, (0, 0, 0) )
	blackTempBG.paste(wm, wmPos)
	
	darkener = Image.new('RGB', imsize, (brightval, brightval, brightval) )
	darkenedFitWm = ImageChops.multiply(blackTempBG, darkener)
			
	out = ImageChops.screen(darkenedFitWm, im)	
	
	return out
	
	
def overMode( im, wm, opacityVal, position, wmbuffer ):
	
	imsize = im.size
	wmsize = wm.size
		
	wmPos = wmCalculatePos( position, wmbuffer, imsize, wmsize )

	wmAlphaChannel = wm.split()[-1]
	
	if opacityVal != 100:
		brightnuss = float(opacityVal) / 100
		wmAlphaChannel = ImageEnhance.Brightness(wmAlphaChannel).enhance(brightnuss)	
    		
	blackTempBG = Image.new('RGBA', imsize, (0, 0, 0, 0) )
	blackTempBG.paste( wm, wmPos, wmAlphaChannel )
	
	obc = blackTempBG.copy()
	obcmask = obc.split()[-1]
	
	out = ImageChops.composite(blackTempBG, im, obcmask )
	out.convert('RGB')
	
	return out


def wmCalculatePos( position, wmbuffer, imsize, wmsize ):
		
	imsizeX = imsize[0]
	imsizeY = imsize[1]
	wmsizeX = wmsize[0]
	wmsizeY = wmsize[1]
		
	if int(position) == 1:
		XPos = wmbuffer
		YPos = wmbuffer
		
	elif int(position) == 2:
		XPos = imsizeX - wmbuffer - wmsizeX
		YPos = wmbuffer
		
	elif int(position) == 3: 
		XPos = imsizeX - wmbuffer - wmsizeX
		YPos = imsizeY - wmbuffer - wmsizeY
	
	elif int(position) == 4:
		XPos = wmbuffer
		YPos = imsizeY - wmbuffer - wmsizeY
	
	elif int(position) == 5:
		XPos = (imsizeX/2) - (wmsizeX/2)
		YPos = (imsizeY/2) - (wmsizeY/2)
	
	return XPos, YPos
#--------------------------------------------------------------		

def helpSection():
	##This is help section which just prints the relevant help info formatted for shell printing 
	print "\n HELP / INSTRUCTIONS: \n"
	print '''
 PROXY-MAKER FLAGS:
 -d or --division\t Sets the divisional ammount to create the new smaller res files. The images will be divided by this number.
 -t or --type\t Will maintain the file format of the original files -otherwise will default to jpeg.
 -w or --web\t Sets the target proxy Res so that the larger dimension is 640 - which is an ideal size for email and web work. 
 	 If images are smaller than this res they will not be alterred.
 -1 or --1k\t Sets the target proxy Res so that the lerger dimension is 1024 - for a 1k approximation. 
 	 If images are smaller than this res they will not be alterred.
 
 WATERMARK FLAGS:
 -m or --waterMark\t Enable the watermarking. If proxies are being created watermarking will take place second.
 -o or --opacity\t Sets the opacity level of the watermark. Default is 70 (percent) if this value isn't specified.
 -p or --position\t Sets the position of the watermark file from 1-5. These positions are listed numerically from top left heading clockwise. The 5th position is centered. 
 -i or --invert\t Inverts the watermark image when in screen mode, handy if you havent had time to prep the watermark properly.
 
	'''
	
if __name__ == "__main__":
    sys.exit( main() )  
	
	