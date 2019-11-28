from difflib import ndiff
from random import random
from math import floor


def get_differing_index(str1, str2):
    char_compare_list = [i[0] for i in enumerate(ndiff(str1, str2)) if '-' in i[1] or '+' in i[1]]
    return char_compare_list[0]


"""
code below obtained from:
https://stackoverflow.com/questions/46057732/open-a-text-file-sort-the-text-file-and-then-save-it-using-python
"""


def update_score_list(new_score):
    try:
        open('scores', 'r')
    except FileNotFoundError:
        x = open('scores', 'w')
        x.close()

    with open('scores', 'r') as f:
        lines = f.readlines()
    numbers = [int(e.strip()) for e in lines] + [new_score]
    numbers.sort(key=lambda scre: -scre)

    with open('scores', 'w') as f:  # open sorted.txt for writing 'w'
        # join numbers with newline '\n' then write them on 'sorted.txt'
        f.write('\n'.join(str(n) for n in numbers))


# [Code Generator]=========================================================================================

BIN_OP = 1
FN = 2
ASS = 3
DOT = 4
LIST_ACCESS = 5
PARENTHESES = 6
ELEMENT = 7
LIST = 8

# I recommend that you add more words to this array
# Preferably technical terms like "Abstraction" or "Parser" or hackerman stuff idk lol
str_list = [
    '"string"',
    '"something"',
    '"string_val"'
]

fn_list = [
    'function',
    'decategorize',
    'get_primitive_type',
    'get_type',
    'set_attrib',
    'rad',
    'bool',
    'get_pointer',
    'deg',
    'hex'
]

var_list = [
    'var',
    'foo',
    'bar',
    'vertex',
    'rect',
    'average_calc',
    'angle',
    'attrib',
    'color',
    'score',
    'parsed',
    'elem',
    'i',
    'x',
    'y',
    'j',
    'enum'
]

obj_list = [
    'obj',
    'entity',
    'vertex_list',
    'window',
    'layout',
    'document',
    'clock',
    'box',
    'OS',
    'DaemonThread',
    'System',
    'map'
]

op_list = [
    '+',
    '-',
    '*',
    '%',
    '//',
    '**',
]


# num generators

def gen_random_float(min_f, max_f):
    return min_f + (random() * (max_f - min_f))


def gen_random_int(min_int, max_int):
    return floor(gen_random_float(min_int, max_int))


def get_random_elem(l: list):
    return l[gen_random_int(0, len(l) - 1)]


# str generators

def gen_int():
    return str(gen_random_int(0, 99))


def gen_float():
    return str(round(gen_random_float(0, 99), 2))


def gen_bool():
    return str(bool(gen_random_int(0, 1)))


def gen_var():
    return get_random_elem(var_list)


def gen_str():
    return get_random_elem(str_list)


def gen_op():
    return get_random_elem(op_list)


def gen_obj():
    return get_random_elem(obj_list)


def gen_fn():
    return get_random_elem(fn_list)


def gen_val(is_num=False):
    if is_num:
        return get_random_elem(num_vals)()
    else:
        return get_random_elem(num_vals + non_num_vals)()


def gen_ptr():
    return get_random_elem(ptr_vals)()


num_vals = [
    gen_var,
    gen_int,
    gen_float
]

non_num_vals = [
    gen_var,
    gen_bool,
    gen_str
]

ptr_vals = [
    gen_var,
    gen_obj,
    gen_op
]


def gen_code(depth: int, is_num=False, allow_ass=True, allow_elem=True, is_dot=False, allow_list=True):
    if depth <= 1:
        # Return a value (int, float, bool) or a variable ()
        if is_dot:
            return gen_ptr()
        else:
            return gen_val(is_num)
    else:
        while True:
            x = gen_random_int(1, 7)
            if x == BIN_OP and not is_dot:
                return '{} {} {}'.format(
                    gen_code(depth - 1, is_num=True, allow_ass=False),
                    gen_op(),
                    gen_code(depth - 1, is_num=True, allow_ass=False)
                )
            elif x == FN:
                return '{}({})'.format(
                    gen_fn(),
                    gen_code(depth - 1, is_num=is_num, allow_ass=False)
                )
            elif x == ASS and allow_ass and not is_dot:
                return '{} = {}'.format(
                    gen_var(),
                    gen_code(depth - 1, is_num=is_num, allow_ass=False)
                )
            elif x == DOT:
                return '{}.{}'.format(
                    gen_obj(),
                    gen_code(depth - 1, is_num=False, allow_ass=False, is_dot=True)
                )
            elif x == LIST_ACCESS:
                return '{}[{}]'.format(
                    gen_var(),
                    gen_code(depth - 1, is_num=True, allow_ass=False, allow_elem=False, allow_list=False)
                )
            elif x == PARENTHESES and not is_dot:
                return '({})'.format(
                    gen_code(depth - 1, is_num=is_num, allow_ass=False)
                )
            elif x == LIST and allow_list and not is_dot:
                return '[{}]'.format(
                    gen_code(depth - 1, is_num=is_num, allow_ass=False)
                )
            elif allow_elem and not is_dot:
                return '{}, {}'.format(
                    gen_code(depth - 1, is_num=is_num, allow_ass=False),
                    gen_code(depth - 1, is_num=is_num, allow_ass=False)
                )
