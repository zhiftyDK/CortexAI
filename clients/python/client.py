import customtkinter as ctk
import keyboard
import requests
import time
import queue
import threading
import tools

command_queue = queue.Queue()

def ease_in_out(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def animate_both(show):
    steps = 50
    duration = 150
    if show:
        overlay_start_y, overlay_end_y = -500, 50
        response_start_y = response_overlay.winfo_screenheight()
        response_end_y = response_overlay.winfo_screenheight() - 300
    else:
        overlay_start_y, overlay_end_y = 50, -500
        response_start_y = response_overlay.winfo_screenheight() - 300
        response_end_y = response_overlay.winfo_screenheight()
    
    for step in range(steps + 1):
        t = step / steps
        overlay_y = overlay_start_y + (overlay_end_y - overlay_start_y) * ease_in_out(t)
        response_y = response_start_y + (response_end_y - response_start_y) * ease_in_out(t)
        
        overlay.geometry(f"500x150+{(overlay.winfo_screenwidth() - 500) // 2}+{int(overlay_y)}")
        response_overlay.geometry(f"700x250+{(response_overlay.winfo_screenwidth() - 700) // 2}+{int(response_y)}")
        
        overlay.update()
        response_overlay.update()
        overlay.after(duration // steps)

def ensure_focus():
    overlay.focus_force()
    input_field.focus_set()
    overlay.after(50, lambda: (overlay.focus_force(), input_field.focus_set()))

def toggle_overlay():
    command_queue.put("toggle_overlay")

def show_response():
    command_queue.put("show_response")

def send_to_model(event):
    text = input_field.get()
    timeconcept = time.strftime("%Y-%m-%d %H-%M-%S")
    url = "https://beta.gideonai.net/api/v1/workspace/he-gideon-project/chat"
    payload = {
        "message": f"{text} {timeconcept}",
        "mode": "chat",
        "user": "berlecool"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer Hehe, you thought ;)'
    }
    response = requests.post(url, json=payload, headers=headers)
    commandparse = response.json().get('textResponse')
    if len(commandparse.split("#")) > 1:
        command = commandparse.split("#")[1]
        tools.parse_command(command)
    if response.status_code == 200:
        response_text = response.json().get('textResponse')
        command_queue.put(("update_response", response_text))
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
    
    input_field.delete(0, 'end')

def process_queue():
    try:
        while True:
            command = command_queue.get_nowait()
            if command == "toggle_overlay":
                if overlay.winfo_viewable():
                    animate_both(False)
                    overlay.withdraw()
                    response_overlay.withdraw()
                else:
                    overlay.deiconify()
                    if response_overlay.winfo_viewable():
                        response_overlay.deiconify()
                    animate_both(True)
                    overlay.after(10, ensure_focus)
            elif command == "show_response":
                if not response_overlay.winfo_viewable():
                    response_overlay.deiconify()
                    animate_both(True)
            elif isinstance(command, tuple) and command[0] == "update_response":
                response_text = command[1]
                response_field.delete('0.0', 'end')
                response_field.insert('end', response_text)
                response_field.see('end')
                show_response()
    except queue.Empty:
        pass
    overlay.after(100, process_queue)

overlay = ctk.CTk()
overlay.geometry(f"500x150+{(overlay.winfo_screenwidth() - 500) // 2}+-500")
overlay.overrideredirect(True)
overlay.attributes("-topmost", True)
overlay.wm_attributes("-transparentcolor", overlay["bg"])
overlay.withdraw()

input_field = ctk.CTkEntry(overlay, width=450, height=50, text_color="white", fg_color="#333333", 
                           border_color="white", border_width=2, font=("Arial", 20), corner_radius=20)
input_field.place(relx=0.5, rely=0.5, anchor="center")
input_field.bind("<Return>", send_to_model)

response_overlay = ctk.CTk()
response_overlay.geometry(f"700x250+{(response_overlay.winfo_screenwidth() - 700) // 2}+{response_overlay.winfo_screenheight()}")
response_overlay.overrideredirect(True)
response_overlay.attributes("-topmost", True)
response_overlay.wm_attributes("-transparentcolor", response_overlay["bg"])
response_overlay.withdraw()

response_field = ctk.CTkTextbox(response_overlay, width=650, height=200, text_color="white", fg_color="#333333", 
                                border_color="white", border_width=2, font=("Arial", 18), corner_radius=20,
                                wrap="word")
response_field.place(relx=0.5, rely=0.5, anchor="center")

keyboard.add_hotkey('ctrl+alt+x', toggle_overlay)

overlay.after(100, process_queue)

overlay.mainloop()