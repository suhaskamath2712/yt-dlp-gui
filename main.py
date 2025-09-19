import customtkinter as ctk
import subprocess
import threading

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
    

# --- Core Functionality ---
def download_video():
    """Grabs the URL and starts the download process in a separate thread."""
    url = url_entry.get()

    # Check if multiple urls are provided, urls must be separated by space
    urls = url_entry.get().split(" ")

    if not url:
        status_box.insert("end", "Error: Please enter a URL.\n")
        return

    # Clear status box for new download
    status_box.delete("1.0", "end")
    status_box.insert("end", f"Starting download for: {url}\n\n")
    
    for url in urls:
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
            title_thread = threading.Thread(target=get_video_title, args=(url,))
            title_thread.start()

        status_box.insert("end", f"Processing URL: {url}\n")
        # Run the download in a separate thread to prevent the GUI from freezing
        #download_thread = threading.Thread(target=run_yt_dlp, args=(url,))
        #download_thread.start()

def stop_download():
    """Stops the ongoing download process."""
    # This is a placeholder function. Implementing process termination requires tracking the subprocess.
    status_box.insert("end", "Stop functionality is not implemented yet.\n")

def get_video_title(url):
    """Fetches the video title using yt-dlp."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", url],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        title = result.stdout.strip()
        status_box.insert("end", f"Video Title: {title}\n")

        return title
    except Exception as e:
        status_box.insert("end", f"Error fetching title: {e}\n")
        return "Unknown Title"

def run_yt_dlp(url):
    """Constructs and runs the yt-dlp command."""
    # Command to download the best quality video and audio combined
    command = [
        "yt-dlp",
        url,
        "-o", # Output template
        "%(title)s.%(ext)s"
    ]

    # Run the command using subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

    # Read output line by line and update the status box
    for line in iter(process.stdout.readline, ''):
        status_box.insert("end", line)
        status_box.see("end") # Auto-scroll
    
    process.stdout.close()
    return_code = process.wait()

    if return_code == 0:
        status_box.insert("end", "\n--- Download successful! ---\n")
    else:
        # Get error message if it failed
        error_output = process.stderr.read()
        status_box.insert("end", f"\n--- Download failed! ---\nError:\n{error_output}\n")
    status_box.see("end")

# Download Button
download_button = ctk.CTkButton(app, text="Download", command=download_video)
download_button.pack(pady=20)

# Stop Button
stop_button = ctk.CTkButton(app, text="Stop", command=stop_download)
stop_button.pack(pady=5)

# --- Run the application ---
app.mainloop()