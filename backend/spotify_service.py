# spotify_service.py

import requests
import base64
import time

# 🔐 Add your credentials here OR use environment variables
CLIENT_ID = "592f2b85aabc470db0a0bf61ea263875"
CLIENT_SECRET = "1141f0c1a8384b378c59fdd18ae7859e"

# Token cache
access_token = None
token_expiry = 0


# 🎧 Emotion → Genre Mapping
EMOTION_GENRE_MAP = {
    "Happy": "pop",
    "Sad": "acoustic",
    "Angry": "rock",
    "Relaxed": "chill",
    "Excited": "edm"
}


def get_access_token():
    global access_token, token_expiry

    # Reuse token if still valid
    if access_token and time.time() < token_expiry:
        return access_token

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
        ).decode()
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    access_token = response_data.get("access_token")
    expires_in = response_data.get("expires_in", 3600)

    token_expiry = time.time() + expires_in - 60  # buffer

    return access_token


def get_songs(emotion, limit=5):
    """
    Fetch songs based on detected emotion

    Args:
        emotion (str): Happy/Sad/Angry/Relaxed/Excited
        limit (int): number of songs

    Returns:
        list: song details
    """

    token = get_access_token()

    genre = EMOTION_GENRE_MAP.get(emotion, "pop")

    url = "https://api.spotify.com/v1/search"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "q": genre,
        "type": "track",
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    songs = []

    for item in data.get("tracks", {}).get("items", []):
        song = {
            "title": item["name"],
            "artist": item["artists"][0]["name"],
            "preview_url": item["preview_url"],
            "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None
        }
        songs.append(song)

    return songs


# 🔍 Test
if __name__ == "__main__":
    test_emotion = "Sad"
    results = get_songs(test_emotion)

    for song in results:
        print(song)