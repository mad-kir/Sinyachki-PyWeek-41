import pygame

import numpy as np

animations = {
    'player_right_idle' : ['player_0.png'],
    'player_left_idle' : ['player_left_8.png'],
    'player_right_run' : ['player_1.png', 'player_2.png'],
    'player_left_run' : ['player_left_9.png', 'player_left_10.png'],
    'player_right_jump' : ['player_3.png'],
    'player_left_jump' : ['player_left_11.png'],
    'player_basket_right_idle' : [],
    'player_basket_left_idle' : [],
    'player_basket_right_run' : [],
    'player_basket_left_run' : [],
    'player_basket_right_jump' : [],
    'player_basket_left_jump' : [],
    'enemy_right_idle' : [],
    'enemy_left_idle' : [],
    'enemy_right_run' : [],
    'enemy_left_run' : [],
    'enemy_right_jump' : [],
    'enemy_left_jump' : [],
    'bat' : []
    }

def set_animation(name):
    animation = []
    for i in animations[name]:
        frame = ''.join(('images/animations/', i))
        animation.append(frame)

    return animation