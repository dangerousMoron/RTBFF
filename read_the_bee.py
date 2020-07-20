#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 14:06:36 2020

@author: tfinney
"""

import sys


from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSlot
from PyQt5 import QtGui
import os
import string
import random
import urllib.request
import webbrowser
import glob
import platform
import subprocess

import fetch_news as fn

class mainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(mainWindow, self).__init__(*args, **kwargs)
        
        """
        some dir stuff
        """
        
        current_working_dir = os.getcwd()
        self.data_dir = current_working_dir + '/rtbff_data/'
        self.setup_directories()
        
        """
        boilerplate things.
        """
        
        self.setWindowTitle('Read the Bee for Free!')
        self.center()
        self.setMinimumSize(500,100)
        
        testLabel = QLabel('Read The Bee For Free!')     
        
        self.urlLine = QLineEdit('')
        self.urlLine.setPlaceholderText('enter a url...')
        self.urlLine.setDragEnabled(True)
        self.urlLine.setToolTip('Enter the url of the news article you want to read.')
        
        urlButton = QPushButton('Download')
        urlButton.setToolTip('Download the article to the data directory.')
        
        viewButton = QPushButton('Download and Read')      
        viewButton.setToolTip('Download the article and open it in the default web browser.')

        deleteButton = QPushButton('Delete Local Data')
        deleteButton.setToolTip('Delete the local html files created by the program.')
        
        openFolderButton = QPushButton('Open Data Directory')
        openFolderButton.setToolTip('Opens the folder on your machine where we are downloading things!')
        
        # curDirLabel = QLabel('Data Directory:')
        
        # urlLabel = QLabel('')
        
        mainLayout = QVBoxLayout()      
        
        urlLayout = QHBoxLayout()
        # urlLayout.addWidget(urlLabel)
        urlLayout.addWidget(self.urlLine)
        # urlLayout.addWidget(urlButton)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(urlButton)
        buttonLayout.addWidget(viewButton)
        buttonLayout.addWidget(deleteButton)
        
        bottomButtonLayout = QHBoxLayout()
        bottomButtonLayout.addWidget(openFolderButton)
        bottomButtonLayout.addStretch()
        
        labelLayout = QHBoxLayout()
        labelLayout.addStretch()
        labelLayout.addWidget(testLabel)
        labelLayout.addStretch()
        
        mainLayout.addLayout(labelLayout)
        mainLayout.addLayout(urlLayout)
        mainLayout.addLayout(buttonLayout)
# 

        # self.output_box = QTextBrowser()
        self.output_box = QTextEdit()
        self.output_box.resize(1,1)
        # self.output_box.text('test')
        self.output_box.setReadOnly(True)
        self.output_box.append('Ready!')
        mainLayout.addWidget(self.output_box)
        mainLayout.addLayout(bottomButtonLayout)
    

        widget = QWidget()
        widget.setLayout(mainLayout)
        
        # self.statusBar = QStatusBar()
        # self.setStatusBar(self.statusBar)
        # self.statusBar.showMessage('ready')
        
        
        
        
        self.setCentralWidget(widget)
        # testButton.clicked.connect(self.test_slot_n_signal)
        
        
        #connections
        urlButton.clicked.connect(self.gen_and_fetch)
        viewButton.clicked.connect(self.fetch_and_open_in_browsah)
        deleteButton.clicked.connect(self.delete_local_data)
        openFolderButton.clicked.connect(self.open_folder)
        
    def setup_directories(self):
        data_dir = self.data_dir
        
        if( os.path.exists(data_dir) == False):
            os.mkdir(data_dir)    
            
            
    def center(self):
        """
        center the main window
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)        
        self.move(qr.topLeft())
    
    
    def delete_local_data(self):
        """
        clean up our data file if we want
        """
        
        choice = QMessageBox.question(self,'delete?','Delete Local Data?', QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            self.output_box.append('Deleting Local files.')
            local_z = glob.glob(self.data_dir+'*.html')
            for i in range(len(local_z)):
                os.remove(local_z[i])
            else:
                pass

    
    def open_folder(self):
        path = self.data_dir
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def test_slot_n_signal(self):
        print('you clicked the piss button')
     
    def generate_out_file(self):
        base_name = ''.join(random.choices(string.hexdigits,k=10))
        full_name = self.data_dir + base_name + '.html'
        return full_name
        # print(full_name)
    
    

    
    def fetch_a_url(self,url,out_file):
        if url.find('www.sacbee.com') !=-1:
            self.output_box.append('Fetching directly with urllib lib (sacbee)')
            real_url = fn.decompose_sacbee(url)
            self.output_box.append(('True sacbee url is: {}'.format(real_url)))
            try:
                fn.fetch_url_liar(real_url, out_file)
            except:
                self.output_box.append('error fetching file...')
                pass
        
        else:
            try:
                fn.fetch_wget(url,out_file)
            except:
                try:
                    self.output_box.append('Error with wget, trying with urllib...')
                    # print('error with wget, trying with urllib...')
                    fn.fetch_url_liar(url,out_file)
                except:
                    self.output_box.append('error fetching file...')
                    pass        
                    
    
    def gen_and_fetch(self):
        # print(self.urlLine.text())
        if(self.urlLine.text()==''):
            # self.statusBar.showMessage('url cannot be blank!')
            self.output_box.append('url cannot be blank!')
        else:
            to_fetch_url = self.urlLine.text()
            local_name = self.generate_out_file()
            self.output_box.append('Downloading: {}\nTo: {}'.format(to_fetch_url,local_name))
            # print(to_fetch_url)
            # print(type(to_fetch_url))
            # self.fetchURL(str(to_fetch_url),local_name)
            self.fetch_a_url(str(to_fetch_url),local_name)
            self.output_box.append('Done!')
        
            return local_name

    def fetch_and_open_in_browsah(self):
        file_name = self.gen_and_fetch()
        webbrowser.open(file_name)
        


if __name__ == '__main__':
    app = QApplication([])
    rtb = mainWindow()
    rtb.show()
    sys.exit(app.exec())