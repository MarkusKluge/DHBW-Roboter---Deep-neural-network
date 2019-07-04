from classes.diagnostics import Diagnostics
from classes.webserver import WebServer
import time

diagnostics = Diagnostics()
webserver = WebServer(diagnostics)

print( diagnostics.getData() )
time.sleep(1)
print( diagnostics.getData() )
time.sleep(1)
print( diagnostics.getData() )
