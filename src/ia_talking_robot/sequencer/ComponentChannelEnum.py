from enum import Enum

class ComponentChannelEnum(Enum):

    #NAME = Channel, (MIN, MAX)
    def value(self):
        return self._value_[0]

    def MIN(self):
        return self._value_[1][0]

    def MAX(self):
        return self._value_[1][1]
