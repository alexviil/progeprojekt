import pygame as pg
import constants as const


class Camera:
    def __init__(self, x_offset, y_offset):
        self.x_offset = const.CAMERA_CENTER_X - x_offset
        self.y_offset = const.CAMERA_CENTER_Y - y_offset

    def set_offset(self, x_offset_new, y_offset_new):
        self.x_offset = const.CAMERA_CENTER_X - x_offset_new
        self.y_offset = const.CAMERA_CENTER_Y - y_offset_new

    def get_x_offset(self):
        return self.x_offset

    def get_y_offset(self):
        return self.y_offset
