import threading, time

class WebServer:
    def __init__(self,diagnostics):
        print("Starting WebServer...")
        from flask import Flask, render_template, request
        # from static.response import distance
        self.app = Flask(__name__)
        self.diagnostics = diagnostics

        @self.app.route("/")
        def main():
            return render_template("index.html")
            
        @self.app.route('/search_animal', methods=['POST'])
        def search_animal():
            print(request.form['animal'])
            return "", 204

        @self.app.route('/testDistance', methods=['POST'])
        def run():
            data = self.diagnostics.getData()
            return str(data['cpu_temp'])

        self.runWebserverThread()
        print("WebServer is running...")

    def runWebserverThread(self):
        x = threading.Thread(target=self.runWebserver)
        x.start()

    def runWebserver(self):
        self.app.run(host='0.0.0.0', port=8080, debug=False)