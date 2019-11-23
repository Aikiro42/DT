import difflib


def get_differing_index(str1, str2):
    char_compare_list = [i[0] for i in enumerate(difflib.ndiff(str1, str2)) if '-' in i[1] or '+' in i[1]]
    return char_compare_list[0]


def update_score_list(new_score):
    pass
