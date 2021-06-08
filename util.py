import random

def choose_e(t_rate):
    if random.random() > t_rate:
        return 'T'
    else:
        return 'H' if random.random() >= 0.5 else 'S'

def choose_t():
    return 'CZ' if random.random() >= 0.5 else 'Split'

def generate_block(t_rate=0.01):
    return (choose_e(t_rate), choose_e(t_rate), choose_t())

def block_pattern(width, height):
    blocks = []
    for i in range(height):
        if i % 2 == 0:
            for j in range(0, width - 1, 2):
                #TODO: fix t_rate
                blocks.append((j, generate_block(0.3)))
        else:
            for j in range(1, width - 1, 2):
                #TODO: fix t_rate
                blocks.append((j, generate_block(0.3)))
    return blocks