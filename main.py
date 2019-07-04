from classes.diagnostics import Diagnostics
from classes.webserver import WebServer
import time

print("Starting Diagnostics...")
diagnostics = Diagnostics()

print("Starting WebServer...")
webserver = WebServer(diagnostics)

print( diagnostics.getData() )
