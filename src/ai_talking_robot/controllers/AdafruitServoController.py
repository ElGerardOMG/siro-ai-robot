from adafruit_servokit import ServoKit

from ai_talking_robot.controllers.AComponentController import AComponentController

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

class AdafruitServoController(AComponentController):
    """
    Controller used for the PCA9685 when its connected over the Raspberry PI.
    """
    def __init__(self, components : type[ComponentEnum], componentCount = 16):
        super().__init__(self, components)
        
        self._components = components

        self._componentCount = componentCount

        self._kit : ServoKit = None

        self._servos = [None for _ in range (componentCount)]

        self._MOTOR_SWEEP_TIMES = [ 0.800 for _ in range( componentCount ) ]

        self.attemptConnect()

        for component in components:
            self._servos[component.channel] = component.min_value

    # MAYBE can be called again to attempting reconnect the servos. This was not tested, s
    # it may not work at all
    def attemptConnect(self):
        try:
            self._kit = ServoKit(channels=self._componentCount)

            for channel, angle in enumerate(self._servos):
                self._kit.servo[channel].angle = round(angle) if angle is not None else None

            self._onLine = True

        except ValueError as E:
            self._kit = None
            print("Something went wrong when initializing Adafruit servokit...")
            print(E.with_traceback())         

    def setComponentValue(self, component: ComponentEnum, value):
        if value is not None:
            value = max(component.min_value, min(value, component.max_value))
            self._kit.servo[component.channel].angle = round(value)       
            self._servos[component.channel] = value   
        else:
            self._kit.servo[component.channel].angle = None 

    def getComponentValue(self, component: ComponentEnum):
        return self._servos[component.channel]


    def _calculate_movement_time(self, angle_diff: float, motor: int) -> float:
        """
        Calculates the time needed to get to the desired angle.
        """

        st = self._MOTOR_SWEEP_TIMES[motor.value]
        return st * angle_diff / 180
        