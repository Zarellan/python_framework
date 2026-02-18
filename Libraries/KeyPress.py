import pygame

class KeyPress:
    left = False
    up = False
    down = False
    right = False

    def __init__(self):
        pass

    @classmethod
    def update_key(cls, events):
        condition = True
        for event in events:
            condition = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cls.left = condition
                elif event.key == pygame.K_RIGHT:
                    cls.right = condition
                elif event.key == pygame.K_UP:
                    cls.up = condition
                elif event.key == pygame.K_DOWN:
                    cls.down = condition
            condition = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    cls.left = condition
                elif event.key == pygame.K_RIGHT:
                    cls.right = condition
                elif event.key == pygame.K_UP:
                    cls.up = condition
                elif event.key == pygame.K_DOWN:
                    cls.down = condition
