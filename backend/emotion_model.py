# emotion_model.py

# -------------------------------
# Import with error handling
# -------------------------------
try:
    from transformers import pipeline
except ImportError:
    raise ImportError(
        "\n❌ Required library 'transformers' is not installed.\n"
        "👉 Install it using:\n"
        "   pip install transformers torch\n"
    )


# -------------------------------
# Load Emotion Model (runs once)
# -------------------------------
try:
    emotion_pipeline = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base"
    )
except Exception as e:
    raise RuntimeError(
        f"\n❌ Failed to load emotion model: {e}\n"
        "👉 Ensure you have internet connection for first-time download.\n"
    )


# -------------------------------
# Emotion Mapping
# -------------------------------
EMOTION_MAP = {
    "joy": "Happy",
    "sadness": "Sad",
    "anger": "Angry",
    "fear": "Sad",
    "surprise": "Excited",
    "neutral": "Relaxed",
    "disgust": "Angry"
}


# -------------------------------
# Main Function
# -------------------------------
def detect_emotion(text: str):
    """
    Detect emotion from user input text

    Args:
        text (str): Input sentence

    Returns:
        dict: {
            "emotion": str,
            "confidence": float
        }
    """

    # Handle empty input
    if not text or not text.strip():
        return {
            "emotion": "Relaxed",
            "confidence": 0.0
        }

    try:
        # Get prediction
        result = emotion_pipeline(text)[0]

        raw_emotion = result['label'].lower()
        confidence = round(result['score'], 3)

        # Map to project emotions
        mapped_emotion = EMOTION_MAP.get(raw_emotion, "Relaxed")

        return {
            "emotion": mapped_emotion,
            "confidence": confidence
        }

    except Exception as e:
        print("⚠️ DEBUG ERROR:", e)
        return {
            "emotion": "Error",
            "confidence": 0.0
        }


# -------------------------------
# Test Block
# -------------------------------
if __name__ == "__main__":
    print("🔍 Testing Emotion Model...\n")

    test_inputs = [
        "I am very happy today!",
        "I feel lonely and sad",
        "I am so angry right now",
        "I feel calm and relaxed"
    ]

    for text in test_inputs:
        result = detect_emotion(text)
        print(f"Input: {text}")
        print(f"Output: {result}\n")