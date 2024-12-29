import pygame.sprite


class Fox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/fox.png").convert_alpha()
        self.rect = self.image.get_rect()

        # This is temporary until I implement the movement
        # Looks kind of cute though
        # Like it's meditating
        self.rect.center = (320, 240)

