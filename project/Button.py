import pygame as pg
import constants as const
import Draw


class Button:
    def __init__(self, surface, text, size, coords, color_mouseover=const.GREEN, color_default=const.GRAY, text_color_mouseover=const.BLACK, text_color_default=const.BLACK):
        self.surface = surface
        self.text = text
        self.size = size
        self.coordinates = coords
        self.color_mouseover = color_mouseover
        self.color_default = color_default
        self.text_color_mouseover = text_color_mouseover
        self.text_color_default = text_color_default

        self.rect = pg.Rect(self.coordinates, size)
        self.rect.center = self.coordinates

        self.draw_obj = Draw.Draw(self.surface)

    def update(self, input):
        events, mouse_loc = input
        mouse_x, mouse_y = mouse_loc

        button_clicked = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and (self.rect.right >= mouse_x >= self.rect.left and self.rect.bottom >= mouse_y >= self.rect.top):
                    button_clicked = True

        return button_clicked


    def draw(self):
        pg.draw.rect(self.surface, self.color_default, self.rect)
        self.draw_obj.draw_text(self.text, self.coordinates[0], self.coordinates[1], self.text_color_default, const.FONT_MENU_BUTTON, True)
