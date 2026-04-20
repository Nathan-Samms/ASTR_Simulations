import numpy as np
import pygame

windowSizes = {'720p':(1280,720), '1080p':(1920,1080), '1440p':(2560,1440), '1600p':(2560,1600), '900p':(1600,900)}


#Window Txt


class body:
    def __init__(self, colors:list[tuple], positions:list, masses:list[int], velocities:list, G:float, boundaryCollisions=False):
        self.colors = colors
        self.positions = np.array(positions, dtype=float)
        self.masses = np.array(masses, dtype=float)
        self.velocities = np.array(velocities, dtype=float)
        self.radii = np.sqrt(2 * self.masses)
        self.tails = [np.empty((0,2), dtype=float) for i in range(len(masses))]
        self.boundaryCollisions = boundaryCollisions
        self.G = G

    def draw(self, screen):
        for i, (position, color, rad) in enumerate(zip(self.positions, self.colors, self.radii)):
            pygame.draw.circle(screen, color, position.astype(int), int(rad))
            if len(self.tails[i]) > 1:
                pygame.draw.lines(screen, color, False, self.tails[i].astype(int), 1) # type: ignore
    
    #G is an arbitrary value to account for arbitrary mass values
    def computeForces(self, softening=5.0):
        diff = self.positions[np.newaxis, :, :] - self.positions[:, np.newaxis, :]  # j - i (attraction)
        distCubed = (np.sum(diff ** 2, axis=-1) + softening ** 2) ** 1.5

        with np.errstate(invalid='ignore'):
            forceMatrix = self.G * self.masses[np.newaxis, :] / distCubed

        np.fill_diagonal(forceMatrix, 0)

        forces = np.sum(forceMatrix[:, :, np.newaxis] * diff, axis=1)
        return forces
    
    def collisionHandler(self, screensize=windowSizes['900p']):
        '''
        If collision handler is turned ON in __init__, bodies will "bounce" off the walls of the simulation window 
        with the opposite velocity of the direction that they were moving in.
        '''
        w,h = screensize[0], screensize[1]
        for i in range(len(self.masses)):
            rad = self.radii[i]

            #X
            if self.positions[i, 0] - rad < 0:
                self.positions[i, 0] = rad
                self.velocities[i, 0] *= -1
            elif self.positions[i, 0] + rad > w:
                self.positions[i, 0] = w - rad
                self.velocities[i, 0] *= -1
            
            #Y
            if self.positions[i, 1] - rad < 0:
                self.positions[i, 1] = rad
                self.velocities[i, 1] *= -1
            elif self.positions[i, 1] + rad > h:
                self.positions[i, 1] = h - rad
                self.velocities[i, 1] *= -1

    def update(self, dt):
        forces = self.computeForces()
        acceleration = forces / self.masses[:, np.newaxis]
        self.positions += self.velocities * dt + 0.5 * acceleration * dt**2
        newForces = self.computeForces()
        newAcceleration = newForces / self.masses[:, np.newaxis]
        self.velocities += 0.5 * (acceleration + newAcceleration) * dt

        if self.boundaryCollisions:
            self.collisionHandler()

        MAX_TAIL = 500
        for i, pos in enumerate(self.positions):
            self.tails[i] = np.vstack([self.tails[i], pos])
            if len(self.tails[i]) > MAX_TAIL:
                self.tails[i] = self.tails[i][-MAX_TAIL:]

'''
EXAMPLE 1

Multi-body deep space interaction
'''
bodies = body(
    positions  = [[440, 260], [840, 260], [640, 560], [800,800]],
    masses     = [100, 100, 100, 200],
    velocities = [[0.5, 0.5], [-0.5, -0.5], [0, 1], [1,0]],
    G=500.0,
    colors     = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (150,150,0)]
)

'''
EXAMPLE 2

Planet and star system
'''
# bodies = body(
#     positions  = [[800, 450], [1100, 450]],
#     masses     = [2000, 50],
#     velocities = [[0, 0], [0, 8]],
#     colors     = [(255, 200, 0), (0, 100, 255)],
#     G=500.0,
#     boundaryCollisions = False
# )

def main():
    pygame.init()
    pygame.display.set_caption("N-body Gravity Simulation")
    screen = pygame.display.set_mode(windowSizes['900p'])
    clock = pygame.time.Clock()

    font = pygame.font.Font("SpaceGrotesk-SemiBold.ttf", 15)
    nameLabel = font.render('Nathan Samms [ASTR 264]', True, (255, 255, 255))    

    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0,0,0))
        pygame.draw.rect(screen, [255,255,255], (1, 1, windowSizes['900p'][0], windowSizes['900p'][1]), 3)
        screen.blit(nameLabel, (windowSizes['900p'][0]-200, windowSizes['900p'][1]-30))
        bodies.update(dt=0.5)
        bodies.draw(screen)
        pygame.display.update()
        
        clock.tick(60)

main()