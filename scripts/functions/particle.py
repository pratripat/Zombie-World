import pygame, random

#Returns random velocity
def get_random_velocity(velocity, intensity):
    velocity = velocity.copy()
    velocity[0] += random.uniform(0,intensity*2)-intensity
    velocity[1] += random.uniform(0,intensity*2)-intensity
    return velocity

class Particle:
    def __init__(self, position, velocity, size, decrementation, color, alpha):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.r = size
        self.decrementation = decrementation
        self.color = color
        self.alpha = alpha

    #Returns surface
    @property
    def surface(self):
        surface = pygame.Surface((self.size*2, self.size*2))
        pygame.draw.circle(surface, self.color, (self.size,self.size), self.r)
        surface.set_colorkey((0,0,0))
        surface.set_alpha(self.alpha)
        return surface

    #Returns if the radius is 0
    @property
    def dead(self):
        return self.r <= 0

    #Renders the particle
    def render(self, surface, scroll):
        surface.blit(self.surface, [self.position[0]-scroll[0], self.position[1]-scroll[1]])

    #Runs the particle
    def run(self):
        self.position = [self.position[0]+self.velocity[0], self.position[1]+self.velocity[1]]
        self.r -= self.decrementation

class Particle_System:
    def __init__(self):
        self.particles = []

    #Runs all the particles
    def run(self, surface, scroll, decrementation):
        for particle in self.particles[:]:
            particle.render(surface, scroll)
            particle.run()

            if particle.dead:
                self.particles.remove(particle)

    #Adds a particle to the list
    def add_particles(self, position, velocity, size, decrementation, color, alpha, intensity, number):
        for i in range(number):
            vel = get_random_velocity(velocity, intensity)
            dec = random.uniform(0.2, decrementation)
            self.particles.append(Particle(position, vel, size, dec, color, alpha))

    #Removes all the particles from the list
    def clear(self):
        self.particles.clear()
