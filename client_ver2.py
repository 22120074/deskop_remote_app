# cái ver 2 là cái lỏ của h anh, cái trên cái tao sửa sơ sơ lại, vẫn đg đợi nó sửa lại dựa trên đó, do nó code bừa với thùa thải nhiều quá
# Socket
import socket
import pickle# thư viện dùng để nén dữ liệu 
from pynput import mouse
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
# from PyQt5.QtWidgets import ...: Import các lớp và phương thức từ PyQt5 để xây dựng giao diện người dùng.
#from PyQt5.QtGui import ...: Import các lớp và phương thức từ PyQt5 để làm việc với đồ họa.
#from PyQt5.QtCore import ...: Import các lớp và phương thức từ PyQt5 để sử dụng các tính năng cơ bản của PyQt5.

from pynput import keyboard# thư viện để nhập kí tự từ bàn phím
from datetime import datetime #datetime: Thư viện datetime dùng để làm việc với thời gian.

server_address = ('127.0.0.1', 12345)


class Dekstop(QMainWindow):
    def __init__(self):#def __init__(self):: Hàm khởi tạo của class Dekstop.
        super().__init__()
        self.initUI()

    def initUI(self):#def initUI(self):: Hàm tạo giao diện người dùng của ứng dụng.
        self.layout = QVBoxLayout(self)
        
        self.pixmap = QPixmap()
        
        self.newWindow = QDialog()
        
        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.label2 = QLabel(parent = self.newWindow)
        self.layout.addWidget(self.label2)
        
        self.label.setPixmap(self.pixmap)
        self.label.resize(self.width(), self.height())
        self.setGeometry(QRect(pyautogui.size()[0] // 4, pyautogui.size()[1] // 4, 400, 90))
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("[CLIENT] Remote Desktop: " + str(randint(99999, 999999)))
        self.start = Thread(target = self.ChangeImage, daemon = True)

        self.btn = QPushButton(self) # nút khởi động chương trình
        self.btn.move(5, 55)
        self.btn.resize(390, 30)
        self.btn.setText("Start Demo")
        self.btn.clicked.connect(self.StartThread)

        
        self.ip = QLineEdit(self) 
        self.ip.move(5, 5)
        self.ip.resize(390, 20)
        self.ip.setPlaceholderText("IP") 

        self.port = QLineEdit(self)
        self.port.move(5, 30)
        self.port.resize(390, 20)
        self.port.setPlaceholderText("PORT")

    def StartThread(self):#def StartThread(self):: Hàm khởi động thread khi nút "Start Demo" được nhấn.
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        self.label2.setPixmap(self.pixmap)
        self.label2.resize(1800, 800)
        self.label2.setFixedSize(self.width(), self.height())
        
        self.newWindow.setGeometry(QRect(0, 0, 400, 90))
        self.newWindow.setFixedSize(1800, 800)
        self.newWindow.setWindowTitle("[Server] Remote Desktop: " + str(randint(99999, 999999)))
        self.newWindow.show()

        thread_keyboard = Thread(target=self.putkeyboard, args=(client_socket,))
        thread_mouse = Thread(target=self.putkeymouse, args=(client_socket,))
        self.start.start()

        # Bắt đầu cả hai thread
        thread_keyboard.start()
        thread_mouse.start()

    def putkeyboard(self, client_socket):
        on_release = True
        while on_release != False:
            with keyboard.Listener(
                on_press=keyPressed,
                on_release=keyReleased
            ) as listener:
                listener.join()

    def putkeymouse(self, client_socket):
        while True:
            with mouse.Listener(
                on_move=lambda x, y: on_move(x, y, client_socket),
                on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, client_socket),
                on_scroll=lambda x, y, dx, dy: on_scroll(x, y, dx, dy, client_socket)
            ) as listener:
                listener.join()


       
    
    
    def ExitApp(self):
        # Dừng các thread và giải phóng tài nguyên trước khi thoát ứng dụng ...
        self.close()

    def ChangeImage(self,client_socket):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)

        while True:
            img_bytes = client_socket.recv(9999999)
            self.pixmap.loadFromData(img_bytes)
            self.label2.setPixmap(self.pixmap)
            self.label2.setScaledContents(True)
            self.label2.setAlignment(Qt.AlignCenter)
            self.label2.setFixedSize(1800, 800)
           
          

# //////////////////////////////////////                     0000000000000000000000000000000            ////////////////////////////////// 
            
# Nhiệm vụ hiện tại là phân luồng và gửi thông tin từ client sang server



def getKeyName(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)
    

def keyPressed(key, logdata):
    keyName = getKeyName(key)
    logdata.append([keyName])


def send_keyboard_data(logdata,client_socket):
    message = f"{keyboard},{logdata}"
    client_socket.send(message.encode('utf-8'))


def keyReleased(key, logdata):
    send_keyboard_data(logdata)
    if key == keyboard.Key.esc:
        send_keyboard_data(logdata)
        return False


def putkeyboard(): 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    on_release = True
    while True &on_release != False:
        with keyboard.Listener(
            on_press=keyPressed,
            on_release=keyReleased
        ) as listener:
            listener.join()
    
    client_socket.close()
# Đảm bảo rằng biến server_address đã được xác định trước khi chạy mã


        
   
        


#  ///////////////                               ooooooooooooooooooo              /////////////////////////////



def on_move(x, y):
    logdata2 = []
    logdata2.append([ f'Mouse moved to ({x}, {y})'])
    send_keymouse_data(logdata2,"on_move")
     #mouse thì sẽ gửi là message = {key}, {trường hợp}, {x}, {y} nếu th là on_scroll thì thêm {dx}, {dy} cuối nũa
    

def on_click(x, y, button, pressed,client_socket):
    logdata2 = []
    action = 'Pressed' if pressed else 'Released'
    logdata2.append([ f'Mouse {action} at ({x}, {y}) with {button}'])
    send_keymouse_data(logdata2,"on_click")
    if (x,y) ==(305,5)& pressed:
         data="disconnect...."
         message=f"{exit},{data}"
         client_socket.send(message.encode('utf-8'))
         



def on_scroll(x, y, dx, dy,client_socket):
    logdata2 = []
    logdata2.append([ f'Scrolled at ({x}, {y}) with delta ({dx}, {dy})'])
   
    th="on_roll"
    message=f"{mouse},{th},{logdata2}{dx}{dy}"
    client_socket.send(message.encode('utf-8'))

#on_move: Được gọi khi chuột di chuyển.
#on_click: Được gọi khi một nút chuột được nhấn hoặc nhả.
#on_scroll: Được gọi khi chuột được cuộn.
# Lắng nghe sự kiện chuột

def send_keymouse_data(data,th,client_socket):
    
     # Tạo chuỗi message sử dụng f-string
    message = f"{mouse},{th},{data}"
        # Gửi message thông qua socket sau khi mã hóa bằng UTF-8
    client_socket.send(message.encode('utf-8'))
    


def putkeymouse():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    while True:
        with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
            listener.join()
    
    client_socket.close()



# ///////////////////////////////            0000000000000000000000000000       ///////////////////////////////// 



if __name__ == '_main_':
    app = QApplication(sys.argv)
    ex = Dekstop()
    ex.show()
    sys.exit(app.exec())
    
   # app = QApplication(sys.argv): Khởi tạo ứng dụng PyQt.
#ex = Dekstop(): Tạo một đối tượng của class Dekstop.
#ex.show(): Hiển thị cửa sổ ứng dụng.
#sys.exit(app.exec()): Chạy vòng lặp sự kiện của PyQt.
    # Ghi rõ các kiểu dữ liệu khi truyền sang server
