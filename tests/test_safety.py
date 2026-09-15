import unittest
from src.safety import SafetyController, SafetyState

class TestSafety(unittest.TestCase):
    def setUp(self):
        self.safety = SafetyController()

    def test_initial_armed_state(self):
        self.assertEqual(self.safety.state, SafetyState.ARMED)
        self.assertTrue(self.safety.is_safe())

    def test_manual_emergency_stop(self):
        self.safety.trigger_emergency_stop("Button Pressed")
        self.assertEqual(self.safety.state, SafetyState.EMERGENCY_STOP)
        self.assertFalse(self.safety.is_safe())

    def test_gamepad_disconnect(self):
        self.safety.on_gamepad_disconnect()
        self.assertEqual(self.safety.state, SafetyState.GAMEPAD_DISCONNECTED)
        self.assertFalse(self.safety.is_safe())

    def test_reset_emergency_stop(self):
        self.safety.trigger_emergency_stop("Button Pressed")
        self.assertFalse(self.safety.is_safe())
        
        self.safety.reset_emergency_stop()
        self.assertEqual(self.safety.state, SafetyState.ARMED)
        self.assertTrue(self.safety.is_safe())

if __name__ == "__main__":
    unittest.main()
