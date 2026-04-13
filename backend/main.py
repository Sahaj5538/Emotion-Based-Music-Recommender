# main.py

from emotion_model import detect_emotion
from spotify_service import get_songs


def recommend_music(text):
    """
    Main function that connects emotion detection + music recommendation
    """

    # Step 1: Detect emotion
    emotion_result = detect_emotion(text)
    emotion = emotion_result["emotion"]
    confidence = emotion_result["confidence"]

    # Step 2: Get songs from Spotify
    songs = get_songs(emotion)

    # Step 3: Final output
    result = {
        "input_text": text,
        "emotion": emotion,
        "confidence": confidence,
        "songs": songs
    }

    return result


# 🔍 Run from terminal
if __name__ == "__main__":
    print("🎵 Emotion-Based Music Recommender")
    print("----------------------------------")

    user_input = input("Enter how you feel: ")

    output = recommend_music(user_input)

    print("\n🧠 Detected Emotion:", output["emotion"])
    print("📊 Confidence:", output["confidence"])

    print("\n🎶 Recommended Songs:\n")

    for i, song in enumerate(output["songs"], start=1):
        print(f"{i}. {song['title']} - {song['artist']}")
        print(f"   Preview: {song['preview_url']}")
        print(f"   Image: {song['image']}")
        print()