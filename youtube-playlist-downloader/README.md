# YouTube Playlist Downloader

This Python script allows you to download information about playlists created by a YouTube account, including both private and public playlists.
This is useful for backing up your playlists or for analyzing the videos in your playlists.

[![codecov](https://codecov.io/gh/siavashyj/toolbox/branch/main/graph/badge.svg)](https://codecov.io/gh/siavashyj/toolbox)

## Features

- Authenticates with the YouTube API using OAuth 2.0
- Retrieves all playlists (both public and private) from the authenticated account
- Downloads information about all videos in each playlist
- Saves playlist information to individual text files

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- A Google account with access to the YouTube API
- OAuth 2.0 credentials from the Google Developers Console

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-playlist-downloader.git
   cd youtube-playlist-downloader
   ```

2. Install the required dependencies using Poetry:
   ```
   poetry install
   ```

   If you don't have Poetry installed, you can install it from [here](https://python-poetry.org/docs/#installation).

2. (Alternative) If you don't want to use Poetry, you can install the dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

## Setup

1. Go to the [Google Developers Console](https://console.developers.google.com/).
2. Create a new project or select an existing one.
3. Enable the YouTube Data API v3 for your project.
4. Create credentials (OAuth client ID) for a desktop application.
5. Download the client configuration and save it as `client_secrets.json` in the project directory.

## Usage

1. Run the script:
   ```
   poetry run python youtube_playlist_downloader.py
   ```
    or
    ```
    python youtube_playlist_downloader.py
    ```


2. The first time you run the script, it will open a web browser and ask you to authorize the application. Follow the prompts to grant access to your YouTube account.

3. The script will retrieve all your playlists and save the video information for each playlist in separate text files.

## Output

For each playlist, the script creates a text file named after the playlist. Each line in the file contains:

- The title of a video in the playlist
- The URL of the video

Example:
```
My Favorite Song: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Contributing

Contributions to this project are welcome. Please feel free to submit a Pull Request.

## Unit Tests

To run the unit tests, use the following command:
```
poetry run pytest
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This script is for personal use only. Please be aware of YouTube's terms of service and API usage limits when using this script.
