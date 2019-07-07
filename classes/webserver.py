from classes.diagnostics import Diagnostics
from classes.liveview import LiveView
from classes.dnn import Dnn
from classes.robotcontrol import RobotControl

import threading, time, json

class WebServer:
    def __init__(self):
        from flask import Flask, render_template, request, send_file, Response, make_response
        # from static.response import distance
        self.app = Flask(__name__)
        self.diagnostics = None
        self.liveview = None
        self.dnn = None
        self.imageDnn = None
        self.dnnResults = None
        
        @self.app.before_first_request
        def before_first_request():
            def run_jobs():
                print("Starting Diagnostics...")
                self.diagnostics = Diagnostics()
                print("Starting LiveView...")
                self.liveview = LiveView(width=1280, height=720, fps=30)
                print("Starting DNN Processing...")
                self.dnn = Dnn(self.liveview)
                print("Starting RobotControl...")
                self.robotcontrol = RobotControl(self.diagnostics, self.liveview, self.dnn)

            thread = threading.Thread(target=run_jobs)
            thread.start()

        @self.app.route("/")
        def main():
            return render_template("index.html")
            
        @self.app.route('/search_animal', methods=['POST'])
        def search_animal():
            print(request.form['animal'])
            return "", 204

        @self.app.route('/getDiagnostics', methods=['GET'])
        def getDiagnostics():
            data = self.diagnostics.getData()
            return json.dumps(data)

        @self.app.route('/getImageRaw', methods=['GET'])
        def getImageRaw():
            image = self.liveview.getImageJpeg()
            if image is not None:
                response = make_response(image)
                response.headers['Content-Type'] = 'image/jpg'
                return response
            else:
                return "",404

        @self.app.route('/getImageDnn', methods=['GET'])
        def getImageDnn():
            image, results = self.liveview.getDnn()
            self.dnnResults = results

            if image is not None:
                response = make_response(image)
                response.headers['Content-Type'] = 'image/jpg'
                return response
            else:
                return "",404

        @self.app.route('/getDnnResults', methods=['GET'])
        def getDnnResults():
            if self.dnnResults is not None:
                return json.dumps(self.dnnResults)
            else:
                return "",404

        self.runWebserver()

    def runWebserver(self):
        self.app.run(host='0.0.0.0', port=8080, debug=True)
