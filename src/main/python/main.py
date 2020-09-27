from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import  Qt

import sys

class MainWindow(QMainWindow):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

        l = QLabel(self)
        l.setPixmap(QPixmap.fromImage(self.ctx.img_smile))
        l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # self.addWidget(l)

class AppContext(ApplicationContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = MainWindow(self)

    def run(self):
        self.window.show()
        return self.app.exec_()

    @cached_property
    def img_smile(self):
        return QImage(self.get_resource('smile.png'))

if __name__ == '__main__':
    appctxt = AppContext()      # 2. Invoke appctxt.app.exec_()
    sys.exit(appctxt.run())