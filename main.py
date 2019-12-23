import cv2
import numpy as np

img = cv2.imread('./img/Document 67_3.jpg')
# cv2.imshow('img', img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY_INV)

# cv2.imshow('thresh', thresh)


kernel = np.ones((25, 25), np.uint8)
result = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# cv2.imshow('morph', result)

contours, hierarchy = cv2.findContours(result, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    crop = thresh[y:y+h, x:x+w]
    cv2.imshow('crop', crop)

    for col in range(w):
        for row in range(h):
            
            if crop[row][col] > 0:
                break

            if row == h - 1:
                cv2.line(crop, (col, 0), (col, row), (255), 1)
                col += 10

    cv2.imshow('crop_line', crop)

    while True:
        if cv2.waitKey(1) == 27:
            break


for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('contours', img)


while True:
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()