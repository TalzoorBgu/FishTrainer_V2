#!/usr/bin/env python

'''
TBD - enter output file name as arg
TBD - create templates
'''
# USAGE
# python scene_planner.py --video fish_video_example.mp4
# python scene_planner.py  # for use with camera

import argparse
import cv2
import random
import os
import sys

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not

refPt = []
fish = []
cropping = False


def get_file_name(_camera):
    full_script_path = '{}{}'.format(os.path.dirname(os.path.realpath(__file__)), '\\')
    file_path = '{}tank_config_cam_{}.txt'.format(full_script_path, _camera)

    return file_path


def draw_current(_img, _camera):
    try:
        file_path = get_file_name(_camera)

        fish_draw = []
        with open(file_path) as f:
            lines = f.read().splitlines()
        for line in lines:
            fish_draw.append(eval(line))
        for fishy in fish_draw:
            cv2.rectangle(_img, (fishy['left'], fishy['upper']), (fishy['right'], fishy['lower']),
                      (255, 255, 255), 1)
    except IOError:
        print ('file dosent exsit - cannot draw')


def click_and_crop(event, x, y, flags, param, _camera):
    global image, fish ,refPt

    # grab references to the global variables
    global refPt, cropping


    print("_camera:{}".format(_camera))
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False

        # arrange points left-right up-down
        ordered=[(min(refPt[0][0],refPt[1][0]),min(refPt[0][1],refPt[1][1]))]
        ordered.append((max(refPt[0][0],refPt[1][0]),max(refPt[0][1],refPt[1][1])))

        fish.append({'camera:': _camera, 'upper': ordered[0][1], 'lower': ordered[1][1], 'left': ordered[0][0], 'right': ordered[1][0]})

        # draw a rectangle around the region of interest
        cv2.rectangle(image, ordered[0], ordered[1],
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)
        cv2.imshow("image", image)

def SP_Main(_camera=0):
    global image, fish, refPt
    refPt = []
    fish = []
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", help="Path to the image")
    ap.add_argument("-v", "--video", help="path to the (optional) video file")
    args = vars(ap.parse_args())

    # load the image, clone it, and setup the mouse callback function
    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        video_capture = cv2.VideoCapture(int(_camera))

    # otherwise, grab a reference to the video file
    else:
        video_capture = cv2.VideoCapture(args["video"])

    ret, image = video_capture.read()

    if(image is None):#check for empty frames
        print ('No Image')

    # draw current configuration
    draw_current(image, _camera)

    # image = cv2.imread(args["image"])
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop, _camera)

    # keep looping until the 'c' key is pressed
    while True:

        # Write Text
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

        cv2.putText(image, 'please mark your tanks',(50,50),font,fontScale,fontColor,lineType)
        cv2.putText(image, 'press "c" to finish and "r" to reset',(50,100),font,fontScale,fontColor,lineType)
        ''
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        # 'r'=99            'c'=99
        # 'R'=82            'C'=67
        # 'heb(r)' = 248    'heb(c)=225

        #print key
        if (key == ord('r') or key == ord('R') or key == 248) :
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif (key == ord('c') or key == ord('C') or key == 225):
            break

    # if there are two reference points, then crop the region of interest
    # from the image and display it

    if len(refPt) == 2:
        file_path = get_file_name(_camera)

        thefile = open(file_path, 'w+')

        print ("file_path:{}".format(file_path))

        for fishy in fish:
            print(fishy)
            thefile.write("%s\n" % fishy)
        thefile.flush()
        thefile.close()
        print("tank_config.txt saved!")



    # close all open windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    SP_Main()