from text_to_speech_interfaces.action import TTS
from subprocess import Popen, PIPE
from .tts_tool import TtsTool
from .utilities import getFilePathAndCreateFolders, fileExists
from google.cloud import texttospeech

languages = {
 "it" : "it-IT",
 "en" : "en-GB",
 "fr" : "fr-FR",
}

models = {
    "it" : {
      "f": "it-IT-Wavenet-A",
      "m": "it-IT-Wavenet-C"  
    },
    "en" : {
      "f": "en-GB-Wavenet-A",
      "m": "en-GB-Wavenet-B"  
    },
    "fr" : {
      "f": "fr-FR-Wavenet-E",
      "m": "fr-FR-Wavenet-B"  
    },
}

try:
    client = texttospeech.TextToSpeechClient()
except:
    client = None

def saveGoogleTSS(request, file_path):
    if not client:
        return

    # Instantiates a client

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=languages[request.config.language], name=models[request.config.language][request.config.gender]
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=request.config.rate / 100.0
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(file_path, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)        

class GTtsTtsTool(TtsTool):

    def say(self, request: TTS.Goal) -> Popen:

        slow = False
        tts_file = None

        if len(request.text) < 100:
            tts_file = getFilePathAndCreateFolders("google_tts", request, "mp3")
            print(tts_file)
       
        
        if not tts_file:
            request_text = request.text
            request.text = "too_long_file_name"
            tts_file = getFilePathAndCreateFolders("google_tts", request, "mp3")
            request.text = request_text
            saveGoogleTSS(request, tts_file)
        elif not fileExists(tts_file):
            saveGoogleTSS(request, tts_file)

        return Popen(
            args=["mpg321",
                  "--stereo",
                  "-g", str(request.config.volume * 100),
                  tts_file
                  ],
            stdout=PIPE,
            start_new_session=True)
