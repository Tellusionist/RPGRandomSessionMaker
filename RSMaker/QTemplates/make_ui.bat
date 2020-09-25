call pyrcc5 -o ../QtResources_rc.py QtResources.qrc
call pyuic5 -x RSM_Main.ui -o RSM_Main.py
call pyuic5 -x Chamber.ui -o Chamber.py