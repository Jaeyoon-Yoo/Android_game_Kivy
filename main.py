from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Color
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import numpy as np
COLS = 13
ROWS = 10
        
class GridUnit():
    def __init__(self, score, on_click = 'normal', score_show = None):
        self.score = score
        self.on_click = on_click
        if score_show is None:
            self.score_show = score
        else:
            self.score_show = score_show
        self.color = (1, 1, 1, 1)
        self.font_size = 20
        self.font_color = (0, 0, 0, 1)
        self.visible = True
        self.clicked = False
        
        
class GameGrid(GridLayout):
    def __init__(self,p,  **kwargs):
        super().__init__(**kwargs)
        
        self.rows = kwargs.get("rows", ROWS)
        self.cols = kwargs.get("cols", COLS)
        
        
        
        
        self.create_grid()
    
    def reset_units(self):
        self.grid_list = [
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10),
            GridUnit(1) for _ in range(10)]
        
    def create_grid(self):
        self.clear_widgets()
        self.stones = []
        for col in range(self.cols):
            for row in range(self.rows):
                # number = np.random.randint(1, 9)
                number = np.random.randint(1, 5)*2-1
                stone = Button(text=f'{number}')
                stone.font_size = self.basic_font_size
                stone.number = number
                stone.color_ori = self.color_set[len(str(number))-1]
                stone.background_color = self.color_set[len(str(number))-1]  # 선택 시 색 변경
                
                self.add_widget(stone)
                self.stones.append(stone)
    
    def select_stone(self, stone):
        if stone not in self.selected_stones:
            self.selected_stones.append(stone)
            stone.background_color = (1, 0, 0)  # 선택 시 색 변경
            
    def on_touch_down(self, touch):
        if not self.visible:
            return super().on_touch_down(touch)
        self.start_pos = touch.pos
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if not self.visible:
            return super().on_touch_move(touch)
        self.end_pos = touch.pos
        self.p.drag_rect.pos = self.start_pos
        self.p.drag_rect.size = (self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1])
        self.select_stones_in_rect()
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if not self.visible:
            return super().on_touch_up(touch)
        run_break = False
        if len(self.selected_stones) <= 1:
            total = 0
        else:
            max_len = np.max([len(str(stone.number)) for stone in self.selected_stones])
            max_idx = np.argmax([len(str(stone.number)) for stone in self.selected_stones])
                
            total = sum(stone.number for stone in self.selected_stones)
            
        if total != 0:
            if max_len == len(str(total)):
                if total % (10**max(max_len-1,1)) == 0:
                    run_break = True  
            else:
                if total % (10**max(max_len,1)) == 0:
                    run_break = True
        
        if run_break:
            # random_number = np.random.randint(0, len(self.selected_stones)-1)
            live_stone = self.selected_stones.pop(max_idx)
            live_stone.number = total
            live_stone.text = f'{live_stone.number}'
            live_stone.color_ori = self.color_set[len(str(total))]
            live_stone.background_color = self.color_set[len(str(total))]
            live_stone.font_size = int(self.basic_font_size*(1+0.1*np.log10(live_stone.number+1)))
            
            self.epoch += 1
            for _ in range(self.revive_count):
                if len(self.destroyed_stones) > 1:
                    self.revive_stone([np.random.randint(0,len(self.destroyed_stones)-1)])
                elif len(self.destroyed_stones) == 1:
                    self.revive_stone([0])
            for stone in self.selected_stones:
                self.left_count -= 1
                 
                stone.text = ""
                stone.number = 0
                stone.background_color = (0, 0, 0)  # 선택된 돌들을 지우기
                self.destroyed_stones.append(stone)
            self.selected_stones = []
            
                
        else:
            for stone in self.selected_stones:
                stone.background_color = stone.color_ori # 원래 색으로 복귀
            self.selected_stones = []
        self.p.score = np.sum([stone.number for stone in self.stones])
        self.p.drag_rect.size = (0,0)
        self.update_text()
        
        return super().on_touch_up(touch)
    
    def update_text(self):
        self.p.score_label.text = f"Score: {self.p.score}"
            
    def revive_stone(self, revive_idx):
        for i in revive_idx:
            self.left_count += 1
            self.destroyed_stones[i].text = f'{np.random.randint(1, 5)*2-1}'
            self.destroyed_stones[i].font_size = self.basic_font_size
            self.destroyed_stones[i].number = int(self.destroyed_stones[i].text)
            self.destroyed_stones[i].color_ori = self.color_set[len(str(self.destroyed_stones[i].number))-1]
            self.destroyed_stones[i].background_color = self.color_set[len(str(self.destroyed_stones[i].number))-1]
            self.destroyed_stones.pop(i)

    def select_stones_in_rect(self):
        if not self.start_pos or not self.end_pos:
            return
        x_min = min(self.start_pos[0], self.end_pos[0])
        x_max = max(self.start_pos[0], self.end_pos[0])
        y_min = min(self.start_pos[1], self.end_pos[1])
        y_max = max(self.start_pos[1], self.end_pos[1])
        
        for stone in self.stones:
            stone_x, stone_y = stone.pos
            stone_w, stone_h = stone.size
            if (x_min <= stone_x + stone_w and stone_x <= x_max and
                y_min <= stone_y + stone_h and stone_y <= y_max and
                stone.number != 0):
                self.select_stone(stone)
            else:
                if stone in self.selected_stones:
                    self.selected_stones.remove(stone)
                    stone.background_color = stone.color_ori  # 선택 해제 시 색 변경
class NumberGameApp(App):
    def build(self):
        layout = FloatLayout()
        self.score = 0
        self.score_label = Label(text=f"Score: 0", size_hint=(0.2, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.95}, font_size='20sp')
        self.generate_btn = Button(text="Generate more", size_hint=(0.2, 0.09), pos_hint={"center_x": 0.9, "center_y": 0.95})
        self.generate_btn.bind(on_release=self.generate_more)
        self.grid = GameGrid(p = self, size_hint=(0.8, 0.8), pos_hint={"center_x": 0.5, "center_y": 0.5}, cols = COLS, rows = ROWS, spacing = 0.1, 
                             width = COLS * 50, height = ROWS * 50)  
        with self.grid.canvas.before:
            self.drag_color = Color(1, 0, 0, 0.5)
            self.drag_rect = Rectangle(size=(0, 0))
            
        # self.start_button = Button(text="Start", size_hint=(0.2, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        # self.start_button.bind(on_release=self.start_game)
        layout.add_widget(self.grid)
        layout.add_widget(self.score_label)
        layout.add_widget(self.generate_btn)
        
        # layout.add_widget(self.start_button)
        return layout
    
    def generate_more(self, instance):
        if len(self.grid.destroyed_stones) >= self.grid.revive_count:
            revive_idx = np.sort(np.unique(np.random.randint(1,len(self.grid.destroyed_stones),3)-1))[::-1].tolist()
        else:
            revive_idx = [i for i in range(len(self.grid.destroyed_stones))][::-1]
        self.grid.revive_stone(revive_idx)
        self.grid.update_text()
    
    def start_game(self, instance):
        self.start_button.opacity = 0  # 버튼 숨기기
        self.start_button.disabled = True
        self.grid.show_grid()
        
if __name__ == "__main__":
    NumberGameApp().run()