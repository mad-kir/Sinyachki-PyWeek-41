import pygame

import numpy as np

def load_level(number):
    
    level = np.genfromtxt(''.join(('levels/', str(number), '.csv')), delimiter=',', dtype='int')
    
    print('level loaded:')
    print(level)