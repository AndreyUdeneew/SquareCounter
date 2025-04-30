# This is a sample Python script.
import csv
from tkinter import *
from tkinter import ttk
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import filedialog
from tkinter.filedialog import *

import cv2

from matplotlib import pyplot as plt, gridspec
import numpy as np
# import xlwt
# from xlsxwriter import Workbook

points = []  # Список для хранения точек контура
drawing = False  # Флаг для отслеживания процесса рисования
image = None  # Исходное изображение
image_copy = None  # Копия для рисования

def mouse_callback(event, x, y, flags, param):
    global points, drawing, image_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        # Добавляем точку при клике
        points.append((x, y))
        drawing = True
        # Рисуем круги и линии
        if len(points) > 1:
            cv2.line(image_copy, points[-2], points[-1], (0, 255, 0), 2)
        cv2.circle(image_copy, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow("Image", image_copy)

def massProcessing():
    global fileNames, points, drawing, image_copy
    fileName = askopenfilename(parent=window)
    # output = format(text2.get("1.0",'end-1c'))
    # sumRed_RAW = []
    # with open(output, 'w', newline='') as Kf:
    #     writer = csv.writer(Kf, delimiter=';')
    # image = cv2.imread(fileName)
    image = cv2.imdecode(np.fromfile(fileName, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    image_copy = image.copy()

    # Создаем окно и устанавливаем обработчик мыши
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouse_callback)

    print("Инструкции:")
    print("1. Кликайте ЛКМ чтобы добавить точки контура")
    print("2. Нажмите 'C' чтобы завершить ввод и посчитать пиксели")
    print("3. Нажмите 'Q' чтобы выйти")

    while True:
        cv2.imshow("Image", image_copy)
        key = cv2.waitKey(1) & 0xFF

        # Завершение ввода контура
        if key == ord('c'):
            if len(points) > 2:
                # Замыкаем контур (соединяем последнюю и первую точки)
                cv2.line(image_copy, points[-1], points[0], (0, 255, 0), 2)
                cv2.imshow("Image", image_copy)

                # Создаем маску и заполняем контур
                mask = np.zeros(image.shape[:2], dtype=np.uint8)
                pts = np.array(points, dtype=np.int32)
                cv2.fillPoly(mask, [pts], 255)

                # Подсчитываем пиксели
                pixel_count = cv2.countNonZero(mask)
                print(f"Количество пикселей в области: {pixel_count}")

                # Показываем залитую область
                filled = cv2.bitwise_and(image, image, mask=mask)
                cv2.imshow("Filled Area", filled)
                text1.insert(INSERT, str(pixel_count))
            else:
                print("Для создания контура нужно минимум 3 точки!")
            points = []  # Сброс точек

        # Выход из программы
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    window = Tk()
    window.geometry('1150x650')
    window.title("Area counter")
    text1 = Text(width=15, height=1)  # image
    text1.grid(column=1, row=1, sticky=W)
    # text2 = Text(width=70, height=1)  # image
    # text2.grid(column=1, row=0, sticky=W)
    btn1 = Button(window, text="Select Images", command=massProcessing)
    btn1.grid(column=0, row=1, sticky=W)
    # btn2 = Button(window, text="Select SavePlace", command=selectOutfile)
    # btn2.grid(column=0, row=0, sticky=W)
    window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
