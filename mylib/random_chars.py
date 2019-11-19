from random import sample, randint, random


def random_num(num):
    chars = '1234567890'
    return ''.join(sample(chars, num))


def random_chars(num):
    chars = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    return ''.join(sample(chars, num))
