import cv2
import numpy as np

if __name__ == '__main__':
    img_file = r'C:\Users\saira\OneDrive\Desktop\Sample.png'
    original_img = cv2.imread(img_file)
    # cv2.imshow('Original', original_img)
    # cv2.waitKey(0)
    copy_img = original_img.copy()
    gray_img = cv2.cvtColor(copy_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Gray', gray_img)
    # cv2.waitKey(0)
    # bw_img = cv2.bitwise_not(gray_img)
    # cv2.imshow('B&W', bw_img)
    # cv2.waitKey(0)
    thresh_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv2.imshow('Thresh', thresh_img)
    # cv2.waitKey(0)
    blur_img = cv2.GaussianBlur(thresh_img, (5, 5), 0)
    # cv2.imshow('Blur', blur_img)
    # cv2.waitKey(0)
    canny_img = cv2.Canny(blur_img, 100, 200)
    # cv2.imshow('Canny', canny_img)
    # cv2.waitKey(0)
    kernel = np.ones((5, 5), np.uint8)
    erode_img = cv2.erode(blur_img, kernel=kernel, iterations=1)
    # cv2.imshow('Erode', erode_img)
    # cv2.waitKey(0)
    dilate_img = cv2.dilate(erode_img, kernel=kernel, iterations=1)
    # cv2.imshow('Dilate', dilate_img)
    # cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(dilate_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            # peri = cv2.arcLength(contour, True)
            # approx = cv2.approxPolyDP(contour, 0.2 * peri, True)
            # x, y, w, h = cv2.boundingRect(approx)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(copy_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('BoundingBox', copy_img)
    cv2.waitKey(0)
