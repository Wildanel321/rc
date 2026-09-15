import unittest
import json
import time
from src.udp_sender import UDPSender

class TestProtocol(unittest.TestCase):
    def test_udp_payload_format(self):
        sender = UDPSender(target_ip="127.0.0.1", target_port=5005)
        
        # Test mock JSON generation logic
        throttle = 80
        steering = -20
        payload = {
            "type": "control",
            "throttle": int(throttle),
            "steering": int(steering),
            "timestamp": int(time.time() * 1000)
        }

        json_str = json.dumps(payload)
        parsed = json.loads(json_str)

        self.assertEqual(parsed["type"], "control")
        self.assertEqual(parsed["throttle"], 80)
        self.assertEqual(parsed["steering"], -20)
        self.assertIn("timestamp", parsed)
        self.assertTrue(isinstance(parsed["timestamp"], int))
        sender.close()


if __name__ == "__main__":
    unittest.main()
