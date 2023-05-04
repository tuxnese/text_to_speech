
from text_to_speech_interfaces.action import TTS
from subprocess import Popen, PIPE, call
from .tts_tool import TtsTool
import os.path

def fileExists(path) :
    return os.path.isfile(path)

models = {
    "it" : {
      "f": "tts_models/it/mai_female/glow-tts",
      "m": "tts_models/it/mai_male/glow-tts"  
    },
    "en" : {
      "f": "tts_models/en/ljspeech/tacotron2-DDC_ph",
      "m": "tts_models/en/ljspeech/tacotron2-DDC"
    }
}

class MozillaTtsTool(TtsTool):

    def say(self, request: TTS.Goal) -> Popen:
        tts_file = "/tmp/" + request.text + ".mp3"
        if not fileExists(tts_file):
            call(
                args=["tts",
                    "--text", "'" + request.text + "'",
                    "--model_name", models[request.config.language][request.config.gender],
                    "--out_path",  tts_file,
                    ],
                stdout=PIPE,
                start_new_session=True)
        return Popen(
            args=["aplay",
                  tts_file
                  ],
            stdout=PIPE,
            start_new_session=True)
