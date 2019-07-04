import threading, time

import numpy as np
# import time
import cv2,base64
# import os
import imutils

class WebServer:
    def __init__(self,diagnostics):
        from flask import Flask, render_template, request, send_file, Response, make_response
        # from static.response import distance
        self.app = Flask(__name__)
        self.diagnostics = diagnostics
        self.vs = cv2.VideoCapture(0)
        self.vs.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.vs.set(cv2.CAP_PROP_FPS, 30)

        @self.app.route("/")
        def main():
            return render_template("index.html")
            
        @self.app.route('/search_animal', methods=['POST'])
        def search_animal():
            print(request.form['animal'])
            return "", 204

        # @self.app.route('/testDistance', methods=['POST'])
        # def run():
        #     data = self.diagnostics.getData()
        #     # return str(data['cpu_temp'])
        #     return str(data)

        @self.app.route('/testDistance', methods=['GET'])
        def testCV2():
            for x in range(6):
                (grabbed, frame) = self.vs.read()

            if grabbed:
                # cv2.imwrite('lul.jpg',frame)
                # image = cv2.imdecode(np.fromstring(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
                ret, image = cv2.imencode('.jpg',frame)
                # return send_file( 'test.jpeg', mimetype="image/jpeg", attachment_filename="test.jpeg", as_attachment=True)
                jpg_as_text = base64.b64encode(image)
                # response = make_response(image.tobytes())
                response = make_response(jpg_as_text)
                response.headers['Content-Type'] = 'image/jpg'
                return response
            else:
                return "",404
        
        @self.app.route('/test', methods=['GET'])
        def run():
            vs = cv2.VideoCapture(0)
            while True:
                (grabbed, frame) = vs.read()
                if not grabbed:
                    break
                frame = imutils.resize(frame, height=600, width=400)
                print("showing image")
                print("showing image")
                print("showing image")
                cv2.imshow("test",frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            vs.release()
            cv2.destroyAllWindows()
            return render_template("index.html")


        self.runWebserverThread()
        print("WebServer is running...")

    def runWebserverThread(self):
        x = threading.Thread(target=self.runWebserver)
        x.start()

    def runWebserver(self):
        self.app.run(host='0.0.0.0', port=8080, debug=False)