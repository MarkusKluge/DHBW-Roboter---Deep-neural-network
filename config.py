# RobotControl
animalFoundAccuracy = 0.45
# resetHeight = 81.5
resetHeight = 64
# resetHeight = 40.0
finishHeight = 11.5
sleepProcessDnn = 0.1

# heights = [
#     28.8,
#     13
# ]
heights = [
    # 81.0,
    56.9, 
    36.0, 
    13.0
    # 11.7
]

gpios = {
    'DISTANCE_TRIGGER': 22,
    'DISTANCE_ECHO': 27,
}

motors = [
    {"EN": 16, "IN_1": 20, "IN_2":21},
    {"EN": 6, "IN_1": 13, "IN_2":26},
    {"EN": 25, "IN_1": 23, "IN_2":24}
]

# LiveView / camera
liveviewSkips = 2 # number of frames to grab for each loop, higher = less input lag
width=1280
height=1024
fps=30

# DNN networks
networks = {}
networks["64_v6"] = {"folder": "64_v6", "resolution": 64, "weights": "team5_62100.weights"}
networks["64_v4"] = {"folder": "64_v4", "resolution": 64, "weights": "yolov3-tiny_last.weights"}
selectedNetwork = networks["64_v6"]

# Diagnostics
sleepDiagnostic = 0.5