import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def get_authenticated_service():
    """
    Authenticate the user and return an authorized YouTube API service object.

    This function checks for existing credentials in a token.pickle file.
    If valid credentials are not found, it initiates the OAuth2 flow to obtain new credentials.

    Returns:
        googleapiclient.discovery.Resource: An authorized YouTube API service object.
    """
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            credentials = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)


def get_playlists(youtube):
    """
    Retrieve all playlists for the authenticated user.

    Args:
        youtube (googleapiclient.discovery.Resource): An authorized YouTube API service object.

    Returns:
        list: A list of playlist resource objects.
    """
    playlists = []
    next_page_token = None

    while True:
        request = youtube.playlists().list(part="snippet", mine=True, maxResults=50, pageToken=next_page_token)
        response = request.execute()

        playlists.extend(response["items"])
        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return playlists


def get_playlist_items(youtube, playlist_id):
    """
    Retrieve all items (videos) from a specific playlist.

    Args:
        youtube (googleapiclient.discovery.Resource): An authorized YouTube API service object.
        playlist_id (str): The ID of the playlist to retrieve items from.

    Returns:
        list: A list of playlist item resource objects.
    """
    items = []
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        response = request.execute()

        items.extend(response["items"])
        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return items


def main():
    """
    Main function to execute the playlist download process.

    This function authenticates the user, retrieves all playlists,
    and then downloads the content of each playlist to a separate text file.
    """
    youtube = get_authenticated_service()
    playlists = get_playlists(youtube)

    for playlist in playlists:
        playlist_id = playlist["id"]
        playlist_title = playlist["snippet"]["title"]
        print(f"Downloading playlist: {playlist_title}")

        items = get_playlist_items(youtube, playlist_id)

        # create a directory to store the downloaded files
        if not os.path.exists("downloaded_playlists"):
            os.makedirs("downloaded_playlists")

        with open(f"downloaded_playlists/{playlist_title}.txt", "w", encoding="utf-8") as f:
            for item in items:
                video_title = item["snippet"]["title"]
                video_id = item["snippet"]["resourceId"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                f.write(f"{video_title}: {video_url}\n")

        # Also write the file in format suitable for youtube-dl
        with open(f"downloaded_playlists/{playlist_title}_ytdl.txt", "w", encoding="utf-8") as f:
            for item in items:
                video_id = item["snippet"]["resourceId"]["videoId"]
                f.write(f"https://www.youtube.com/watch?v={video_id}\n")

        print(f"Saved {len(items)} videos from playlist: {playlist_title}")


if __name__ == "__main__":
    main()
