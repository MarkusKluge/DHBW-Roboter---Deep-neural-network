import threading, time

class WebServer:
    def __init__(self, diagnostics, liveview):
        from flask import Flask, render_template, request, send_file, Response, make_response
        # from static.response import distance
        self.app = Flask(__name__)
        self.diagnostics = diagnostics
        self.liveview = liveview
        
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
            return str(data)

        @self.app.route('/getImageRaw', methods=['GET'])
        def getImageRaw():
            image = self.liveview.getImageJpeg()
            if image is not None:
                response = make_response(image)
                response.headers['Content-Type'] = 'image/jpg'
                return response
            else:
                return "",404

        self.runWebserverThread()
        print("WebServer is running...")

    def runWebserverThread(self):
        x = threading.Thread(target=self.runWebserver)
        x.start()

    def runWebserver(self):
        self.app.run(host='0.0.0.0', port=8080, debug=False)