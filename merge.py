"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    merged_line = [0] * len(line)

    target_idx = 0
    for entrance in line:
        if entrance > 0:
            if  merged_line[target_idx] == 0:
                merged_line[target_idx] = entrance
            elif merged_line[target_idx] == entrance:
                merged_line[target_idx] += entrance
                target_idx += 1
            else:
                target_idx += 1
                merged_line[target_idx] = entrance
    return merged_line

print("1", merge([2,0,2,4]) == [4,4,0,0])
print("2", merge([0,0,2,2]) == [4,0,0,0])
print("3", merge([2,2,0,0]) == [4,0,0,0])
print("4", merge([2,2,2,2,2]) == [4,4,2,0,0])
print("5", merge([8,16,16,8]) == [8,32,8,0])