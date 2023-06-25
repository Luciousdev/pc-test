import time
import numpy as np

def simulate_gpu_load(duration):
    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        # Perform some heavy computation
        a = np.random.rand(1000, 1000)
        b = np.random.rand(1000, 1000)
        c = np.dot(a, b)

if __name__ == "__main__":
    duration = 120  # Duration in seconds
    simulate_gpu_load(duration)
