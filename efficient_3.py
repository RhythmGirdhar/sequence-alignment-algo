import sys
import time
import os
import psutil

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]
DELTA = 30
ALPHA = {
    "A": {"A": 0, "C": 110, "G": 48, "T": 94},
    "C": {"A": 110, "C": 0, "G": 118, "T": 48},
    "G": {"A": 48, "C": 118, "G": 0, "T": 110},
    "T": {"A": 94, "C": 48, "G": 110, "T": 0}
}

def generate_matching(s1: str, s2: str):
    """
    This function generates the matching for s1 and s2
    Parameters:
        s1: First string
        s2: Second string
    Returns:
        matching_s1: Matching for string s1
        matching_s2: Matching for string s2
    """
    m = len(s1)
    n = len(s2)
    
    return s1,s2

def generate_sequences(input_file: str) -> (str, str):
    """
    This function generates input sequences from the base strings and insertion indices
    Parameters:
        input_file: The file containing the base strings and insertion indices
    Returns:
        S1, S2: The 2 generated sequences
    """
    f = open(input_file, "r")
    s1 = " "
    s2 = " "
    return s1, s2

start_time = time.time()
x, y = generate_sequences(INPUT_FILE)
matching_x, matching_y, min_cost = generate_matching(x, y)
end_time = time.time()
time_taken = 1000*(end_time-start_time)
process = psutil.Process(os.getpid())
memory_used = int(process.memory_info().rss / 1024)
with open(OUTPUT_FILE, "w") as f:
    f.write(str(min_cost)+"\n")
    f.write(matching_x+"\n")
    f.write(matching_y+"\n")
    f.write(str(time_taken)+"\n")
    f.write(str(memory_used)+"\n")