def check_valid_URL(url):
    import validators
    """Checks if the provided URL is a valid YouTube link."""
    return validators.url(url)

def check_ffmpeg():
    """Checks if ffmpeg is installed and in the system PATH."""
    import subprocess
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, encoding='utf-8')
    except FileNotFoundError:
        print(f"Warning: ffmpeg is not installed or not found in system PATH. \n Please install ffmpeg for best performance with yt-dlp.")