import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pyngrok import ngrok
import time
import traceback, sys
import allfunc
import webbrowser
import easygui
import qrcode

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



class Ui_MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 225)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 341, 16))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 110, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 80, 111, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(360, 10, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(360, 40, 75, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(10, 40, 321, 21))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 80, 121, 101))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../OneDrive/Desktop/ok-img.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 150, 111, 31))
        self.pushButton_6.setObjectName("pushButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 455, 21))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionEssential_Folder = QtWidgets.QAction(MainWindow)
        self.actionEssential_Folder.setObjectName("actionEssential_Folder")
        self.menuSettings.addAction(self.actionEssential_Folder)
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n""<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">C:/</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "START"))
        self.pushButton.clicked.connect(self.oh_no)
        self.pushButton.setEnabled(False)
        self.pushButton_2.setText(_translate("MainWindow", "STOP"))
        self.pushButton_2.clicked.connect(self.stop_main)
        self.pushButton_3.setText(_translate("MainWindow", "CONTROL PANEL"))
        self.pushButton_3.clicked.connect(self.Control_Panel_main)
        self.pushButton_4.setText(_translate("MainWindow", "BROWSE"))
        self.pushButton_4.clicked.connect(self.select_folder)
        self.pushButton_5.setText(_translate("MainWindow", "COPY LINK"))
        self.textBrowser_2.setHtml(_translate("MainWindow", f"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n""<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">{}</p></body></html>"))
        # self.label.setText(_translate("MainWindow", "                 QR"))
        self.pushButton_6.setText(_translate("MainWindow", "ENTER WEBSITE"))
        self.pushButton_6.clicked.connect(self.Get_link_main)
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionEssential_Folder.setText(_translate("MainWindow", "Essential Folder"))

    def select_folder(self):
        self.path = easygui.diropenbox()
        self.textBrowser.setHtml(QtCore.QCoreApplication.translate("MainWindow", f"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">{self.path}</span></p></body></html>"))
        self.pushButton.setEnabled(True)

    def Control_Panel_main(self):
        allfunc.Control_Panel()

    def stop_main(self):
        allfunc.stop()
        self.pushButton.setText(QtCore.QCoreApplication.translate("MainWindow", "START"))

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        ngrok_process = ngrok.get_ngrok_process()
        ngrok.connect(f"file:///{self.path}")
        try:
            # Block until CTRL-C or some other terminating event
            ngrok_process.proc.wait()
        except KeyboardInterrupt:
            print(" Shutting down server.")

            ngrok.kill()


    def execute_this_fn_2(self, progress_callback):
        # generating a QR code using the make() function
        print(self.y)
        qr_img = qrcode.make(f"{allfunc.Get_link()}")
        # saving the image file
        qr_img.save(r"C:\Users\verma\OneDrive\Desktop\ok-img.jpg")

        print("hohohoho")

    def execute_this_fn_3(self, progress_callback):
        self.label.setPixmap(QtGui.QPixmap("../../OneDrive/Desktop/ok-img.jpg"))
        print("hohohoho")



    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        worker_2 = Worker(self.execute_this_fn_2) # Any other args, kwargs are passed to the run function
        worker_2.signals.result.connect(self.print_output)
        worker_2.signals.finished.connect(self.thread_complete)
        worker_2.signals.progress.connect(self.progress_fn)

        worker_3 = Worker(self.execute_this_fn_3) # Any other args, kwargs are passed to the run function
        worker_3.signals.result.connect(self.print_output)
        worker_3.signals.finished.connect(self.thread_complete)
        worker_3.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)
        self.threadpool.start(worker_2)
        self.threadpool.start(worker_3)

        self.y = allfunc.Get_link()
        print(self.y)
        _translate = QtCore.QCoreApplication.translate
        self.textBrowser_2.setHtml(_translate("MainWindow",f"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n""p, li { white-space: pre-wrap; }\n""</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"f"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">{self.y}</p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "RUNNING"))




    def Get_link_main(self):
        webbrowser.open(self.y)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())