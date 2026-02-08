# Utility functions with various vulnerabilities

import os
import subprocess
import yaml
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse

# VULNERABILITY: Hardcoded API keys and secrets
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
STRIPE_API_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

def execute_command(cmd):
    # VULNERABILITY: Command injection - using shell=True
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def read_file(filename):
    # VULNERABILITY: Path traversal - no validation
    with open(filename, 'r') as f:
        return f.read()

def write_file(filename, content):
    # VULNERABILITY: Arbitrary file write
    with open(filename, 'w') as f:
        f.write(content)

def parse_yaml_config(yaml_string):
    # VULNERABILITY: Unsafe YAML loading (allows code execution)
    config = yaml.load(yaml_string, Loader=yaml.Loader)
    return config

def parse_xml_data(xml_string):
    # VULNERABILITY: XML External Entity (XXE) injection
    tree = ET.fromstring(xml_string)
    return tree

def make_http_request(url):
    # VULNERABILITY: Server-Side Request Forgery (SSRF)
    # No validation of URL - can access internal services
    response = requests.get(url)
    return response.text

def redirect_user(redirect_url):
    # VULNERABILITY: Open redirect
    # No validation of redirect URL
    return f"<meta http-equiv='refresh' content='0; url={redirect_url}'>"

def generate_token(user_id):
    # VULNERABILITY: Weak random number generation
    import random
    token = str(random.randint(100000, 999999))
    return token

def encrypt_data(data):
    # VULNERABILITY: Using weak encryption (XOR)
    key = 42
    encrypted = ''.join(chr(ord(c) ^ key) for c in data)
    return encrypted

def decrypt_data(encrypted):
    # VULNERABILITY: Same weak encryption
    key = 42
    decrypted = ''.join(chr(ord(c) ^ key) for c in encrypted)
    return decrypted

def validate_email(email):
    # VULNERABILITY: Regex DoS (ReDoS)
    import re
    pattern = r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
    # This regex can cause catastrophic backtracking
    return re.match(pattern, email) is not None

def log_user_action(user_id, action, details):
    # VULNERABILITY: Log injection
    log_message = f"User {user_id} performed {action}: {details}\n"
    with open('/var/log/app.log', 'a') as f:
        f.write(log_message)

def get_user_data_from_cache(cache_key):
    # VULNERABILITY: Cache poisoning - no validation
    import pickle
    with open(f'/tmp/cache_{cache_key}.pkl', 'rb') as f:
        return pickle.load(f)

def save_user_data_to_cache(cache_key, data):
    # VULNERABILITY: Insecure deserialization
    import pickle
    with open(f'/tmp/cache_{cache_key}.pkl', 'wb') as f:
        pickle.dump(data, f)

def download_file(url, destination):
    # VULNERABILITY: Arbitrary file download and write
    response = requests.get(url)
    with open(destination, 'wb') as f:
        f.write(response.content)

def eval_expression(expression):
    # VULNERABILITY: Code injection via eval()
    result = eval(expression)
    return result

def execute_user_code(code):
    # VULNERABILITY: Code injection via exec()
    exec(code)
