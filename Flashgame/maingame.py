import pygame
import os
import random

pygame.init()
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flash chase")
clock = pygame.time.Clock()

try:
    pygame.mixer.quit()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except:
    pygame.mixer.init()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

def load_font(size):
    for name in ["Minecraft.otf", "Minecraft.ttf", "Mojangles.ttf"]:
        if os.path.exists(name):
            try: return pygame.font.Font(name, size)
            except: pass
    return pygame.font.Font(None, size)

font = load_font(20)
small_font = load_font(14)
menu_font = load_font(24)
title_font = load_font(32)
font_18 = load_font(18)
font_20 = load_font(20)

# BIGGER BUT SAME POSITION - 64x96
CHAR_W, CHAR_H = 56, 84
OLD_H = 72
Y_OFFSET = OLD_H - CHAR_H

def load_img(name):
    path = os.path.join(SCRIPT_DIR, name) if os.path.exists(os.path.join(SCRIPT_DIR, name)) else name
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (CHAR_W, CHAR_H))
def load_any(name, size=None):
    for base in [name, os.path.join(SCRIPT_DIR, name)]:
        if os.path.exists(base):
            try:
                img = pygame.image.load(base).convert_alpha()
                if size: img = pygame.transform.scale(img, size)
                return img
            except: pass
    return None

def load_bg(name):
    for base in [name, os.path.join(SCRIPT_DIR, name)]:
        if os.path.exists(base):
            try:
                img = pygame.image.load(base).convert()
                return img
            except: pass
    return None

idle_img = load_img("idle.png")
run1_img = load_img("run1.png")
run2_img = load_img("run2.png")
idle_rf = load_img("idle_rf.png")
run1_rf = load_img("run1_rf.png")
run2_rf = load_img("run2_rf.png")
idle_ww = load_img("wwidle.png")
run1_ww = load_img("wwrun1.png")
run2_ww = load_img("wwrun2.png")
idle_jr = load_img("jridle.png")
run1_jr = load_img("jrrun1.png")
run2_jr = load_img("jrrun2.png")
# NEW - GODSPEED
idle_god = load_img("godidle.png")
run1_god = load_img("godrun1.png")
run2_god = load_img("godrun2.png")

def load_bf(name):
    for base in [name, os.path.join(SCRIPT_DIR, name)]:
        if os.path.exists(base):
            try:
                img = pygame.image.load(base).convert_alpha()
                return pygame.transform.scale(img, (CHAR_W, CHAR_H))
            except: pass
    return idle_rf

bf_idle = load_bf("bfidle.png")
bf_run1 = load_bf("bfrun1.png")
bf_run2 = load_bf("bfrun2.png")
bf_roar = load_bf("bfroar.png")
if bf_roar == idle_rf: bf_roar = bf_idle

bolt_yellow = load_any("flight.png", (44, 16))
bolt_red = load_any("rflight.png", (44, 16))
bolt_bf = load_any("bflight.png", (44, 16)) or bolt_red
bolt_wwlight = load_any("wwlight.png", (44, 16))
heart_img = load_any("heart.png", (32,32))
heart_img_small = pygame.transform.scale(heart_img, (20,20)) if heart_img else None
boom_img = load_any("boom.png", (48, 32))

loop_bg_raw = load_bg("loop.png")
fspeed_bg_raw = load_bg("fspeed.png")
rfspeed_bg_raw = load_bg("rfspeed.png")
wwspeed_bg_raw = load_bg("wwspeed.png")
jrspeed_bg_raw = load_bg("jrspeed.png")
godspeed_bg_raw = load_bg("godspeed.png")

bg_cache = {"w":0,"h":0,"loop":None,"fspeed":None,"rspeed":None,"wwspeed":None,"jrspeed":None,"godspeed":None}
def get_bg(raw, key, w, h):
    if bg_cache["w"] != w or bg_cache["h"] != h:
        bg_cache["w"]=w; bg_cache["h"]=h
        for k in list(bg_cache.keys()):
            if k not in ("w","h"): bg_cache[k]=None
    if bg_cache[key] is None and raw is not None:
        bg_cache[key] = pygame.transform.scale(raw, (w, h)).convert()
    return bg_cache[key]

