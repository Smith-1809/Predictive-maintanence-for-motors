import tkinter as tk
from tkinter import ttk
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak():
    text = text_input.get("1.0", tk.END)
    if text.strip():
        try:
            engine.setProperty("rate", rate_scale.get())
            engine.setProperty("volume", volume_scale.get())
            engine.setProperty("voice", voice_combobox.get())
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            error_label.config(text=f"Error: {e}")
    else:
        error_label.config(text="Please enter some text.")

def stop():
    engine.stop()
    error_label.config(text="")

def save_audio():
    text = text_input.get("1.0", tk.END).strip()
    if text:
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3")
            if file_path:
                engine.save_to_file(text, file_path)
                engine.runAndWait()
                error_label.config(text=f"Audio saved to: {file_path}")
        except Exception as e:
            error_label.config(text=f"Error saving audio: {e}")
    else:
        error_label.config(text="Please enter some text.")

def change_language(event):
    selected_language = language_combobox.get()
    voices = engine.getProperty("voices")
    for voice in voices:
        if voice.languages[0] == selected_language:
            engine.setProperty("voice", voice.id)
            voice_combobox.set(voice.name)
            break

# Create the main window
root = tk.Tk()
root.title("Text-to-Speech")

# Create the GUI elements
text_input = tk.Text(root, height=5, width=40)
text_input.grid(row=0, column=0, padx=10, pady=10)

language_label = tk.Label(root, text="Language:")
language_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

languages = list(set([voice.languages[0] for voice in engine.getProperty("voices")]))
language_combobox = ttk.Combobox(root, values=languages)
language_combobox.grid(row=1, column=1, padx=10, pady=5)
language_combobox.bind("<<ComboboxSelected>>", change_language)

voice_label = tk.Label(root, text="Voice:")
voice_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

voices = [voice.name for voice in engine.getProperty("voices")]
voice_combobox = ttk.Combobox(root, values=voices)
voice_combobox.grid(row=2, column=1, padx=10, pady=5)

rate_label = tk.Label(root, text="Rate:")
rate_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

rate_scale = tk.Scale(root, from_=50, to=300, orient=tk.HORIZONTAL, length=200)
rate_scale.grid(row=3, column=1, padx=10, pady=5)

volume_label = tk.Label(root, text="Volume:")
volume_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

volume_scale = tk.Scale(root, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=200)
volume_scale.grid(row=4, column=1, padx=10, pady=5)

speak_button = tk.Button(root, text="Speak", command=speak)
speak_button.grid(row=5, column=0, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop", command=stop)
stop_button.grid(row=5, column=1, padx=10, pady=10)

save_button = tk.Button(root, text="Save Audio", command=save_audio)
save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

error_label = tk.Label(root, fg="red")
error_label.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

# Start the main event loop
root.mainloop()