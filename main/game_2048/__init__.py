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