import pygame


class Button:
    def __init__(self, image, position, text, font_name, font_size, text_color):
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text_color = text_color
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def set_position(self, new_position):
        self.rect = self.image.get_rect(center=new_position)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def set_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
