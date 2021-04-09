import pygame
import json
from scripts.functions.font_renderer import Font

#Basic settings

pygame.init()

width = 1200
height = 700

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Zombie World')

clock = pygame.time.Clock()

colors = json.load(open('data/configs/colors.json', 'r'))

font = Font('data/graphics/spritesheet/character_spritesheet')
font.load_characters()

scroll = [0,0]
gravity = 1
directions = {'right': False, 'left': False, 'up': False, 'down': True}
projectiles = []
