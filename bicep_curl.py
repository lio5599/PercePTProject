import time
from exercise import Exercise
from oneEuroFilter import OneEuroFilter

class BicepCurl(Exercise):
    def __init__(self, target_angle=40.0):
        super().__init__("Bicep Curl")
        self.min_angle_reached = 180.0
        self.euro_filter = OneEuroFilter(min_cutoff=1.0, beta=0.007)
        self.current_angle = 180.0
        self.target_angle = float(target_angle)

    def process_landmarks(self, landmarks, mp_pose):
        shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]

        if shoulder.visibility > 0.5 and elbow.visibility > 0.5 and wrist.visibility > 0.5:
            shoulder_coord = [shoulder.x, shoulder.y]
            elbow_coord = [elbow.x, elbow.y]
            wrist_coord = [wrist.x, wrist.y]

            raw_angle = self.calculate_angle(shoulder_coord, elbow_coord, wrist_coord)
            self.current_angle = self.euro_filter(time.time(), raw_angle)
            self.update_fsm(self.current_angle)
            
            return True
        return False

    def update_fsm(self, elbow_angle):
        if self.current_state == 'IDLE':
            if elbow_angle < 150.0:
                self.current_state = 'FLEXING'
                self.min_angle_reached = elbow_angle
                self.rep_quality = "In Progress"
                
        elif self.current_state in ['FLEXING', 'TARGET']:
            if elbow_angle < self.min_angle_reached:
                self.min_angle_reached = elbow_angle
                
            if self.current_state == 'FLEXING' and elbow_angle <= self.target_angle:
                self.current_state = 'TARGET'
                
            if elbow_angle > self.min_angle_reached + 15.0:
                self.current_state = 'STRAIGHTENING'
                
                angle_diff = self.min_angle_reached - self.target_angle
                
                if -10.0 <= angle_diff <= 5.0:
                    self.rep_quality = "GOOD"
                elif (-20.0 <= angle_diff < -10.0) or (5.0 < angle_diff <= 15.0):
                    self.rep_quality = "OKAY"
                elif angle_diff < -20.0:
                    self.rep_quality = "BAD"
                else:
                    self.rep_quality = "BAD"
                    
        elif self.current_state == 'STRAIGHTENING':
            if elbow_angle > 150.0:
                self.current_state = 'IDLE'
                self.rep_count += 1
                self.rep_history.append(self.min_angle_reached)
                self.quality_history.append(self.rep_quality)