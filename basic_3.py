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
        opt[m][n]: Minimum cost of the matching between s1 and s2
    """
    m = len(s1)
    n = len(s2)
    opt = memoize(s1, s2)
    cur_i = m
    cur_j = n
    matching_s1 = ""
    matching_s2 = ""
    while cur_i > 0 and cur_j > 0:
        cost_s1_s2 = opt[cur_i - 1][cur_j - 1] + ALPHA[s1[cur_i - 1]][s2[cur_j - 1]]
        cost_s1_delta = opt[cur_i - 1][cur_j] + DELTA
        cost_s2_delta = opt[cur_i][cur_j - 1] + DELTA
        prev = min(
            cost_s1_s2,
            cost_s1_delta,
            cost_s2_delta
        )
        if prev == cost_s1_delta:
            # If (cur_i)th character of s1 is not matched
            matching_s1 += s1[cur_i - 1]
            matching_s2 += "_"
            cur_i -= 1
        elif prev == cost_s2_delta:
            # If (cur_j)th character of s2 is not matched
            matching_s1 += "_"
            matching_s2 += s2[cur_j - 1]
            cur_j -= 1
        else:
            # Both (cur_i)th and (cur_j)th characters are present in the matching
            matching_s1 += s1[cur_i - 1]
            matching_s2 += s2[cur_j - 1]
            cur_i -= 1
            cur_j -= 1

    while cur_i > 0:
        matching_s1 += s1[cur_i - 1]
        matching_s2 += "_"
        cur_i -= 1
    while cur_j > 0:
        matching_s2 += s2[cur_j - 1]
        matching_s1 += "_"
        cur_j -= 1
    return matching_s1[::-1], matching_s2[::-1], opt[m][n]


def memoize(s1: str, s2: str):
    """
    This function generates the memoization table for matching s1 and s2
    Parameters:
        s1: First string
        s2: Second string
    Returns:
        opt: Memoization table
    """
    m = len(s1)
    n = len(s2)
    opt = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(m + 1):
        opt[i][0] = i * DELTA
    for j in range(n + 1):
        opt[0][j] = j * DELTA
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            opt[i][j] = min(
                ALPHA[s1[i - 1]][s2[j - 1]] + opt[i - 1][j - 1],
                DELTA + opt[i - 1][j],
                DELTA + opt[i][j - 1]
            )
    return opt


def generate_sequences(input_file: str):
    """
    This function generates input sequences from the base strings and insertion indices
    Parameters:
        input_file: The file containing the base strings and insertion indices
    Returns:
        S1, S2: The 2 generated sequences
    """
    with open(input_file, "r") as f:
        s1 = ""
        s2 = ""
        end_of_s1 = False
        j = 0  # Variables to store number of index inputs to s1
        k = 0  # Variables to store number of index inputs to s2
        len_s1 = 0
        len_s2 = 0
        for line in f.readlines():
            line = line.strip("\n")
            if not s1:
                s1 = line
                len_s1 = len(line)
            else:
                # Check whether line represents string or index
                if line.isnumeric():
                    index = int(line)
                    if not end_of_s1:
                        cur_len = len(s1)
                        j += 1
                        new_string = s1[:index + 1] + s1
                        if index + 1 < cur_len:
                            new_string += s1[index + 1:]
                        s1 = new_string
                    else:
                        cur_len = len(s2)
                        k += 1
                        new_string = s2[:index + 1] + s2
                        if index + 1 < cur_len:
                            new_string += s2[index + 1:]
                        s2 = new_string
                else:
                    s2 = line
                    len_s2 = len(line)
                    end_of_s1 = True

    # Verify that the strings are generated correctly
    assert len(s1) == len_s1 * (2 ** j)
    assert len(s2) == len_s2 * (2 ** k)
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
