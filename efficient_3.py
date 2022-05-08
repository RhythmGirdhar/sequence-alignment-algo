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


def find_cost_arr(s1: str, s2: str) -> [int]:
    """
    This function finds the memoization table for matching s1 and s2 in a memory efficient way
    Parameters:
        s1: First string
        s2: Second string
    Returns:
        opt_arr: An array containing the matching cost for s1 with all possible leading substrings of s2
    """
    m = len(s1)
    n = len(s2)
    opt_arr = [[0 for _ in range(n+1)] for _ in range(2)]
    for j in range(n + 1):
        opt_arr[1][j] = j * DELTA
    cur_s1_idx = 1
    while cur_s1_idx < m+1:
        # Copy the results of previous iteration
        for j in range(n+1):
            opt_arr[0][j] = opt_arr[1][j]
        # Update the new values of the memoization table
        opt_arr[1][0] = opt_arr[0][0] + DELTA
        for j in range(1, n+1):
            opt_arr[1][j] = min(
                ALPHA[s1[cur_s1_idx-1]][s2[j-1]] + opt_arr[0][j-1],
                DELTA + opt_arr[1][j-1],
                DELTA + opt_arr[0][j]
            )
        cur_s1_idx += 1
    return opt_arr[1]


def generate_matching_optimized(s1: str, s2: str) -> (str, str, int):
    """
    This function generates the matching for s1 and s2 using the DNC with DP approach
    Parameters:
        s1: First string
        s2: Second string
    Returns:
        matching_s1: Matching for string s1
        matching_s2: Matching for string s2
        opt_cost: Minimum cost of the matching between s1 and s2
    """
    m = len(s1)
    n = len(s2)

    # Base cases
    if m == 0 and n == 0:
        return s1, s2, 0
    if m == 0:
        return "_" * n, s2, n * DELTA
    if n == 0:
        return s1, "_" * m, m * DELTA
    if m == 1 and n == 1:
        mismatch_cost = ALPHA[s1][s2]
        if 2 * DELTA < mismatch_cost:
            return s1 + "_", "_" + s2, 2 * DELTA
        return s1, s2, mismatch_cost

    small_str = s1
    large_str = s2
    large_str_len = n
    if m > n:
        large_str = s1
        small_str = s2
        large_str_len = m

    large_str_mid = large_str_len // 2
    '''
    Calculate the memoization tables for matching the larger strings' halves with every possible length of the 
    smaller string
    '''
    large_left_opt = find_cost_arr(large_str[:large_str_mid], small_str)
    large_right_opt = find_cost_arr(large_str[large_str_mid:][::-1], small_str[::-1])

    # Find the optimal split position for the smaller string
    split_opt_len = len(large_left_opt)
    min_split_cost = DELTA*(m+n)
    split_position = 0
    for i in range(split_opt_len):
        if large_left_opt[i]+large_right_opt[split_opt_len-1-i] < min_split_cost:
            min_split_cost = large_left_opt[i]+large_right_opt[split_opt_len-1-i]
            split_position = i

    # Recursively find the matchings for the 2 sub-problems and combine the results
    left_matching_large, left_matching_small, left_cost = \
        generate_matching_optimized(large_str[:large_str_mid], small_str[:split_position])
    right_matching_large, right_matching_small, right_cost = \
        generate_matching_optimized(large_str[large_str_mid:], small_str[split_position:])
    if n == large_str_len:
        return left_matching_small+right_matching_small, left_matching_large+right_matching_large, left_cost+right_cost
    return left_matching_large+right_matching_large, left_matching_small+right_matching_small, left_cost+right_cost


def generate_sequences(input_file: str) -> (str, str):
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
matching_x, matching_y, min_cost = generate_matching_optimized(x, y)
end_time = time.time()
time_taken = 1000 * (end_time - start_time)
process = psutil.Process(os.getpid())
memory_used = int(process.memory_info().rss / 1024)
with open(OUTPUT_FILE, "w") as f:
    f.write(str(min_cost) + "\n")
    f.write(matching_x + "\n")
    f.write(matching_y + "\n")
    f.write(str(time_taken) + "\n")
    f.write(str(memory_used) + "\n")
