from classes.diagnostics import Diagnostics
from classes.webserver import WebServer
from classes.liveview import LiveView
import time

print("Starting Diagnostics...")
diagnostics = Diagnostics()

print("Starting LiveView...")
liveview = LiveView(width=1280, height=720, fps=30)

print("Starting WebServer...")
webserver = WebServer(diagnostics, liveview)

