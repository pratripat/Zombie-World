import pygame
import sys
import json
from .funcs import *

graphics_file_path = 'data/graphics/spritesheet/'
res = 48

class TileMap:
    def __init__(self, filename):
        self.tiles = []
        self.filename = filename

    def load_map(self):
        data = json.load(open(self.filename, 'r'))

        for entity in data.values():
            id = entity['id']
            position = entity['position']
            position = [position[0]*res, position[1]*res]
            index = entity['index']
            layer = entity['layer']
            dimensions = entity['dimensions']
            spritesheet_path = graphics_file_path+id+'.png'

            try:
                image = load_images_from_spritesheet(spritesheet_path)[index]
                image = pygame.transform.scale(image, dimensions)
                self.tiles.append({'image':image, 'position':position, 'layer':layer, 'id': id})
            except Exception as e:
                print(e)

    def get_tiles(self, id, layer=None):
        tiles = []

        for tile in self.tiles:
            if tile['id'] == id:
                if layer != None:
                    if tile['layer'] != layer:
                        continue
                rect = pygame.Rect(*tile['position'], *tile['image'].get_size())
                tiles.append(rect)

        return tiles
