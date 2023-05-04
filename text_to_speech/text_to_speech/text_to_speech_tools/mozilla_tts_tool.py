
from text_to_speech_interfaces.action import TTS
from subprocess import Popen, PIPE, call
from .tts_tool import TtsTool

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

gtts_file = "/tmp/gtts_tmp_file.mp3"


class MozillaTtsTool(TtsTool):

    def say(self, request: TTS.Goal) -> Popen:
        call(
            args=["tts",
                  "--text", "'" + request.text + "'",
                  "--model_name", models[request.config.language][request.config.gender],
                  "--out_path",  gtts_file,
                  ],
            stdout=PIPE,
            start_new_session=True)
        return Popen(
            args=["aplay",
                  gtts_file
                  ],
            stdout=PIPE,
            start_new_session=True)
