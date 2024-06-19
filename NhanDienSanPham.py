import tkinter
from PIL import Image, ImageTk
import numpy as np
import imutils
import serial
import time
import cv2


np.set_printoptions(suppress=True)


def run():
    global anhbia
    anhbia.destroy()
    url = 'http://192.168.0.107:4747/video'
    
    cap = cv2.VideoCapture(url)
    cap.set(3, 640)
    cap.set(4, 480)

    count_R = 0
    count_G = 0
    count_B = 0

    count_R_Tr = 0
    count_R_Sq = 0
    count_R_Ci = 0

    count_G_Tr = 0
    count_G_Sq = 0
    count_G_Ci = 0

    count_B_Tr = 0
    count_B_Sq = 0
    count_B_Ci = 0

    count_T = 0

    Arduino_serial = serial.Serial('COM4', 115200,)
    time.sleep(1)

    while True:
        ret, frame = cap.read()
        imgFrame = cv2.flip(frame, 1)
        belt = imgFrame[135:450, 0:580]
        hsv = cv2.cvtColor(belt, cv2.COLOR_BGR2HSV)
        _, threshold = cv2.threshold(belt, 235, 255, cv2.THRESH_BINARY)

        # Nếu không thể đọc khung hình, thoát khỏi vòng lặp
        if not ret:
            break

        lower_Red = np.array([0, 50, 150])  # 0 90 190
        upper_Red = np.array([15, 255, 255])

        lower_Green = np.array([35, 95, 220])
        upper_Green = np.array([70, 255, 255])

        lower_Blue = np.array([90, 60, 100])  # 90 60 70
        upper_Blue = np.array([114, 255, 255])

        mask1 = cv2.inRange(hsv, lower_Red, upper_Red)
        mask2 = cv2.inRange(hsv, lower_Green, upper_Green)
        mask3 = cv2.inRange(hsv, lower_Blue, upper_Blue)

        cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = imutils.grab_contours(cnts1)

        cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts2 = imutils.grab_contours(cnts2)

        cnts3 = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts3 = imutils.grab_contours(cnts3)

        cv2.line(belt, (340, 0), (340, belt.shape[0]), (255, 127, 0), 2)
        for c in cnts1:
            area1 = cv2.contourArea(c)
            (x, y, w, h) = cv2.boundingRect(c)

            if area1 > 450:
                approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
                cv2.drawContours(belt, [approx], -1, (0, 0, 0), 2)
                cv2.rectangle(belt, (x, y), (x + w, y + h), (0, 255, 255), 2)

                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                if len(approx) == 3:
                    if 340 <= cx <= 345:
                        count_R_Tr += 1
                    cv2.putText(belt, "Tam Giac", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
                elif len(approx) == 4:
                    if 340 <= cx <= 345:
                        count_R_Sq += 1
                    cv2.putText(belt, "Hinh Vuong", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                1)
                else:
                    if 340 <= cx <= 345:
                        count_R_Ci += 1
                    cv2.putText(belt, "Hinh Tron", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                1)

                if 340 <= cx <= 345:
                    count_R += 1
                    Arduino_serial.write('R'.encode())
                    time.sleep(0.1)

                cv2.circle(belt, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(belt, "Red", (cx - 60, cy - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        for c in cnts2:
            area2 = cv2.contourArea(c)
            (x, y, w, h) = cv2.boundingRect(c)

            if area2 > 450:
                approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
                cv2.drawContours(belt, [approx], -1, (0, 0, 0), 2)
                cv2.rectangle(belt, (x, y), (x + w, y + h), (0, 255, 255), 2)

                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                if len(approx) == 3:
                    if 340 <= cx <= 345:
                        count_G_Tr += 1
                    cv2.putText(belt, "Tam Giac", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
                elif len(approx) == 4:
                    if 340 <= cx <= 345:
                        count_G_Sq += 1
                    cv2.putText(belt, "Hinh Vuong", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                1)
                else:
                    if 340 <= cx <= 345:
                        count_G_Ci += 1
                    cv2.putText(belt, "Hinh Tron", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                1)

                if 340 <= cx <= 345:
                    count_G += 1
                    Arduino_serial.write('G'.encode())
                    time.sleep(0.1)

                cv2.circle(belt, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(belt, "Green", (cx - 60, cy - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        for c in cnts3:
            area3 = cv2.contourArea(c)
            (x, y, w, h) = cv2.boundingRect(c)

            if area3 > 450:
                approx = cv2.approxPolyDP(c, 0.02 * cv2.arcLength(c, True), True)
                cv2.drawContours(belt, [approx], -1, (0, 0, 0), 2)

                cv2.rectangle(belt, (x, y), (x + w, y + h), (0, 255, 255), 2)

                M = cv2.moments(c)
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                if len(approx) == 3:
                    if 340 <= cx <= 345:
                        count_B_Tr += 1
                    cv2.putText(belt, "Tam Giac", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
                elif len(approx) == 4:
                    if 340 <= cx <= 345:
                        count_B_Sq += 1
                    cv2.putText(belt, "Hinh Vuong", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                1)
                else:
                    if 340 <= cx <= 345:
                        count_B_Ci += 1
                    cv2.putText(belt, "Hinh Tron", (cx - 80, cy - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255),
                                1)

                if 340 <= cx <= 345:
                    count_B += 1
                    Arduino_serial.write('B'.encode())
                    time.sleep(0.1)

                cv2.circle(belt, (cx, cy), 7, (255, 255, 255), -1)
                cv2.putText(belt, "Blue", (cx - 60, cy - 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        count_T = count_R + count_G + count_B
        mask = mask1 | mask2 | mask3

        def show_cameras(mask, belt):
            if mask is not None:
                # Đảm bảo cả hai frame có cùng kích thước
                mask = cv2.resize(mask, belt.shape[:2][::-1])
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)

                height, width, _ = belt.shape
                new_height = max(mask.shape[0], height) + 500
                new_width = mask.shape[1] + width + 500
                new_frame = np.ones((new_height, new_width, 3), dtype=np.uint8) * 255

                # Tính toán vị trí của hai frame
                mask_x = 10
                mask_y = 20
                belt_x = 10
                belt_y = 360

                # Đặt hai frame vào vị trí mới trong khung hình mới
                new_frame[mask_y:mask_y + mask.shape[0], mask_x:mask_x + mask.shape[1]] = mask  # [y1:y2, x1:x2]
                new_frame[belt_y:belt_y + belt.shape[0], belt_x:belt_x + belt.shape[1]] = belt

                # Thêm các label vào khung hình mới
                font_scale = 1
                thickness = 2

                # Giao diện hiển thị
                cv2.putText(new_frame, f"RED", (635, 300), 4, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f"GREEN", (635, 380), 4, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f"BLUE", (635, 460), 4, font_scale, (255, 0, 0), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f"TOTAL: {count_T}", (635, 600), 4, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
                cv2.rectangle(new_frame, (620, 550), (830, 630), (22, 224, 218), 10)  # (x1,y1), (x2,y2)

                cv2.putText(new_frame, f"SQUARE", (785, 200), 4, font_scale, (128, 128, 128), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_R_Sq}", (815, 300), 4, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_G_Sq}", (815, 380), 4, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_B_Sq}", (815, 460), 4, font_scale, (255, 0, 0), thickness, cv2.LINE_AA)

                cv2.putText(new_frame, f"TRIANGLE", (945, 200), 4, font_scale, (128, 128, 128), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_R_Tr}", (995, 300), 4, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_G_Tr}", (995, 380), 4, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_B_Tr}", (995, 460), 4, font_scale, (255, 0, 0), thickness, cv2.LINE_AA)

                # Thêm Label Hình tròn và đếm số
                cv2.putText(new_frame, f"CIRCLE", (1140, 200), 4, font_scale, (128, 128, 128), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_R_Ci}", (1165, 300), 4, font_scale, (0, 0, 255), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_G_Ci}", (1165, 380), 4, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)
                cv2.putText(new_frame, f" {count_B_Ci}", (1165, 460), 4, font_scale, (255, 0, 0), thickness, cv2.LINE_AA)
                cv2.rectangle(new_frame, (620, 140), (1260, 500), (0, 0, 0), 2)  # (x1,y1), (x2,y2)

                cv2.putText(new_frame, f"HE THONG PHAN LOAI", (630, 80), 4, 1.7, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.rectangle(new_frame, (620, 15), (1260, 110), (0, 0, 0), 2)
                cv2.putText(new_frame, f"COLOR", (635, 200), 4, font_scale, (128, 128, 128), thickness, cv2.LINE_AA)

                cv2.imshow('Nhan Dien San Pham', new_frame)
            else:
                print("Khong co du lieu hinh anh.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        show_cameras(mask, belt)


# Tao cua so giao dien
anhbia = tkinter.Tk()
anhbia.geometry("1280x720")
anhbia.title("He thong phan loai san pham")
# Mô hình ảnh bìa
anh = Image.open(r"D:/XLA/ESP32_CAM_COUNTER/AnhBia.jpg")
# Chỉnh kích thước ảnh
resizeimage = anh.resize((1280, 650))
a = ImageTk. PhotoImage(resizeimage)
img = tkinter.Label(image=a)
img.grid(column=0, row=0)

Btn = tkinter.Button(anhbia, text="START", font=("Constantia", 20, 'bold'), bg='green', fg='black', command=run)
Btn.place(x=600, y=500)
anhbia.mainloop()

