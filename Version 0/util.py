import pygame
pygame.init()
pygame.font.init()

#scaling the images
def scale_images(img, scale_factor):
    new_size = round(img.get_width() * scale_factor), round(img.get_height() * scale_factor)  
    #round() -> rounds off the decimal values to an integer value
    return  pygame.transform.scale(img, new_size)

#function to return a rotated image
def rotate(win, image, top_left, angle):
    rotate_image = pygame.transform.rotate(image, angle)
    new_rect = rotate_image.get_rect(center = image.get_rect(topleft = top_left).center)
    win.blit(rotate_image, new_rect.topleft)

#function to draw text in the center of the screen
def blit_text_center(win, font, text):
    render = font.render(text, 1, (204,204,0))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 -render.get_height()/2 -20))