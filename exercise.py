import numpy as np

class Exercise:
    def __init__(self, name):
        self.name = name
        self.current_state = 'IDLE'
        self.rep_count = 0
        self.rep_quality = ""
        self.rep_history = []
        self.quality_history = []
    
    #calculates 2d angle between three points, b is vertex and tuple is returned
    @staticmethod
    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        #calculate radians using arctangent, further explained in the report
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        #convert to degrees
        angle = np.abs(radians * 180.0 / np.pi)
        
        #keeps angle interior to 180 degrees
        if angle > 180.0:
            angle = 360.0 - angle
            
        return angle

    #for getting MediaPipe landmarks
    def process_landmarks(self, landmarks, mp_pose):
        raise NotImplementedError("Implement process_landmarks()")

    #for FSM's specific to that exercise
    def update_fsm(self, angle):
        raise NotImplementedError("Implement update_fsm()")