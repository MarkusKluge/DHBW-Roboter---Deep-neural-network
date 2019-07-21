from gpiozero import CPUTemperature
import threading, time, psutil

class Diagnostics:
    def __init__(self):
        self.data = {
            'cpu_temp': 0,
            'cpu_usage': 0,
            'ram_usage': 0,
            'cpu_clock': '',
            'distance': 0,
            'animal_found': False,
            'finished': False,
            'status': '',
        }
        
        self.runDiagnosticThread()
        print("Diagnostics started.")

    def runDiagnosticThread(self):
        x = threading.Thread(target=self.runDiagnostic)
        x.start()
        
    def runDiagnostic(self):
        while True:
            self.data['cpu_temp'] = CPUTemperature().temperature
            self.data['cpu_usage'] = psutil.cpu_percent(interval=None) # non blocking
            self.data['ram_usage'] = psutil.virtual_memory()
            self.data['cpu_clock'] = psutil.cpu_freq()
            time.sleep(0.5)

    def getData(self):
        return self.data

    def setDistance(self, distance):
        self.data['distance'] = distance
    
    def finished(self, finished):
        self.data['finished'] = finished

    def animalFound(self, found):
        self.data['animal_found'] = found

    def setStatus(self, status):
        self.data['status'] = status