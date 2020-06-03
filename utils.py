def first_num_idx(s):
    for i in range(len(s)):
        if s[i].isdigit():
            return i
    return -1


def first_non_num_idx(s):
    for i in range(len(s)):
        if not s[i].isdigit() and not s[i] == '.':
            return i
    return len(s)
