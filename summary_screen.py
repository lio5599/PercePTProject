import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_summary(exercise_name, target_angle, total_reps, rep_history, current_set, total_sets):
    root = tk.Tk()
    root.title(f"PercePT - Set {current_set} Summary")
    root.geometry("600x550")

    def close_window():
        plt.close('all')
        root.quit()
        root.destroy()

    ttk.Label(root, text=f"Session Summary: {exercise_name}", font=("Helvetica", 16, "bold")).pack(pady=10)
    ttk.Label(root, text=f"Set {current_set} of {total_sets} Completed", font=("Helvetica", 12, "italic")).pack(pady=(0, 10))

    stats_frame = ttk.Frame(root)
    stats_frame.pack(pady=10)
    
    ttk.Label(stats_frame, text=f"Total Reps: {total_reps}", font=("Helvetica", 12)).grid(row=0, column=0, padx=30)
    ttk.Label(stats_frame, text=f"Target Angle: {target_angle}°", font=("Helvetica", 12)).grid(row=0, column=1, padx=30)

    if rep_history:
        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        reps = range(1, len(rep_history) + 1)
        
        ax.plot(reps, rep_history, marker='o', linestyle='-', color='blue', label="Angle Reached")
        ax.axhline(y=target_angle, color='red', linestyle='--', label="Target")
        
        ax.set_title("Range of Motion Breakdown")
        ax.set_xlabel("Repetition Number")
        ax.set_ylabel("Degrees")
        ax.legend()
        ax.set_xticks(reps)
        
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    else:
        ttk.Label(root, text="No completed repetitions to graph.", font=("Helvetica", 10, "italic")).pack(pady=30)

    if current_set < total_sets:
        button_text = "Start Next Set"
    else:
        button_text = "Finish Workout"
    ttk.Button(root, text=button_text, command=close_window).pack(pady=10)

    #clicking x in the corner closes safely
    root.protocol("WM_DELETE_WINDOW", close_window)

    root.mainloop()



def show_final_summary(exercise_name, target_angle, total_sets, total_reps, all_qualities):
    root = tk.Tk()
    root.title(f"PercePT - Final Workout Summary")
    root.geometry("600x550")

    def close_window():
        plt.close('all')
        root.quit()
        root.destroy()

    ttk.Label(root, text=f"FINAL WORKOUT SUMMARY", font=("Helvetica", 18, "bold")).pack(pady=10)
    ttk.Label(root, text=f"{exercise_name} - Target: {target_angle}°", font=("Helvetica", 12, "italic")).pack(pady=(0, 10))

    good_count = sum(1 for q in all_qualities if "GOOD" in q)
    okay_count = sum(1 for q in all_qualities if "OKAY" in q)
    bad_count = sum(1 for q in all_qualities if "BAD" in q)
    
    success_rate = (good_count / total_reps * 100) if total_reps > 0 else 0

    stats_frame = ttk.Frame(root)
    stats_frame.pack(pady=10)
    
    ttk.Label(stats_frame, text=f"Total Sets: {total_sets}", font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=20)
    ttk.Label(stats_frame, text=f"Total Reps: {total_reps}", font=("Helvetica", 12, "bold")).grid(row=0, column=1, padx=20)
    ttk.Label(stats_frame, text=f"Perfect Form: {success_rate:.1f}%", font=("Helvetica", 12, "bold")).grid(row=0, column=2, padx=20)

    if total_reps > 0:
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        
        labels = []
        sizes = []
        colors = []
        
        if good_count > 0:
            labels.append(f'Good ({good_count})')
            sizes.append(good_count)
            colors.append('#2ca02c')
        if okay_count > 0:
            labels.append(f'Okay ({okay_count})')
            sizes.append(okay_count)
            colors.append('#ff7f0e')
        if bad_count > 0:
            labels.append(f'Bad ({bad_count})')
            sizes.append(bad_count)
            colors.append('#d62728')

        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') 
        ax.set_title("Overall Repetition Quality Breakdown")
        
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    else:
        ttk.Label(root, text="No completed repetitions to analyze.", font=("Helvetica", 10, "italic")).pack(pady=30)

    ttk.Button(root, text="Exit PercePT", command=close_window).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()