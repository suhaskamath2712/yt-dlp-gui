import customtkinter as ctk
import threading
import sys

#Self-made modules
import util
import ytdlp_interface as ytdlp

# Set the appearance mode
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- Main Application Window ---
app = ctk.CTk()
app.title("My yt-dlp GUI")
app.geometry("700x350")

# --- UI Widgets ---
# URL Input
url_label = ctk.CTkLabel(app, text="Video URL:")
url_label.pack(pady=5)
url_entry = ctk.CTkEntry(app, width=400, placeholder_text="Enter URL")
url_entry.pack(pady=5)

#Audio Only Checkbox
audio_only_var = ctk.BooleanVar()
audio_only_checkbox = ctk.CTkCheckBox(app, text="Audio Only", variable=audio_only_var)
audio_only_checkbox.pack(pady=5)

sponsorblock_checkbox_var = ctk.BooleanVar(value=True)
sponsorblock_checkbox = ctk.CTkCheckBox(app, text="Skip Sponsor Segments (SponsorBlock)", variable=sponsorblock_checkbox_var)
sponsorblock_checkbox.pack(pady=5)

# Status Box
status_box = ctk.CTkTextbox(app, height=150, width=600)
status_box.pack(pady=10)

#Ensure ffmpeg is installed and in PATH for best performance with yt-dlp
if not util.check_ffmpeg():
    status_box.insert("end", "Warning: ffmpeg is not installed or not found in system PATH. \n Please install ffmpeg for best performance with yt-dlp.")
    sys.exit(1)


def download_video():
    """Grabs the URL and starts the download process in a separate thread."""
    url = url_entry.get()

    # Check if multiple urls are provided, urls must be separated by space
    urls = url_entry.get().split(" ")

    if not url:
        status_box.insert("end", "Error: Please enter a URL.\n")
        return

    
    for url in urls:
        # Clear status box for new download
        status_box.delete("1.0", "end")
        status_box.insert("end", f"Starting download for: {url}\n\n")

        if not util.check_valid_URL(url):
            status_box.insert("end", f"Error: The URL '{url}' is not valid.\n")
            continue

        playlist = False
        
        #Check if playlist is provided
        if "list" in url:
            status_box.insert("end", f"Playlist detected: {url}\n")
            playlist = True
        
        if not playlist:
            #Get video title using yt-dlp
            title_thread = threading.Thread(target=ytdlp.get_video_title, args=(status_box, url))
            title_thread.start()

        status_box.insert("end", f"Processing URL: {url}\n")

        # Run the download in a separate thread to prevent the GUI from freezing
        download_thread = threading.Thread(target=ytdlp.run_yt_dlp, args=(status_box,url,audio_only_var.get()))
        #download_thread.start()

def stop_download():
    """Stops the ongoing download process."""
    # This is a placeholder function. Implementing process termination requires tracking the subprocess.
    status_box.insert("end", "Stop functionality is not implemented yet.\n")

# Add a checkbox for manual quality selection
manual_quality_var = ctk.BooleanVar()
manual_quality_checkbox = ctk.CTkCheckBox(app, text="Manually choose quality", variable=manual_quality_var)
manual_quality_checkbox.pack(pady=5)

# Download Button
download_button = ctk.CTkButton(app, text="Download", command=download_video)
download_button.pack(pady=20)

# Stop Button
stop_button = ctk.CTkButton(app, text="Stop", command=stop_download)
stop_button.pack(pady=5)

# --- Run the application ---
app.mainloop()