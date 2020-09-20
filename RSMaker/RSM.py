import sys, json, sqlite3
from random import randint

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./QTemplates/RSM_Main.ui', self)
        self.initial_setup()

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
    
    def simple_reroll(self, pt_target, lck, table):
        try:
            if not self.lck_StartArea.isChecked():
                results = self.roll_query(table, 'value')
                txt = results[0]
                pt_target.clear()
                pt_target.appendPlainText(txt)
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


    def initial_setup(self):
        _translate = QtCore.QCoreApplication.translate
         # load dungeon type values, enumerating to get incremental id
        for item in enumerate(self.sql_query('Select value from DungeonType;')):
            self.cb_DungeonType.addItem("")
            self.cb_DungeonType.setItemText(item[0], _translate("MainWindow", item[1][0]))  

        self.lbl_Environment.setText(_translate("MainWindow", "Environment:"))
        # load environment values, enumerating to get incremental id
        for item in enumerate(self.sql_query('Select value from Environment;')):
            self.cb_Environment.addItem("")
            self.cb_Environment.setItemText(item[0], _translate("MainWindow", item[1][0]))

        self.lbl_StartArea.setText(_translate("MainWindow", "Starting Area:"))
        
        self.btn_rr_StartArea.clicked.connect(lambda: self.simple_reroll(self.txt_StartArea, self.lck_StartArea, 'StartArea'))
        
        # Set default starting area
        results = self.roll_query('StartArea')
        self.txt_StartArea.appendPlainText(results[0])

         


def get_table_metadata():
    sql = 'Select tbl_name from sqlite_master;'
    conn = sqlite3.connect('rolltables.db')
    c = conn.cursor()
    c.execute(sql)
    results = c.fetchall()
    rtable_rows={}
    for table in results:
        tbl_name = table[0]
        sql = f"Select count(1) from {tbl_name};"
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


