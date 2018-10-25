import libtcodpy as libtcod


def main():
    screen_width = 80
    screen_height = 50

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD) ## font saab välja vahetada, peaks olema fondid kaust

    libtcod.console_init_root(screen_width, screen_height, 'tiitel', False) ## boolean määrab kas fullscreen või mitte

    while not libtcod.console_is_window_closed(): ## main loop nö
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()

        if key.vk == libtcod.KEY_ESCAPE:
            return True


if __name__ == '__main__': ## teeb nii, et main() käivitub ainult siis, kui see engine.py on main script ehk esimesena käima lükatud
     main()