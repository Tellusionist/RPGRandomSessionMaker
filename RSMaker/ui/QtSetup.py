import  sqlite3
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow


def get_table_metadata():
    sql = 'Select tbl_name from sqlite_master;'
    conn = sqlite3.connect('rolltables.db')
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    rtable_rows={}
    for table in results:
        tbl_name = table[0]
        sql = f"Select sum(weight) from {tbl_name};"
        c.execute(sql)
        cnt = c.fetchone()
        rtable_rows[tbl_name] = cnt[0]
    conn.close()
    return rtable_rows

rtable_rows = get_table_metadata()

def generic_setup(self):
    _translate = QtCore.QCoreApplication.translate
    
    # load generic dropdown default values 
    rx = QtCore.QRegExp("cb_.*")
    dropdowns = self.findChildren(QtWidgets.QComboBox, rx)
    for dropdown in dropdowns:
        table = dropdown.objectName()[3:]
        sql = f"Select value from {table};"
        for item in enumerate(sql_query(sql)): # enumerating to get incremental id
            dropdown.addItem("")
            dropdown.setItemText(item[0], _translate("MainWindow", item[1][0]))  

    # connect generic dropdown and text buttons
    rx = QtCore.QRegExp("btn_rr[dt]_.*")
    btns = self.findChildren(QtWidgets.QPushButton, rx)
    for btn in btns:
        btn.clicked.connect(lambda: reroll(self))

    # connect roll all button
    self.btn_all_rr.clicked.connect(lambda: reroll_all(self))

def sql_query(sql):
        conn = sqlite3.connect('rolltables.db')
        c = conn.cursor()
        c.execute(sql)
        results = c.fetchall()
        conn.close()
        return results
    
def roll_query(table, columns='value'):

    roll = randint(1,rtable_rows[table])
    
    if isinstance(columns, str) or columns == '*':
        select_cols = columns
    else:   
        select_cols = ''
        for col in columns:
            select_cols += col + ','
        select_cols = select_cols[:-1]
    
    sql = f"Select {select_cols} from (Select rowid, *, sum(weight) over(Order by rowid) rt from {table}) where rt >= {roll} order by rt asc limit 1;"
    conn = sqlite3.connect('rolltables.db')
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchone()
    conn.close()
    return results

def reroll(self):
    try:
        # Use the name of the sender to check locks and set table
        table = self.sender().objectName()[8:]
        target_type = self.sender().objectName()[6]
        rx = QtCore.QRegExp("lck_"+table+".[0-9]|lck_"+table+"\\b")
        lcks = self.findChildren(QtWidgets.QCheckBox, rx) # in case there are more than 1 features
        for lck in lcks:
            if not lck.isChecked():
                if target_type == 't':
                    target = self.findChild(QtWidgets.QPlainTextEdit, lck.objectName().replace('lck','tx'))
                    results = roll_query(table, 'value')
                    txt = results[0]
                    target.clear()
                    target.appendPlainText(txt)
                elif target_type == 'd':
                    target = self.findChild(QtWidgets.QComboBox, lck.objectName().replace('lck','cb'))
                    results = roll_query(table, 'rowid')
                    rowid = results[0]-1 #sqlite is 1 based, Qt5 is 0 based
                    target.setCurrentIndex(rowid)
            #else:
            #    print(lck.objectName(), "is locked, not updating")
    except Exception as e:
        warning_popup("Error received:", e)

def reroll_all(self):
    rx = QtCore.QRegExp("btn_rr[a-z]_.*")
    btns = self.findChildren(QtWidgets.QPushButton, rx)
    for btn in btns:
        btn.click()


def warning_popup(message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(str(message))
    msgBox.setWindowTitle("Error!")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()