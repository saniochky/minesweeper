from random import randrange

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.config import Config

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 220)
Config.set('graphics', 'height', 320)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.core.audio import SoundLoader
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image


class Mine(Button):
    def __init__(self, w_cells, list_pos, field, **kwargs):
        super(Mine, self).__init__(**kwargs)
        self.w_cells = w_cells
        self.list_pos = list_pos
        self.field = field

        self.neighbors = 0
        self.neighbors_list = []

        self.background_normal = 'default.png'
        self.bind(on_press=self.pressed)

    def check_bomb(self, pos):
        if isinstance(self.field.mines_list[pos], Bomb):
            self.neighbors += 1
        else:
            self.neighbors_list.append(pos)

    def get_neighbors(self):
        if self.list_pos == 0:
            self.check_bomb(self.list_pos + 1)
            self.check_bomb(self.list_pos + self.w_cells)
            self.check_bomb(self.list_pos + self.w_cells + 1)
        elif self.list_pos == len(self.field.mines_list) - 1:
            self.check_bomb(self.list_pos - 1)
            self.check_bomb(self.list_pos - self.w_cells)
            self.check_bomb(self.list_pos - self.w_cells - 1)
        elif self.list_pos == self.w_cells - 1:
            self.check_bomb(self.list_pos - 1)
            self.check_bomb(self.list_pos + self.w_cells - 1)
            self.check_bomb(self.list_pos + self.w_cells)
        elif self.list_pos == len(self.field.mines_list) - self.w_cells:
            self.check_bomb(self.list_pos + 1)
            self.check_bomb(self.list_pos - self.w_cells)
            self.check_bomb(self.list_pos - self.w_cells + 1)
        elif 0 < self.list_pos < self.w_cells - 1:
            self.check_bomb(self.list_pos - 1)
            self.check_bomb(self.list_pos + 1)
            self.check_bomb(self.list_pos + self.w_cells - 1)
            self.check_bomb(self.list_pos + self.w_cells)
            self.check_bomb(self.list_pos + self.w_cells + 1)
        elif len(self.field.mines_list) - self.w_cells < self.list_pos < len(self.field.mines_list) - 1:
            self.check_bomb(self.list_pos - 1)
            self.check_bomb(self.list_pos + 1)
            self.check_bomb(self.list_pos - self.w_cells - 1)
            self.check_bomb(self.list_pos - self.w_cells)
            self.check_bomb(self.list_pos - self.w_cells + 1)
        elif self.list_pos % self.w_cells == 0:
            self.check_bomb(self.list_pos + 1)
            self.check_bomb(self.list_pos - self.w_cells)
            self.check_bomb(self.list_pos - self.w_cells + 1)
            self.check_bomb(self.list_pos + self.w_cells)
            self.check_bomb(self.list_pos + self.w_cells + 1)
        elif self.list_pos % self.w_cells == self.w_cells - 1:
            self.check_bomb(self.list_pos - 1)
            self.check_bomb(self.list_pos - self.w_cells - 1)
            self.check_bomb(self.list_pos - self.w_cells)
            self.check_bomb(self.list_pos + self.w_cells - 1)
            self.check_bomb(self.list_pos + self.w_cells)
        else:
            self.check_bomb(self.list_pos - 1)
            self.check_bomb(self.list_pos + 1)
            self.check_bomb(self.list_pos - self.w_cells - 1)
            self.check_bomb(self.list_pos - self.w_cells)
            self.check_bomb(self.list_pos - self.w_cells + 1)
            self.check_bomb(self.list_pos + self.w_cells - 1)
            self.check_bomb(self.list_pos + self.w_cells)
            self.check_bomb(self.list_pos + self.w_cells + 1)

    def pressed(self, instance='left'):
        if instance == 'left':
            self.field.open.play()
            self.get_neighbors()
            self.field.triggered -= 1
            self.disabled = True
            self.background_disabled_normal = self.get_image()

            if self.neighbors == 0:
                for pos in self.neighbors_list:
                    if not self.field.mines_list[pos].disabled:
                        self.field.mines_list[pos].pressed()

            if self.field.triggered == 0:
                self.field.win_popup.title = f'You won   Time: {self.field.represent(self.field.time)}'
                self.field.win_popup.open()
                self.field.f = False
                self.field.time = 0
                self.field.update_time('instance')
        elif instance.last_touch.button == 'left':
            if self.background_normal != 'flag.png':
                self.field.open.play()
                self.get_neighbors()
                self.field.triggered -= 1
                self.disabled = True
                self.background_disabled_normal = self.get_image()

                if self.neighbors == 0:
                    for pos in self.neighbors_list:
                        if not self.field.mines_list[pos].disabled:
                            self.field.mines_list[pos].pressed()

                if self.field.triggered == 0:
                    self.field.win_popup.title = f'You won   Time: {self.field.represent(self.field.time)}'
                    self.field.win_popup.open()
                    self.field.f = False
                    self.field.time = 0
                    self.field.update_time('instance')
        elif instance.last_touch.button == 'right':
            if instance.background_normal == 'default.png':
                instance.background_normal = 'flag.png'
                self.field.flags -= 1
                self.field.flag_on.play()
            else:
                instance.background_normal = 'default.png'
                self.field.flags += 1
                self.field.flag_off.play()
            self.field.update_flags()

    def get_image(self):
        if self.neighbors == 0:
            return 'default_pressed.png'
        elif self.neighbors == 1:
            return 'one.png'
        elif self.neighbors == 2:
            return 'two.png'
        elif self.neighbors == 3:
            return 'three.png'
        elif self.neighbors == 4:
            return 'four.png'
        elif self.neighbors == 5:
            return 'five.png'
        elif self.neighbors == 6:
            return 'six.png'
        elif self.neighbors == 7:
            return 'seven.png'
        elif self.neighbors == 8:
            return 'eight.png'


