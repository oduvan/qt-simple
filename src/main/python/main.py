from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QMainWindow, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import  Qt

import sys
import webbrowser

class AppContext(ApplicationContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.window = MainWindow(self)
        #self.stray = SystemTray(self)

    def run(self):
        app = self.app

        app.setQuitOnLastWindowClosed(False)

        # Create the icon
        icon = QIcon(self.img_icon)

        # Create the tray
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        # Create the menu
        menu = QMenu()
        open_site = QAction("Open")
        open_site.triggered.connect(self.open_site)

        menu.addAction(open_site)

        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(app.quit)
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)

        return self.app.exec_()

    def open_site(self):
        webbrowser.open_new_tab('https://checkio.org/')


    @cached_property
    def img_icon(self):
        return QIcon(self.get_resource('icon.png'))

if __name__ == '__main__':
    appctxt = AppContext()      # 2. Invoke appctxt.app.exec_()
    sys.exit(appctxt.run())