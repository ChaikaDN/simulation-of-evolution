import random
from grass import Grass
from cell import Cell
from meat import Meat
import pygame as pg
import pygame.gfxdraw


class App:
    def __init__(self, pixel_size=10, pixel_count=90, panel_size=400):
        pg.init()
        self.PIXEL_SIZE = pixel_size
        self.PIXEL_COUNT = pixel_count
        self.PANEL_SIZE = panel_size
        self.FIELD_RES = self.WIDTH, self.HEIGHT = self.PIXEL_SIZE * self.PIXEL_COUNT, self.PIXEL_SIZE * self.PIXEL_COUNT
        self.RES = self.WIDTH + self.PANEL_SIZE, self.HEIGHT
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

    def draw_field(self):
        self.surface.fill('grey')
        pygame.gfxdraw.box(self.surface, (self.WIDTH, 0, self.PANEL_SIZE, self.HEIGHT), (128, 128, 128))

    def draw_obj(self, obj):
        self.draw_pixel(obj.position[0] * self.PIXEL_SIZE, obj.position[1] * self.PIXEL_SIZE, obj.color)

    def draw_pixel(self, x, y, color=(0, 0, 0)):
        pygame.gfxdraw.box(self.surface,
                           (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE),
                           color)

    def run(self):
        grass_list = [Grass((random.randint(0, self.PIXEL_COUNT-1),
                             random.randint(0, self.PIXEL_COUNT-1))) for _ in range(256)]
        cell_list = [Cell((random.randint(0, self.PIXEL_COUNT - 1),
                           random.randint(0, self.PIXEL_COUNT - 1)),
                          [random.randint(0, 23) for _ in range(64)]) for _ in range(128)]
        meat_list = []

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        pass

            self.draw_field()
            print(cell_list[0].gene_pos)
            for grass in grass_list:
                self.draw_obj(grass)
            for meat in meat_list:
                self.draw_obj(meat)
            for cell in list(cell_list):
                self.draw_obj(cell)

                tmp = cell.position
                cell.live(cell_list, grass_list, meat_list)
                cell.position = tmp if cell.check_collision(cell_list) else cell.position

                collided_grass = cell.check_collision(grass_list)
                collided_meat = cell.check_collision(meat_list)

                if collided_grass:
                    cell.health += 50
                    grass_list.remove(collided_grass)
                if collided_meat:
                    cell.health += 70
                    meat_list.remove(collided_meat)

                if cell.is_ready_to_divide:
                    cell_list.append(cell.divide())

                if not cell.is_alive:
                    meat_list.append(Meat(cell.position))
                    cell_list.remove(cell)

            pg.display.set_caption(f'{len(cell_list)} | {str(self.clock.get_fps())}')
            pg.display.flip()
            self.clock.tick(5)


if __name__ == '__main__':
    app = App()
    app.run()
