import speech_recognition as sr
import datetime
import os
import time

def listen_for_pizza(audio_source, keyword="pizza", log_file="pizza_log.txt", timeout=3):  # Added timeout
    """Listens with a timeout and handles KeyboardInterrupt."""

    r = sr.Recognizer()

    try:
        print(f"Listening for '{keyword}' (timeout {timeout} seconds)...")

        try:
            audio = r.listen(audio_source, timeout=timeout)  # Listen with timeout

            try:
                recognized_text = r.recognize_google(audio)
                print("You said: " + recognized_text)

                if keyword.lower() in recognized_text.lower():
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"{timestamp}: '{keyword}' mentioned.\n"

                    with open(log_file, "a") as f:
                        f.write(log_entry)

                    print(f"'{keyword}' detected and logged at {timestamp}")

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

        except sr.WaitTimeoutError:  # Timeout occurred
            print("Timeout. Listening again...")
            pass # Continue the loop to listen again
        except KeyboardInterrupt:
            print("Listening stopped.")
            return  # Exit the function to break the loop

    except KeyboardInterrupt: # Handle ctrl+c even before the timeout
        print("Listening stopped.")
        return # Exit the function to break the loop



if __name__ == "__main__":
    log_file = "pizza_log.txt"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Pizza Log:\n")

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone... Please be quiet.")
        r.adjust_for_ambient_noise(source, duration=2)
        print("Calibration complete.")

        while True:
            listen_for_pizza(source, log_file=log_file)
            time.sleep(0.1)  # Small delay to reduce CPU usage (optional)