'''
RF Signal Diff Tool
Compares two RF signal strings and highlights differences in red.
Usage: python rf_diff.py <string1> <string2>
Example: python rf_diff.py "00100001" "00100011"
Output:
--- RF Signal Diff ---
Signal 1 Length: 8
Signal 2 Length: 8
Differences:     1
----------------------
S1: 0010000[1] 
S2: 0010000[1]
----------------------
This script takes two RF signal strings as input, compares them character by character, and highlights any differences in red. It also counts the number of differences and displays the lengths of both signals for reference. The output is formatted for easy readability, with spaces added every 8 characters to mimic typical RF signal formatting.
'''

import sys
import re

def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def diff_strings(s1, s2):
    # Ensure strings are the same length for direct comparison
    max_len = max(len(s1), len(s2))
    s1 = s1.ljust(max_len, ' ')
    s2 = s2.ljust(max_len, ' ')

    out1 = ""
    out2 = ""
    diff_count = 0

    for i in range(max_len):
        char1 = s1[i]
        char2 = s2[i]

        if char1 != char2:
            # Highlight differences in Red (31)
            out1 += colorize(char1, "31")
            out2 += colorize(char2, "31")
            diff_count += 1
        else:
            # Keep identical characters normal
            out1 += char1
            out2 += char2

        # Add a space every 8 characters for readability
        if (i + 1) % 8 == 0:
            out1 += " "
            out2 += " "

    return out1, out2, diff_count

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python rf_diff.py <string1> <string2>")
        sys.exit(1)

    signal_a = sys.argv[1]
    signal_b = sys.argv[2]

    # Clean the input strings (remove spaces if any)
    signal_a = re.sub(r'\s+', '', signal_a)
    signal_b = re.sub(r'\s+', '', signal_b)

    res1, res2, diffs = diff_strings(signal_a, signal_b)

    print("\n--- RF Signal Diff ---")
    print(f"Signal 1 Length: {len(signal_a)}")
    print(f"Signal 2 Length: {len(signal_b)}")
    print(f"Differences:     {colorize(str(diffs), '31' if diffs > 0 else '32')}")
    print("-" * 22)
    print("S1:", res1)
    print("S2:", res2)
    print("-" * 22 + "\n")