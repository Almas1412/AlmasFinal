from PyQt5 import QtWidgets,uic
from PyQt5.QtSerialPort import QSerialPort,QSerialPortInfo
from PyQt5.QtCore import QIODevice, QByteArray,QThread,Qt,QFile,QTimer,QDateTime,pyqtSignal
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.QtWidgets import *
import cv2
import pyrebase
import re
import json
import _datetime                                                                                    # Подключение библеотек

interation = 0                                                                                      # Логический счетчик кода
recipe= ""
userId=""


class camThread(QThread):                                                                           # Поток захвата Камеры и пойска QR - кода
    def __init__(self,mainwindow,parent=None):                                                      # Запуск камеры
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):                                                                                  # Вывод картины с камеры
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        def displayimage(img, window=1):
            if len(img.shape) == 3:
                if (img.shape) == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888

            img = QImage(img, img.shape[1], img.shape[0], qformat)
            img = img.rgbSwapped()
            ui.imglabel.setPixmap(QPixmap.fromImage(img))
            ui.imglabel.setMinimumSize(1, 1)
            ui.imglabel.setScaledContents(True)

        while (cap.isOpened()):                                                                     # Считывания Данных с захваченной рисунка QR кода
            ret, frame = cap.read()
            if ret == True:
                displayimage(frame, 1)
                cv2.waitKey()
                data, one, ret = detector.detectAndDecode(frame)
                if data:
                    cv2.destroyAllWindows()
                    print("got it")
                    itemid = data
                    if(interation == 0):                                                            # Если лог.счетчик ровно нулю то просим авторизацию
                        print(str(interation))
                        authQR(itemid)
                    else:                                                                           # Если лог.счетчик не ровно нулю то просим id продукта
                        print(str(interation))
                        readQR(itemid)

                    cap.release()
                    cv2.destroyAllWindows()


            else:
                print('return not found')

    def stop(self):                                                                                 # Остановка потока
        self.terminate()






app = QtWidgets.QApplication([])                                                                    # Запуск основного оконного приложения
ui = uic.loadUi("cart2.ui")                                                                         # Загрузка .ui файла
ui.setWindowTitle("ShopCart")                                                                       # Задаем титулное название окну

buttontoLayout = {}                                                                                 # Объявление  list для дальнейшех операций в строках 330 и 341

serial=QSerialPort()                                                                                # Объявление Серийного порта для подключение Arduino
serial.setBaudRate(9600)                                                                            # Задается частота бодов передаваемых по бодам

sshFile="Adaptic.qss"                                                                               # .qss  Файл для стиля элементов окна (кнопки и лейбли)
with open(sshFile,"r") as fh:
    app.setStyleSheet(fh.read())


firebaseConfig = {'apiKey': "AIzaSyADtjjQDQdbvNEAUJzan3_XMS6zQEOLGsA",                              # Настройки Firebase для подключения к приложению
  'authDomain': "fir-crud-5b277.firebaseapp.com",
  'databaseURL': "https://fir-crud-5b277-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "fir-crud-5b277",
  'storageBucket': "fir-crud-5b277.appspot.com",
  'messagingSenderId': "1064906260461",
  'appId': "1:1064906260461:web:28b16483fe17252476f1e4",
  'measurementId': "G-LE7ZJDG8FE"}
firebase = pyrebase.initialize_app(firebaseConfig)                                                  # Объявляем подключение к Firebase
db=firebase.database()                                                                              #Подключаем Firebase Database
auth=firebase.auth()                                                                                #Подключаем систему аутентификаций Firebase
storage=firebase.storage()                                                                          #Подключаем Firebase Storage

ui.exitbtn.hide()                                                                                   # Для начала прячем ненужные элементы
ui.label.hide()
ui.label_2.hide()
ui.label_3.hide()
ui.label_4.hide()
ui.label_6.hide()
ui.totallabel.hide()
ui.datalabel.hide()
ui.datalabel_2.hide()
ui.datalabel_3.hide()
ui.nameinfolabel.hide()
ui.typelabel.hide()
ui.pnamelabel.hide()
ui.priceinfolabel.hide()
ui.pricelabel.hide()
ui.amountinfolabel.hide()
ui.overallpricelabel.hide()
ui.overallpriceinfolabel.hide()
ui.lcdN.hide()
ui.nextbtn.hide()
ui.controlbtn_3.hide()
ui.endbtn.hide()
ui.controlbtn_2.hide()
ui.label_8.hide()
ui.balancelbl.hide()




