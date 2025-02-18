import speech_recognition as sr
import datetime
import os

def listen_for_pizza(audio_source, keyword="pizza", log_file="pizza_log.txt"):
    """
    Listens for a specific keyword in audio and logs the timestamp.

    Args:
        audio_source: The audio source to listen to (e.g., microphone).
        keyword: The word to listen for (default: "pizza").
        log_file: The file to log the timestamps to.
    """

    r = sr.Recognizer()

    try:
        print(f"Listening for '{keyword}'...")

        audio = r.listen(audio_source)  # Listen to the audio source

        try:
            recognized_text = r.recognize_google(audio)  # Recognize speech using Google Speech Recognition
            print("You said: " + recognized_text) # Print for verification

            if keyword.lower() in recognized_text.lower():  # Case-insensitive check
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"{timestamp}: '{keyword}' mentioned.\n"

                with open(log_file, "a") as f: # Append to file
                    f.write(log_entry)

                print(f"'{keyword}' detected and logged at {timestamp}")

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    except KeyboardInterrupt:
        print("Listening stopped.")



if __name__ == "__main__":
    # Check if the log file exists, create it if it doesn't
    log_file = "pizza_log.txt"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Pizza Log:\n")  # Add a header

    # Initialize the speech recognizer and microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone... Please be quiet.") # Important for accuracy
        r.adjust_for_ambient_noise(source, duration=2)  # Adjust for ambient noise
        print("Calibration complete.")

        while True:  # Listen continuously
            listen_for_pizza(source, log_file=log_file)