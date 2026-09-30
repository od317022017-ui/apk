from kivy.animation import Animation
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

Window.size = (400, 700)
Window.clearcolor = (0.188, 0.184, 0.2, 0.5)

# Екран меню
class Menu(Screen):
    def go_game(self):
        self.manager.current = "game"
    def go_settings(self):
        self.manager.current = "settings"
    def exit_app(self):
        App.get_running_app().stop()


# Екран налаштувань
class Settings(Screen):
    def go_menu(self):
        self.manager.current = "menu"
    def set_creature(self, creature):
        text_label = self.ids.chosen_creature
        text_label.text = f"Selected creature: {creature}"
        game_screen = self.manager.get_screen("game")
        game_screen.creature = creature


# Екран гри
class Game(Screen):
    # rad = radiation counter
    rad = 0
    img_per_clicks = 50
    creature = "Larry"
    images_data = {
        "Larry": {"path": "Images/larry/", "img_per_clicks": 50},
        "Barry": {"path": "Images/barry/", "img_per_clicks": 75},
        "Husk": {"path": "Images/husk/", "img_per_clicks": 60},
        "Abomination": {"path": "Images/abomination/", "img_per_clicks": 80},
        "Spider": {"path": "Images/spider/", "img_per_clicks": 55},
        "Stalker": {"path": "Images/stalker/", "img_per_clicks": 75},
    }
    
    def on_enter(self):
        our_image = self.ids.our_image
        our_image.opacity = 1
        data = self.images_data.get(self.creature)
        self.img_per_clicks = data["img_per_clicks"]
        self.rad = 0
        self.ids.rad_label.text = f"Radiation: {self.rad}"
    def go_menu(self, *args):
        self.manager.current = "menu"
    def change_image(self, *args):
        # Change the image based on the current radiation level, creature, and img_per_clicks
        data = self.images_data.get(self.creature)
        img_per_clicks = data["img_per_clicks"]
        image_index = self.rad // img_per_clicks
        self.ids.our_image.source = f"{data['path']}{image_index}.png"
    def on_touch_down(self, touch):
        our_image = self.ids.our_image
        if our_image.collide_point(*touch.pos):
            self.hit_image()
            return True
        return super().on_touch_down(touch)
    def hit_image(self):
        if self.rad == 650:
            return
        self.rad += 1
        self.ids.rad_label.text = f"Radiation: {self.rad}"

        our_image = self.ids.our_image
        our_image_size = (300, 300)

        target_lenght = our_image_size[0] * 1.15
        target_height = our_image_size[1] * 1.15

        anim = (
            Animation(size = (target_lenght, target_height), duration=0.1) +
            Animation(size = (our_image_size[0], our_image_size[1]), duration=0.1)
        )
        anim.start(our_image)
        #animations for 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600 clicks
        if self.rad in [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]:
            Clock.schedule_once(self.mut, 0.5)

    def mut(self, dt):
        def _on_fade_out(anim, widget):
            self.change_image()
            Animation(opacity=1, duration=0.5).start(widget)

        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=_on_fade_out)
        anim.start(self.ids.our_image)

        # final animation for 650 clicks
        if self.rad == 650:
            Clock.schedule_once(self.mutate, 0.5)

    def mutate(self, dt):
        anim = Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=self.change_image)
        anim.bind(on_complete=self.go_menu)
        anim.start(self.ids.our_image)




# Додаток
class ClickerApp(App):
    def build(self):
        menu_screen = Menu(name="menu")
        settings_screen = Settings(name="settings")
        game_screen = Game(name="game")
        sm = ScreenManager()
        sm.add_widget(menu_screen)
        sm.add_widget(settings_screen)
        sm.add_widget(game_screen)
        return sm

app = ClickerApp()
app.run()