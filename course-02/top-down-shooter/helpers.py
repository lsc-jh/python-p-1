import pygame


def load_images(path_prefix):
    frames = []
    i = 0
    while True:
        try:
            img = pygame.image.load(f"{path_prefix}{i}.png").convert_alpha()
            frames.append(img)
            i += 1
        except:
            break
    return frames
