import tkinter as tk
from tkinter import ttk
import cv2
import mediapipe as mp
import time
from squat import Squat
from standing_knee_bend import StandingKneeBend
from lateral_raise import LateralRaise
from bicep_curl import BicepCurl
from front_lunge import FrontLunge
from display_utils import draw_exercise_overlay, draw_warning
from summary_screen import show_summary, show_final_summary

def main():
    #this section initializes the GUI
    selected_exercise_class = None
    
    root = tk.Tk()
    root.title("PercePT - Menu")
    root.geometry("350x450") 
    
    #starting values for the GUI
    angle_var = tk.StringVar(value="145") 
    reps_var = tk.StringVar(value="10")
    sets_var = tk.StringVar(value="3")
    timer_var = tk.StringVar(value="6")

    target_angle = 145.0
    target_reps = 10
    target_sets = 3
    target_timer = 6.0 

    def start_camera(exercise_class):
        #use same variable from above scope
        nonlocal selected_exercise_class, target_angle, target_reps, target_sets, target_timer
        
        selected_exercise_class = exercise_class
        target_angle = float(angle_var.get())   
        target_reps = int(reps_var.get())
        target_sets = int(sets_var.get())
        target_timer = float(timer_var.get())

        root.destroy() 
        
    ttk.Label(root, text="Welcome to PercePT", font=("Helvetica", 14, "bold")).pack(pady=10)
    
    param_frame = ttk.Frame(root)
    param_frame.pack(pady=5)

    ttk.Label(param_frame, text="Target Angle (°):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(param_frame, textvariable=angle_var, width=8, justify="center").grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(param_frame, text="Target Reps:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(param_frame, textvariable=reps_var, width=8, justify="center").grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(param_frame, text="Target Sets:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(param_frame, textvariable=sets_var, width=8, justify="center").grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(param_frame, text="Setup Timer (sec):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    ttk.Entry(param_frame, textvariable=timer_var, width=8, justify="center").grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(root, text="Select an exercise to begin:").pack(pady=5)

    ttk.Button(root, text="Standard Squat", command=lambda: start_camera(Squat)).pack(pady=3)
    ttk.Button(root, text="ACL Standing Knee Bend", command=lambda: start_camera(StandingKneeBend)).pack(pady=3)
    ttk.Button(root, text="Lateral Raise", command=lambda: start_camera(LateralRaise)).pack(pady=3)
    ttk.Button(root, text="Bicep Curl", command=lambda: start_camera(BicepCurl)).pack(pady=3)
    ttk.Button(root, text="Front Lunge", command=lambda: start_camera(FrontLunge)).pack(pady=3)

    root.mainloop()

    #OpenCV Code
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    workout_total_reps = 0
    workout_all_qualities = []
    actual_sets_completed = 0

    #loop is based on selected sets by user
    for current_set in range(1, target_sets + 1):
        active_exercise = selected_exercise_class(target_angle=target_angle)
        cap = cv2.VideoCapture(0)
        
        set_start_time = time.time()
        countdown_duration = target_timer 

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success_read, frame = cap.read()
                if not success_read:
                    continue

                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)
                frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

                elapsed_time = time.time() - set_start_time
                
                if elapsed_time < countdown_duration:
                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                    
                    seconds_left = int(countdown_duration - elapsed_time)
                    cv2.putText(frame, "GET READY!", (120, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3, cv2.LINE_AA)
                    cv2.putText(frame, str(seconds_left), (280, 250), cv2.FONT_HERSHEY_SIMPLEX, 4.0, (0, 255, 255), 5, cv2.LINE_AA)  
                else:
                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                        success = active_exercise.process_landmarks(results.pose_landmarks.landmark, mp_pose)

                        if success:
                            draw_exercise_overlay(frame, active_exercise, current_set, target_sets)
                        else:
                            draw_warning(frame)

                cv2.imshow(f'PercePT - {active_exercise.name}', frame)

                if active_exercise.rep_count >= target_reps:
                    break
                
                #user hits q to leave the session
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    current_set = target_sets 
                    break

        cap.release()
        cv2.waitKey(1)
        cv2.destroyAllWindows()

        #for workout summary
        workout_total_reps += active_exercise.rep_count
        workout_all_qualities.extend(active_exercise.quality_history)
        actual_sets_completed += 1

        show_summary(
            exercise_name=active_exercise.name,
            target_angle=active_exercise.target_angle,
            total_reps=active_exercise.rep_count,
            rep_history=active_exercise.rep_history,
            current_set=current_set,
            total_sets=target_sets
        )
        
        if current_set == target_sets:
            break

    #overall workout summary
    if workout_total_reps > 0:
        show_final_summary(
            exercise_name=active_exercise.name,
            target_angle=target_angle,
            total_sets=actual_sets_completed,
            total_reps=workout_total_reps,
            all_qualities=workout_all_qualities
        )

if __name__ == "__main__":
    main()