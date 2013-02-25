import uuid
import base64
import re

def generate_key():
    return base64.b32encode(uuid.uuid4().bytes).strip('=').lower()

def normalize_number(input_number):
	result = input_number.replace(".","")
	return result

def thousand_separator(x, sep='.', dot=','):
    num, _, frac = str(x).partition(dot)
    num = re.sub(r'(\d{3})(?=\d)', r'\1'+sep, num[::-1])[::-1]
    if frac:
        num += dot + frac
    return num