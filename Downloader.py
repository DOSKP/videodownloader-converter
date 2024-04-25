import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import re
from moviepy.editor import VideoFileClip
import os

def download_video():
    video_url = url_entry.get()
    output_path = path_entry.get()
    if not validate_url(video_url):
        messagebox.showerror("Hiba", "Kérem, adjon meg egy érvényes YouTube videó URL-t.")
        return
    try:
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        if output_path:
            video_path = video.download(output_path)
        else:
            video_path = video.download()
        messagebox.showinfo("Sikeres letöltés", "A videó sikeresen letöltve!")
        return video_path
    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba történt a videó letöltése közben: {e}")

def convert_to_mp3():
    video_path = download_video()
    if video_path:
        try:
            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            output_path = os.path.splitext(video_path)[0] + ".mp3"
            audio_clip.write_audiofile(output_path)
            audio_clip.close()
            video_clip.close()
            messagebox.showinfo("Sikeres konverzió", "A videó sikeresen konvertálva lett MP3 formátumba!")
        except Exception as e:
            messagebox.showerror("Hiba", f"Hiba történt a konverzió közben: {e}")

def validate_url(url):
    pattern = r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]+(&\S+)?"
    return re.match(pattern, url)

def browse_output_path():
    output_path = filedialog.askdirectory()
    if output_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, output_path)

root = tk.Tk()
root.title("YouTube Videó Letöltő és Konvertáló Csöpi által")
root.geometry("720x800")

url_label = tk.Label(root, text="YouTube Videó URL:")
url_label.pack()
url_entry = tk.Entry(root, width=60)
url_entry.pack()

path_label = tk.Label(root, text="Letöltési útvonal (opcionális):")
path_label.pack()
path_entry = tk.Entry(root, width=50)
path_entry.pack()

browse_button = tk.Button(root, text="Tallózás", command=browse_output_path)
browse_button.pack()


download_button = tk.Button(root, text="Letöltés", command=convert_to_mp3)
download_button.pack()

root.mainloop()
