class PID:
    def __init__(self, p, i, d, integral_limit=1000, derivative_filter=0.1):
        self.p = p
        self.i = i
        self.d = d
        self.integral_limit = integral_limit
        self.derivative_filter = derivative_filter
        self.prev_error = 0
        self.integral = 0
    
    def compute(self, setpoint, actual_value, delta_time):
        error = setpoint - actual_value
        self.integral += error * delta_time
        self.integral = max(min(self.integral, self.integral_limit), -self.integral_limit)
        
        derivative = (error - self.prev_error) / delta_time if delta_time > 0 else 0
        derivative = self.derivative_filter * derivative + (1 - self.derivative_filter) * self.prev_error
        
        output = self.p * error + self.i * self.integral + self.d * derivative
        self.prev_error = error
        return output
