import queue
import threading

from adafruit_servokit import ServoKit

from ai_talking_robot.controllers.AComponentController import AComponentController

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

class AdafruitServoController(AComponentController):
    
    def __init__(self, components : type[ComponentEnum], componentCount = 16):
        self._components = components

        self._componentCount = componentCount

        self._kit : ServoKit = None

        self._servos = [None for _ in range (componentCount)]

        self._MOTOR_SWEEP_TIMES = [ 0.800 for _ in range( componentCount ) ]

        self._onLine = False

        self._command_queue: queue.Queue = queue.Queue()
        self._response_queue: queue.Queue = queue.Queue()
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

        self.attemptConnect()

        for component in components:
            self._servos[component.channel] = component.min_value
            component.initialize(self)

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


    def _worker_loop(self):
        while True:
            channel, value = self._command_queue.get()
            try: 
                self._kit.servo[channel].angle = round(value) if value is not None else None
                self._response_queue.put(True)
            except Exception:
                self._response_queue.put(False)

    def _write_via_worker(self, channel: int, value):
        if not self._onLine:
            return

        self._command_queue.put((channel, value))
        
        try:
            ok = self._response_queue.get(timeout=2.0)
            self._servos[channel] = value
        except queue.Empty:
            self._onLine = False
            return
        if not ok:
            self._onLine = False
            

    def setComponentValue(self, component: ComponentEnum, value):
        if value is not None:
            value = max(component.min_value, min(value, component.max_value))
            self._write_via_worker(component.channel, round(value))
        else:
            self._write_via_worker(component.channel, None)

    def setComponentValue(self, componentChannel: int, value):
        if value is not None:
            self._write_via_worker(componentChannel, round(value))
        else:
            self._write_via_worker(componentChannel, None)

    def getComponentValue(self, component: ComponentEnum):
        return self.components[component.channel]

    def getComponentValue(self, componentChannel : int):
        return self.components[componentChannel]


    def _calculate_movement_time(self, angle_diff: float, motor: int) -> float:
        """
        Calculates the time needed to get to the desired angle.
        """

        st = self._MOTOR_SWEEP_TIMES[motor.value]
        return st * angle_diff / 180
        