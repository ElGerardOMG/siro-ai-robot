import unittest
import threading
from ai_talking_robot.sequencer.DefaultMoveSequencer import DefaultMoveSequencer
from ai_talking_robot.controllers.MockController import MockController
from ai_talking_robot.controllers.AudioPlayerController import AudioPlayerController

from .SampleTestAnimationSuite import *


import time

class TestComponents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        controller = MockController(SampleComponents)

    def setUp(self):
        self.sequencer = DefaultMoveSequencer()

    def execute_task_with_max_time(self, max_time, func, args):
        finishtime = None

        def cancel_with_timeout():
            nonlocal finishtime
            start = time.time()
            if args is not None:
                func(*args)
            else:
                func()
            finishtime = time.time() - start

        cancel_thread = threading.Thread(target=cancel_with_timeout)
        cancel_thread.start()
        cancel_thread.join(timeout=max_time)
        
        if cancel_thread.is_alive():
            return None

        return finishtime

    def test_final_component_values_are_correct(self):
        self.sequencer.executeSequence(ANIMACION_1)

        # Get current component values and expected (from last step of ANIMACION_1)
        component_values = [x.currentValue for x in SampleComponents]
        # The order in ANIMACION_1[-1]["components"].items() may not match enumeration order,
        # so use per-component matching to avoid ordering bugs:
        expected_dict = {
            SampleComponents.COMPONENTE_A: 45, 
            SampleComponents.COMPONENTE_B: 90, 
            SampleComponents.COMPONENTE_C: 10, 
            SampleComponents.COMPONENTE_D: 45
            }
        expected_values = [expected_dict.get(x, x.min_value) for x in SampleComponents]

        self.assertListEqual(component_values, expected_values)

    def test_components_dont_surpass_max_values(self):
        self.sequencer.executeSequence([ANIMACION_3[0]])

        component_values = [x.currentValue for x in SampleComponents]
        maximum_values = [x.max_value for x in SampleComponents]

        # Check that no component value exceeds its maximum
        for value, maximum in zip(component_values, maximum_values):
            self.assertLessEqual(value, maximum, f"Component value {value} exceeds maximum {maximum}")

    def test_components_dont_surpass_min_values(self):
        self.sequencer.executeSequence([ANIMACION_3[1]])

        component_values = [x.currentValue for x in SampleComponents]
        minimum_values = [x.min_value for x in SampleComponents]

        # Check that no component value goes below its minimum
        for value, minimum in zip(component_values, minimum_values):
            self.assertGreaterEqual(value, minimum, f"Component value {value} is less than minimum {minimum}")

    def test_executing_sequence_can_be_cancelled(self):
        self.sequencer.valueUpdateInterval = 0.1

        execution = threading.Thread(target=self.sequencer.executeSequence, args=(ANIMACION_2,), daemon=True)
        execution.start()

        time.sleep(0.1)

        max_time = 0.5

        elapsed_time = self.execute_task_with_max_time(max_time, self.sequencer.cancelExecution, None)

        if elapsed_time is None:
            self.fail(f"cancelExecution blocked for more than {max_time} seconds")
        else:
            self.assertLessEqual(elapsed_time, max_time, f"cancelExecution took too long: {elapsed_time:.3f}s > {max_time}s")
       

    def test_executing_sequence_after_cancelling_previous(self):
        self.sequencer.valueUpdateInterval = 0.1
        max_cancel_time = 0.5
        max_exec_time = 5.0

        execution = threading.Thread(target=self.sequencer.executeSequence, args=(ANIMACION_2,), daemon=True)
        execution.start()

        time.sleep(0.1)

        elapsed_time = self.execute_task_with_max_time(max_cancel_time, self.sequencer.cancelExecution, None)

        if elapsed_time is None:
            self.fail(f"cancelExecution blocked for more than {max_cancel_time} seconds")
        else:
            self.assertLessEqual(elapsed_time, max_cancel_time, f"cancelExecution took too long: {elapsed_time:.3f}s > {max_cancel_time}s")

        elapsed_time = self.execute_task_with_max_time(max_exec_time, self.sequencer.executeSequence, (ANIMACION_1,))

        if elapsed_time is None:
            self.fail(f"executeSequence blocked for more than {max_exec_time} seconds")
        else:
            self.assertLessEqual(elapsed_time, max_exec_time, f"executeSequence took too long: {elapsed_time:.3f}s > {max_exec_time}s")


    def test_cancelling_non_executing_sequence_dont_block(self):
        max_time = 3.0
        # No sequence is running here

        elapsed_time = self.execute_task_with_max_time(max_time, self.sequencer.cancelExecution, None)

        if elapsed_time is None:
            self.fail(f"cancelExecution blocked for more than {max_time} seconds")
        else:
            self.assertLessEqual(elapsed_time, max_time, f"cancelExecution took too long: {elapsed_time:.3f}s > {max_time}s")

    def test_can_execute_sequence_after_attempting_cancelling_non_existent(self):
        max_cancel_time = 3.0
        max_exec_time = 5.0


        elapsed_time = self.execute_task_with_max_time(max_cancel_time, self.sequencer.cancelExecution, None)

        if elapsed_time is None:
            self.fail(f"cancelExecution blocked for more than {max_cancel_time} seconds")
        else:
            self.assertLessEqual(elapsed_time, max_cancel_time, f"cancelExecution took too long: {elapsed_time:.3f}s > {max_cancel_time}s")

        elapsed_time = self.execute_task_with_max_time(max_exec_time, self.sequencer.executeSequence, (ANIMACION_1,))

        if elapsed_time is None:
            self.fail(f"executeSequence blocked for more than {max_exec_time} seconds")
        else:
            self.assertLessEqual(elapsed_time, max_exec_time, f"executeSequence took too long: {elapsed_time:.3f}s > {max_exec_time}s")

if __name__ == '__main__':
    unittest.main()