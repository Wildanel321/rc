import unittest
from src.input_mapper import InputMapper

class TestInputMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = InputMapper(
            deadzone=0.10,
            invert_throttle=True,
            invert_steering=False,
            max_speed=100,
            acceleration_step=100.0  # instant step for static tests
        )

    def test_deadzone_filtering(self):
        # Within deadzone (< 0.10)
        self.assertEqual(self.mapper.apply_deadzone(0.05), 0.0)
        self.assertEqual(self.mapper.apply_deadzone(-0.08), 0.0)

        # Outside deadzone (1.0)
        self.assertAlmostEqual(self.mapper.apply_deadzone(1.0), 1.0)
        self.assertAlmostEqual(self.mapper.apply_deadzone(-1.0), -1.0)

    def test_differential_drive_forward(self):
        # Raw stick: Y = -1.0 (UP -> Forward), X = 0.0 (CENTER)
        left, right = self.mapper.compute_differential_drive(0.0, -1.0)
        self.assertEqual(left, 100.0)
        self.assertEqual(right, 100.0)

    def test_differential_drive_reverse(self):
        # Raw stick: Y = +1.0 (DOWN -> Reverse), X = 0.0 (CENTER)
        left, right = self.mapper.compute_differential_drive(0.0, 1.0)
        self.assertEqual(left, -100.0)
        self.assertEqual(right, -100.0)

    def test_differential_drive_turning(self):
        # Forward + Steering Right (Y = -1.0, X = 0.3)
        left, right = self.mapper.compute_differential_drive(0.3, -1.0)
        # Left should be higher than Right
        self.assertTrue(left > right)
        self.assertEqual(left, 100.0) # clamped to 100

    def test_max_speed_clamping(self):
        mapper_50 = InputMapper(deadzone=0.10, max_speed=50, acceleration_step=100.0)
        left, right = mapper_50.compute_differential_drive(0.0, -1.0)
        self.assertEqual(left, 50.0)
        self.assertEqual(right, 50.0)

    def test_acceleration_ramp(self):
        mapper_ramp = InputMapper(deadzone=0.0, acceleration_step=20.0)
        # Step from 0 to 100
        l1, r1 = mapper_ramp.update_smooth_acceleration(100.0, 100.0)
        self.assertEqual(l1, 20)
        self.assertEqual(r1, 20)

        l2, r2 = mapper_ramp.update_smooth_acceleration(100.0, 100.0)
        self.assertEqual(l2, 40)
        self.assertEqual(r2, 40)

if __name__ == "__main__":
    unittest.main()
