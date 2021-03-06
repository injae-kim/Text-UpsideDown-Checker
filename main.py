import cv2
import numpy as np
import time
import os

path_dir = './img/img2_reversed'
file_list = os.listdir(path_dir)

for file in file_list:

    start = time.time()

    img = cv2.imread(path_dir+'/'+file)
    _img = img.copy()

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
        cv2.rectangle(_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # cv2.imshow('contours', _img)


    direction_good_count = 0
    direction_bad_count = 0
    character_count = 0

    for cnt in contours:    # for each string

        x, y, w, h = cv2.boundingRect(cnt)

        crop = thresh[y:y+h, x:x+w]
        # cv2.imshow('crop', crop)

        pass_flag = False

        crop_points = [0]

        _crop = cv2.cvtColor(crop, cv2.COLOR_GRAY2RGB)

        # slicing string by one by one character
        for col in range(w):
            for row in range(h):

                if crop[row][col] > 0:
                    pass_flag = False
                    break

                if row == h - 1 and pass_flag == False:
                    cv2.line(_crop, (col, 0), (col, row), (0, 0, 255), 2)
                    crop_points.append(col)
                    pass_flag = True

        crop_points.append(w - 1)
        # cv2.imshow('crop_line', _crop)

        one_character_width = 0
        one_character_height = h

        for i in range(len(crop_points) - 1):   # for each one character

            consonant_list = []# 자음 리스트
            vowel_list = [] # 모음 리스트

            one_character_width = crop_points[i+1] - crop_points[i]

            if crop_points[i+1] - crop_points[i] > 0:

                crop_one_character = crop[:,crop_points[i]:crop_points[i+1]]
                # cv2.imshow('crop_frag', crop_one_character)

                backtorgb = cv2.cvtColor(crop_one_character,cv2.COLOR_GRAY2RGB)
                _contours, _hierarchy = cv2.findContours(crop_one_character, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # 한 글자 안에 너무 많은 자음/모음이 검출되거나 아예 검출되지 않은 경우 pass
                if len(_contours) >= 4 or len (_contours) == 0:
                    continue

                character_count += 1

                for cnt in _contours:
                    x, y, w, h = cv2.boundingRect(cnt)

                    if h / w >= 2.5 or h / w <= 0.4:    # 모음 후보
                        cv2.rectangle(backtorgb, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        vowel_list.append([x, y, w, h])

                    else:   # 자음 후보
                        cv2.rectangle(backtorgb, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        consonant_list.append([x, y, w, h])


            # 자음이 여러개, 모음이 하나만 검출된 경우 (best case)
            if len(consonant_list) == 1 and len(vowel_list) == 1:

                consonant_w, consonant_h = consonant_list[0][2:]
                vowel_w, vowel_h = vowel_list[0][2:]

                #TODO: false case 예외처리

                # 모음이 너무 작은경우, 직선 등의 노이즈가 모음으로 잘못 검출된 경우
                if vowel_w / one_character_width < 0.5 and vowel_h / one_character_height < 0.5:
                    continue

                # 자음이 너무 작은경우
                if consonant_w / one_character_width < 0.25 and consonant_h / one_character_height < 0.25:
                    continue


                if consonant_list[0][0] < vowel_list[0][0]:    # 모음이 자음보다 오른쪽에 위치, ex) 가
                    direction_good_count += 1
                    # print('good direction!')

                elif consonant_list[0][1] < vowel_list[0][1]:   # 모음이 자음보다 아래에 위치, ex) 그
                    direction_good_count += 1
                    # print('good direction!')
                
                else:
                    direction_bad_count += 1
                    # print('bad direction!')

                # print('good_count: ', direction_good_count)
                # print('bad_count: ', direction_bad_count)
                # print()


                # backtorgb = cv2.resize(backtorgb, (512, 512))
                # cv2.imshow('crop_result', backtorgb)

                # while True:
                #     if cv2.waitKey(1) == 27:
                #         break

    print()
    print('--- RESULT: ',path_dir+'/'+file, '---')
    print('good: ', direction_good_count)
    print('bad: ', direction_bad_count)
    print('total character: ', character_count)
    print('direction: ', direction_good_count - direction_bad_count)
    print('time: ', time.time() - start)
        

    cv2.destroyAllWindows()