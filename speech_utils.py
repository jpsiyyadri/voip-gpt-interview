import os

import azure.cognitiveservices.speech as speechsdk

# Set up subscription key and region from environment variables
speech_key = os.environ.get("SUBSCRIPTION_KEY", "")
service_region = os.environ.get("REGION", "")


# Dropdown for voice selection
voice_mapping = {
    "JennyMultilingualNeural": "Microsoft Server Speech Text to Speech Voice (en-US, JennyMultilingualNeural)",
    "JennyMultilingualV2Neural": "Microsoft Server Speech Text to Speech Voice (en-US, JennyMultilingualV2Neural)",
    "RyanMultilingualNeural": "Microsoft Server Speech Text to Speech Voice (en-US, RyanMultilingualNeural)",
    "JennyNeural": "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)",
    "GuyNeural": "Microsoft Server Speech Text to Speech Voice (en-US, GuyNeural)",
    "AriaNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AriaNeural)",
    "DavisNeural": "Microsoft Server Speech Text to Speech Voice (en-US, DavisNeural)",
    "AmberNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AmberNeural)",
    "AnaNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AnaNeural)",
    "AndrewNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AndrewNeural)",
    "AshleyNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AshleyNeural)",
    "BrandonNeural": "Microsoft Server Speech Text to Speech Voice (en-US, BrandonNeural)",
    "BrianNeural": "Microsoft Server Speech Text to Speech Voice (en-US, BrianNeural)",
    "ChristopherNeural": "Microsoft Server Speech Text to Speech Voice (en-US, ChristopherNeural)",
    "CoraNeural": "Microsoft Server Speech Text to Speech Voice (en-US, CoraNeural)",
    "ElizabethNeural": "Microsoft Server Speech Text to Speech Voice (en-US, ElizabethNeural)",
    "EmmaNeural": "Microsoft Server Speech Text to Speech Voice (en-US, EmmaNeural)",
    "EricNeural": "Microsoft Server Speech Text to Speech Voice (en-US, EricNeural)",
    "JacobNeural": "Microsoft Server Speech Text to Speech Voice (en-US, JacobNeural)",
    "JaneNeural": "Microsoft Server Speech Text to Speech Voice (en-US, JaneNeural)",
    "JasonNeural": "Microsoft Server Speech Text to Speech Voice (en-US, JasonNeural)",
    "MichelleNeural": "Microsoft Server Speech Text to Speech Voice (en-US, MichelleNeural)",
    "MonicaNeural": "Microsoft Server Speech Text to Speech Voice (en-US, MonicaNeural)",
    "NancyNeural": "Microsoft Server Speech Text to Speech Voice (en-US, NancyNeural)",
    "RogerNeural": "Microsoft Server Speech Text to Speech Voice (en-US, RogerNeural)",
    "SaraNeural": "Microsoft Server Speech Text to Speech Voice (en-US, SaraNeural)",
    "SteffanNeural": "Microsoft Server Speech Text to Speech Voice (en-US, SteffanNeural)",
    "TonyNeural": "Microsoft Server Speech Text to Speech Voice (en-US, TonyNeural)",
    "AIGenerate1Neural": "Microsoft Server Speech Text to Speech Voice (en-US, AIGenerate1Neural)",
    "AIGenerate2Neural": "Microsoft Server Speech Text to Speech Voice (en-US, AIGenerate2Neural)",
    "AndrewMultilingualNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AndrewMultilingualNeural)",
    "AvaMultilingualNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AvaMultilingualNeural)",
    "AvaNeural": "Microsoft Server Speech Text to Speech Voice (en-US, AvaNeural)",
    "BlueNeural": "Microsoft Server Speech Text to Speech Voice (en-US, BlueNeural)",
    "BrianMultilingualNeural": "Microsoft Server Speech Text to Speech Voice (en-US, BrianMultilingualNeural)",
    "EmmaMultilingualNeural": "Microsoft Server Speech Text to Speech Voice (en-US, EmmaMultilingualNeural)",
    "ShrutiNeural": "Microsoft Server Speech Text to Speech Voice (te-IN, ShrutiNeural)",
    "MohanNeural": "Microsoft Server Speech Text to Speech Voice (te-IN, MohanNeural)",
}


# Function to perform speech synthesis
def speech_synthesis_to_wave_file(text, simplified_voice):
    full_voice_name = voice_mapping[simplified_voice]
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_synthesis_voice_name = full_voice_name

    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config
    )

    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return file_name
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(
            f"Speech synthesis canceled: {cancellation_details.reason}\n"
            f"Error details: {cancellation_details.error_details}\n"
            f"Did you update the subscription info?"
        )
        return None


def wave_file_to_text(file_name):
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )

    audio_config = speechsdk.audio.AudioConfig(filename=file_name)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(
            f"Speech Recognition canceled: {cancellation_details.reason}\n"
            f"Error details: {cancellation_details.error_details}\n"
            f"Did you update the subscription info?"
        )
        return None


if __name__ == "__main__":
    # Test the function
    speech_synthesis_to_wave_file("Hello, world!", "JennyMultilingualNeural")
