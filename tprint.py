import sys

def print_output(output: str):
    sys.stdout.write(output)
    sys.stdout.flush()
    
def clear_output(output: str):
    length = len(output.split("\n"))
    sys.stdout.write(f"\033[{length-1}A")

