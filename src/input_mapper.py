class InputMapper:
    def __init__(
        self,
        deadzone: float = 0.10,
        invert_throttle: bool = True,
        invert_steering: bool = False,
        max_speed: int = 100,
        acceleration_step: float = 10.0
    ):
        self.deadzone = deadzone
        self.invert_throttle = invert_throttle
        self.invert_steering = invert_steering
        self.max_speed = max_speed
        self.acceleration_step = acceleration_step

        # Internal state for smooth acceleration (ramping)
        self.current_left_motor = 0.0
        self.current_right_motor = 0.0

    def apply_deadzone(self, value: float) -> float:
        """Applies deadzone threshold and re-scales remaining range to 0.0 .. 1.0"""
        abs_val = abs(value)
        if abs_val < self.deadzone:
            return 0.0
        # Re-scale linearly so 0 threshold maps to 0.0 and 1.0 maps to 1.0
        scaled = (abs_val - self.deadzone) / (1.0 - self.deadzone)
        scaled = min(1.0, max(0.0, scaled))
        return scaled if value > 0 else -scaled

    def compute_differential_drive(self, raw_x: float, raw_y: float) -> tuple[float, float]:
        """
        Calculates raw throttle and steering, applies inversions, deadzone,
        and computes differential tank drive output [-100 .. +100].
        
        raw_x: Left Stick X (-1.0 to 1.0)
        raw_y: Left Stick Y (-1.0 to 1.0, negative is usually UP in evdev)
        """
        # Apply deadzone to raw stick inputs
        x_filtered = self.apply_deadzone(raw_x)
        y_filtered = self.apply_deadzone(raw_y)

        # Standard conversion:
        # Stick Up (raw_y negative) => Positive Throttle (Forward)
        # Stick Down (raw_y positive) => Negative Throttle (Reverse)
        throttle = -y_filtered if self.invert_throttle else y_filtered
        steering = x_filtered if not self.invert_steering else -x_filtered

        # Scale to -100 .. +100 range
        throttle_pct = throttle * 100.0
        steering_pct = steering * 100.0

        # Differential Drive math:
        # left = throttle + steering
        # right = throttle - steering
        left_motor = throttle_pct + steering_pct
        right_motor = throttle_pct - steering_pct

        # Clamp output to [-100 .. +100]
        left_motor = max(-100.0, min(100.0, left_motor))
        right_motor = max(-100.0, min(100.0, right_motor))

        # Apply max speed limit
        speed_factor = self.max_speed / 100.0
        left_motor *= speed_factor
        right_motor *= speed_factor

        return left_motor, right_motor

    def update_smooth_acceleration(self, target_left: float, target_right: float) -> tuple[int, int]:
        """
        Ramps motor speed gradually towards targets using acceleration_step.
        Returns final integer values for left and right motor [-100 .. 100].
        """
        # Ramp Left Motor
        if target_left > self.current_left_motor:
            self.current_left_motor = min(target_left, self.current_left_motor + self.acceleration_step)
        elif target_left < self.current_left_motor:
            self.current_left_motor = max(target_left, self.current_left_motor - self.acceleration_step)

        # Ramp Right Motor
        if target_right > self.current_right_motor:
            self.current_right_motor = min(target_right, self.current_right_motor + self.acceleration_step)
        elif target_right < self.current_right_motor:
            self.current_right_motor = max(target_right, self.current_right_motor - self.acceleration_step)

        return int(round(self.current_left_motor)), int(round(self.current_right_motor))

    def reset_smooth_acceleration(self):
        """Immediately resets current motor states to 0 (used during Emergency Stop)"""
        self.current_left_motor = 0.0
        self.current_right_motor = 0.0

    def process(self, raw_x: float, raw_y: float) -> tuple[int, int]:
        """Convenience method combining differential calculation and acceleration smoothing."""
        target_left, target_right = self.compute_differential_drive(raw_x, raw_y)
        return self.update_smooth_acceleration(target_left, target_right)
