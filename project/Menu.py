import pygame as pg
import constants as const
import Draw, Button, Actor, Slider


class Menu:
    def __init__(self, main_surface, player, clock, items, buffs, music_volume, effect_volume):
        self.main_surface = main_surface
        self.player = player
        self.clock = clock
        self.items = items
        self.inventory_surface = pg.Surface((const.INV_MENU_WIDTH, const.INV_MENU_HEIGHT))
        self.draw = Draw.Draw(self.main_surface)
        self.draw_inv = Draw.Draw(self.inventory_surface)
        self.buffs = buffs
        self.music_volume = music_volume
        self.effect_volume = effect_volume

    def menu_main(self):
        play_button = Button.Button(self.main_surface, "CONTINUE", (200, 100),
                                    (const.MAIN_SURFACE_WIDTH // 2 - 330, const.MAIN_SURFACE_HEIGHT // 2+50))
        new_game_button = Button.Button(self.main_surface, "NEW GAME", (200, 100),
                                    (const.MAIN_SURFACE_WIDTH // 2 - 110, const.MAIN_SURFACE_HEIGHT // 2+50))
        settings_button = Button.Button(self.main_surface, "SETTINGS", (200, 100),
                                    (const.MAIN_SURFACE_WIDTH // 2 + 110, const.MAIN_SURFACE_HEIGHT // 2+50))
        exit_button = Button.Button(self.main_surface, "EXIT", (200, 100),
                                    (const.MAIN_SURFACE_WIDTH // 2 + 330, const.MAIN_SURFACE_HEIGHT // 2+50))

        self.music = pg.mixer.Sound(const.MENU_MUSIC)
        self.music.set_volume(self.music_volume)
        self.music.play(-1)

        menu_open = True
        while menu_open:
            self.main_surface.blit(pg.image.load("background.png"), (0, 0))
            play_button.draw()
            new_game_button.draw()
            settings_button.draw()
            exit_button.draw()

            events = pg.event.get()
            mouse = pg.mouse.get_pos()
            input = (events, mouse)

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            if play_button.update(input):
                self.music.stop()
                return "CONTINUE"

            if new_game_button.update(input):
                self.music.stop()
                return "NEW_GAME"

            if settings_button.update(input):
                self.settings_menu(self.music)

            if exit_button.update(input):
                pg.quit()
                exit()

            font_height = self.draw.get_font_height(const.FONT_CONSOLE)
            self.draw.draw_text("Music by Hendy Marvin", 5, const.MAIN_SURFACE_HEIGHT-font_height-5, const.DARK_GRAY,
                                const.FONT_CONSOLE)
            self.draw.draw_text("Art by 0x72", const.MAIN_SURFACE_WIDTH - 132, const.MAIN_SURFACE_HEIGHT-font_height-5, const.DARK_GRAY,
                                const.FONT_CONSOLE)

            pg.display.update()

    def settings_menu(self, music):
        sett_surf = pg.Surface((const.SETTINGS_MENU_WIDTH, const.SETTINGS_MENU_HEIGHT))
        exit_button = Button.Button(self.main_surface, "EXIT", (100, 50),
                                    (const.MAIN_SURFACE_WIDTH // 2, const.MAIN_SURFACE_HEIGHT // 2 + 100))
        music_slider = Slider.Slider(self.main_surface, "MUSIC", (400, 7), music.get_volume(),
                                     (const.MAIN_SURFACE_WIDTH // 2, const.MAIN_SURFACE_HEIGHT // 2 - 60))
        effect_slider = Slider.Slider(self.main_surface, "SOUND EFFECTS", (400, 7), self.effect_volume,
                                     (const.MAIN_SURFACE_WIDTH // 2, const.MAIN_SURFACE_HEIGHT // 2 + 15))

        close = False
        while not close:
            events = pg.event.get()
            mouse = pg.mouse.get_pos()
            input = (events, mouse)

            sett_surf.fill(const.BLACK)
            self.main_surface.blit(sett_surf, (const.MAIN_SURFACE_WIDTH // 2 - const.SETTINGS_MENU_WIDTH // 2,
                                               const.MAIN_SURFACE_HEIGHT // 2 - const.SETTINGS_MENU_HEIGHT // 2))
            exit_button.draw()
            music_slider.draw()
            effect_slider.draw()

            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            button_held = music_slider.update(input)
            while button_held:
                events = pg.event.get()
                mouse = pg.mouse.get_pos()
                music.set_volume((music_slider.rect.centerx-400)/400)
                self.music_volume = (music_slider.rect.centerx-400)/400
                self.main_surface.blit(sett_surf, (const.MAIN_SURFACE_WIDTH // 2 - const.SETTINGS_MENU_WIDTH // 2,
                                                   const.MAIN_SURFACE_HEIGHT // 2 - const.SETTINGS_MENU_HEIGHT // 2))
                if 400 <= mouse[0] <= 800:
                    music_slider.rect.centerx = mouse[0]
                elif mouse[0] < 400:
                    music_slider.rect.centerx = 400
                elif mouse[0] > 800:
                    music_slider.rect.centerx = 800
                music_slider.update(input)
                exit_button.draw()
                music_slider.draw()
                effect_slider.draw()
                pg.display.update()

                for event in events:
                    if event.type == pg.MOUSEBUTTONUP:
                        button_held = False

            button_held = effect_slider.update(input)
            while button_held:
                events = pg.event.get()
                mouse = pg.mouse.get_pos()
                self.effect_volume = (effect_slider.rect.centerx-400)/400
                self.main_surface.blit(sett_surf, (const.MAIN_SURFACE_WIDTH // 2 - const.SETTINGS_MENU_WIDTH // 2,
                                                   const.MAIN_SURFACE_HEIGHT // 2 - const.SETTINGS_MENU_HEIGHT // 2))
                if 400 <= mouse[0] <= 800:
                    effect_slider.rect.centerx = mouse[0]
                elif mouse[0] < 400:
                    effect_slider.rect.centerx = 400
                elif mouse[0] > 800:
                    effect_slider.rect.centerx = 800
                music_slider.draw()
                effect_slider.update(input)
                exit_button.draw()
                effect_slider.draw()
                pg.display.update()

                for event in events:
                    if event.type == pg.MOUSEBUTTONUP:
                        button_held = False

            if exit_button.update(input):
                close = True

            self.clock.tick(const.FPS_LIMIT)
            pg.display.update()

    def inventory_menu(self):
        close = False

        text_height = self.draw_inv.get_font_height(const.FONT_INVENTORY)

        while not close:
            self.inventory_surface.fill(const.DARK_GRAY)

            events = pg.event.get()
            if self.player.selection > len(self.player.inventory) - 1:
                current_index = self.player.selection = 0
            else:
                current_index = self.player.selection

            # Close inventory if press I
            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_i:
                        close = True
                    if event.key == pg.K_s:
                        self.player.next_selection()
                        current_index = self.player.selection
                    if event.key == pg.K_w:
                        self.player.prev_selection()
                        current_index = self.player.selection
                    if event.key == pg.K_f:
                        if not self.player.inventory:
                            self.player.messages.append("You have no items to drop")
                        else:
                            item_here = False
                            for item in self.items:
                                if item.get_location() == self.player.get_location():
                                    self.player.messages.append("There is already an item here.")
                                    item_here = True
                                    break
                            if not item_here:
                                self.player.messages.append("Dropped " + self.player.inventory[current_index].name + ".")
                                self.player.inventory[current_index].drop(self.player, self.items)
                    elif event.key == pg.K_e:
                        if not self.player.inventory:
                            self.player.messages.append("You have no items noob")
                        else:
                            if self.player.inventory and not self.player.equipped and isinstance(self.player.inventory[current_index], Actor.Equipable):
                                self.player.equip(self.player.inventory[current_index])
                            elif isinstance(self.player.equipped, Actor.Equipable) and not isinstance(self.player.inventory[current_index], Actor.Consumable):
                                self.player.messages.append("You already have something equipped.")
                            elif self.player.inventory:
                                self.player.consume(self.player.inventory[current_index], self.buffs, self.effect_volume)
                    elif event.key == pg.K_r:
                        if self.player.equipped is not None:
                            self.player.unequip(self.player.equipped)
                        else:
                            self.player.messages.append("You have nothing equipped.")

            # Display list of items
            for i, item in enumerate(self.player.inventory):
                if i == current_index:
                    self.draw_inv.draw_text(item.name, 0, 0 + (i * text_height), const.BLACK, const.FONT_INVENTORY,
                                        False, const.WHITE)
                else:
                    self.draw_inv.draw_text(item.name, 0, 0 + (i * text_height), const.WHITE, const.FONT_INVENTORY)

            self.main_surface.blit(self.inventory_surface, (0, const.MAIN_SURFACE_HEIGHT // 2 - const.INV_MENU_HEIGHT // 2))

            console_surf = pg.Surface((720, text_height*5))
            console_surf.fill(const.BLACK)
            self.main_surface.blit(console_surf, (0, 4+const.MAIN_SURFACE_HEIGHT-text_height*5))

            self.draw.draw_text("w - previous item", 2, const.MAIN_SURFACE_HEIGHT // 2+70-text_height,
                                const.WHITE, const.FONT_INVENTORY)
            self.draw.draw_text("s - next item", 2, const.MAIN_SURFACE_HEIGHT//2+70,
                                const.WHITE, const.FONT_INVENTORY)
            self.draw.draw_text("e - use/equip item", 2, const.MAIN_SURFACE_HEIGHT // 2+text_height+70,
                                const.WHITE, const.FONT_INVENTORY)
            self.draw.draw_text("r - unequip item", 2, const.MAIN_SURFACE_HEIGHT // 2+text_height*2+70,
                                const.WHITE, const.FONT_INVENTORY)
            self.draw.draw_text("f - drop item", 2, const.MAIN_SURFACE_HEIGHT // 2+text_height*3+70,
                                const.WHITE, const.FONT_INVENTORY)
            self.draw.draw_text("spacebar - cast spell", 2, const.MAIN_SURFACE_HEIGHT // 2+text_height*4+70,
                                const.WHITE, const.FONT_INVENTORY)

            self.draw.draw_console_messages(self.player.messages, const.FONT_CONSOLE)

            hud_surf = pg.Surface((320, 240))
            hud_surf.fill(const.BLACK)
            self.main_surface.blit(hud_surf, (0, 0))
            self.player.draw_hud()

            self.clock.tick(const.FPS_LIMIT)

            pg.display.update()

    def esc_menu(self):
        esc_surf = pg.Surface((const.ESC_MENU_WIDTH, const.ESC_MENU_HEIGHT))
        menu_button = Button.Button(self.main_surface, "MAIN MENU", (200, 100),
                                        (const.MAIN_SURFACE_WIDTH // 2 - 220, const.MAIN_SURFACE_HEIGHT // 2))
        settings_button = Button.Button(self.main_surface, "SETTINGS", (200, 100),
                                        (const.MAIN_SURFACE_WIDTH // 2, const.MAIN_SURFACE_HEIGHT // 2))
        close_button = Button.Button(self.main_surface, "EXIT GAME", (200, 100),
                                    (const.MAIN_SURFACE_WIDTH // 2 + 220, const.MAIN_SURFACE_HEIGHT // 2))

        menu_open = True
        while menu_open:
            esc_surf.fill(const.DARK_GRAY)
            self.main_surface.blit(esc_surf, (const.MAIN_SURFACE_WIDTH // 2 - const.ESC_MENU_WIDTH // 2,
                                               const.MAIN_SURFACE_HEIGHT // 2 - const.ESC_MENU_HEIGHT // 2))

            menu_button.draw()
            settings_button.draw()
            close_button.draw()

            events = pg.event.get()
            mouse = pg.mouse.get_pos()
            input = (events, mouse)

            for event in events:
                if event.type == pg.QUIT:
                    return "EXIT"
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    menu_open = False

            if menu_button.update(input):
                return "MAIN_MENU"

            if settings_button.update(input):
                return "SETTINGS"

            if close_button.update(input):
                return "EXIT"

            pg.display.update()

    def death_screen_menu(self, floor):
        death_surface = pg.Surface((const.MAIN_SURFACE_WIDTH, 300))
        menu_button = Button.Button(self.main_surface, "MAIN MENU", (200, 100),
                                        (const.MAIN_SURFACE_WIDTH // 2, const.MAIN_SURFACE_HEIGHT // 2+220))

        self.music = pg.mixer.Sound(const.DEATH_MUSIC)
        self.music.set_volume(self.music_volume)
        self.music.play(-1)

        menu_open = True
        while menu_open:
            death_surface.fill(const.DARK_GRAY)
            self.main_surface.blit(death_surface, (0, const.MAIN_SURFACE_HEIGHT//2-150))
            self.draw.draw_text("YOU DIED", const.MAIN_SURFACE_WIDTH // 2, const.MAIN_SURFACE_HEIGHT // 2, const.RED, const.FONT_DEATH_MESSAGE, center=True)
            self.draw.draw_text("You made it to floor "+str(floor), const.MAIN_SURFACE_WIDTH // 2, const.MAIN_SURFACE_HEIGHT // 2+115, const.RED,
                                const.FONT_CONSOLE, center=True)
            menu_button.draw()

            events = pg.event.get()
            mouse = pg.mouse.get_pos()
            input = (events, mouse)

            for event in events:
                if event.type == pg.QUIT:
                    return "EXIT"

            if menu_button.update(input):
                self.music.stop()
                return "MAIN_MENU"

            pg.display.update()
