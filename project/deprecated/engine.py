import libtcodpy as libtcod

from map_objects.game_map import GameMap
from entity import Entity
from handle_keys import handle_keys
from render_functions import clear_all, render_all


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    
    colors = {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150)
    }
    
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", libtcod.white)
    
    entities = [player]

    libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD) ## font saab välja vahetada, peaks olema fondid kaust

    libtcod.console_init_root(screen_width, screen_height, 'tiitel', False) ## boolean määrab kas fullscreen või mitte

    con = libtcod.console_new(screen_width, screen_height)
    
    game_map = GameMap(map_width, map_height)

    key = libtcod.Key()     ## sisendi muutujad
    mouse = libtcod.Mouse()
    
    while not libtcod.console_is_window_closed(): ## main loop
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse) ## seab sisendi muutujatele väärtused kui kb/mouse midagi teeb
        
        render_all(con, entities, game_map, screen_width, screen_height, colors)
        
        libtcod.console_flush() ## uuendab ekraani
        
        clear_all(con, entities)
        
        action = handle_keys(key) ## vastavalt klahvivajutusele tagastab sõnastiku, kus key on tegu ja value kas koordinaadid või boolean vms
        
        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")
        
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit:
            return True
        
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__': ## teeb nii, et main() käivitub ainult siis, kui see engine.py on main script ehk esimesena käima lükatud
     main()