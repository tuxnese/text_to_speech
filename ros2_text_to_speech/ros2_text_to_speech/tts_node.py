
""" Text to Speech for ROS2 """

import os
import signal
import time
import rclpy
from ros2_text_to_speech_interfaces.action import TTS
from ros2_text_to_speech_interfaces.msg import Config

from custom_ros2 import (
    Node,
    ActionSingleServer
)

from .ros2_text_to_speech_tools import (
    EspeakTtsTool,
    SpdSayTtsTool,
    FestivalTtsTool,
    GTtsTtsTool
)


class TtsNode(Node):
    """ TTS Node Class """

    def __init__(self):

        super().__init__('tts_node')

        self.__process = None
        self.__server_cancelled = False

        self.__tools_dict = {
            Config.ESPEAK: EspeakTtsTool(),
            Config.SPD_SAY: SpdSayTtsTool(),
            Config.FESTIVAL: FestivalTtsTool(),
            Config.GTTS: GTtsTtsTool()
        }

        # action server
        self.__action_server = ActionSingleServer(self,
                                                  TTS,
                                                  "tts",
                                                  execute_callback=self.__execute_server,
                                                  cancel_callback=self.__cancel_callback
                                                  )

    def destroy(self):
        """ destroy node method """

        self.__action_server.destroy()
        super().destroy_node()

    def __cancel_callback(self):
        self.__server_cancelled = True
        if self.__process:
            os.killpg(os.getpgid(self.__process.pid), signal.SIGTERM)

    def __execute_server(self, goal_handle):
        """ execute action server

        Args:
            goal_handle: goal_handle
        """

        self.__server_cancelled = False
        request = goal_handle.request
        result = TTS.Result()

        if request.config.tool not in self.__tools_dict:
            goal_handle.abort()
            return result

        self.__process = self.__tools_dict[request.config.tool].say(request)
        self.__process.wait()

        if(not self.__server_cancelled):
            goal_handle.succeed()
        else:
            while not goal_handle.is_cancel_requested:
                time.sleep(1)
            goal_handle.canceled()

        return result


def main(args=None):
    rclpy.init(args=args)

    node = TtsNode()

    node.join_spin()

    node.destroy()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
