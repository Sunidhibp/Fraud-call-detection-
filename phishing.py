#Fraud call detection through intelligent speech recognition
import speech_recognition as sr
import re

def identify_speech():
    # Create a recognizer object
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust ambient noise for better recognition
        recognizer.adjust_for_ambient_noise(source)

        # Listen for speech and convert it to text
        audio = recognizer.listen(source)

        try:
            # Use Google Speech Recognition to convert audio to text
            text = recognizer.recognize_google(audio)
            print("Recognized speech:", text)

            # Check for the specific phrase "Please share"
            if "please share" in text.lower():
                print("Warning: The person is asking for your sensitive information. \n This may be a phishing call. Do you trust this call?")
            else:
                print("No sensitive information detected.")

            # Check sensitive information using string matching
            if check_speech(text):
                print("Warning: This may be a phishing call.")

            # Check sensitive information using regular expressions
            if identify_sensitive_info(text):
                print("Warning: This may be a phishing call (using regex). Do you trust this call?")

            # Ask the user to input their response
            trust_call = input("Do you trust this call? (y/n): ")

            # Check the user's response
            if trust_call.lower() == "y":
                print("You trust this call.")
            elif trust_call.lower() == "n":
                print("You do not trust this call. Taking actions...")

                # Implement actions here (e.g., hang up, block number, log activity)
                # For demonstration purposes, we'll print a message.
                print("Call terminated. Number blocked. Activity logged.")
            else:
                print("Invalid input. Please enter 'yes' or 'no.'")

        except sr.UnknownValueError:
            print("Unable to recognize speech.")
        except sr.RequestError as e:
            print("Error:", str(e))

def check_speech(speech):
    # Convert the speech to lowercase for case-insensitive matching
    speech = speech.lower()

    # Define the words to check for
    words_to_check = ['share otp', 'cvv', 'passwords']

    # Check if any of the words are present in the speech
    for word in words_to_check:
        if word in speech:
            return True

    return False

def identify_sensitive_info(transcript):
    # Create a regular expression pattern to match sensitive information
    regex_pattern = r"(share\s?otp|cvv|passwords)"

    # Search for the pattern in the transcript
    match = re.search(regex_pattern, transcript, re.IGNORECASE)

    # Return True if sensitive information is found, False otherwise
    return bool(match)

# Call the function to identify speech
identify_speech()

