import sys

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
    return matching_s1[::-1], matching_s2[::-1]

