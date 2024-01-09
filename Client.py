# Socket
import time
import socket
from pynput import mouse, keyboard
from pynput.mouse import Button
# Work with Image
from PIL import ImageGrab #Import thư viện ImageGrab từ Pillow để chụp ảnh màn hình.
import io #Import thư viện io để thao tác với dữ liệu nhị phân.
import numpy as np #Import thư viện numpy để làm việc với mảng nhiều chiều.
from random import randint #Import hàm randint để tạo số ngẫu nhiên.
import pyautogui #Import thư viện pyautogui để làm việc với điều khiển màn hình.
# Thread
import threading
from threading import Thread #Import class Thread để tạo và quản lý các thread.
# PyQt5
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QAction, QMessageBox, QLineEdit,  QVBoxLayout, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect, Qt, pyqtSlot
from PyQt5.QtNetwork import QTcpSocket

class Dekstop(QMainWindow):
    def __init__(self): # def __init__(self):: Hàm khởi tạo của class Dekstop.
        super().__init__()
        self.initUI()

    def initUI(self): # def initUI(self):: Hàm tạo giao diện người dùng của ứng dụng.
        # Khởi tạo pixmap
        self.pixmap = QPixmap()
        # Khởi tạo Dialog mới để hiển thị hình ảnh
        self.newWindow = QDialog()
        # Khởi tạo label mới để đăng nhập
        self.label = QLabel(self)
        # Khởi tạo label mới để hiển thị hình ảnh
        self.label2 = QLabel(parent = self.newWindow)

        self.label.setPixmap(self.pixmap)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4 + 170, pyautogui.size()[1] // 4, 600, 200))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("[CLIENT] Remote Desktop: " + str(randint(99999, 999999)))

        self.button = QPushButton(self) # nút khởi động chương trình
        self.button.move(150, 100)
        self.button.resize(300, 90)
        self.button.setStyleSheet("font-size: 30px")
        self.button.setText("Start Demo")
        self.button.clicked.connect(self.StartThread)

        self.ip = QLineEdit(self) # edit text để nhập IP
        self.ip.move(70, 5)
        self.ip.resize(460, 45)
        self.ip.setStyleSheet("font-size: 30px")
        self.ip.setPlaceholderText("IP")

        self.port = QLineEdit(self) # edit text để nhập PORT
        self.port.move(70, 55)
        self.port.resize(460, 45)
        self.port.setStyleSheet("font-size: 30px")
        self.port.setPlaceholderText("PORT")

    def StartThread(self): #def StartThread(self):: Hàm khởi động thread khi nút "Start Demo" được nhấn.
        
        self.label2.setPixmap(self.pixmap)
        self.label2.resize(1920, 1080)
        self.label2.setFixedSize(self.width(), self.height())
        
        self.newWindow.setGeometry(QRect(0, -5, 400, 90))
        self.newWindow.setFixedSize(1920, 1080)
        self.newWindow.setWindowTitle("[Server] Remote Desktop: " + str(randint(99999, 999999)))
        self.newWindow.show()

        # Khởi tạo Main Program
        self.mainthread = Thread(target = self.MainProgram, daemon = True)
        self.mainthread.start()

    # Kiêm tra kết nối 
    def check_connection(self, client_socket):
        try:
            client_socket.connect((self.ip.text(), int(self.port.text())))
            return True
        except Exception as e:
            return False
        
    # Thread đổi ảnh _________________________________________________________________________________________________
    def MainProgram(self):
        # Khởi tạo kết nối
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        if(self.check_connection(client_socket)):
            with client_socket:     
                self.thread_keyboard = Thread(target = lambda: self.putkeyboard(client_socket), daemon = True)
                self.thread_keyboard.start()

                self.thread_mouse = Thread(target = lambda: self.putkeymouse(client_socket), daemon = True)         
                self.thread_mouse.start()

                try:
                    while True:
                        img_bytes = client_socket.recv(9999999)
                        self.pixmap.loadFromData(img_bytes)
                        self.label2.setPixmap(self.pixmap)
                        self.label2.setScaledContents(True)
                        self.label2.setAlignment(Qt.AlignCenter)
                        self.label2.setFixedSize(1920, 1080)       
                except:
                    client_socket.close()
        else:
            self.newWindow.close()
            self.ip.clear()
            self.ip.setStyleSheet("font-size: 30px")
            self.ip.setPlaceholderText(" Wrong IP or PORT")

        


    # Thread gửi kí tự _______________________________________________________________________________________________
    def putkeyboard(self, client_socket):
        on_release = True
        while on_release:
            with keyboard.Listener(
                on_press = lambda key: self.keyPressed(key, client_socket),
                on_release = lambda key: self.keyReleased(key, client_socket)
            ) as listener:
                listener.join()
    
        
    def getKeyName(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char
        else:
            return str(key)


    def keyPressed(self, key,client_socket):
        keyName = self.getKeyName(key)
        message = f"{'keyboard'},{keyName},{'on_press'}"
        client_socket.send(message.encode('utf-8'))
        time.sleep(0.3)

        
    def keyReleased(self, key,client_socket):
        keyName = self.getKeyName(key)
        message = f"{'keyboard'},{keyName},{'on_release'}"
        client_socket.send(message.encode('utf-8'))
        if key == keyboard.Key.esc:
            return False
        time.sleep(0.3)

   

    # Thread gửi chuột ____________________________________________________________________________________________
    def putkeymouse(self, client_socket):
        while True:
            with mouse.Listener(
                on_move = lambda x, y: self.on_move(x, y, client_socket),                                         #on_move: Được gọi khi chuột di chuyển.
                on_click = lambda x, y, button, pressed: self.on_click(x, y, button, pressed, client_socket),     #on_click: Được gọi khi một nút chuột được nhấn hoặc nhả.
                on_scroll = lambda x, y, dx, dy: self.on_scroll(dx, dy, client_socket)                            #on_scroll: Được gọi khi chuột được cuộn.
            ) as listener:
                listener.join()
        
    def on_move(self, x, y, client_socket):
        th = "on_move"
        message = f"{'mouse'},{th},{x},{y},{'_'},{'_'}"
        client_socket.send(message.encode('utf-8'))
        # time.sleep(0.2)
        
                                                                                                                                                                                                                
        

    def on_click(self, x, y, button, pressed, client_socket):
        th = "on_click"
        action = 'Pressed' if pressed else 'Released'
        
        if button == Button.right:
            message = f"{'mouse'},{th},{x},{y},{action},{'right'}" 

        if button == Button.left:
            message = f"{'mouse'},{th},{x},{y},{action},{'left'}" 

        if button == Button.middle:
            message = f"{'mouse'},{th},{x},{y},{action},{'middle'}"

        client_socket.send(message.encode('utf-8'))
        time.sleep(0.3)




    def on_scroll(self, dx, dy, client_socket):
        th = "on_roll"
        message = f"{'mouse'},{th},{dx},{dy},{'_'},{'_'} "
        client_socket.send(message.encode('utf-8'))
        time.sleep(0.3)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())
    
# app = QApplication(sys.argv): Khởi tạo ứng dụng PyQt.
# ex = Dekstop(): Tạo một đối tượng của class Dekstop.
# ex.show(): Hiển thị cửa sổ ứng dụng.
# sys.exit(app.exec()): Chạy vòng lặp sự kiện của PyQt.
# Ghi rõ các kiểu dữ liệu khi truyền sang server
