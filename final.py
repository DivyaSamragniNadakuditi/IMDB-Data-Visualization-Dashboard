import sys
import pandas as pd

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGroupBox, QLineEdit, QComboBox, QFrame, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QPixmap

import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None

__window_gui__ = "gui.ui"
__movie_data__ = "moviedata.csv"
__window_icon__ = "icon.png"

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi(__window_gui__, self)
        self.setWindowTitle("Movie Data Explorer")
        self.setWindowIcon(QIcon(__window_icon__))
        self.setStyleSheet("QMainWindow {background: 'white';}")
        self.cbox_items = ['Rank','Year','Runtime','Rating','Votes','Revenue','Metascore']
        graphicsView = QGraphicsView(self)
        scene = QGraphicsScene()
        self.pixmap = QGraphicsPixmapItem()
        scene.addItem(self.pixmap)
        graphicsView.setScene(scene)
        graphicsView.resize(700,700)
        self.movie_data = import_data(__movie_data__)
        self.init_cboxes()
        self.init_gboxes()
        self.filter_plot()
        self.show()

    def init_gboxes(self):
        self.groupBox.clicked.connect(self.filter_plot)
        self.groupBox_6.clicked.connect(self.filter_plot)
        self.groupBox_8.clicked.connect(self.filter_plot)
        self.groupBox_12.clicked.connect(self.filter_plot)
        self.groupBox_14.clicked.connect(self.filter_plot)
        self.groupBox_16.clicked.connect(self.filter_plot)
        self.groupBox_21.clicked.connect(self.filter_plot)
        self.groupBox_22.clicked.connect(self.filter_plot)
        self.groupBox_23.clicked.connect(self.filter_plot)
        self.groupBox_18.clicked.connect(self.filter_plot)
        self.groupBox_24.clicked.connect(self.preset_plot)
        
        self.lineEdit.editingFinished.connect(self.filter_plot)
        self.lineEdit_2.editingFinished.connect(self.filter_plot)
        self.lineEdit_7.editingFinished.connect(self.filter_plot)
        self.lineEdit_8.editingFinished.connect(self.filter_plot)

        self.lineEdit_13.editingFinished.connect(self.filter_plot)
        self.lineEdit_14.editingFinished.connect(self.filter_plot)
        self.lineEdit_21.editingFinished.connect(self.filter_plot)
        self.lineEdit_22.editingFinished.connect(self.filter_plot)

        self.lineEdit_15.editingFinished.connect(self.filter_plot)
        self.lineEdit_16.editingFinished.connect(self.filter_plot)
        self.lineEdit_17.editingFinished.connect(self.filter_plot)
        self.lineEdit_18.editingFinished.connect(self.filter_plot)

        self.lineEdit_19.editingFinished.connect(self.filter_plot)
        self.lineEdit_20.editingFinished.connect(self.filter_plot)
        self.lineEdit_23.editingFinished.connect(self.filter_plot)
        self.lineEdit_24.editingFinished.connect(self.filter_plot)
        self.lineEdit_25.editingFinished.connect(self.filter_plot)


    def init_cboxes(self):
        self.comboBox.addItems(self.cbox_items)
        self.comboBox_2.addItems(self.cbox_items)
        self.comboBox.removeItem(1)
        self.comboBox.currentIndexChanged.connect(self.xlist_changed)
        self.comboBox_2.removeItem(0)
        self.comboBox_2.currentIndexChanged.connect(self.ylist_changed)
        self.comboBox_3.currentIndexChanged.connect(self.preset_plot)
        preset_list = ['Votes vs Rating of Action Movies','Rank vs Votes of Comedy Movies','Revenue of Movies 2012 to 2016',
                       'Rank and Revenue of Vin Diesel Movies','Runtime vs Revenue of Movies', 'Rating vs Metascore of Movies',
                       'Revenue vs Metascore of Horror Movies','Rank vs Metacore of Movies of rating 5 - 10','Runtime vs Votes of Sci-Fi Movies',
                       'Rank and Ratings of James Movies']
        self.comboBox_3.addItems(preset_list)

    def xlist_changed(self):
        self.comboBox_2.currentIndexChanged.disconnect()
        temp = self.cbox_items[:]
        xs = self.comboBox.currentText()
        ys = self.comboBox_2.currentText()
        temp.remove(xs)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(temp)
        self.comboBox_2.setCurrentIndex(temp.index(ys))
        self.comboBox_2.currentIndexChanged.connect(self.ylist_changed)
        self.filter_plot()
        
    def ylist_changed(self):
        self.comboBox.currentIndexChanged.disconnect()
        temp = self.cbox_items[:]
        xs = self.comboBox.currentText()
        ys = self.comboBox_2.currentText()
        temp.remove(ys)
        self.comboBox.clear()
        self.comboBox.addItems(temp)
        self.comboBox.setCurrentIndex(temp.index(xs))
        self.comboBox.currentIndexChanged.connect(self.xlist_changed)
        self.filter_plot()

    def filter(self,mini,maxi,ind):
        if mini != "":
            try:
                mini = float(mini)
                self.temp_data = self.temp_data[self.temp_data[ind] >= mini]
            except:
                pass
        if maxi != "":
            try:
                maxi = float(maxi)
                self.temp_data = self.temp_data[(self.temp_data[ind] <= maxi)]
            except:
                pass

            
    def set_combo(self,x,y):
        xs = self.cbox_items[x]
        ys = self.cbox_items[y]
        self.comboBox.currentIndexChanged.disconnect()
        self.comboBox_2.currentIndexChanged.disconnect()
        self.comboBox.clear()
        self.comboBox_2.clear()
        temp = self.cbox_items[:]
        temp.remove(ys)
        self.comboBox.clear()
        self.comboBox.addItems(temp)
        self.comboBox.setCurrentIndex(temp.index(xs))
        temp = self.cbox_items[:]
        temp.remove(xs)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(temp)
        self.comboBox_2.setCurrentIndex(temp.index(ys))
        self.comboBox.currentIndexChanged.connect(self.xlist_changed)
        self.comboBox_2.currentIndexChanged.connect(self.ylist_changed)

    def preset_plot(self):
        self.groupBox_21.setChecked(False)
        self.groupBox_22.setChecked(False)
        self.groupBox_23.setChecked(False)
        self.groupBox.setChecked(False)
        self.groupBox_8.setChecked(False)

        self.groupBox_14.setChecked(False)
        self.groupBox_6.setChecked(False)
        self.groupBox_12.setChecked(False)
        self.groupBox_16.setChecked(False)
        self.groupBox_18.setChecked(False)
        
        self.temp_data = self.movie_data
        self.temp_data['filter'] = [1]*1000
        if self.groupBox_24.isChecked() == True:
            sel = self.comboBox_3.currentIndex()
            if sel == 0:
                self.set_combo(4,3)
                self.groupBox_21.setChecked(True)
                self.lineEdit_23.setText('Action')
                self.finder('Action','Genre')
            elif sel == 1:
                self.set_combo(0,4)
                self.groupBox_21.setChecked(True)
                self.lineEdit_23.setText('Comedy')
                self.finder('Comedy','Genre')
            elif sel == 2:
                self.set_combo(5,1)
                self.groupBox_6.setChecked(True)
                self.lineEdit_8.setText('2012')
                self.lineEdit_7.setText('2016')
                self.filter('2012','2016','Year')
            elif sel == 3:
                self.set_combo(0,5)
                self.groupBox_23.setChecked(True)
                self.lineEdit_25.setText('Vin Diesel')
                self.finder('Vin Diesel','Actors')
            elif sel == 4:
                self.set_combo(2,5)
            elif sel == 5:
                self.set_combo(3,6)
            elif sel == 6:
                self.set_combo(5,6)
                self.groupBox_21.setChecked(True)
                self.lineEdit_23.setText('Horror')
                self.finder('Horror','Genre')
            elif sel == 7:
                self.set_combo(0,6)
                self.groupBox_12.setChecked(True)
                self.lineEdit_14.setText('5')
                self.lineEdit_13.setText('10')
                self.filter('5','10','Rating')
            elif sel == 8:
                self.set_combo(2,4)
                self.groupBox_21.setChecked(True)
                self.lineEdit_23.setText('Sci-Fi')
                self.finder('Sci-Fi','Genre')
            elif sel == 9:
                self.set_combo(0,3)
                self.groupBox_22.setChecked(True)
                self.lineEdit_24.setText('James')
                self.finder('James','Director')

        self.temp_data = self.temp_data[self.temp_data['filter'] > 0]
        xs = self.comboBox.currentText()
        ys = self.comboBox_2.currentText()
        xlist = list(self.temp_data[xs])
        ylist = list(self.temp_data[ys])
        self.plot(xlist,ylist,str(xs + " vs " + ys + " Movie Data (" + str(len(xlist)) + " Results)" ))

    def filter_plot(self):
        self.groupBox_24.setChecked(False)
        self.temp_data = self.movie_data
        self.temp_data['filter'] = [1]*1000
        if self.groupBox_21.isChecked() == True:
            self.finder(self.lineEdit_23.text(),'Genre')
        if self.groupBox_22.isChecked() == True:
            self.finder(self.lineEdit_24.text(),'Director')
        if self.groupBox_23.isChecked() == True:
            self.finder(self.lineEdit_25.text(),'Actors')
        if self.groupBox.isChecked() == True:
            self.filter(self.lineEdit_2.text(),self.lineEdit.text(),'Rank')
        if self.groupBox_8.isChecked() == True:
            self.filter(self.lineEdit_22.text(),self.lineEdit_21.text(),'Runtime')
        if self.groupBox_14.isChecked() == True:
            self.filter(self.lineEdit_16.text(),self.lineEdit_15.text(),'Votes')
        if self.groupBox_6.isChecked() == True:
            self.filter(self.lineEdit_8.text(),self.lineEdit_7.text(),'Year')
        if self.groupBox_12.isChecked() == True:
            self.filter(self.lineEdit_14.text(),self.lineEdit_13.text(),'Rating')
        if self.groupBox_16.isChecked() == True:
            self.filter(self.lineEdit_18.text(),self.lineEdit_17.text(),'Revenue')
        if self.groupBox_18.isChecked() == True:
            self.filter(self.lineEdit_20.text(),self.lineEdit_19.text(),'Metascore')
        self.temp_data = self.temp_data[self.temp_data['filter'] > 0]
        xs = self.comboBox.currentText()
        ys = self.comboBox_2.currentText()
        xlist = list(self.temp_data[xs])
        ylist = list(self.temp_data[ys])
        self.plot(xlist,ylist,str(xs + " vs " + ys + " Movie Data (" + str(len(xlist)) + " Results)" ))

    def finder(self,c_list,ind):
        if c_list != "":
            cls = split_line(c_list.lower())
            for i in range(len(self.temp_data[ind])):
                if self.temp_data['filter'][i] == 1:
                    p = 0
                    temp = self.temp_data[ind][i]
                    if len(temp[0]) > 1:
                        for x in temp:
                            for y in cls:
                                if y in x:
                                    p = 1
                                    break
                            if p == 1:
                                break
                    else:
                        for y in cls:
                            if y in temp:
                                p = 1
                                break
                    self.temp_data['filter'][i] = p
            

    def plot(self,xls,yls,title):
        fig, ax = plt.subplots( nrows=1, ncols=1 )
        ax.scatter(xls,yls)
        ax.set_title(title)
        fig.set_size_inches(7, 7, forward=True)
        fig.savefig('foo.png')
        plt.close(fig)
        img = QPixmap('foo.png')
        self.pixmap.setPixmap(img)


def split_line(line):
    splitline = []
    char_start = 0
    char = 0
    for char in range(len(line)):
        if line[char] == ",":
            if line[char_start] == "\"" and line[char-1] == "\"":
                splitline.append(split_line(line[char_start + 1:char]))
                char_start = char + 1
            elif line[char_start] == "\"":
                char = char + 1
            else:    
                splitline.append(line[char_start:char])
                char_start = char + 1
    splitline.append(line[char_start:char])
    return splitline

            
def import_data(file_name):
    columns_list = []
    data = []
    file = open(file_name,"r")
    columns_list = split_line(file.readline())
    for line in file:
        data.append(split_line(line.lower()))
    data = pd.DataFrame(data,columns = columns_list)
    num_items = ['Rank','Year','Runtime','Rating','Votes','Revenue','Metascore']
    for n in num_items:
        for i in range(len(data[n])):
            if data[n][i] == "":
                data[n][i] = 0.0
            else:
                data[n][i] = float(data[n][i])
    return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
