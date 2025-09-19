import subprocess

def get_available_formats(status_box, url):
    try:
        result = subprocess.run(
            ["yt-dlp", "--list-formats", url],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        formats = result.stdout.strip()
        status_box.insert("end", f"Available Formats:\n{formats}\n")

        return formats
    except Exception as e:
        status_box.insert("end", f"Error fetching formats: {e}\n")
        return "Unknown Formats"

def get_video_title(status_box, url):
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
    

def download(status_box, url, quality_code="bestvideo+bestaudio/best"):
    """Constructs and runs the yt-dlp command."""
    # Command to download the best quality video and audio combined
    command = [
        "yt-dlp",
        url,
        "-f", quality_code, # Format code
        "-o", # Output template
        "%(title)s.%(ext)s"
    ]

    # Run the command using subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

    # Read output line by line and update the status box
    for line in iter(process.stdout.readline, ''):
        if "[download]" in line:
            #Remove "[download]" from the line
            line = line.replace("[download]", "").strip()
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