import constants as const
import pygame as pg
import Draw, Actor, Buffs
from math import acos, degrees, sqrt


class Spells:
    def __init__(self, player, camera, map_obj, game_map, surface, actors, actors_containers, items, buffs, clock, messages, effect_volume, floor):
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
        self.effect_volume = effect_volume
        self.floor = floor

    def cast_spell(self):
        if not self.player.spell:
            self.player.messages.append("You don't have any spells to cast.")
            self.player.spell_status = "cancelled"
        elif self.player.turns_since_spell < self.player.spell_cooldown:
            plural = "s"
            cooldown_left = self.player.spell_cooldown - self.player.turns_since_spell
            if cooldown_left == 1:
                plural = ""
            self.player.messages.append("Spell still on cooldown, wait {0} more turn{1}!".format(cooldown_left, plural))
            self.player.spell_status = "cancelled"
        else:
            effect = ""
            if self.player.spell == "Lightning":
                effect = pg.mixer.Sound(const.LIGHTNING_SOUND)
                self.lightning_spell()
            elif self.player.spell == "Fireball":
                effect = pg.mixer.Sound(const.FIREBALL_SOUND)
                self.fireball_spell(2)
            elif self.player.spell == "Daze":
                self.daze_spell()
            elif self.player.spell == "Ranged":
                effect = pg.mixer.Sound(const.RANGED_SOUND)
                self.ranged_attack()
            elif self.player.spell == "Nuke":
                effect = pg.mixer.Sound(const.FIREBALL_SOUND)
                self.fireball_spell(99)
                self.player.messages.append("{0} burned everything to a crisp! Including himself.".format(self.player.name))
                self.player.sprites_key = "SPRITES_SKELETON"
                self.player.sprites = const.ACTOR_DICT["SPRITES_SKELETON"]
                self.player.sprites_mirrored = [pg.transform.flip(e, True, False) for e in const.ACTOR_DICT["SPRITES_SKELETON"]]
                self.player.max_hp = 1
                self.player.hp = 1
            if effect:
                effect.set_volume(self.effect_volume)
                effect.play()


    def lightning_spell(self):
        while True:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            events_spell = pg.event.get()
            map_x = mouse_x // const.TILE_WIDTH - self.camera.get_x_offset()
            map_y = (mouse_y - 1 * const.TILE_HEIGHT) // const.TILE_HEIGHT - self.camera.get_y_offset()

            valid_tiles_list = []
            valid_tiles_list_collision = []
            tiles_list = []
            tiles_list_initial = self.map_obj.find_line(self.player.get_location(), (int(map_x), int(map_y)))
            for tile in tiles_list_initial:
                try:
                    if not self.map_obj.get_tile(tile[0], tile[1]).get_is_wall():
                        tiles_list.append(tile)
                except IndexError:
                    continue

            for i, (x, y) in enumerate(tiles_list):
                valid_tiles_list.append((x + self.camera.get_x_offset(), y + self.camera.get_y_offset() + 1))
                valid_tiles_list_collision.append((x, y))
                if i == self.player.spell_range - 1 and not self.map_obj.get_tile(x, y).get_is_wall():
                    break

            for spell_event in events_spell:
                if spell_event.type == pg.KEYDOWN:
                    if spell_event.key == pg.K_SPACE:
                        self.player.spell_status = "cancelled"
                        return
                if spell_event.type == pg.MOUSEBUTTONDOWN:
                    initial_status = self.player.mirror
                    try:
                        if valid_tiles_list_collision[-1][0] == self.player.get_location()[0]:
                            pass
                        elif valid_tiles_list_collision[-1][0] > self.player.get_location()[0]:
                            self.player.mirror = False
                        else:
                            self.player.mirror = True
                        if initial_status != self.player.mirror:
                            self.player.sprite = pg.transform.flip(self.player.sprite, True, False)
                        self.spell_animation(valid_tiles_list, const.SPRITES_SPELL_LIGHTNING, 4, 3)
                    except IndexError:
                        return
                    self.player.turns_since_spell = 0
                    self.player.messages.append("{0} casts {1}!".format(self.player.name, self.player.spell))
                    npcs_hit = False
                    for npc in self.actors:
                        if npc.get_location() in valid_tiles_list_collision and isinstance(npc, Actor.Enemy):
                            npcs_hit = True
                            npc.messages.append("{0} is hit by {1} for {2} damage!".format(npc.name, self.player.spell, self.player.spell_damage))
                            npc.take_damage(self.player.spell_damage, self.actors, self.items)
                    if not npcs_hit:
                        self.player.messages.append("It didn't hit anyone... noob")
                    self.player.spell_status = "cast"
                    return

            select_surface = pg.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
            select_surface.fill(const.WHITE)
            select_surface.set_alpha(150)
            select_surface.convert_alpha()

            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera, self.floor)
            for (x, y) in valid_tiles_list:
                    self.surface_main.blit(select_surface, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)

    def fireball_spell(self, r):
        while True:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            events_spell = pg.event.get()
            map_x = mouse_x // const.TILE_WIDTH - self.camera.get_x_offset()
            map_y = (mouse_y - 1 * const.TILE_HEIGHT) // const.TILE_HEIGHT - self.camera.get_y_offset()

            valid_tiles_list = []
            valid_tiles_list_collision = []
            tiles_list = self.map_obj.find_line(self.player.get_location(), (int(map_x), int(map_y)), False, self.actors)

            for i, (x, y) in enumerate(tiles_list):
                valid_tiles_list.append((x + self.camera.get_x_offset(), y + self.camera.get_y_offset() + 1))
                valid_tiles_list_collision.append((x, y))
                if i == self.player.spell_range - 1:
                    break
            self.append_spell_radius(r, valid_tiles_list, valid_tiles_list_collision)

            for spell_event in events_spell:
                if spell_event.type == pg.KEYDOWN:
                    if spell_event.key == pg.K_SPACE:
                        self.player.spell_status = "cancelled"
                        return
                if spell_event.type == pg.MOUSEBUTTONDOWN:
                    initial_status = self.player.mirror
                    try:
                        if valid_tiles_list_collision[0][0] == self.player.get_location()[0]:
                            pass
                        elif valid_tiles_list_collision[0][0] > self.player.get_location()[0]:
                            self.player.mirror = False
                        else:
                            self.player.mirror = True
                        if initial_status != self.player.mirror:
                            self.player.sprite = pg.transform.flip(self.player.sprite, True, False)
                        circle_area = 13
                        if r == 99:
                            circle_area = -1
                        valid_tiles_list = valid_tiles_list[-circle_area:]
                        valid_tiles_list_collision = valid_tiles_list_collision[-circle_area:]
                        self.spell_animation(valid_tiles_list, const.SPRITES_SPELL_FIREBALL, 4, 5)
                    except IndexError:
                        return
                    self.player.turns_since_spell = 0
                    self.player.messages.append("{0} casts {1}!".format(self.player.name, self.player.spell))
                    npcs_hit = False
                    for npc in self.actors:
                        if npc.get_location() in valid_tiles_list_collision and isinstance(npc, Actor.Enemy):
                            npcs_hit = True
                            npc.messages.append("{0} is hit by {1} for {2} damage!".format(npc.name, self.player.spell, self.player.spell_damage))
                            npc.take_damage(self.player.spell_damage, self.actors, self.items)
                    if not npcs_hit:
                        self.player.messages.append("It didn't hit anyone... noob")
                    self.player.spell_status = "cast"
                    return

            select_surface = pg.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
            select_surface.fill(const.WHITE)
            select_surface.set_alpha(150)
            select_surface.convert_alpha()

            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera, self.floor)
            for (x, y) in valid_tiles_list:
                self.surface_main.blit(select_surface, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)

    def daze_spell(self):
        while True:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            events_spell = pg.event.get()
            map_x = mouse_x // const.TILE_WIDTH - self.camera.get_x_offset()
            map_y = (mouse_y - 1 * const.TILE_HEIGHT) // const.TILE_HEIGHT - self.camera.get_y_offset()

            valid_tiles_list = []
            valid_tiles_list_collision = []
            r = 1
            tiles_list = self.map_obj.find_line(self.player.get_location(), (int(map_x), int(map_y)), True, None, False)

            for i, (x, y) in enumerate(tiles_list):
                valid_tiles_list.append((x + self.camera.get_x_offset(), y + self.camera.get_y_offset() + 1))
                valid_tiles_list_collision.append((x, y))
                if i == self.player.spell_range - 1:
                    break
            self.append_spell_radius(r, valid_tiles_list, valid_tiles_list_collision)

            for spell_event in events_spell:
                if spell_event.type == pg.KEYDOWN:
                    if spell_event.key == pg.K_SPACE:
                        self.player.spell_status = "cancelled"
                        return
                if spell_event.type == pg.MOUSEBUTTONDOWN:
                    initial_status = self.player.mirror
                    try:
                        if valid_tiles_list_collision[0][0] == self.player.get_location()[0]:
                            pass
                        elif valid_tiles_list_collision[0][0] > self.player.get_location()[0]:
                            self.player.mirror = False
                        else:
                            self.player.mirror = True
                        if initial_status != self.player.mirror:
                            self.player.sprite = pg.transform.flip(self.player.sprite, True, False)
                        valid_tiles_list = valid_tiles_list[-5:]
                        valid_tiles_list_collision = valid_tiles_list_collision[-5:]
                        self.spell_animation(valid_tiles_list, const.SPRITES_SPELL_DAZE, 4, 6)
                    except IndexError:
                        return
                    self.player.turns_since_spell = 0
                    self.player.messages.append("{0} casts {1}!".format(self.player.name, self.player.spell))
                    npcs_hit = False
                    for npc in self.actors:
                        if npc.get_location() in valid_tiles_list_collision and isinstance(npc, Actor.Enemy):
                            no_buff = True
                            npcs_hit = True
                            npc.messages.append("{0} is affected by {1} for 10 turns!".format(npc.name, self.player.spell))
                            for buff in self.buffs:
                                if buff.target == npc and buff.ai_change == "dazed":
                                    buff.turn_counter = 0
                                    no_buff = False
                            if no_buff:
                                self.buffs.append(Buffs.Buff(self.surface_main, "SPRITES_DAZED_BUFF", npc, 0, 0, 0, 10, "dazed"))
                                npc.ai = "dazed"
                                npc.frame_counter = 0
                                npc.idle_frames = round(npc.idle_frames * 1.25)
                    if not npcs_hit:
                        self.player.messages.append("It didn't hit anyone... noob")
                    self.player.spell_status = "cast"
                    return

            select_surface = pg.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
            select_surface.fill(const.WHITE)
            select_surface.set_alpha(150)
            select_surface.convert_alpha()

            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors,
                           self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera, self.floor)
            for (x, y) in valid_tiles_list:
                self.surface_main.blit(select_surface, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)

    def ranged_attack(self):
        while True:
            mouse_x = pg.mouse.get_pos()[0]
            mouse_y = pg.mouse.get_pos()[1]
            events_spell = pg.event.get()
            map_x = mouse_x // const.TILE_WIDTH - self.camera.get_x_offset()
            map_y = (mouse_y - 1 * const.TILE_HEIGHT) // const.TILE_HEIGHT - self.camera.get_y_offset()

            valid_tiles_list = []
            valid_tiles_list_collision = []
            tiles_list = self.map_obj.find_line(self.player.get_location(), (int(map_x), int(map_y)), False, self.actors)

            for i, (x, y) in enumerate(tiles_list):
                try:
                    if self.map_obj.get_tile(x, y).get_is_wall():
                        continue
                except IndexError:
                    continue
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
                    initial_status = self.player.mirror
                    try:
                        if valid_tiles_list_collision[-1][0] == self.player.get_location()[0]:
                            pass
                        elif valid_tiles_list_collision[-1][0] > self.player.get_location()[0]:
                            self.player.mirror = False
                        else:
                            self.player.mirror = True
                        if initial_status != self.player.mirror:
                            self.player.sprite = pg.transform.flip(self.player.sprite, True, False)
                        self.projectile_animation(valid_tiles_list, const.SPRITES_PROJECTILE_ARROW)
                    except IndexError:
                        return
                    self.player.turns_since_spell = 0
                    self.player.messages.append("{0} shoots their {1}!".format(self.player.name, self.player.equipped.name))
                    npcs_hit = False
                    for npc in self.actors:
                        if npc.get_location() == valid_tiles_list_collision[-1] and isinstance(npc, Actor.Enemy):
                            npcs_hit = True
                            damage = round((self.player.spell_damage + 1) * len(valid_tiles_list_collision) / self.player.spell_range)
                            if damage < 1:
                                damage = 1
                            npc.messages.append("{0} is hit by {1} for {2} damage!!".format(npc.name, self.player.equipped.name, damage))
                            npc.take_damage(damage, self.actors, self.items)
                            break
                    if not npcs_hit:
                        self.player.messages.append("It didn't hit anyone... noob")
                    self.player.spell_status = "cast"
                    return

            select_surface = pg.Surface((const.TILE_WIDTH, const.TILE_HEIGHT))
            select_surface.fill(const.WHITE)
            select_surface.set_alpha(150)
            select_surface.convert_alpha()

            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera, self.floor)
            for (x, y) in valid_tiles_list:
                self.surface_main.blit(select_surface, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)

    def append_spell_radius(self, r, valid_tiles_list, valid_tiles_list_collision):
        if not valid_tiles_list_collision:
            return
        if r == 2:
            circle = [(0, -1), (0, -2), (1, -1), (1, 0), (2, 0), (1, 1), (0, 1), (0, 2), (-1, 1), (-1, 0), (-2, 0), (-1, -1)]
        elif r == 1:
            circle = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        elif r == 0:
            circle = []
        elif r == 99:
            circle = [(x, y) for x in range(-99, 99) for y in range(-99, 99)]
        center = valid_tiles_list_collision[-1]
        for x, y in circle:
            valid_tiles_list.append((int(center[0]) + x + self.camera.get_x_offset(), int(center[1]) + y + self.camera.get_y_offset() + 1))
            valid_tiles_list_collision.append((int(center[0]) + x, int(center[1]) + y))

    def spell_animation(self, valid_tiles_list, animation_sprites, sprite_count=4, anim_frames=4):
        for i in range(sprite_count * anim_frames):
            if i % anim_frames == 0:
                Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors,
                               self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages,
                                                                                         self.camera, self.floor)
            for (x, y) in valid_tiles_list:
                self.surface_main.blit(animation_sprites[i // anim_frames],
                                       (x * const.TILE_WIDTH, (y - 0.5) * const.TILE_HEIGHT))

            pg.display.flip()

            self.clock.tick(const.FPS_LIMIT)

    def projectile_animation(self, valid_tiles_list, projectile_sprite, draw_frames=3):
        player_vector = (valid_tiles_list[0][0]-valid_tiles_list[-1][0], -(valid_tiles_list[0][1]-valid_tiles_list[-1][1]))
        player_vector_len = sqrt(player_vector[0] ** 2 + player_vector[1] ** 2)
        if player_vector_len == 0:
            return
        angle = -90 + degrees(acos(player_vector[1]/player_vector_len))
        sprite = projectile_sprite
        if self.player.mirror:
            sprite = pg.transform.flip(sprite, True, False)
            angle = -angle
        sprite = pg.transform.rotate(sprite, angle)
        for (x, y) in valid_tiles_list[:-1]:
            Draw.DrawWorld(self.surface_main, self.game_map, self.player, self.map_obj.fov_map, self.actors, self.actors_containers, self.items, self.buffs).draw_game(self.clock, self.messages, self.camera, self.floor)
            for i in range(draw_frames):
                self.surface_main.blit(sprite, (x * const.TILE_WIDTH, y * const.TILE_HEIGHT))

                pg.display.flip()

                self.clock.tick(const.FPS_LIMIT)
