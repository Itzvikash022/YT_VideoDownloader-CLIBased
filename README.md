I'll create a detailed README.md file for your YouTube downloader application that includes all the necessary information about installation, usage, and configuration.

```markdown:d:\Trae\README.md
# YouTube Video Downloader

A powerful command-line tool for downloading YouTube videos with quality selection options.

## Features

- Download videos from YouTube in various quality options
- Support for high-resolution downloads (720p, 1080p, 4K)
- Interactive quality selection menu
- Progress bar with download status
- Automatic URL cleaning and validation
- Detailed error handling and troubleshooting

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - yt-dlp
  - pytube
- FFmpeg (required for high-resolution downloads)

## Installation

### 1. Clone or download this repository

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

### 2. Install required Python packages

```bash
pip install yt-dlp pytube
```

### 3. Install FFmpeg (required for high-resolution downloads)

#### Windows

1. Download FFmpeg from [https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
2. Extract the zip file to a folder (e.g., C:\ffmpeg)
3. Add FFmpeg to your PATH:
   - Search for 'Environment Variables' in Windows search
   - Click 'Edit the system environment variables'
   - Click 'Environment Variables' button
   - Under 'System variables', find 'Path' and click 'Edit'
   - Click 'New' and add the path to the bin folder (e.g., C:\ffmpeg\bin)
   - Click 'OK' on all dialogs
4. Restart your command prompt or PowerShell

Alternatively, you can use a package manager like Chocolatey:
```bash
choco install ffmpeg
```

#### macOS

Using Homebrew:
```bash
brew install ffmpeg
```

#### Linux

Using apt (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

Using yum (CentOS/RHEL):
```bash
sudo yum install ffmpeg
```

## Usage

### Basic Usage

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Specify Output Directory

```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o "D:\Downloads"
```

### Command-line Arguments

- `url`: YouTube video URL (required)
- `-o, --output`: Output directory (optional, defaults to current directory)

## How It Works

1. The program validates and cleans the provided YouTube URL
2. It checks if FFmpeg is installed (required for high-resolution downloads)
3. It fetches available video formats from YouTube
4. It presents a menu of available quality options
5. After you select a quality, it downloads the video with a progress bar
6. The downloaded video is saved to the specified output directory

## Quality Options

The program offers various quality options depending on what's available for the video:

- Combined streams (video+audio in one file) - typically up to 360p
- Separate streams (requires FFmpeg to merge) - up to the highest resolution available (720p, 1080p, 4K)

If FFmpeg is not installed, only combined streams will be available, limiting the maximum quality.

## Troubleshooting

### No Audio in Downloaded Videos

If your downloaded videos have no audio:
- Make sure FFmpeg is properly installed and available in your PATH
- Try downloading a different video to see if the issue is specific to one video
- Try using the "best" quality option by pressing Enter at the quality selection prompt

### HTTP 403 Forbidden Error

If you encounter a 403 Forbidden error:
- Check if the video is available in your region
- Try a different video to see if the issue is specific to one video
- Wait a while and try again later

### FFmpeg Not Found

If you get an error about FFmpeg not being found:
- Follow the FFmpeg installation instructions in this README
- Make sure to restart your command prompt or PowerShell after installation
- Verify FFmpeg is in your PATH by running `ffmpeg -version` in your terminal

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The core downloading library
- [pytube](https://github.com/pytube/pytube) - Additional YouTube functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
```
