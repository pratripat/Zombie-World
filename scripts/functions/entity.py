import pygame

class Entity:
    def __init__(self, animations, id, position, centered, current_animation):
        self.animations = animations
        self.id = id
        self.position = position
        self.centered = centered
        self.current_animation_id = self.id+'_'+current_animation
        self.current_animation = self.animations.get_animation(self.current_animation_id)
        self.velocity = [0,0]
        self.flipped = False
        self.collisions = {k:False for k in ('top', 'right', 'bottom', 'left')}

    def render(self, surface, scroll, colorkey=None):
        offset = [0,0]

        if self.centered:
            offset[0] -= self.image.get_width()//2
            offset[1] -= self.image.get_height()//2

        self.current_animation.render(surface, (self.position[0]+offset[0]-scroll[0], self.position[1]+offset[1]-scroll[1]), self.flipped, colorkey)

    def update(self, dt):
        self.current_animation.run(dt)

    def move(self, rects):
        self.collisions = {k:False for k in ('top', 'right', 'bottom', 'left')}

        self.position[0] += self.velocity[0]
        hit_list = self.get_colliding_objects(rects)
        rect = self.rect

        for obj in hit_list:
            if self.velocity[0] > 0:
                rect.right = obj.left
                self.position[0] = rect.x
                self.collisions['right'] = True
            if self.velocity[0] < 0:
                rect.left = obj.right
                self.position[0] = rect.x
                self.collisions['left'] = True
            if self.centered:
                self.position[0] += self.image.get_width()//2

        self.position[1] += self.velocity[1]
        hit_list = self.get_colliding_objects(rects)
        rect = self.rect

        for obj in hit_list:
            if self.velocity[1] > 0:
                rect.bottom = obj.top
                self.position[1] = rect.y
                self.collisions['bottom'] = True
            if self.velocity[1] < 0:
                rect.top = obj.bottom
                self.position[1] = rect.y
                self.collisions['top'] = True
            if self.centered:
                self.position[1] += self.image.get_height()//2

    def get_colliding_objects(self, objs):
        hit_list = []
        for obj in objs:
            if obj.colliderect(self.rect):
                hit_list.append(obj)

        return hit_list

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_animation(self, animation):
        animation = self.id+'_'+animation

        if self.current_animation_id == animation:
            return

        if animation in self.animations.animations:
            self.current_animation = self.animations.get_animation(animation)
            self.current_animation_id = animation

    def flip(self, bool):
        self.flipped = bool

    @property
    def image(self):
        return self.current_animation.current_image

    @property
    def rect(self):
        if self.centered:
            return pygame.Rect(self.position[0]-self.image.get_width()//2, self.position[1]-self.image.get_height()//2, *self.image.get_size())

        return pygame.Rect(*self.position, *self.image.get_size())

    @property
    def center(self):
        if self.centered:
            return self.position

        return [self.position[0]+self.image.get_width()//2, self.position[1]+self.image.get_height()//2]
