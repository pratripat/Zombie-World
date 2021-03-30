import pygame
import json
from scripts.functions.font_renderer import Font

width = 1200
height = 700

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE+pygame.SCALED)
pygame.display.set_caption('Platformer')

clock = pygame.time.Clock()

colors = json.load(open('data/graphics/colors.json', 'r'))

font = Font('data/graphics/spritesheet/character_spritesheet')
font.load_characters()

scroll = [0,0]
gravity = 1
movement = [0,0]
directions = {'right': False, 'left': False, 'up': False, 'down': True}
