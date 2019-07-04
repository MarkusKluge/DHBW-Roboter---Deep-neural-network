from gpiozero import CPUTemperature
import threading, time

class Diagnostics:
    def __init__(self):
        print("Starting Diagnostics...")
        self.data = {
            'cpu_temp': 0,
            'cpu_usage': 0,
            'ram_usage': 0,
            'cpu_clock': '',
            'status': None,
        }
        
        self.runDiagnosticThread()
        print("Diagnostics started.")

    def runDiagnosticThread(self):
        x = threading.Thread(target=self.runDiagnostic)
        x.start()
        
    def runDiagnostic(self):
        while True:
            self.data['cpu_temp'] = CPUTemperature().temperature
            time.sleep(1)

    def getData(self):
        return self.data