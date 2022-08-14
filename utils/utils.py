import pygame

def load_image(path, *, scale=-1, max_size=(-1, -1)):
    """
    Loads image and - if arguments were passed - scales it or fits
    to the given max size.
    
    Returns: the newly created image (Surface)
    """
    image = pygame.image.load(path).convert_alpha()

    image_size = image.get_size()
    # Resizes image to the max_size
    if scale < 0 and len(list(filter(lambda x: x > 0, max_size))) == 2:
        image_size = (
            image_size[0] * (max_size[0] / image_size[0]),
            image_size[1] * (max_size[1] / image_size[1]))
    elif scale > 0:
        image_size = (image_size[0] * scale, image_size[1] * scale)

    image = pygame.transform.scale(image, image_size)

    return image