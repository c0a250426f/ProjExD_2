import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5), pg.K_DOWN:(0,5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(5,0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs: list[pg.Surface] = []
    bb_accs: list[int] = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect(center=(300, 200))

    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect(center=(random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    bb_mv = [5, 5]

    def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
        yoko, tate = True, True
        if obj_rct.left < 0 or WIDTH < obj_rct.right:
            yoko = False
        if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
            tate = False
        return yoko, tate

    def gameover(screen: pg.surface) -> None:
        result = pg.Surface((WIDTH, HEIGHT))
        result.set_alpha(200)

        font = pg.font.Font(None, 120)
        text = font.render("GAME OVER", True, (255, 255, 255))
        text_rct = text.get_rect(center=(WIDTH//2, HEIGHT//2))

        ck_img = pg.image.load("fig/8.png")
        ck_rct1 = ck_img.get_rect()
        ck_rct2 = ck_img.get_rect()
        ck_rct1.midleft = (text_rct.right + 20, text_rct.centery)
        ck_rct2.midright = (text_rct.left - 20, text_rct.centery)
        screen.blit(result, (0, 0))
        screen.blit(text, text_rct)
        screen.blit(ck_img, ck_rct1)
        screen.blit(ck_img, ck_rct2)

        pg.display.update()
        time.sleep(5)

    def calc_orientation(org: pg.Rect, dst: pg.Rect,current_xy: tuple[float, float]) -> tuple[float, float]:

        dx = dst.centerx - org.centerx
        dy = dst.centery - org.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist < 300:
            return current_xy
        if dist != 0:
            scale = (50 ** 0.5) / dist
            vx = dx * scale
            vy = dy * scale
        else:
            vx, vy = 0, 0
        return (vx, vy)


    clock = pg.time.Clock()
    tmr = 0
    vx, vy = 5, 5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, (0, 0))

        idx = min(tmr // 500, 9)
        acc = bb_accs[idx]
        avx = bb_mv[0] * acc
        avy = bb_mv[1] * acc
        bb_img = bb_imgs[idx]
        old_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = old_center
        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            bb_mv[0] *= -1
        if not tate:
            bb_mv[1] *= -1

        sum_mv = [0, 0]
        key_lst = pg.key.get_pressed()
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bb_img, bb_rct)
        screen.blit(kk_img, kk_rct)

        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        bb_rct.move_ip(vx, vy)

        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()