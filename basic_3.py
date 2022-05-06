import sys
import math

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
    m = len(s1)
    n = len(s2)
    opt = memoize(x, y)
    print(opt[m][n])
    cur_i = m
    cur_j = n
    matching_s1 = ""
    matching_s2 = ""
    while cur_i > 0 and cur_j > 0:
        cost_s1_s2 = opt[cur_i - 1][cur_j - 1]
        cost_s1_delta = opt[cur_i - 1][cur_j]
        cost_s2_delta = opt[cur_i][cur_j - 1]
        prev = min(
            cost_s1_s2,
            cost_s1_delta,
            cost_s2_delta
        )
        if prev == cost_s1_delta:
            # If (cur_i)th character of s1 is not matched
            matching_s1 += s1[cur_i-1]
            matching_s2 += "_"
            cur_i -= 1
        elif prev == cost_s2_delta:
            # If (cur_j)th character of s2 is not matched
            matching_s1 += "_"
            matching_s2 += s2[cur_j-1]
            cur_j -= 1
        else:
            # Both (cur_i)th and (cur_j)th characters are present in the matching
            matching_s1 += s1[cur_i - 1]
            matching_s2 += s2[cur_j - 1]
            cur_i -= 1
            cur_j -= 1

    while len(matching_s1) > len(matching_s2):
        matching_s2 += "_"
    while len(matching_s1) < len(matching_s2):
        matching_s1 += "_"
    return matching_s1[::-1], matching_s2[::-1]


def memoize(s1: str, s2: str) -> [[int]]:
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


def generate_sequences(input_file: str) -> (str, str):
    """
    This function generates input sequences from the base strings and insertion indices
    Parameters:
        input_file: The file containing the base strings and insertion indices
    Returns:
        S1, S2: The 2 generated sequences
    """
    f = open(input_file, "r")
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


x, y = generate_sequences(INPUT_FILE)
matching_x, matching_y = generate_matching(x, y)
print(matching_x)
print(matching_y)
