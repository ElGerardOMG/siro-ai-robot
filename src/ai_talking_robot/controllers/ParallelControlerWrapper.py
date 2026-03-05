import queue
import threading

from ai_talking_robot.controllers.AComponentController import AComponentController

from ai_talking_robot.sequencer.ComponentEnum import ComponentEnum

#TODO: Maybe coding a way to try to make the controller online again. However, this may casue
# the need to code every controller with an option to "Reconnect"""

class ParallelControllerWrapper(AComponentController):
    """
    This controller wraps another controller. Calls to this controller's setComponentValue() 
    will call the wrapped controller's setComponentValue() in a separate thread. This can 
    be used when setting a component value can block the current thread (Ej: When disconnecting 
    a driver physically so the program starts waiting for reconnection). If the thread fails to
    set the value of the component or it cannot set a value before it reaches max_time_out, then
    subsequent calls to this controller's setComponentValue() will be ignored.
    """
    def __init__(self, controller : AComponentController, max_time_out : float = 2.0):
        self._controler = controller

        self._onLine = True

        self._command_queue: queue.Queue = queue.Queue()
        self._response_queue: queue.Queue = queue.Queue()
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()
        self._max_time_out = max_time_out
        pass


    def _worker_loop(self):
        while True:
            component, value = self._command_queue.get()
            try: 
                self._controler.setComponentValue(component, value)
                self._response_queue.put(True)
            except Exception:
                self._response_queue.put(False)

    def setComponentValue(self, component: ComponentEnum, value):
        if not self._onLine:
            return

        self._command_queue.put((component, value))
        
        try:
            ok = self._response_queue.get(timeout=2.0)
        except queue.Empty:
            self._onLine = False
            return

        if not ok:
            self._onLine = False
            
    def getComponentValue(self, component: ComponentEnum):
        return self._controler.getComponentValue(component)
        
    