roar_sound = None
for roar_name in ["roar.ogg", "roar.mp3", os.path.join(SCRIPT_DIR,"roar.ogg")]:
    if os.path.exists(roar_name):
        try:
            roar_sound = pygame.mixer.Sound(roar_name)
            roar_sound.set_volume(0.34)
            break
        except: pass

high_score = 0
if os.path.exists("highscore.txt"):
    try:
        with open("highscore.txt","r") as f: high_score = float(f.read().strip() or 0)
    except: high_score = 0

def save_highscore(sc):
    global high_score
    if sc > high_score:
        high_score = sc
        try:
            with open("highscore.txt","w") as f: f.write(str(high_score))
        except: pass

def character_select():
    global WIDTH, HEIGHT, screen
    selected = "flash"
    choosing = True
    options = ["flash", "reverse", "wally", "jay", "godspeed"]
    label_font = load_font(16)
    sub_font = load_font(12)
    idle_big = pygame.transform.scale(idle_img, (96,144))
    rf_big = pygame.transform.scale(idle_rf, (96,144))
    ww_big = pygame.transform.scale(idle_ww, (96,144))
    jr_big = pygame.transform.scale(idle_jr, (96,144))
    god_big = pygame.transform.scale(idle_god, (96,144))

    while choosing:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = e.w, e.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                bg_cache["w"]=0
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT: selected = options[(options.index(selected)-1)%len(options)]
                if e.key == pygame.K_RIGHT: selected = options[(options.index(selected)+1)%len(options)]
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): choosing = False
                if e.key == pygame.K_ESCAPE: pygame.quit(); exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos
                box_w, box_h = 160, 320; gap = 12
                total_w = box_w*len(options) + gap*(len(options)-1); start_x = WIDTH//2 - total_w//2; y = HEIGHT//2 - box_h//2
                for i, opt in enumerate(options):
                    bx = start_x + i*(box_w+gap)
                    if bx < mx < bx+box_w and y < my < y+box_h: selected = opt; choosing = False
        screen.fill((20,20,30))
        title = title_font.render("CHOOSE YOUR SPEEDSTER", True, (255,255,255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))
        box_w, box_h = 160, 320; gap = 12; total_w = box_w*len(options) + gap*(len(options)-1); start_x = WIDTH//2 - total_w//2; y = HEIGHT//2 - box_h//2 + 20
        for i, opt in enumerate(options):
            bx = start_x + i*(box_w+gap)
            if opt=="flash": col = (255,255,0) if selected=="flash" else (80,80,80)
            elif opt=="reverse": col = (255,0,0) if selected=="reverse" else (80,80,80)
            elif opt=="wally": col = (17,173,173) if selected=="wally" else (80,80,80)
            elif opt=="jay": col = (210, 50, 50) if selected=="jay" else (80,80,80)
            else: col = (255,255,255) if selected=="godspeed" else (80,80,80)
            pygame.draw.rect(screen, col, (bx, y, box_w, box_h), 4, border_radius=12)
            if opt == "flash":
                screen.blit(idle_big, (bx+32, y+40))
                t = label_font.render("FLASH", True, (255,255,0) if selected=="flash" else (200,200,200))
                screen.blit(t, (bx + box_w//2 - t.get_width()//2, y+230))
            elif opt == "reverse":
                screen.blit(rf_big, (bx+32, y+40))
                t = label_font.render("REVERSE", True, (255,0,0) if selected=="reverse" else (200,200,200))
                t2 = sub_font.render("FLASH", True, (255,0,0) if selected=="reverse" else (200,200,200))
                screen.blit(t, (bx + box_w//2 - t.get_width()//2, y+230))
                screen.blit(t2, (bx + box_w//2 - t2.get_width()//2, y+250))
            elif opt == "wally":
                screen.blit(ww_big, (bx+32, y+40))
                t = label_font.render("WALLY", True, (17,173,173) if selected=="wally" else (200,200,200))
                t2 = sub_font.render("WEST", True, (17,173,173) if selected=="wally" else (200,200,200))
                screen.blit(t, (bx + box_w//2 - t.get_width()//2, y+230))
                screen.blit(t2, (bx + box_w//2 - t2.get_width()//2, y+250))
            elif opt == "jay":
                screen.blit(jr_big, (bx+32, y+40))
                t = label_font.render("JAY", True, (210,50,50) if selected=="jay" else (200,200,200))
                t2 = sub_font.render("GARRICK", True, (210,50,50) if selected=="jay" else (200,200,200))
                screen.blit(t, (bx + box_w//2 - t.get_width()//2, y+230))
                screen.blit(t2, (bx + box_w//2 - t2.get_width()//2, y+250))
            else:
                screen.blit(god_big, (bx+32, y+40))
                t = label_font.render("GOD", True, (255,255,255) if selected=="godspeed" else (200,200,200))
                t2 = sub_font.render("SPEED", True, (255,255,255) if selected=="godspeed" else (200,200,200))
                screen.blit(t, (bx + box_w//2 - t.get_width()//2, y+230))
                screen.blit(t2, (bx + box_w//2 - t2.get_width()//2, y+250))
        hint = small_font.render("CLICK CARD OR ARROWS + ENTER", True, (150,150,150))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-40))
        pygame.display.flip()
    return selected

def game_over_screen(reason, distance_km):
    waiting = True
    full_text = "You have been ripped to shreds and your existence is erased beyond time. lol gg."
    rip_font = load_font(18)
    def render_multiline(text, font_obj, max_width):
        words = text.split(' '); lines = []; current = ""
        for w in words:
            test = current + " " + w if current else w
            if font_obj.size(test)[0] > max_width: lines.append(current); current = w
            else: current = test
        if current: lines.append(current)
        return lines
    wrapped_lines = render_multiline(full_text, rip_font, WIDTH - 100)
    while waiting:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return "retry"
                if e.key == pygame.K_ESCAPE: return "menu"
            if e.type == pygame.MOUSEBUTTONDOWN: return "retry"
        screen.fill((10,0,0))
        y = HEIGHT//2 - 100
        for line in wrapped_lines:
            t = rip_font.render(line, True, (255,0,0))
            screen.blit(t, (WIDTH//2 - t.get_width()//2, y))
            y += t.get_height() + 6
        t_score = font.render(f"SCORE: {distance_km:.2f} Mm  BEST: {high_score:.2f} Mm", True, (255,255,0))
        screen.blit(t_score, (WIDTH//2 - t_score.get_width()//2, y + 10))
        y += 30
        t2 = font.render(reason, True, (255,255,255))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, y + 10))
        t3 = small_font.render("Press R / TAP to retry - ESC for menu", True, (150,150,150))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, y + 50))
        pygame.display.flip()

def game_loop(selected):
    global WIDTH, HEIGHT, screen, high_score
    if selected == "flash":
        idle_chosen, run1_chosen, run2_chosen = idle_img, run1_img, run2_img
        speed_color = (255, 235, 0); bolt_img = bolt_yellow
        speed_bg_raw = fspeed_bg_raw; speed_key = "fspeed"
    elif selected == "reverse":
        idle_chosen, run1_chosen, run2_chosen = idle_rf, run1_rf, run2_rf
        speed_color = (255, 20, 20); bolt_img = bolt_red if bolt_red else bolt_yellow
        speed_bg_raw = rfspeed_bg_raw; speed_key = "rspeed"
    elif selected == "wally":
        idle_chosen, run1_chosen, run2_chosen = idle_ww, run1_ww, run2_ww
        speed_color = (17, 173, 173); bolt_img = bolt_wwlight if bolt_wwlight else bolt_yellow
        speed_bg_raw = wwspeed_bg_raw; speed_key = "wwspeed"
    elif selected == "godspeed":
        idle_chosen, run1_chosen, run2_chosen = idle_god, run1_god, run2_god
        speed_color = (255, 255, 255); bolt_img = bolt_yellow
        speed_bg_raw = godspeed_bg_raw; speed_key = "godspeed"
    else: # jay
        idle_chosen, run1_chosen, run2_chosen = idle_jr, run1_jr, run2_jr
        speed_color = (200, 40, 40); bolt_img = bolt_yellow
        speed_bg_raw = jrspeed_bg_raw; speed_key = "jrspeed"

    idle_chosen_flip = pygame.transform.flip(idle_chosen, True, False)
    run1_chosen_flip = pygame.transform.flip(run1_chosen, True, False)
    run2_chosen_flip = pygame.transform.flip(run2_chosen, True, False)
    BLOCK = 48; ROAR_GAP = 5.1 * BLOCK
    ROAR_DURATION = 5.0

    class Player:
        __slots__ = ('x','y','speed','hold','anim','frame','imgs','imgs_flip','cur','cur_flip','facing_left','vy','jumping','hearts_collected','max_speed_base','lose_blink_timer','lose_blinks','hearts_since_reset')
        def __init__(self):
            self.x = 0; self.y = 0; self.speed = 1; self.hold = 0; self.anim = 0; self.frame = 0
            self.imgs = [run1_chosen, run2_chosen]; self.imgs_flip = [run1_chosen_flip, run2_chosen_flip]
            self.cur = idle_chosen; self.cur_flip = idle_chosen_flip; self.facing_left = True; self.vy = 0; self.jumping = False
            self.hearts_collected = 0; self.max_speed_base = 15.0; self.lose_blink_timer = 0; self.lose_blinks = 0; self.hearts_since_reset = 0
        def get_max_speed(self): return 24.0 if speed_force_active else self.max_speed_base + self.hearts_collected * 1.0
        def update(self, dt, hold_d, ground_y):
            target_max = self.get_max_speed()
            if hold_d:
                self.hold += dt; self.speed = min(target_max, 1.0 + self.hold * 0.68); self.x += self.speed
                self.anim += dt*(1+self.speed*0.15)
                if self.anim > 0.07: self.anim = 0; self.frame = (self.frame+1)%2; self.cur = self.imgs[self.frame]; self.cur_flip = self.imgs_flip[self.frame]
            else:
                self.hold = 0
                if not self.jumping: self.cur = idle_chosen; self.cur_flip = idle_chosen_flip
            if self.jumping:
                self.y += self.vy; self.vy += 0.9
                if self.y >= ground_y: self.y = ground_y; self.jumping = False; self.vy = 0
            else: self.y = ground_y
        def jump(self):
            if not self.jumping: self.jumping = True; self.vy = -17
        def get_draw_img(self): return self.cur_flip if self.facing_left else self.cur

    class BlackFlash:
        __slots__ = ('x','y','gap','target_gap','anim','frame','imgs','cur','visible','throw_timer','sprint_boost','idle_mode')
        def __init__(self):
            self.x = 0; self.y = 0; self.gap = 9*BLOCK; self.target_gap = 9*BLOCK; self.anim = 0; self.frame = 0
            self.imgs = [bf_run1, bf_run2]; self.cur = bf_idle; self.visible = True; self.throw_timer = 0; self.sprint_boost = 0; self.idle_mode = False
        def update(self, dt, player, ground_y, hold_d):
            self.y = ground_y
            if self.idle_mode: self.gap = player.x - self.x; return
            current_gap = player.x - self.x; gap_diff = current_gap - self.target_gap
            if speed_force_active: self.x += player.speed * 0.99 + gap_diff * 0.12
            else:
                if hold_d:
                    if gap_diff > 5: self.sprint_boost = min(12.0, self.sprint_boost + dt*6)
                    else: self.sprint_boost = max(0, self.sprint_boost - dt*4)
                    self.x += player.speed * 0.98 + self.sprint_boost + gap_diff * 0.15
                else: self.x += 7.5 + self.sprint_boost; self.sprint_boost = max(0, self.sprint_boost - dt*2)
            self.gap = player.x - self.x; self.anim += dt*(1.5 + player.speed*0.1)
            if self.anim > 0.07: self.anim = 0; self.frame = (self.frame+1)%2; self.cur = self.imgs[self.frame]
            self.throw_timer -= dt
        def set_gap_for_hits(self, hit_count): self.target_gap = max(3*BLOCK, 9*BLOCK - hit_count * 1*BLOCK)
        def try_throw(self):
            if self.idle_mode: return False
            if speed_force_active: return False
            if self.throw_timer <= 0:
                if random.random() < 0.266767: self.throw_timer = random.uniform(1.5, 2.5); return True
                self.throw_timer = 0.4
            return False

    class Bolt:
        __slots__ = ('x','y','speed')
        def __init__(self, x, y, player_speed): self.x = x; self.y = y; self.speed = player_speed + 35
        def update(self): self.x += self.speed
    class EnemyBolt:
        __slots__ = ('x','y','speed')
        def __init__(self, x, y, player_speed, y_offset=0):
            self.x = x; self.y = y + y_offset; self.speed = player_speed + 6.0
        def update(self): self.x += self.speed
    class BoomBolt:
        __slots__ = ('x','y','speed_out','speed_back','returning','max_dist_past_player')
        def __init__(self, x, y, player_speed):
            self.x = x; self.y = y
            self.speed_out = player_speed + 6.0
            self.speed_back = player_speed + 3.5
            self.returning = False
            self.max_dist_past_player = 400
        def update(self, blackflash_x):
            if not self.returning: self.x += self.speed_out
            else: self.x -= self.speed_back
    class HeartPickup:
        __slots__ = ('x','y')
        def __init__(self, x, ground_y): self.x = x; self.y = ground_y - random.choice([20, 70, 120, 170])

    player = Player(); blackflash = BlackFlash(); cam = 0; bg_fade = 0.0; t_enter = 100
    bolts = []; enemy_bolts = []; boom_bolts = []; heart_pickups = []; heart_timer = 0; distance_km = 0.0
    intro_active = True; intro_stage = 0; intro_timer = 0; roar_played = False; roar_start_time = 0; roar_done = False; game_started = False; hit_counter = 0; music_started = False
    global speed_force_active; speed_force_active = False; speed_force_time = 0; draining = False; drain_timer = 0
    blackflash.x = player.x - 1400; blackflash.target_gap = ROAR_GAP; player.facing_left = True; blackflash.idle_mode = False

    hud_bg_surf = pygame.Surface((340, 95), pygame.SRCALPHA)
    hud_bg_surf.fill((0,0,0,110))
    btn_surf = pygame.Surface((85,85), pygame.SRCALPHA)
    pygame.draw.rect(btn_surf, (0,0,0,130), (0,0,85,85), border_radius=20)
    pygame.draw.rect(btn_surf, (255,255,255,90), (0,0,85,85), 2, border_radius=20)

    def get_buttons():
        w, h = screen.get_size(); size = 85; margin = 15; y = h - size - margin
        return pygame.Rect(margin, y, size, size), pygame.Rect(w//2 - size//2, y, size, size), pygame.Rect(w - size - margin, y, size, size)

    def start_finale_music():
        nonlocal music_started
        if music_started: return True
        for fname in ["finale.ogg", os.path.join(SCRIPT_DIR, "finale.ogg")]:
            if os.path.exists(fname):
                try: pygame.mixer.music.load(fname); pygame.mixer.music.set_volume(1.0); pygame.mixer.music.play(-1); music_started = True; return True
                except: pass
        return False

    def draw_background(cam_x, fade):
        w, h = screen.get_size()
        loop_scaled = get_bg(loop_bg_raw, "loop", w, h)
        if loop_scaled is None:
            screen.fill((20,20,30)); return
        scroll = int(cam_x * 0.5) % w if w>0 else 0
        screen.blit(loop_scaled, (-scroll, 0))
        screen.blit(loop_scaled, (w - scroll, 0))
        if fade > 0:
            speed_scaled = get_bg(speed_bg_raw, speed_key, w, h)
            if speed_scaled:
                speed_scaled.set_alpha(int(fade*255))
                screen.blit(speed_scaled, (-scroll, 0))
                screen.blit(speed_scaled, (w - scroll, 0))
                speed_scaled.set_alpha(255)

    bob_up = True
    bob_timer = 0

    while True:
        dt = clock.tick(60)/1000
        if dt > 0.033: dt = 0.033
        WIDTH, HEIGHT = screen.get_size()
        ground_y = HEIGHT//2 + 50
        btn_d, btn_f, btn_jump = get_buttons()
        hold_d_touch = False; jump_touch = False; fire_touch = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.VIDEORESIZE: 
                 WIDTH, HEIGHT = e.w, e.h
                 screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                 bg_cache["w"]=0
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                mx = e.x * WIDTH if e.type == pygame.FINGERDOWN else e.pos[0]; my = e.y * HEIGHT if e.type == pygame.FINGERDOWN else e.pos[1]
                if btn_d.collidepoint(mx, my): hold_d_touch = True
                if btn_jump.collidepoint(mx, my): jump_touch = True
                if btn_f.collidepoint(mx, my): fire_touch = True
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE and not intro_active: player.jump()
                if e.key == pygame.K_f and not intro_active: bolts.append(Bolt(player.x+65, player.y+28, player.speed))
                if e.key == pygame.K_ESCAPE: 
                     try: pygame.mixer.music.stop()
                     except: pass
                     return "menu"
                if e.key == pygame.K_r: return "retry"
                if e.key == pygame.K_d and intro_stage==1 and roar_done and not game_started:
                    game_started = True; intro_active = False; blackflash.idle_mode = False; blackflash.cur = bf_idle; blackflash.target_gap = 9*BLOCK; blackflash.x = player.x - 9*BLOCK; player.facing_left = False
                    start_finale_music()
        keys = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if btn_d.collidepoint(mx, my): hold_d_touch = True
        hold_d = keys[pygame.K_d] or hold_d_touch
        if hold_d and intro_stage==1 and roar_done and not game_started:
            game_started = True; intro_active = False; blackflash.idle_mode = False; blackflash.cur = bf_idle; blackflash.target_gap = 9*BLOCK; blackflash.x = player.x - 9*BLOCK; player.facing_left = False
            start_finale_music()
        
        if intro_active:
            intro_timer += dt
            if intro_stage == 0:
                blackflash.y = ground_y; blackflash.x += 5.8; blackflash.anim += dt*0.28
                if blackflash.anim > 0.07: blackflash.anim = 0; blackflash.frame = (blackflash.frame+1)%2; blackflash.cur = blackflash.imgs[blackflash.frame]
                player.y = ground_y; player.facing_left = True
                if player.x - blackflash.x <= ROAR_GAP:
                    blackflash.x = player.x - ROAR_GAP; blackflash.idle_mode = True; blackflash.cur = bf_roar; intro_stage = 1; roar_start_time = intro_timer
                    if roar_sound and not roar_played:
                        try: roar_sound.play()
                        except: pass
                        roar_played = True
            elif intro_stage == 1:
                blackflash.y = ground_y; blackflash.x = player.x - ROAR_GAP; blackflash.gap = ROAR_GAP
                roar_elapsed = intro_timer - roar_start_time
                if roar_elapsed < ROAR_DURATION:
                    blackflash.cur = bf_roar; player.facing_left = True
                else: 
                     roar_done = True; blackflash.cur = bf_idle; player.facing_left = False
                player.y = ground_y
        else:
            if game_started:
                if keys[pygame.K_SPACE] or jump_touch: player.jump()
                if keys[pygame.K_f] or fire_touch:
                    if len(bolts)==0 or player.x - bolts[-1].x > 90: bolts.append(Bolt(player.x+65, player.y+28, player.speed))
            player.update(dt, hold_d if game_started else False, ground_y) if game_started else setattr(player, 'y', ground_y)
            blackflash.update(dt, player, ground_y, hold_d if game_started else False)
                 
        cam = player.x - WIDTH//2
        if not intro_active and game_started and not hold_d and not speed_force_active:
            if abs(player.x - blackflash.x) < 50:
                try: pygame.mixer.music.stop()
                except: pass
                res = game_over_screen(f"Hit counter: {hit_counter}/4", distance_km); return res

        if not intro_active and game_started and hold_d and not speed_force_active:
            if blackflash.try_throw():
                boom_chance = 0.2111 if distance_km >= 200 else 0.1411
                double_chance = 0.25 if distance_km >= 500 else 0.15
                if random.random() < boom_chance:
                    boom_bolts.append(BoomBolt(blackflash.x + 40, blackflash.y + 28, player.speed))
                else:
                    if random.random() < double_chance:
                        enemy_bolts.append(EnemyBolt(blackflash.x + 40, blackflash.y + 22, player_speed=player.speed, y_offset=-6))
                        enemy_bolts.append(EnemyBolt(blackflash.x + 15, blackflash.y + 22, player_speed=player.speed, y_offset=6))
                    else:
                        enemy_bolts.append(EnemyBolt(blackflash.x + 40, blackflash.y + 28, player_speed=player.speed))

        if not intro_active and game_started and hold_d:
            boost = 8.0 if speed_force_active else 1.0; distance_km += (player.speed * dt / 18.0) * boost
        save_highscore(distance_km)
                 
        MAX_HEARTS = 9
        if not intro_active and game_started and not speed_force_active and player.hearts_collected < MAX_HEARTS:
            heart_timer -= dt
            if heart_timer <= 0 and len(heart_pickups) < 2:
                heart_pickups.append(HeartPickup(player.x + WIDTH + random.randint(200,500), ground_y)); heart_timer = random.uniform(1.2, 2.0)

        for hp in heart_pickups[:]:
            if hp.x < player.x - 500: heart_pickups.remove(hp); continue
            if abs(hp.x - player.x) < 45 and abs(hp.y - player.y) < 55:
                if player.hearts_collected < MAX_HEARTS and not speed_force_active:
                    player.hearts_collected += 1; player.hearts_since_reset += 1
                    if player.hearts_since_reset >= 2:
                        blackflash.target_gap = min(10*BLOCK, blackflash.target_gap + 1*BLOCK)
                        if hit_counter > 0: hit_counter -= 1; blackflash.set_gap_for_hits(hit_counter)
                        player.hearts_since_reset = 0
                heart_pickups.remove(hp); continue
            for b in bolts[:]:
                if abs(b.x - hp.x) < 40 and abs(b.y - hp.y) < 40:
                    if player.hearts_collected < MAX_HEARTS and not speed_force_active:
                        player.hearts_collected += 1; player.hearts_since_reset += 1
                        if player.hearts_since_reset >= 2:
                            blackflash.target_gap = min(10*BLOCK, blackflash.target_gap + 1*BLOCK)
                            if hit_counter > 0: hit_counter -= 1; blackflash.set_gap_for_hits(hit_counter)
                            player.hearts_since_reset = 0
                    heart_pickups.remove(hp)
                    if b in bolts: bolts.remove(b)
                    break

        for eb in enemy_bolts[:]:
            eb.update()
            if eb.x > player.x + 200 or eb.x > player.x + WIDTH + 200: enemy_bolts.remove(eb); continue
            if abs(eb.x - player.x) < 40 and abs(eb.y - player.y) < 50:
                player.speed = max(1, player.speed - 2); player.hold = max(0, player.hold - 1); player.hearts_collected = max(0, player.hearts_collected - 1)
                hit_counter += 1; blackflash.set_gap_for_hits(hit_counter); enemy_bolts.remove(eb)
                if hit_counter >= 4:
                    try: pygame.mixer.music.stop()
                    except: pass
                    res = game_over_screen(f"You have been speared a lot. Ouch.", distance_km); return res

        for boom in boom_bolts[:]:
            boom.update(blackflash.x)
            if abs(boom.x - player.x) < 42 and abs(boom.y - player.y) < 52:
                player.speed = max(1, player.speed - 2); player.hold = max(0, player.hold - 1); player.hearts_collected = max(0, player.hearts_collected - 1)
                hit_counter += 1; blackflash.set_gap_for_hits(hit_counter); boom_bolts.remove(boom)
                if hit_counter >= 4:
                    try: pygame.mixer.music.stop()
                    except: pass
                    res = game_over_screen(f"You have been BOOMED. Ouch.", distance_km); return res
                continue
            if not boom.returning and boom.x > player.x + boom.max_dist_past_player: boom.returning = True
            if boom.returning and boom.x <= blackflash.x + 10: boom_bolts.remove(boom)

        if not intro_active and game_started and not speed_force_active and not draining and player.hearts_collected >= MAX_HEARTS:
            speed_force_active = True; speed_force_time = 15.0; t_enter = 0; heart_pickups.clear(); hit_counter = 0; blackflash.set_gap_for_hits(hit_counter); player.hearts_since_reset = 0
            enemy_bolts.clear(); boom_bolts.clear()
        if speed_force_active:
            speed_force_time -= dt; bg_fade = min(1.0, bg_fade + dt*0.8)
            if speed_force_time <= 0:
                speed_force_active = False; draining = True; drain_timer = 0.2; heart_timer = 0
                blackflash.target_gap = 9*BLOCK; blackflash.sprint_boost = 8; blackflash.visible = True; blackflash.idle_mode = False
        else:
            if draining: bg_fade = max(0.0, bg_fade - dt*0.6)
            else: bg_fade = max(0.0, bg_fade - dt*1.2)
        if draining:
            drain_timer -= dt
            if drain_timer <= 0 and player.hearts_collected > 0:
                player.hearts_collected -= 1; drain_timer = 1.2
                if player.hearts_collected == 0: 
                     draining = False; heart_timer = 0

        for b in bolts[:]:
            b.update()
            if b.x > player.x + WIDTH + 400: bolts.remove(b)

        draw_background(cam, bg_fade)

        bob_timer += dt
        if bob_timer > 0.3: bob_timer = 0; bob_up = not bob_up
        bob = 4 if bob_up else -4

        for hp in heart_pickups:
            sx = hp.x - cam
            if -80 < sx < WIDTH+80: screen.blit(heart_img, (sx, hp.y + bob))
        for blt in bolts:
            sx = blt.x - cam
            screen.blit(bolt_img, (sx, blt.y))
        for eb in enemy_bolts:
            sx = eb.x - cam
            screen.blit(bolt_bf, (sx, eb.y))
        for boom in boom_bolts:
            sx = boom.x - cam
            if boom_img:
                img = pygame.transform.flip(boom_img, True, False) if boom.returning else boom_img
                screen.blit(img, (sx, boom.y))
            else:
                pygame.draw.circle(screen, (255,200,0), (int(sx), int(boom.y)), 12)
        bf_sx = blackflash.x - cam
        if -200 < bf_sx < WIDTH+200: screen.blit(blackflash.cur, (bf_sx, blackflash.y + Y_OFFSET))
        screen.blit(player.get_draw_img(), (WIDTH//2 - CHAR_W//2, player.y + Y_OFFSET))

        screen.blit(hud_bg_surf, (8,8))
        screen.blit(font.render(f"SPEED: {player.speed:.1f} / {player.get_max_speed():.1f}", True, (255,255,255)), (14, 12))
        mult = " 5X!" if speed_force_active else ""
        screen.blit(small_font.render(f"DIST: {distance_km:.2f} Mm{mult}  BEST: {high_score:.2f}  HITS: {hit_counter}/4", True, (255,255,255)), (14, 36))
        for i in range(9):
            hx = 14 + i * 30; hy = 58
            if i < player.hearts_collected and heart_img_small:
                screen.blit(heart_img_small, (hx, hy))
            else:
                pygame.draw.circle(screen, (70,70,70), (hx+10, hy+10), 7, 2)

        def draw_btn(rect, label):
            screen.blit(btn_surf, (rect.x, rect.y))
            t = small_font.render(label, True, (255,255,255)); screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))
        draw_btn(btn_d, "D RUN"); draw_btn(btn_f, "F FIRE"); draw_btn(btn_jump, "JUMP")

        def draw_text_with_bg(text_str, font_obj, y):
            txt = font_obj.render(text_str, True, (255,255,255)); bg_s = pygame.Surface((txt.get_width()+20, txt.get_height()+8), pygame.SRCALPHA); bg_s.fill((0,0,0,180))
            screen.blit(bg_s, (WIDTH//2 - txt.get_width()//2 -10, y-4)); screen.blit(txt, (WIDTH//2 - txt.get_width()//2, y))
        if intro_stage == 0 and intro_active: draw_text_with_bg("Something is coming", menu_font, HEIGHT//2 - 100)
        elif intro_stage == 1 and intro_active:
            if not roar_done: draw_text_with_bg("It's here...", menu_font, HEIGHT//2 - 100)
            else: draw_text_with_bg("Press D to RUN!", menu_font, HEIGHT//2 - 100)
        if speed_force_active:
            t_enter += dt
            if t_enter < 2.3:
                draw_text_with_bg("Entering Speed force!!", menu_font, HEIGHT//2-110)
            elif t_enter >= 2.3:
                box_w, box_h = 420, 55
                bx = WIDTH//2 - box_w//2; by = 140
                pygame.draw.rect(screen, (0,0,0), (bx, by, box_w, box_h), border_radius=12)
                pygame.draw.rect(screen, speed_color, (bx, by, box_w, box_h), 3, border_radius=12)
                timer_txt = font_18.render(f"SPEED FORCE ACTIVE! {int(speed_force_time)+1}s", True, speed_color)
                screen.blit(timer_txt, (WIDTH//2 - timer_txt.get_width()//2, by+16))
        if draining:
            player.lose_blink_timer += dt
            if player.lose_blinks < 3:
                if int(pygame.time.get_ticks() / 500) % 2 == 0: draw_text_with_bg("Losing momentum...", small_font, HEIGHT//2-50)
                if player.lose_blink_timer >= 1.0: player.lose_blink_timer = 0; player.lose_blinks += 1
        pygame.display.flip()

while True:
    sel = character_select()
    result = game_loop(sel)
    if result in ("retry","menu"):
        try: pygame.mixer.music.stop()
        except: pass
        continue
