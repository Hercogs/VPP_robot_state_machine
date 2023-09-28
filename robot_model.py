
class RobotModel:
    def __init__(self, name):
        print(f'Robot {name } model creating')

        # Set default values
        self.robot_name = name
        self.__line_detected    = False
        self.__at_charger       = False
        self.__rc_asked         = False
        self.__err              = False

    @property
    def line_detected(self):
        return self.__line_detected

    @line_detected.setter
    def line_detected(self, value):
        self.__line_detected = value

    @property
    def at_charger(self):
        return self.__at_charger

    @at_charger.setter
    def at_charger(self, value):
        self.__at_charger = value

    @property
    def rc_asked(self):
        return self.__rc_asked

    @rc_asked.setter
    def rc_asked(self, value):
        self.__rc_asked = value

    @property
    def err(self):
        return self.__err

    @err.setter
    def err(self, value):
        self.__err = value