class Bomb(Button):
    def __init__(self, bomb_pos, list_pos, field, **kwargs):
        super(Bomb, self).__init__(**kwargs)
        self.bomb_pos = bomb_pos
        self.list_pos = list_pos
        self.field = field
        self.background_normal = 'default.png'
        self.bind(on_press=self.pressed)

    def pressed(self, instance='left'):
        if instance == 'left':
            self.disabled = True
            self.background_disabled_normal = 'fire.png'

            for pos in self.bomb_pos:
                if pos != self.list_pos:
                    self.field.mines_list[pos].reveal()

            self.field.explosion.play()
            self.field.lost_popup.open()
            self.field.f = False
            self.field.time = 0
            self.field.update_time('instance')
        elif instance.last_touch.button == 'left':
            if self.background_normal != 'flag.png':
                self.disabled = True
                self.background_disabled_normal = 'fire.png'

                for pos in self.bomb_pos:
                    if pos != self.list_pos:
                        self.field.mines_list[pos].reveal()

                self.field.explosion.play()
                self.field.lost_popup.open()
                self.field.f = False
                self.field.time = 0
                self.field.update_time('instance')
        elif instance.last_touch.button == 'right':
            if instance.background_normal == 'default.png':
                instance.background_normal = 'flag.png'
                self.field.flags -= 1
                self.field.flag_on.play()
            else:
                instance.background_normal = 'default.png'
                self.field.flags += 1
                self.field.flag_off.play()
            self.field.update_flags()

    def reveal(self):
        self.disabled = True
        self.background_disabled_normal = 'bomb.png'


