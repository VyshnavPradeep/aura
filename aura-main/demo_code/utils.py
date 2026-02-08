import pickle
import subprocess

# Security issue: Unsafe deserialization
def load_user_data(data):
    return pickle.loads(data)  # Vulnerable to code injection

# Security issue: Command injection
def process_file(filename):
    cmd = f"cat {filename}"  # Vulnerable on Linux
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout

# Performance issue: Memory inefficient
def process_large_list(items):
    result = []
    for item in items:
        result.append(item * 2)  # Could use list comprehension
    return result

# Scalability issue: No caching
def expensive_calculation(x, y):
    # Simulating expensive operation
    total = 0
    for i in range(x):
        for j in range(y):
            total += i * j
    return total
