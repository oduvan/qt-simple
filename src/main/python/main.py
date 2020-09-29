from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtWidgets import QMainWindow, QLabel, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import  Qt

import aiohttp
from asyncqt import QEventLoop, asyncSlot, asyncClose
import asyncio
import aiohttp_cors
from aiohttp import web

import sys
import webbrowser

class AppContext(ApplicationContext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ii = 0
        self.opens = 0

    async def web_get_inc_link(self, request):
        self.opens += 1
        self.open_site_link.setText('Clicked {}'.format(self.opens))
        return web.Response(text='OK');

    async def web_get_root(self, request):
        self.ii += 1
        return web.Response(text='hi {}'.format(self.ii))

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
        self.open_site_link = open_site = QAction("Open")
        open_site.triggered.connect(self.open_site)

        menu.addAction(open_site)

        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(app.quit)
        menu.addAction(quit)

        # Add the menu to the tray
        tray.setContextMenu(menu)

        loop = QEventLoop(self.app)
        asyncio.set_event_loop(loop)

        web_app = web.Application()

        cors = aiohttp_cors.setup(web_app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_headers="*",
                )
        })
        cors.add(web_app.router.add_get('/', self.web_get_root))
        cors.add(web_app.router.add_get('/inc-link/', self.web_get_inc_link))

        return loop.run_until_complete(web._run_app(web_app, port=8766, host='127.0.0.1'))

    def open_site(self):
        webbrowser.open_new_tab('http://127.0.0.1:8766/')


    @cached_property
    def img_icon(self):
        return QIcon(self.get_resource('icon.png'))

if __name__ == '__main__':
    appctxt = AppContext()      # 2. Invoke appctxt.app.exec_()
    sys.exit(appctxt.run())