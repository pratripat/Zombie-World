import pygame, os, sys, json

animation_path = 'data/graphics/animations'

class Animation_Data:
    def __init__(self, path, colorkey=(0,0,0)):
        self.path = path
        self.load_frames(colorkey)
        self.load_config()

    def load_frames(self, colorkey):
        paths = []
        self.images = []

        for file in os.listdir(self.path):
            if file.split('.')[-1] == 'png':
                path = self.path+'/'+file
                paths.append(path)

        try:
            paths.sort()
        except Exception as e:
            print(e)
            print('could not sort the animation ->'+self.path)

        for path in paths:
            image = pygame.image.load(path).convert()
            image.set_colorkey(colorkey)
            self.images.append(image)

    def load_config(self):
        try:
            self.config = json.load(open(self.path+'/'+'config.json', 'r'))
        except:
            print('not able to load file, using default configuration of animation..')
            self.config = {
                'frames': [5 for _ in range(len(self.images))],
                'loop': True,
                'speed': 1,
                'scale': 1,
                'centered': False
            }
            file = open(self.path+'/'+'config.json', 'w')
            file.write(json.dumps(self.config))
            file.close()

    def get_frames(self):
        return self.config['frames']

    def get_images(self):
        return self.images

    def get_scale(self):
        return self.config['scale']

    def duration(self):
        return sum(self.config['frames'])

class Animation:
    def __init__(self, animation_data):
        self.animation_data = animation_data
        self.frame = 0
        self.load_image()

    def load_image(self):
        frames = self.animation_data.get_frames()
        images = self.animation_data.get_images()
        scale = self.animation_data.get_scale()
        self_frame = self.frame

        for i, frame in enumerate(frames):
            if self_frame > frame:
                self_frame -= frame
            else:
                self.image = pygame.transform.scale(images[i], (round(images[i].get_width()*scale), round(images[i].get_height()*scale)))
                break

    def render(self, surface, position, flipped, colorkey):
        offset = [0,0]
        image = self.image
        if flipped:
            image = pygame.transform.flip(self.image, True, False)
        if colorkey:
            image.set_colorkey(colorkey)

        if self.animation_data.config['centered']:
            offset[0] -= image.get_width()//2
            offset[1] -= image.get_height()//2

        surface.blit(image, (position[0]+offset[0], position[1]+offset[1]))

    def run(self, dt):
        self.frame += dt*60*self.animation_data.config['speed']

        if self.frame > self.animation_data.duration():
            if self.animation_data.config['loop']:
                self.frame = 0
            else:
                self.frame = self.animation_data.duration()

        self.load_image()

    @property
    def current_image(self):
        return self.image

    @property
    def mask(self):
        return pygame.mask.from_surface(self.current_image)

class Animation_Handler:
    def __init__(self):
        self.animations = {}

        for animation in os.listdir(animation_path):
            self.animations[animation] = Animation_Data(animation_path+'/'+animation)

    def get_animation(self, animation_id):
        return Animation(self.animations.get(animation_id))

if __name__ == '__main__':
    width = height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Animation Handler')

    clock = pygame.time.Clock()

    animation_handler = Animation_Handler()
    player_idle_animation = animation_handler.get_animation('player_idle')
    player_run_animation = animation_handler.get_animation('player_run')

    def get_fps():
        if clock.get_fps() == 0:
            return 0
        return 1/clock.get_fps()

    while True:
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0,0,0))
        player_idle_animation.run(get_fps())
        player_idle_animation.render(screen, (width//2, height//2))
        player_run_animation.run(get_fps())
        player_run_animation.render(screen, (width//2+100, height//2))
        pygame.display.update()
