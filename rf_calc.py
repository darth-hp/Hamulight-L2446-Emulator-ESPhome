'''
Usage: python rf_calc.py <string> [<number>]

Example: python rf_calc.py 00100001 415
Output:
3320
-830,415,-1660,415

This script calculates the total signal length of a string multiplied by a given number (milliseconds),
and then generates a list of pulse values based on the consecutive characters in the string.
Each value is either positive or negative depending on whether the character is '1' or '0',
and is multiplied by the length of the group of consecutive characters.
It's basically RLE encoding the string and then applying a transformation to the counts.
The signal leght should be close to the actual duration of the signal in milliseconds,
which is useful for analyzing RF signals captured from devices like the Hamulight Apex L2446.

The string can be any combination of '0' and '1', and the number is a positive integer
that represents the duration in milliseconds for each character.
It's extraction is comming from URH (Universal Radio Hacker) which is a software for analyzing and decoding signals,
often used in the context of software-defined radio (SDR) and wireless communication analysis.

For the Hamulight Apex L2446 the default pulse length value is 415ms, but it can be adjusted
based on the specific timing requirements of the signal being analyzed.
'''

import sys, itertools
b = int(sys.argv[2]) if len(sys.argv) > 2 else 415
# Total signal length in ms
print(len(sys.argv[1])*b)
# List of values (ms)based on consecutive characters
print(','.join(str((b if k == '1' else -b) * len(list(g))) for k, g in itertools.groupby(sys.argv[1])))
