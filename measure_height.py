#!/usr/bin/python
# Imports
import cv2
import numpy as np


def measure_plant(dir):
    green = measure_green(dir)
    height = measure_height(dir)
    print(green, height)
    return green, height

def measure_height(dir):
    # Opening image
    img = cv2.imread(dir)

    # Scale your BIG image into a small one:
    scalePercent = 0.3

    # Calculate the new dimensions
    width = int(img.shape[1] * scalePercent)
    height = int(img.shape[0] * scalePercent)
    newSize = (width, height)

    # Resize the image:
    img = cv2.resize(img, newSize, None, None, None, cv2.INTER_AREA)
    #cv2.imshow("this",img)
    # OpenCV opens images as BRG 
    # but we want it as RGB We'll 
    # also need a grayscale version
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    
    # Use minSize because for not 
    # bothering with extra-small 
    # dots that would look like STOP signs

    stop_data = cv2.CascadeClassifier('cascade.xml')
    found = stop_data.detectMultiScale(img_gray, 
                                    minSize =(int(img.shape[0]*0.7), int(img.shape[1]*0.7)))
    
    # Don't do anything if there's 
    # no sign
    amount_found = len(found)
    ppi = 50
    heights = []
    if amount_found != 0:
        
        # There may be more than one
        # sign in the image
        for (x, y, width, height) in found:
            
            # We draw a green rectangle around
            # every recognized sign
            cv2.rectangle(img_rgb, (x, y), 
                        (x + height, y + width), 
                        (0, 255, 0), 5)
            heights.append(height/ppi)
            
    # Creates the environment of 
    # the picture and shows it
    #plt.subplot(1, 1, 1)
    
    cv2.imshow("ANDed mask",img_rgb)
    cv2.waitKey(0)
    if(len(heights) != 0):
        return max(heights)
    else:
        return 0

def measure_green(dir):
    # Opening image
    img = cv2.imread(dir)
    # Here, you define your target color as
    # a tuple of three values: RGB
    green = [130, 158, 0]

    # You define an interval that covers the values
    # in the tuple and are below and above them by 20
    diff = 20

    # Be aware that opencv loads image in BGR format,
    # that's why the color values have been adjusted here:
    boundaries = [([green[2], green[1]-diff, green[0]-diff],
            [green[2]+diff, green[1]+diff, green[0]+diff])]

    # Scale your BIG image into a small one:
    scalePercent = 0.3

    # Calculate the new dimensions
    width = int(img.shape[1] * scalePercent)
    height = int(img.shape[0] * scalePercent)
    newSize = (width, height)

    # Resize the image:
    img = cv2.resize(img, newSize, None, None, None, cv2.INTER_AREA)

    # check out the image resized:
    #cv2.imshow("img resized", img)
    #cv2.waitKey(0)

    lowerValues = np.array([29, 89, 70])
    upperValues = np.array([179, 255, 255]) 
    # for each range in your boundary list:
    for (lower, upper) in boundaries:
        hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # You get the lower and upper part of the interval:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # cv2.inRange is used to binarize (i.e., render in white/black) an image
        # All the pixels that fall inside your interval [lower, uipper] will be white
        # All the pixels that do not fall inside this interval will
        # be rendered in black, for all three channels:
        hsvMask = cv2.inRange(hsvImage, lowerValues, upperValues)

        # Check out the binary mask:
        cv2.imshow("binary mask", hsvMask)
        cv2.waitKey(0)

        # Now, you AND the mask and the input image
        # All the pixels that are white in the mask will
        # survive the AND operation, all the black pixels
        # will remain black
        hsvOutput = cv2.bitwise_and(img, img, mask=hsvMask)

        # Check out the ANDed mask:
        cv2.imshow("ANDed mask", hsvOutput)
        cv2.waitKey(0)

        # You can use the mask to count the number of white pixels.
        # Remember that the white pixels in the mask are those that
        # fall in your defined range, that is, every white pixel corresponds
        # to a green pixel. Divide by the image size and you got the
        # percentage of green pixels in the original image:
        ratio_green = cv2.countNonZero(hsvMask)/(img.size/3)

        # This is the color percent calculation, considering the resize I did earlier.
        colorPercent = (ratio_green * 100)

        # Print the color percent, use 2 figures past the decimal point
        #print('green pixel percentage:', np.round(colorPercent, 2))
        print(colorPercent)
        cv2.imshow("images", np.hstack([img, hsvOutput]))
        cv2.waitKey(0)
        return  np.round(colorPercent, 2)
        # numpy's hstack is used to stack two images horizontally,
        # so you see the various images generated in one figure:
