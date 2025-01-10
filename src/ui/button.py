import pygame


class Button:
    """A class to represent a button"""

    def __init__(self, image, position, text, font_name, font_size, text_color):
        self.image = image
        self.rect = self.image.get_rect(center=position)
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text_color = text_color
        self.text_surface = self.font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def is_clicked(self, mouse_pos: tuple) -> bool:
        """
        Check if the button is clicked

        Args:
            mouse_pos (tuple): The position of the mouse pointer

        Returns:
            bool: True if the button is clicked, False otherwise
        """
        return self.rect.collidepoint(mouse_pos)

    def set_position(self, new_position: tuple) -> None:
        """
        Set the position of the button

        Args:
            new_position (tuple): The new position of the button
        """
        self.rect = self.image.get_rect(center=new_position)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button on the screen

        Args:
            screen (pygame.Surface): The screen to draw the button on
        """
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def set_text(self, new_text: str) -> None:
        """
        Set the text of the button

        Args:
            new_text (str): The new text of the button
        """
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
