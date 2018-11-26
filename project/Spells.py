import constants as const
import pygame as pg
import Draw, Actor


class Spells:
    def __init__(self, player, camera, map_obj, game_map, surface, actors, actors_containers, items, buffs, clock, messages):
        self.player = player
        self.camera = camera
        self.map_obj = map_obj
        self.game_map = game_map
        self.surface_main = surface
        self.actors = actors
        self.actors_containers = actors_containers
        self.items = items
        self.buffs = buffs
        self.clock = clock
        self.messages = messages

    def cast_spell(self):
        if not self.player.spell:
            self.player.messages.append("You don't have any spells to cast.")
            self.player.spell_status = "cancelled"
        elif self.player.turns_since_spell < self.player.spell_cooldown:
            self.player.messages.append("Spell still on cooldown, wait {0} more turns!".format(self.player.spell_cooldown - self.player.turns_since_spell))
            self.player.spell_status = "cancelled"
        else:
            if self.player.spell == "Lightning":
                self.lightning_spell()
            elif self.player.spell == "Fireball":
                self.fireball_spell()

    def lightning_spell(self):
        while True:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            events_spell = pg.event.get()
            map_x = mouse_x // const.TILE_WIDTH - self.camera.get_x_offset()
            map_y = (mouse_y - 1 * const.TILE_HEIGHT) // const.TILE_HEIGHT - self.camera.get_y_offset()

            valid_tiles_list = []
            valid_tiles_list_collision = []
            tiles_list = self.map_obj.find_line(self.player.get_location(), (int(map_x), int(map_y)))

            for i, (x, y) in enumerate(tiles_list):
                valid_tiles_list.append((x + self.camera.get_x_offset(), y + self.camera.get_y_offset() + 1))
                valid_tiles_list_collision.append((x, y))
                if i == self.player.spell_range - 1:
                    break

            for spell_event in events_spell:
                if spell_event.type == pg.KEYDOWN:
                    if spell_event.key == pg.K_SPACE:
                        self.player.spell_status = "cancelled"
                        return
                if spell_event.type == pg.MOUSEBUTTONDOWN:
                    self.player.turns_since_spell = 0
                    self.player.messages.append("{0} casts {1}!".format(self.player.name, self.player.spell))
                    npcs_hit = False
                    for npc in self.actors:
                        if npc.get_location() in valid_tiles_list_collision and isinstance(npc, Actor.Enemy):
                            npcs_hit = True
                            npc.messages.append("{0} is hit by {1}!".format(npc.name, self.player.spell))
                            npc.take_damage(self.player.spell_damage)
                    if not npcs_hit:
                        self.player.messages.append("It didn't hit anyone... noob")
                    self.lightning_spell_animation(valid_tiles_list)
                    self.player.spell_status = "cast"
                    return

            select_surface = pg.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
            select_surface.fill(const.WHITE)
            select_surface.set_alpha(150)
            select_surface.convert_alpha()

            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera)
            for (x, y) in valid_tiles_list:
                    self.surface_main.blit(select_surface, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)

    def fireball_spell(self):
        while True:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            events_spell = pg.event.get()
            map_x = mouse_x // const.TILE_WIDTH - self.camera.get_x_offset()
            map_y = (mouse_y - 1 * const.TILE_HEIGHT) // const.TILE_HEIGHT - self.camera.get_y_offset()

            valid_tiles_list = []
            valid_tiles_list_collision = []
            radius = 2
            tiles_list = self.map_obj.find_line(self.player.get_location(), (int(map_x), int(map_y)), False, self.actors, radius)

            for i, (x, y) in enumerate(tiles_list):
                valid_tiles_list.append((x + self.camera.get_x_offset(), y + self.camera.get_y_offset() + 1))
                valid_tiles_list_collision.append((x, y))
                if i == self.player.spell_range + int((radius*2+1)**2):
                    break

            for spell_event in events_spell:
                if spell_event.type == pg.KEYDOWN:
                    if spell_event.key == pg.K_SPACE:
                        self.player.spell_status = "cancelled"
                        return
                if spell_event.type == pg.MOUSEBUTTONDOWN:
                    self.player.turns_since_spell = 0
                    self.player.messages.append("{0} casts {1}!".format(self.player.name, self.player.spell))
                    npcs_hit = False
                    for npc in self.actors:
                        if npc.get_location() in valid_tiles_list_collision and isinstance(npc, Actor.Enemy):
                            npcs_hit = True
                            npc.messages.append("{0} is hit by {1}!".format(npc.name, self.player.spell))
                            npc.take_damage(self.player.spell_damage)
                    if not npcs_hit:
                        self.player.messages.append("It didn't hit anyone... noob")
                    self.lightning_spell_animation(valid_tiles_list)
                    self.player.spell_status = "cast"
                    return

            select_surface = pg.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
            select_surface.fill(const.WHITE)
            select_surface.set_alpha(150)
            select_surface.convert_alpha()

            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors,
                           self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages,
                                                                                     self.camera)
            for (x, y) in valid_tiles_list:
                self.surface_main.blit(select_surface, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)


    def lightning_spell_animation(self, valid_tiles_list):
        anim_sprites = 4
        anim_frames = 3
        animation_sprites = const.SPRITES_SPELL_LIGHTNING
        for i in range(anim_sprites * anim_frames):
            if i % anim_frames == 0:
                Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera)
            for (x, y) in valid_tiles_list:
                self.surface_main.blit(animation_sprites[i // anim_frames], (x * const.TILE_WIDTH, (y-0.5) * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)
