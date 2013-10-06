batch-watermark
===============

Python scripts to resize and watermark images before you upload them to social networks.

There are two scripts:
* resmark_pic.py : To resize AND watermark an image (by default only resize unless given flag.)
* mark_pic : Only watermark image.

In any case your original image remains untouched, scripts create proxies (duplicate files) for resizing, watermarking.


## resmark_pic.py

- will automatically try to reorient your images properly.

- will create lower resolution 'proxies'/duplicates with options for 1/2, 1/4, 1/8th of the original image size.

- has the option for applying a watermark to your images once they have been reduced in size. 
There are 2 modes for completing this. If your image has an alpha channel, this will be used to create the transparency of the composite over the watermark image. If no alpha is found the script will 'screen' the brighter values over the image. So you create your watermark image file to cater for your composite mode preference.
 
**You need to place watermark image in the same directory as the script with filename watermark.jpg** This is hardcoded.

Watermark position can be customized, there are 5 options, initiated with the "-p" flag and a number from 1 to 5. Number 1 being the top left and other position counted around clockwise from here. So 2 is top right, 3 is lower right, 4 is lower left, and 5 is the centre. Default is 3.

### Supported Flags

-d or --division Sets the divisional ammount to create the new smaller res files. The images will be divided by this number.
-t or --type	Will maintain the file format of the original files -otherwise will default to jpeg.
-w or --web	Sets the target proxy Res so that the larger dimension is 640 - which is an ideal size for email and web work. 
         			If images are smaller than this res they will not be alterred.
-1 or --1k		Sets the target proxy Res so that the lerger dimension is 1024 - for a 1k approximation. 
         			If images are smaller than this res they will not be alterred.
-m or --waterMark	Enable the watermarking. If proxies are being created watermarking will take place second.
-o or --opacity         	Sets the opacity level of the watermark. Default is 70 (percent) if this value isn't specified.
-p or --position		Sets the position of the watermark file from 1-5. These positions are listed numerically from top left heading clockwise. The 5th position is centered. 
-i or --invert		Inverts the watermark image when in screen mode, handy if you havent had time to prep the watermark properly.

### Usage example:

> $python resmark_pic.py -d 2 -m -p 4 -o 50 /Path/To/File/Or/Folder

this example will make half resolution proxies with a watermark in the lower left corner at 50% opacity.



## mark_pic.py

It's the same as resmark_pic.py except the image resizing capabilities.

###Usage example:

> $ python mark_pic.py -p 3 -o 75 -t /Path/To/File/Or/Folder

this example will place the watermark in the lower right corner of the images, with opacity set to 75%.