def readQR(itemid):                                                                                 # Функция считывания данных полученного с потока камеры сверху(53 - строка)
    imageidstr = str(itemid) + ".jpg"                                                               # Получаем строку формата .jpg для дальнешего использования

    storage.child("product_images/" + imageidstr).download("", imageidstr)                          # Ведем пойск фото нужного нам продукта в Firebase Storage по полученному сверху строке и скачиваем ее
    imageid = QImage(imageidstr)                                                                    # Выводим скачанное фото продукта на экран
    ui.imglabel.setPixmap(QPixmap.fromImage(imageid))
    ui.imglabel.setMinimumSize(1, 1)
    ui.imglabel.setScaledContents(True)
    ui.nameinfolabel.show()                                                                         # Показываем нужные нам элементы интерфейса
    ui.infolabel.show()
    ui.pnamelabel.show()
    ui.priceinfolabel.show()
    ui.pricelabel.show()
    ui.amountinfolabel.show()
    ui.overallpricelabel.show()
    ui.overallpriceinfolabel.show()
    ui.typelabel.show()
    ui.lcdN.show()
    ui.nextbtn.show()

    ui.endbtn.show()


    ui.infolabel_2.setText("Өнімді таразыға салыңыз")                                               #Меняем главный текст интерфейса

    productinfo = db.child("products").order_by_child("id").equal_to(int(itemid)).get()             #Получаем данные продукта(Цена, Имя, Цену за вес,Тип) c БД Firebase
    for product in productinfo.each():
        productname = product.val()['name']
        producttype = product.val()['type']
        productprice = product.val()['price']
        productweight = product.val()['weightperproduct']

    ui.pnamelabel.setText(productname)

    if (producttype == "countable"):                                                                # Присваеваем полученные данные
        ui.priceinfolabel.setText("Баға 1 дн.:")
        ui.pricelabel.setText(str(productprice) + " тг")
        ui.typelabel.setText("ШТ")
        ui.controlbtn_2.clicked.connect(lambda :onUpdate(productweight,productprice,producttype))
        ui.controlbtn_2.click()
    if(producttype == "uncountable"):
        ui.priceinfolabel.setText("Баға/кг:")
        ui.pricelabel.setText(str(productprice)+" тг")
        ui.typelabel.setText("гр.")
        ui.controlbtn_2.clicked.connect(lambda :onUpdate(productweight,productprice,producttype))
        ui.controlbtn_2.click()






def authQR(userid):                                                                                 # Функция авторизация клиента по QR
    global interation
    global userId
    userId=userid
    userinfo = db.child("Users").order_by_child("id").equal_to(str(userid)).get()                   # Считывание QR покупателя
    for user in userinfo.each():
        username = user.val()['name']                                                               # Получение данных клиента
        userbalance = user.val()['balance']
    ui.infolabel.setText("Қош келдіңіз "+username)                                                  # Вывод данных клиента
    ui.infolabel_2.setText("Өтініш,өнімді сканерден өткізіңіз")
    ui.balancelbl.setText(str(userbalance))
    ui.label_8.show()
    ui.balancelbl.show()
    ui.label.show()
    ui.label_2.show()
    ui.label_3.show()
    ui.label_4.show()
    ui.label_6.show()
    ui.exitbtn.show()
    ui.totallabel.show()
    interation+=1
    ui.controlbtn_3.click()                                                                         # Активируем слот кнопки controlbtn_3

def onStop():                                                                                       # Функиця остоновки потока
    global interation
    camThreadinstance.stop()                                                                        # Остановка потока захвата камеры
    camThreadinstance.start()                                                                       # Запуск потока захвата камеры
    interation+=1                                                                                   # Прибавляем +1 к лог.счетчику





def onUpdate(productweight,productprice,producttype):                                               # Функция переписывания значений строк интерфейса
    ui.datalabel.setText(str(productprice))
    ui.datalabel_2.setText(str(productweight))
    ui.datalabel_3.setText(str(producttype))



def onRead():                                                                                       # Функция считывания входящего потока данных с Arduinp
    if not serial.canReadLine(): return
    rx = serial.readLine()
    rxs = str(rx,'utf-8')
    if(ui.datalabel_3.text()=="countable"):
        if( isfloat(rxs)):
            if (float(rxs) > 0.005):
                count=round(float(rxs)*3571.42/float(ui.datalabel_2.text()))
                ui.lcdN.display(count)
                ui.overallpricelabel.setText(str(round((count*float(ui.datalabel.text())),3)))
            else:
                ui.lcdN.display("0.000")
                ui.overallpricelabel.setText(str("0.000"))
    elif(ui.datalabel_3.text()=="uncountable"):
        if (isfloat(rxs)):
            if (float(rxs) > 0.005):
                count = float(rxs) * 3571.42 / float(ui.datalabel_2.text())
                ui.lcdN.display(float(rxs)*3571.42)
                ui.overallpricelabel.setText(str(round((count * float(ui.datalabel.text()))))+" тг")
            else:
                ui.lcdN.display("0.000")
                ui.overallpricelabel.setText(str("0. тг"))





list=[]

class items:                                                                                        # создаем класс items
    def __init__(self,name,weight,price):
        self.name = name
        self.weight = weight
        self.price = price



def isfloat(num):                                                                                   # Функция проверки на float. Нужно для считывания данных с Arduino
    try:
        float(num)
        return True
    except ValueError:
        return False


def onOpen():                                                                                       # Открытие порта для Arduino, Тригеррится слотом ниже
    serial.setPortName("COM3")
    serial.open(QIODevice.ReadWrite)

