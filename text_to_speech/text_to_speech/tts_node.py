
""" Text to Speech for ROS2 """

import os
import time
import signal
import rclpy
from text_to_speech_interfaces.action import TTS
from text_to_speech_interfaces.msg import Config

from rclpy.node import Node
from rclpy.action import ActionServer


from .text_to_speech_tools import (
    ESpeakTtsTool,
    SpdSayTtsTool,
    FestivalTtsTool,
    GTtsTtsTool,
    MozillaTtsTool
)


class TtsNode(Node):
    """ TTS Node Class """

    def __init__(self):

        super().__init__("tts_node")

        self.__process = None
        self.__cancelled = False

        self.__tools_dict = {
            Config.ESPEAK: ESpeakTtsTool(),
            Config.SPD_SAY: SpdSayTtsTool(),
            Config.FESTIVAL: FestivalTtsTool(),
            Config.GTTS: GTtsTtsTool(),
            Config.MOZILLA: MozillaTtsTool()
        }

        # action server
        self.__action_server = ActionServer(self, TTS,
                                                         "tts",
                                                         execute_callback=self.__execute_server,
                                                         cancel_callback=self.__cancel_callback
                                                         )

    def __cancel_callback(self):
        self.__cancelled = True
        if self.__process:
            while self.__process == "started":
                time.sleep(0.05)

            os.killpg(os.getpgid(self.__process.pid), signal.SIGTERM)

    def __execute_server(self, goal_handle) -> TTS.Result:
        """ execute action server

        Args:
            goal_handle: goal_handle

        Returns:
            TTS.Result: tts result
        """

        self.__process = "started"

        request = goal_handle.request
        result = TTS.Result()

        if request.config.tool not in self.__tools_dict:
            goal_handle.abort()
            return result

        self.__process = self.__tools_dict[request.config.tool].say(request)
        self.__process.wait()

        if self.__cancelled:
            goal_handle.canceled()

        else:
            goal_handle.succeed()

        return result


def main(args=None):
    rclpy.init(args=args)

    node = TtsNode()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
