from unittest.mock import Mock, mock_open, patch

import pytest
from googleapiclient.discovery import Resource

from main import get_authenticated_service, get_playlist_items, get_playlists, main


@pytest.fixture
def mock_youtube_service():
    mock_service = Mock(spec=Resource)
    mock_playlists = Mock()
    mock_playlists.list.return_value.execute.return_value = {
        "items": [{"id": "playlist1", "snippet": {"title": "Test Playlist"}}],
        "nextPageToken": None,
    }

    mock_service.playlists = Mock()
    mock_service.playlists.return_value = mock_playlists

    mock_playlist_items = Mock()
    mock_playlist_items.list.return_value.execute.return_value = {
        "items": [{"snippet": {"title": "Test Video", "resourceId": {"videoId": "video1"}}}],
        "nextPageToken": None,
    }
    mock_service.playlistItems = Mock()
    mock_service.playlistItems.return_value = mock_playlist_items

    return mock_service


def test_get_authenticated_service():
    with (
        patch("main.build") as mock_build,
        patch("main.InstalledAppFlow.from_client_secrets_file") as mock_flow,
        patch("builtins.open", new_callable=mock_open) as _,
        patch("pickle.dump") as _,
        patch("pickle.load") as mock_load,
        patch("os.path.exists", return_value=False),
    ):

        mock_credentials = Mock()
        mock_flow.return_value.run_local_server.return_value = mock_credentials
        mock_build.return_value = Mock(spec=Resource)
        mock_load.return_value = mock_credentials

        result = get_authenticated_service()

        assert isinstance(result, Mock)
        mock_build.assert_called_once_with("youtube", "v3", credentials=mock_credentials)


def test_get_playlists(mock_youtube_service):
    result = get_playlists(mock_youtube_service)

    assert len(result) == 3
    assert result[0]["id"] == "playlist1"
    assert result[0]["snippet"]["title"] == "Test Playlist"


def test_get_playlists_without_defaults(mock_youtube_service):
    result = get_playlists(mock_youtube_service, get_liked=False, get_watch_list=False)

    assert len(result) == 1
    assert result[0]["id"] == "playlist1"
    assert result[0]["snippet"]["title"] == "Test Playlist"


def test_get_playlist_items(mock_youtube_service):
    result = get_playlist_items(mock_youtube_service, "playlist1")

    assert len(result) == 1
    assert result[0]["snippet"]["title"] == "Test Video"
    assert result[0]["snippet"]["resourceId"]["videoId"] == "video1"


@patch("main.get_authenticated_service")
@patch("main.get_playlists")
@patch("main.get_playlist_items")
@patch("builtins.open", new_callable=mock_open)
@patch("os.path.exists", return_value=False)
@patch("os.makedirs")
def test_main(
    mock_makedirs,
    mock_exists,
    mock_file,
    mock_get_playlist_items,
    mock_get_playlists,
    mock_get_authenticated_service,
):
    mock_youtube = Mock(spec=Resource)
    mock_get_authenticated_service.return_value = mock_youtube
    mock_get_playlists.return_value = [{"id": "playlist1", "snippet": {"title": "Test Playlist"}}]
    mock_get_playlist_items.return_value = [{"snippet": {"title": "Test Video", "resourceId": {"videoId": "video1"}}}]

    main()

    assert mock_file.call_count == 2  # Two files are created per playlist
    mock_file().write.assert_any_call("Test Video: https://www.youtube.com/watch?v=video1\n")
    mock_file().write.assert_any_call("https://www.youtube.com/watch?v=video1\n")


@pytest.mark.parametrize(
    "get_liked,get_watch_list,expected_calls",
    [(True, True, 3), (True, False, 2), (False, True, 2), (False, False, 1)],
)
def test_get_playlists_with_options(mock_youtube_service, get_liked, get_watch_list, expected_calls):
    result = get_playlists(mock_youtube_service, get_liked=get_liked, get_watch_list=get_watch_list)

    assert mock_youtube_service.playlists.return_value.list.call_count == expected_calls
    assert len(result) == expected_calls
