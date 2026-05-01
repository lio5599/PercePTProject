import cv2

def draw_exercise_overlay(frame, active_exercise, current_set, target_sets):
    #colors for different rep quality (Good, Bad, Okay)
    color_white = (255, 255, 255)
    color_yellow = (0, 255, 255)
    color_green = (0, 255, 0)
    color_red = (0, 0, 255)
    
    quality_color = color_white
    if "GOOD" in active_exercise.rep_quality:
        quality_color = color_green
    elif "OKAY" in active_exercise.rep_quality:
        quality_color = color_yellow
    elif "BAD" in active_exercise.rep_quality:
        quality_color = color_red

    cv2.rectangle(frame, (0, 0), (280, 145), (0, 0, 0), -1)
    
    cv2.putText(frame, f"REPS: {active_exercise.rep_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_white, 2, cv2.LINE_AA)
                
    cv2.putText(frame, f"STATE: {active_exercise.current_state}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_white, 2, cv2.LINE_AA)
    
    cv2.putText(frame, f"ANGLE: {int(active_exercise.current_angle)}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_white, 2, cv2.LINE_AA)
        
    cv2.putText(frame, f"LAST REP: {active_exercise.rep_quality}", (10, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.65, quality_color, 2, cv2.LINE_AA)

    cv2.putText(frame, f"SET {current_set} OF {target_sets}", (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_white, 2, cv2.LINE_AA)

#draws warning if user is not fully in frame
def draw_warning(frame):
    cv2.putText(frame, "Ensure full body is in frame.", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)