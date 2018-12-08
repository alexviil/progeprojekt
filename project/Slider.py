import pygame as pg
import constants as const
import Draw


class Slider:
    def __init__(self, surface, text, size, start_pos, coords, color_default=const.GRAY, color_mouseover=const.GREEN):
        self.surface = surface
        self.size = size
        self.coords = coords
        self.color_default = color_default
        self.color_mouseover = color_mouseover
        self.current_color = color_default
        self.start_x = start_pos*400+400
        self.text = text

        self.rect = pg.Rect(self.coords, (10, 30))
        self.rect.center = (self.start_x, self.coords[1])

        self.bg_rect = pg.Rect(self.coords, self.size)
        self.bg_rect.center = self.coords

        self.draw_obj = Draw.Draw(self.surface)

    def update(self, input):
        events, mouse_loc = input
        mouse_x, mouse_y = mouse_loc

        mouseover = self.rect.right >= mouse_x >= self.rect.left and self.rect.bottom >= mouse_y >= self.rect.top
        button_clicked = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and mouseover:
                    button_clicked = True

        if mouseover:
            self.current_color = self.color_mouseover
        else:
            self.current_color = self.color_default

        return button_clicked

    def draw(self):
        pg.draw.rect(self.surface, const.WHITE, self.bg_rect)
        pg.draw.rect(self.surface, self.current_color, self.rect)
        self.draw_obj.draw_text(self.text, self.coords[0], self.coords[1]-25, const.BLACK, const.FONT_SETTINGS, True)
