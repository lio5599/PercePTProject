import time
from exercise import Exercise
from oneEuroFilter import OneEuroFilter

class StandingKneeBend(Exercise):
    def __init__(self, target_angle=145.0):
        super().__init__("Standing Knee Bend (ACL Rehab)")
        self.min_angle_reached = 180.0
        self.euro_filter = OneEuroFilter(min_cutoff=1.0, beta=0.007)
        self.current_angle = 180.0 
        self.target_angle = float(target_angle)

    #extracts MediaPipe landmarks for a standing knee bend
    def process_landmarks(self, landmarks, mp_pose):
        hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        if hip.visibility > 0.5 and knee.visibility > 0.5 and ankle.visibility > 0.5:
            hip_coord = [hip.x, hip.y]
            knee_coord = [knee.x, knee.y]
            ankle_coord = [ankle.x, ankle.y]
            raw_knee_angle = self.calculate_angle(hip_coord, knee_coord, ankle_coord)
            self.current_angle = self.euro_filter(time.time(), raw_knee_angle)
            self.update_fsm(self.current_angle)
            return True 
        
        return False 

    def update_fsm(self, knee_angle):
        if self.current_state == 'IDLE':
            if knee_angle < 170.0:
                self.current_state = 'FLEXING'
                self.min_angle_reached = knee_angle
                self.rep_quality = "In Progress"
                
        elif self.current_state in ['FLEXING', 'TARGET']:
            if knee_angle < self.min_angle_reached:
                self.min_angle_reached = knee_angle
                
            if self.current_state == 'FLEXING' and knee_angle <= self.target_angle:
                self.current_state = 'TARGET'
                
            if knee_angle > self.min_angle_reached + 10.0:
                self.current_state = 'STRAIGHTENING'
                
                if 130.0 <= self.min_angle_reached <= 140.0:
                    self.rep_quality = "GOOD"
                elif 120.0 <= self.min_angle_reached < 130.0:
                    self.rep_quality = "OKAY"
                elif 140.0 < self.min_angle_reached <= 150.0:
                    self.rep_quality = "OKAY"
                elif self.min_angle_reached < 120.0:
                    self.rep_quality = "BAD"
                else:
                    self.rep_quality = "BAD"
                    
        elif self.current_state == 'STRAIGHTENING':
            if knee_angle >= 170.0:
                self.current_state = 'IDLE'
                self.rep_count += 1
                self.rep_history.append(self.min_angle_reached)
                self.quality_history.append(self.rep_quality)