class FieldGrid(BoxLayout):
    def __init__(self, back, **kwargs):
        super(FieldGrid, self).__init__(**kwargs)
        self.back = back
        self.back_image = 'back1.png'
        self.orientation = 'vertical'
        self.padding = 10
        self.explosion = SoundLoader.load('explosion.wav')
        self.open = SoundLoader.load('open.wav')
        self.flag_on = SoundLoader.load('flag_on.wav')
        self.flag_off = SoundLoader.load('flag_off.wav')
        self.volume_button = Button(size_hint=(None, None), size=(28, 28), background_normal='volume_on.png', on_press=self.change_volume)

        self.lost_popup = Popup(
            title='You lost',
            title_align='center',
            title_size=20,
            content=Button(
                text='        Restart',
                size_hint=(None, None),
                size=(175, 90),
                font_size=25,
                on_press=self.refresh,
                background_normal='restart.png'
            ),
            size_hint=(None, None),
            size=(200, 150),
            auto_dismiss=False,
            separator_height=0
        )

        self.win_popup = Popup(
            title='',
            title_align='center',
            title_size=15,
            content=Button(
                text='        Restart',
                size_hint=(None, None),
                size=(175, 90),
                font_size=25,
                on_press=self.refresh,
                background_normal='restart.png'
            ),
            size_hint=(None, None),
            size=(200, 150),
            auto_dismiss=False,
            separator_height=0
        )

        self.dd = DropDown()
        self.time = 0
        self.f = None
        self.flags = 10
        self.clock = Clock

        self.b_easy = Button(
            text='Easy',
            size_hint=(None, None),
            size=(75, 22),
            on_press=self.refresh,
            background_normal='easy.png'
        )
        self.b_medium = Button(
            text='Medium',
            size_hint=(None, None),
            size=(75, 22),
            on_press=self.refresh,
            background_normal='medium.png'
        )
        self.b_hard = Button(
            text='Hard',
            size_hint=(None, None),
            size=(75, 22),
            on_press=self.refresh,
            background_normal='hard.png'
        )
        self.mainbutton = Button(
            text='Difficulty',
            size_hint=(None, None),
            size=(75, 22),
            background_normal='difficulty.png'
        )
        self.mainbutton.bind(on_release=self.dd.open)

        self.dd.add_widget(self.b_easy)
        self.dd.add_widget(self.b_medium)
        self.dd.add_widget(self.b_hard)
        self.dd.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

        self.mines_list = [
            Button(text=' ', background_normal='default.png', on_press=self.refresh) for x in range(64)
        ]
        self.triggered = 54

        self.flag_label = Label(text=f'[color=000000]{str(self.flags)}[/color]', markup=True, size_hint=(.7, .7), font_size=20)
        self.time_label = Label(text='[color=000000]00:00[/color]', markup=True)
        self.bl = BoxLayout(size_hint=(1, 100 / (8 * 25 + 20 + 100)), spacing=2)
        self.al_left = AnchorLayout(anchor_x='left', anchor_y='top')
        self.al_left.add_widget(self.mainbutton)
        self.al_center = AnchorLayout(anchor_x='center', anchor_y='center')
        self.al_center.add_widget(self.time_label)
        self.bl_right = BoxLayout(orientation='vertical')
        self.al_flag = AnchorLayout(anchor_x='right', anchor_y='top')
        self.al_flag.add_widget(self.flag_label)
        self.al_volume = AnchorLayout(anchor_x='right', anchor_y='center')
        self.al_volume.add_widget(self.volume_button)
        self.bl_right.add_widget(self.al_flag)
        self.bl_right.add_widget(self.al_volume)

        self.bl.add_widget(self.al_left)
        self.bl.add_widget(self.al_center)
        self.bl.add_widget(self.bl_right)

        self.gl = GridLayout(cols=8, size_hint=(1, (8 * 25) / (8 * 25 + 20 + 100)))
        self.generate_field()

        self.add_widget(self.bl)
        self.add_widget(self.gl)

    def represent(self, num):
        whole = '0' + str(int(num // 60))
        end = '0' + str(num - int(whole) * 60)
        return f'{whole[-2::]}:{end[-2::]}'

    def update_time(self, instance):
        if self.f is None:
            self.time += 1
        self.time_label.text = f'[color=000000]{self.represent(self.time)}[/color]'
        return self.f

    def update_flags(self):
        self.flag_label.text = f'[color=000000]{str(self.flags)}[/color]'

    def change_volume(self, instance):
        if instance.background_normal == 'volume_on.png':
            instance.background_normal = 'volume_off.png'
            self.explosion.volume = 0
            self.open.volume = 0
            self.flag_on.volume = 0
            self.flag_off.volume = 0
        else:
            instance.background_normal = 'volume_on.png'
            self.explosion.volume = 1
            self.open.volume = 1
            self.flag_on.volume = 1
            self.flag_off.volume = 1

    def generate_mines(self, w_cells, h_cells, bombs, restricted_pos):
        mine_list = [None for i in range(w_cells * h_cells)]
        restricted_list = [restricted_pos, restricted_pos + 1, restricted_pos - 1, restricted_pos + h_cells - 1,
                           restricted_pos + h_cells, restricted_pos + h_cells + 1, restricted_pos - h_cells - 1,
                           restricted_pos - h_cells, restricted_pos - h_cells + 1]
        bomb_pos = set()

        while len(bomb_pos) < bombs:
            b_pos = randrange(0, w_cells * h_cells)
            if b_pos not in restricted_list:
                bomb_pos.add(b_pos)

        bomb_pos = list(bomb_pos)

        for pos in bomb_pos:
            mine_list[pos] = Bomb(bomb_pos, pos, self)

        for pos in range(len(mine_list)):
            if not mine_list[pos]:
                mine_list[pos] = Mine(w_cells, pos, self)

        return mine_list

    def generate_field(self):
        for mine in self.mines_list:
            self.gl.add_widget(mine)

    def refresh(self, instance):
        for mine in self.mines_list:
            self.gl.remove_widget(mine)

        if instance.text == ' ':
            cells = int((len(self.mines_list)) ** (1 / 2))
            if len(self.mines_list) == 484:
                bombs = 99
            else:
                bombs = int(len(self.mines_list) / 6.4)

            trigger = self.mines_list.index(instance)
            self.mines_list = self.generate_mines(cells, cells, bombs, trigger)
            self.mines_list[trigger].pressed()
            self.f = None
            self.clock.schedule_interval(self.update_time, 1)
        else:
            if instance.text == 'Easy':
                self.mines_list = [
                    Button(text=' ', background_normal='default.png', on_press=self.refresh) for x in range(64)
                ]
                self.back_image = 'back1.png'
                self.f = False
                self.time = 0
                self.update_time('instance')
            elif instance.text == 'Medium':
                self.mines_list = [
                    Button(text=' ', background_normal='default.png', on_press=self.refresh) for x in range(256)
                ]
                self.back_image = 'back2.png'
                self.f = False
                self.time = 0
                self.update_time('instance')
            elif instance.text == 'Hard':
                self.mines_list = [
                    Button(text=' ', background_normal='default.png', on_press=self.refresh) for x in range(484)
                ]
                self.back_image = 'back3.png'
                self.f = False
                self.time = 0
                self.update_time('instance')
            else:
                self.mines_list = [
                    Button(text=' ', background_normal='default.png', on_press=self.refresh) for x in
                    range(len(self.mines_list))
                ]
            cells = int((len(self.mines_list)) ** (1 / 2))
            if len(self.mines_list) == 484:
                bombs = 99
            else:
                bombs = int(len(self.mines_list) / 6.4)
            self.triggered = cells * cells - bombs
            self.flags = bombs
            self.update_flags()

        self.gl.cols = cells
        self.gl.size_hint = (1, (cells * 25) / (cells * 25 + 20 + 100))
        self.bl.size_hint = (1, 100 / (cells * 25 + 20 + 100))

        for mine in self.mines_list:
            self.gl.add_widget(mine)

        self.lost_popup.dismiss()
        self.win_popup.dismiss()
        Window.size = (cells * 25 + 20, cells * 25 + 20 + 100)
        self.back.source = self.back_image


class MinesweeperApp(App):
    def build(self):
        scr = ScreenManager()
        scr.transition = FadeTransition()
        scr_start = Screen()

        back = Image(source='back1.png')
        scr_start.add_widget(back)

        field = FieldGrid(back)
        scr_start.add_widget(field)
        scr.add_widget(scr_start)

        return scr


if __name__ == "__main__":
    MinesweeperApp().run()
