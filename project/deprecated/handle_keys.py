import libtcodpy as libtcod

def handle_keys(key):
    if key.vk == libtcod.KEY_CHAR:
        if key.c == 119: ## w
            return {"move": (0, -1)}
        elif key.c == 115: ## s
            return {"move": (0, 1)}
        elif key.c == 97: ## a
            return {"move": (-1, 0)}
        elif key.c == 100: ## d
            return {"move": (1, 0)}
    
    if key.vk == libtcod.KEY_ESCAPE:
        return {"exit": True}
    
    elif key.vk == libtcod.KEY_ENTER and key.lalt:
        return {"fullscreen": True}
    
    return {}