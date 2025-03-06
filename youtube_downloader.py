from pytube import YouTube
import argparse
import sys
import re
import random
import yt_dlp

def clean_url(url):
    # Remove any trailing backslashes or spaces
    url = url.strip()
    if url.endswith('\\'):
        url = url[:-1]  # Remove the trailing backslash
    
    # Extract video ID and reconstruct the URL
    video_id_match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', url)
    if video_id_match:
        return f'https://www.youtube.com/watch?v={video_id_match.group(1)}'
    return url

def download_video(url, output_path=None):
    try:
        # Clean and validate the URL
        cleaned_url = clean_url(url)
        print(f"Processing URL: {cleaned_url}")
        
        # Set default output path if not provided
        if not output_path:
            output_path = '.'
        
        # Check if ffmpeg is installed
        ffmpeg_installed = check_ffmpeg()
        if not ffmpeg_installed:
            print("\nWARNING: ffmpeg is not installed. High-resolution downloads require ffmpeg.")
            print("Would you like to:")
            print("1. Continue with limited resolution options (up to 360p combined streams)")
            print("2. Get instructions to install ffmpeg")
            print("3. Exit")
            
            while True:
                choice = input("\nEnter your choice (1-3): ")
                if choice == "1":
                    print("\nContinuing with limited resolution options...")
                    break
                elif choice == "2":
                    show_ffmpeg_instructions()
                    sys.exit(0)
                elif choice == "3":
                    print("Exiting...")
                    sys.exit(0)
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
        
        # Fetch video information first
        print("Fetching video information...")
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(cleaned_url, download=False)
            
            print(f"\nTitle: {info.get('title', 'Unknown')}")
            print(f"Duration: {info.get('duration', 'Unknown')} seconds")
            
            # Get available formats - include both combined and separate streams
            formats = []
            
            # Add best combined formats (audio+video)
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    height = f.get('height')
                    if height:
                        formats.append((f['format_id'], f'{height}p', f.get('ext', 'unknown'), 'combined'))
            
            # Add best video-only formats (for higher resolutions) only if ffmpeg is installed
            if ffmpeg_installed:
                for f in info.get('formats', []):
                    if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                        height = f.get('height')
                        if height:
                            formats.append((f['format_id'], f'{height}p', f.get('ext', 'unknown'), 'video-only'))
            
            # Sort formats by resolution (height)
            formats.sort(key=lambda x: int(x[1][:-1]) if x[1][:-1].isdigit() else 0, reverse=True)
            
            # Remove duplicates (keep highest quality for each resolution)
            seen_resolutions = set()
            unique_formats = []
            for fmt in formats:
                if fmt[1] not in seen_resolutions:
                    unique_formats.append(fmt)
                    seen_resolutions.add(fmt[1])
            
            if not unique_formats:
                print("No formats found. Will download best available quality.")
                format_choice = 'best' if not ffmpeg_installed else 'bestvideo+bestaudio/best'
            else:
                # Display available formats
                print("\nAvailable quality options:")
                for i, (format_id, resolution, ext, stream_type) in enumerate(unique_formats, 1):
                    type_label = " (combined)" if stream_type == "combined" else ""
                    print(f"{i}. {resolution} ({ext}){type_label}")
                
                # Ask user to select format
                while True:
                    try:
                        choice = input("\nSelect quality (number) or press Enter for best quality: ")
                        if choice == "":
                            format_choice = 'best' if not ffmpeg_installed else 'bestvideo+bestaudio/best'
                            print("Selected: Best available quality")
                            break
                        choice_index = int(choice) - 1
                        if 0 <= choice_index < len(unique_formats):
                            selected_format = unique_formats[choice_index]
                            if selected_format[3] == 'combined':
                                # For combined streams, use the format ID directly
                                format_choice = selected_format[0]
                            else:
                                # For video-only streams, we need to add audio
                                format_choice = f"{selected_format[0]}+bestaudio/best"
                            print(f"Selected: {selected_format[1]} ({selected_format[2]})")
                            break
                        else:
                            print("Invalid selection. Please try again.")
                    except ValueError:
                        print("Please enter a valid number.")
        # Configure yt-dlp options with selected format
        ydl_opts = {
            'format': format_choice,  # Use selected format
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Output template
            'noplaylist': True,  # Download single video, not playlist
            'progress_hooks': [progress_hook],  # Progress callback
            'quiet': False,  # Show output
            'no_warnings': False,  # Show warnings
        }
        
        # Add merge_output_format only if ffmpeg is installed
        if ffmpeg_installed:
            ydl_opts['merge_output_format'] = 'mp4'
            # Ensure audio is included
            if 'bestvideo' in format_choice and '+bestaudio' not in format_choice:
                ydl_opts['format'] = f"{format_choice}+bestaudio"
            
            # Add metadata postprocessor but NOT audio extraction
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegMetadata',
            }]
        
        # Download the video
        print("\nDownloading...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([cleaned_url])
            
        print("\nDownload completed!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Additional error information
        if "ffmpeg not installed" in str(e) or "ffmpeg" in str(e):
            print("\nThis error occurred because ffmpeg is not installed.")
            show_ffmpeg_instructions()
        elif "HTTP Error 403" in str(e):
            print("This might be due to YouTube's security measures.")
            print("Try these solutions:")
            print("1. Check if the video is available in your region")
            print("2. Try a different video to see if the issue is specific to this one")
            print("3. Wait a while and try again later")
        sys.exit(1)

def check_ffmpeg():
    """Check if ffmpeg is installed and available in PATH"""
    try:
        import subprocess
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        return True
    except (FileNotFoundError, subprocess.SubprocessError):
        return False

def show_ffmpeg_instructions():
    """Show instructions for installing ffmpeg"""
    print("\n=== How to Install FFmpeg ===")
    print("FFmpeg is required for downloading high-resolution videos (720p and above).")
    print("\nWindows Installation Instructions:")
    print("1. Download FFmpeg from https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip")
    print("2. Extract the zip file to a folder (e.g., C:\\ffmpeg)")
    print("3. Add FFmpeg to your PATH:")
    print("   a. Search for 'Environment Variables' in Windows search")
    print("   b. Click 'Edit the system environment variables'")
    print("   c. Click 'Environment Variables' button")
    print("   d. Under 'System variables', find 'Path' and click 'Edit'")
    print("   e. Click 'New' and add the path to the bin folder (e.g., C:\\ffmpeg\\bin)")
    print("   f. Click 'OK' on all dialogs")
    print("4. Restart your command prompt or PowerShell")
    print("5. Run this program again")
    print("\nAlternatively, you can use a package manager like Chocolatey:")
    print("   choco install ffmpeg")

# Progress hook for download
def progress_hook(d):
    if d['status'] == 'downloading':
        # Calculate percentage
        total_bytes = d.get('total_bytes')
        if total_bytes is None:
            total_bytes = d.get('total_bytes_estimate', 0)
        
        if total_bytes > 0:
            downloaded_bytes = d.get('downloaded_bytes', 0)
            percentage = (downloaded_bytes / total_bytes) * 100
            
            # Print progress bar
            bar_length = 30
            filled_length = int(bar_length * downloaded_bytes // total_bytes)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            sys.stdout.write(f"\rProgress: |{bar}| {percentage:.1f}% of {format_size(total_bytes)}")
            sys.stdout.flush()

def format_size(bytes):
    """Format file size in a human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} PB"

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Downloader")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", help="Output directory (optional)")
    
    args = parser.parse_args()
    
    download_video(args.url, args.output)

if __name__ == "__main__":
    main()