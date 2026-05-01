import time
from exercise import Exercise
from oneEuroFilter import OneEuroFilter

class LateralRaise(Exercise):
    def __init__(self, target_angle=90.0):
        super().__init__("Lateral Raise")
        self.max_angle_reached = 0.0 
        self.euro_filter = OneEuroFilter(min_cutoff=1.0, beta=0.007)
        self.current_angle = 0.0
        self.target_angle = float(target_angle)

    #tracking mediapipe landmarks for lateral raise
    def process_landmarks(self, landmarks, mp_pose):
        hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

        if hip.visibility > 0.5 and shoulder.visibility > 0.5 and elbow.visibility > 0.5:
            hip_coord = [hip.x, hip.y]
            shoulder_coord = [shoulder.x, shoulder.y]
            elbow_coord = [elbow.x, elbow.y]

            raw_angle = self.calculate_angle(hip_coord, shoulder_coord, elbow_coord)
            self.current_angle = self.euro_filter(time.time(), raw_angle)
            self.update_fsm(self.current_angle)
            
            return True
        return False

    def update_fsm(self, shoulder_angle):
        if self.current_state == 'IDLE':
            if shoulder_angle > 20.0:
                self.current_state = 'FLEXING'
                self.max_angle_reached = shoulder_angle
                self.rep_quality = "In Progress"
                
        elif self.current_state in ['FLEXING', 'TARGET']:
            if shoulder_angle > self.max_angle_reached:
                self.max_angle_reached = shoulder_angle
                
            if self.current_state == 'FLEXING' and shoulder_angle >= self.target_angle:
                self.current_state = 'TARGET'
                
            if shoulder_angle < self.max_angle_reached - 15.0:
                self.current_state = 'STRAIGHTENING'
                
                angle_diff = self.max_angle_reached - self.target_angle
                
                if -5.0 <= angle_diff <= 10.0:
                    self.rep_quality = "GOOD"
                elif (-15.0 <= angle_diff < -5.0) or (10.0 < angle_diff <= 20.0):
                    self.rep_quality = "OKAY"
                elif angle_diff < -15.0:
                    self.rep_quality = "BAD"
                else:
                    self.rep_quality = "BAD"
                    
        elif self.current_state == 'STRAIGHTENING':
            if shoulder_angle < 20.0:
                self.current_state = 'IDLE'
                self.rep_count += 1
                self.rep_history.append(self.max_angle_reached)
                self.quality_history.append(self.rep_quality)