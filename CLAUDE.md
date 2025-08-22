# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a toolbox repository containing Python utilities. The main project is `youtube-playlist-downloader`, a YouTube API client for backing up playlist information.

## Common Development Commands

### Python Environment Setup
```bash
cd youtube-playlist-downloader
poetry install
```

### Running the Application
```bash
# Using Poetry (recommended)
poetry run python main.py

# Or with pip-installed dependencies
python main.py
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=main
```

### Code Quality
```bash
# Format code
poetry run black main.py tests/

# Sort imports
poetry run isort main.py tests/

# Lint code
poetry run flake8 main.py tests/
```

## Architecture

### YouTube Playlist Downloader (`youtube-playlist-downloader/`)

**Core Components:**
- `main.py` - Primary module with YouTube API integration
- `get_authenticated_service()` - OAuth2 authentication using Google APIs
- `get_playlists()` - Retrieves user's playlists (including private, liked videos, watch later)
- `get_playlist_items()` - Fetches all videos from a specific playlist
- `main()` - Orchestrates the download process

**Authentication Flow:**
- Uses OAuth2 with `client_secrets.json` (not committed)
- Stores credentials in `token.pickle` for reuse
- Requires YouTube Data API v3 scope: `youtube.readonly`

**Output Format:**
- Creates `downloaded_playlists/` directory
- Two files per playlist: 
  - `{playlist_name}.txt` - Human-readable format with titles and URLs
  - `{playlist_name}_ytdl.txt` - YouTube-dl compatible URL list

**Dependencies:**
- Primary: `google-api-python-client`, `google-auth-oauthlib`
- Dev: `pytest`, `black`, `isort`, `flake8`, `pytest-cov`

## Configuration

- Black formatter: 120 character line length, Python 3.8+ target
- isort: Black-compatible profile
- pytest: Tests in `tests/` directory
- Poetry: Primary dependency manager, pip fallback via `requirements.txt`

## Testing Strategy

Unit tests mock Google API responses and file operations. Test coverage includes:
- Authentication service initialization
- Playlist retrieval with various options
- Playlist item fetching
- Main function integration
- Parameterized tests for different playlist inclusion options