def sendcheck():                                                                                    # Запись и отправка чека ( список полученных продуктов) в БД и storage
    global recipe
    if (int(ui.totallabel.text()) > int(ui.balancelbl.text())):
        ui.infolabel_2.setText("Теңгеріміңіз жеткіліксіз!")
    else:
        ui.balancelbl.setText(str(int(int(ui.balancelbl.text()) - int(ui.totallabel.text()))))
        ui.infolabel_2.setText("Саудаңыз үшін Рахмет!")
        now = QDateTime.currentDateTime()
        filename=now.toString("dd.MM.yyyy hh-mm-ss")+".txt"
        recipe=filename
        with open(filename, 'w') as f:
            f.write("Имя             Кол-во          Цена\n")
            for obj in list:
                row_item = [str(obj.name), str(obj.weight),str(obj.price)]
                output = '{: <15} {: <15} {: <15}'.format(row_item[0], row_item[1],row_item[2])
                f.write(output+"\n")
        storage.child("recipes").child(userId).child(recipe).put(recipe)
        db.child("Users").child(userId).update({"balance":ui.balancelbl.text()})

def exit():                                                                                         # Выход и сбрасывание лог. счетчика до нуля
    ui.label_8.hide()
    ui.balancelbl.hide()
    ui.label.hide()
    ui.label_2.hide()
    ui.label_3.hide()
    ui.label_4.hide()
    ui.label_6.hide()
    ui.exitbtn.hide()
    ui.totallabel.hide()
    ui.infolabel.setText("Қош келдіңіз,өтініш,жүйеге тіркеліңіз")
    ui.infolabel_2.setText("")
    global interation
    interation = 0
    camThreadinstance.stop()
    camThreadinstance.start()

def onClose():                                                                                      # Функция закрытия порта
    serial.close()

def onAdd():                                                                                        # Добавляем продукт в корзину интерфейса и записываем в чек
    print('Clicked')
    ui.nextbtn.hide()
    ui.nameinfolabel.hide()
    ui.pnamelabel.hide()
    ui.priceinfolabel.hide()
    ui.pricelabel.hide()
    ui.amountinfolabel.hide()
    ui.lcdN.hide()
    ui.typelabel.hide()
    ui.overallpriceinfolabel.hide()
    ui.overallpricelabel.hide()
    horizontalLayout=QHBoxLayout()
    buttonText=("Жою")
    buttonS=QPushButton(buttonText,ui)
    label_pname = QLabel(ui.pnamelabel.text())
    label_count=QLabel(str(round(ui.lcdN.value(),3)))
    label_overall=QLabel(str(int(re.search(r'\d+',ui.overallpricelabel.text()).group())))
    horizontalLayout.addWidget(label_pname)
    horizontalLayout.addWidget(label_count)
    horizontalLayout.addWidget(label_overall)
    horizontalLayout.addWidget(buttonS)
    ui.verticalLayout.insertLayout(0,horizontalLayout)
    buttontoLayout[buttonS]=horizontalLayout
    print(ui.totallabel.text())
    print(label_overall.text())
    ui.totallabel.setText(str(int(int(ui.totallabel.text())+int(label_overall.text()))))
    list.append(items(label_pname.text(),label_count.text(),label_overall.text()))
    buttonS.clicked.connect(onDelete)
    camThreadinstance.stop()
    camThreadinstance.start()

def onDelete():                                                                                     # Удаляем выбранные продукт с корзины интерфейса и удаляем с чека
    rbt=ui.sender()
    hlt=buttontoLayout.get(rbt)
    widget = hlt.itemAt(2).widget()
    ui.totallabel.setText(str(int(int(ui.totallabel.text()) - int(widget.text()))))
    while(hlt.count()!= 0):
         item=hlt.takeAt(0)
         widget=item.widget()
         widget.deleteLater()

    hlt.deleteLater()





camThreadinstance = camThread(mainwindow=ui)                                                        # Задаем интерфейс для потока камеры
camThreadinstance.setTerminationEnabled(True)                                                       # Делаем поток ликвидруемой
camThreadinstance.start()                                                                           # Запускаем поток при запуске приложения

ui.controlbtn_3.clicked.connect(onStop)                                                             # Запуск функций onStop

ui.exitbtn.clicked.connect(exit)                                                                    # Запуск функций exit при нажатий на соответствующую кнопку exitbtn
ui.endbtn.clicked.connect(sendcheck)                                                                # Запуск функций sendcheck при нажатий на соответствующую кнопку endbtn
ui.nextbtn.clicked.connect(onAdd)                                                                   # Запуск функций onAdd при нажатий на соответствующую кнопку nextbtn
ui.controlbtn.clicked.connect(onOpen)                                                               # Запуск функций onOpen при нажатий на соответствующую кнопку controlbtn
serial.readyRead.connect(onRead)                                                                    # Запуск функций onRead при поступлений данных на сериний порт от Arduino
ui.controlbtn.click()                                                                               # Запусаем функцию onOpen
ui.controlbtn.hide()
ui.show()                                                                                           # Показываем ui
app.exec()                                                                                          # останавливаем приложение


##
#* *#