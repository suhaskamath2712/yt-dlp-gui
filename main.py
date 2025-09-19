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

# Status Box
status_box = ctk.CTkTextbox(app, height=150, width=600)
status_box.pack(pady=10)

#Ensure ffmpeg is installed and in PATH for best performance with yt-dlp
if not util.check_ffmpeg():
    status_box.insert("end", "Warning: ffmpeg is not installed or not found in system PATH. \n Please install ffmpeg for best performance with yt-dlp.")
    sys.exit(1)

quality_set = False

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
        #Check if url is from YouTube
        if "youtube.com" not in url and "youtu.be" not in url:
            status_box.insert("end", f"Error: The URL '{url}' is not a valid YouTube link.\n")
        
        #Check if playlist is provided
        if "list" in url:
            status_box.insert("end", f"Playlist detected: {url}\n")
            playlist = True
        
        if not playlist:
            #Get video title using yt-dlp
            title_thread = threading.Thread(target=ytdlp.get_video_title, args=(status_box, url))
            title_thread.start()
        
        if not playlist and manual_quality_var.get():
            global quality_set
            quality_set = False

            #Manually choose quality
            threading.Thread(target=ytdlp.get_available_formats, args=(status_box, url)).start()
            status_box.insert("end", f"Available Formats:\n")
            status_box.insert("end", "Please enter the desired format code in the formats field.\n")
            quality_entry.configure(state="normal")
            quality_entry.focus()
            
            # Wait until user enters the format code and clicks the Set Quality button
            while not quality_set:
                app.update()
            
            quality_code = quality_entry.get()

            quality_set = False
            quality_entry.configure(state="disabled")
            status_box.insert("end", f"Selected format code: {quality_code}\n")
            download_thread = threading.Thread(target=ytdlp.download, args=(status_box, url, quality_code))
            download_thread.start()

        status_box.insert("end", f"Processing URL: {url}\n")

        # Run the download in a separate thread to prevent the GUI from freezing
        #download_thread = threading.Thread(target=run_yt_dlp, args=(url,))
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

# Quality Selection
quality_label = ctk.CTkLabel(app, text="Quality Selection (if manual quality is checked):")
quality_label.pack(pady=5)
quality_label.place_forget()  # Hide initially

quality_entry = ctk.CTkEntry(app, width=200, placeholder_text="Enter format code")
quality_entry.pack(pady=5)
quality_entry.insert(0, "bestvideo+bestaudio/best")
quality_entry.configure(state="disabled")
quality_entry.place_forget()  # Hide initially

quality_button = ctk.CTkButton(app, text="Set Quality", command=lambda: quality_set.__setitem__(0, True)) 
quality_button.pack(pady=5)
quality_button.place_forget()  # Hide initially

def toggle_quality_selection():
    if not manual_quality_var.get():
        quality_label.place(x=10, y=250)
        quality_entry.place(x=10, y=280)
        quality_button.place(x=220, y=280)
    else:
        quality_label.place_forget()
        quality_entry.place_forget()
        quality_button.place_forget()

# --- Run the application ---
app.mainloop()