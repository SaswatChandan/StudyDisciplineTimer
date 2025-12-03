import tkinter as tk
import time
import threading
from tkinter import simpledialog

# Create root BEFORE asking dialogs
root = tk.Tk()
root.title("Blink Timer")
root.geometry("220x150+50+50")
root.attributes("-topmost", True)

# Hide only visually (but keep window alive)
root.update()
root.withdraw()

# ---------------- ASK USER INPUT ----------------
INTERVAL_MINUTES = simpledialog.askfloat(
    "Timer Interval",
    "Enter interval in minutes:",
    minvalue=0.01,
    parent=root
)

FLASH_TEXT = simpledialog.askstring(
    "Flash Message",
    "Enter the message to display:",
    parent=root
)

# If user cancels → exit safely
if INTERVAL_MINUTES is None or FLASH_TEXT is None:
    root.destroy()
    exit()

# After inputs → show main window
root.deiconify()

# ===== SETTINGS =====
FLASH_DURATION = 500
running = True
remaining_sec = int(INTERVAL_MINUTES * 60)

# ---------------- FLASH WINDOW ----------------
def flash_once():
    flash = tk.Toplevel()
    flash.overrideredirect(True)
    flash.attributes("-topmost", True)
    flash.geometry("500x250+450+250")
    flash.config(bg="#000000")

    frame = tk.Frame(
        flash,
        bg="#ffeb3b",
        highlightthickness=6,
        highlightbackground="#ffffff"
    )
    frame.place(relx=0.5, rely=0.5, anchor="center", width=480, height=230)

    msg = tk.Label(
        frame,
        text=FLASH_TEXT,
        font=("Helvetica", 28, "bold"),
        bg="#ffeb3b",
        fg="#000000"
    )
    msg.pack(expand=True)

    # glow animation
    def animate_glow(alpha=0):
        color_value = 200 + int(55 * abs((alpha % 20) - 10) / 10)
        glow_color = f"#{color_value:02x}{color_value:02x}{color_value:02x}"
        frame.config(highlightbackground=glow_color)
        flash.after(50, lambda: animate_glow(alpha + 1))

    animate_glow()
    flash.after(FLASH_DURATION, flash.destroy)

# ---------------- TIMER LOOP ----------------
def timer_loop():
    global remaining_sec, running

    while True:
        if running:
            time.sleep(1)
            remaining_sec -= 1
            label.config(text=format_time(remaining_sec))

            if remaining_sec <= 0:
                flash_once()
                remaining_sec = int(INTERVAL_MINUTES * 60)

# ---------------- HELPERS ----------------
def format_time(sec):
    sec = int(sec)
    m = sec // 60
    s = sec % 60
    return f"{m:02d}:{s:02d}"

def pause_resume():
    global running
    running = not running
    btn_pause.config(text="Resume" if not running else "Pause")

def reset_timer():
    global remaining_sec
    remaining_sec = int(INTERVAL_MINUTES * 60)
    label.config(text=format_time(remaining_sec))

# ---------------- MAIN UI ----------------
label = tk.Label(root, text=format_time(remaining_sec), font=("Arial", 32))
label.pack(pady=10)

btn_pause = tk.Button(root, text="Pause", width=12, command=pause_resume)
btn_pause.pack()

btn_reset = tk.Button(root, text="Reset", width=12, command=reset_timer)
btn_reset.pack(pady=5)

threading.Thread(target=timer_loop, daemon=True).start()

root.mainloop()
