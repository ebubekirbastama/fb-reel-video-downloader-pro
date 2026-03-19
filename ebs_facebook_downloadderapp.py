import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import os
import re

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader PRO")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use('default')

        # URL LIST
        tk.Label(root, text="Video Linkleri (Her satıra 1 link)", bg="#1e1e1e", fg="white").pack(pady=5)
        self.url_text = tk.Text(root, height=8, width=80, bg="#2b2b2b", fg="white", insertbackground="white")
        self.url_text.pack(pady=5)

        # BUTTON
        self.download_btn = tk.Button(root, text="İNDİR", command=self.start_download, bg="#00c853", fg="white", height=2, width=20)
        self.download_btn.pack(pady=10)

        # PROGRESS
        self.progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=10)

        self.progress_label = tk.Label(root, text="0%", bg="#1e1e1e", fg="white")
        self.progress_label.pack()

        # TAG OUTPUT
        tk.Label(root, text="Çıkan Hashtag / Etiketler", bg="#1e1e1e", fg="white").pack(pady=5)
        self.tag_output = tk.Text(root, height=8, width=80, bg="#2b2b2b", fg="#00ff9c")
        self.tag_output.pack(pady=5)

    def clean_tags(self, title):
        tags = re.findall(r"#\w+", title)
        return tags

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                self.progress['value'] = percent
                self.progress_label.config(text=f"{int(percent)}%")
                self.root.update_idletasks()

    def download_video(self, url):
        try:
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_DIR}/%(title).40s_%(id)s.%(ext)s',
                'restrictfilenames': True,
                'format': 'best',
                'progress_hooks': [self.progress_hook],
                'noplaylist': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', '')

                tags = self.clean_tags(title)
                if tags:
                    self.tag_output.insert(tk.END, f"{title}\n{', '.join(tags)}\n\n")

        except Exception as e:
            print("Hata:", e)

    def start_download(self):
        urls = self.url_text.get("1.0", tk.END).strip().split("\n")

        if not urls or urls == ['']:
            messagebox.showwarning("Uyarı", "Link eklemelisin")
            return

        def run():
            for url in urls:
                self.progress['value'] = 0
                self.download_video(url.strip())
            messagebox.showinfo("Bitti", "Tüm videolar indirildi")

        threading.Thread(target=run).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
