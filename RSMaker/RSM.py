import sys, json, sqlite3
from random import randint

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./QTemplates/RSM_Main.ui', self)
        self.initial_setup()


    def initial_setup(self):
        _translate = QtCore.QCoreApplication.translate
        
        # load dropdown default values and connect buttons
        dropdowns = [self.cb_DungeonType, self.cb_Environment]
        for dropdown in dropdowns:
            table = dropdown.objectName()[3:]
            # Connect re-roll buttons
            btn = self.findChild(QtWidgets.QPushButton, "btn_rr_"+table)
            btn.clicked.connect(lambda: self.reroll('ComboBox'))
            
            # load default values
            sql = f"Select value from {table};"
            for item in enumerate(self.sql_query(sql)): # enumerating to get incremental id
                dropdown.addItem("")
                dropdown.setItemText(item[0], _translate("MainWindow", item[1][0]))  



        # load plaintext default values and connect buttons
        plaintexts = [self.txt_StartArea, self.txt_Noise, self.txt_Odor, self.txt_Air]
        for pt in plaintexts:
            table = pt.objectName()[4:]
            results = self.roll_query(table)
            pt.appendPlainText(results[0])

            # Connect re-roll buttons
            btn = self.findChild(QtWidgets.QPushButton, "btn_rr_"+table)
            btn.clicked.connect(lambda: self.reroll('PlainText'))

    def sql_query(self, sql):
            conn = sqlite3.connect('rolltables.db')
            c = conn.cursor()
            c.execute(sql)
            results = c.fetchall()
            conn.close()
            return results
        
    def roll_query(self, table, columns='value'):
    
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
    
    def reroll(self, target_type='PlainText'):
        # Use the name of the sender to check locks and set table
        # this may be a problem for multiple buttons that query the same table
        table = self.sender().objectName()[7:]
        lck = self.findChild(QtWidgets.QCheckBox, "lck_"+table)
        try:
            if not lck.isChecked():
                if target_type == 'PlainText':
                    target = self.findChild(QtWidgets.QPlainTextEdit, 'txt_'+table)
                    results = self.roll_query(table, 'value')
                    txt = results[0]
                    target.clear()
                    target.appendPlainText(txt)
                elif target_type == 'ComboBox':
                    target = self.findChild(QtWidgets.QComboBox, 'cb_'+table)
                    results = self.roll_query(table, 'rowid')
                    rowid = results[0]-1 #sqlite is 1 based, Qt5 is 0 based
                    target.setCurrentIndex(rowid)
            else:
                print("Field is locked, not updating")
        except Exception as e:
            print("Error received:", e)
            self.warning_popup(e)
    
    def warning_popup(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(str(message))
        msgBox.setWindowTitle("Error!")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()


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

if __name__ == "__main__":  
    # import roll tables
    rtable_rows = get_table_metadata()

    # load Ui
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())