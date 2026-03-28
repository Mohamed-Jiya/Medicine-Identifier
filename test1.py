import cv2 as cv

img = cv.imread('duo.jpg')

if img is None:
    print("Image not found")
else:
    # cv.imshow('duo', img)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #resized = cv.resize(gray, (600, 500))#width and hight
    blur = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)
    _, clean = cv.threshold(blur, 150, 255, cv.THRESH_BINARY)
    resized_clean = cv.resize(clean, (600, 500))
    #cv.imshow('Threshold', clean)
    cv.imshow('Threshold', resized_clean)
    # cv.imshow('resized', blur)

cv.waitKey(0)