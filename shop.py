import pygame
from helper import resource_path, character_images
from saves import get_coins, save_coins
from play import clock
import sys

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.DOUBLEBUF)

FONT = pygame.font.Font(resource_path("assets/font/font.ttf"), 64)
fontTxt = pygame.font.Font(resource_path("assets/font/font.ttf"), 20)

shop_ui = pygame.image.load(resource_path("assets/image/shop-ui.png")).convert()
shop_ui = pygame.transform.scale(shop_ui, (WIDTH // 2 + 200, HEIGHT // 2 + 150))
shop_ui_rect = shop_ui.get_rect(center=(WIDTH // 2, HEIGHT // 2))

close_img = pygame.image.load(resource_path("assets/image/X.png")).convert_alpha()
close_img = pygame.transform.scale(close_img, (40, 40))
close_rect = close_img.get_rect(topright=(WIDTH // 2 + 290, HEIGHT // 2 - 215))

selected_character = "default"
owned_characters = {"default"}

character_costs = {
    "default": 0,
    "Blue": 10,
    "Yellow": 10,
    "Green": 10,
    "Glitch": 30,
    "Navy": 25
}
player_coins = get_coins()

def confirm_purchase(name, cost):
    """
    Draws a blocking confirmation dialog asking if the player wants to purchase the character.
    Returns True if the player presses 'Y' ; False if 'N'.
    """
    small_ui = shop_ui.copy()
    small_width = int(shop_ui_rect.width * 0.5)
    small_height = int(shop_ui_rect.height * 0.5)
    small_ui = pygame.transform.scale(small_ui, (small_width, small_height))
    small_rect = small_ui.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    SCREEN.blit(small_ui, small_rect)

    question_text = fontTxt.render(f"Buy {name} for {cost} coins?", True, (255, 255, 255))
    question_rect = question_text.get_rect(center=(small_rect.centerx, small_rect.top + 40))
    SCREEN.blit(question_text, question_rect)

    yes_btn = pygame.image.load(resource_path("assets/image/Yes.png")).convert_alpha()
    no_btn = pygame.image.load(resource_path("assets/image/No.png")).convert_alpha()

    yes_btn = pygame.transform.scale(yes_btn, (85, 45))
    no_btn = pygame.transform.scale(no_btn, (85, 45))

    yes_rect = yes_btn.get_rect(center=(small_rect.centerx - 50, small_rect.top + 80))
    no_rect = no_btn.get_rect(center=(small_rect.centerx + 50, small_rect.top + 80))

    SCREEN.blit(yes_btn, yes_rect)
    SCREEN.blit(no_btn, no_rect)

    pygame.display.flip()

    waiting = True

    while waiting:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if yes_rect.collidepoint(event.pos):
                return True
            elif no_rect.collidepoint(event.pos):
                return False

def draw_shop(scroll_offset):
    SCREEN.blit(shop_ui, shop_ui_rect)

    title_text = FONT.render("Character Shop", True, (255, 255, 255))
    title_rect = title_text.get_rect(midtop=(shop_ui_rect.centerx, shop_ui_rect.top + 30))
    SCREEN.blit(title_text, title_rect)

    SCREEN.blit(close_img, close_rect)

    coins_text = fontTxt.render(f"Coins: {player_coins}", True, (255, 255, 255))
    coins_rect = coins_text.get_rect(midtop=(shop_ui_rect.centerx, shop_ui_rect.top + 10))
    SCREEN.blit(coins_text, coins_rect)

    selection_width = shop_ui_rect.width - 40
    selection_height = shop_ui_rect.height - 120
    selection_area = pygame.Surface((selection_width, selection_height), pygame.SRCALPHA)
    selection_area.fill((0, 0, 0, 0))
    start_y = 20

    for index, (name, image) in enumerate(character_images.items()):
        y_pos = start_y + (index * 100) + scroll_offset

        if 0 <= y_pos <= selection_height - 70:
            character_rect = image.get_rect(center=(selection_width // 2, y_pos))
            selection_area.blit(image, character_rect)

            if name in owned_characters:
                cost_text = fontTxt.render("Owned", True, (0, 255, 0))
            else:
                cost_text = fontTxt.render(f"{character_costs[name]} Coins", True, (255, 215, 0))
            cost_rect = cost_text.get_rect(midtop=(character_rect.centerx, character_rect.bottom + 5))
            selection_area.blit(cost_text, cost_rect)

            if name == selected_character:
                pygame.draw.rect(selection_area, (255, 215, 0), character_rect.inflate(10, 10), 3)

    selection_area_rect = selection_area.get_rect(center=(shop_ui_rect.centerx, shop_ui_rect.centery + 30))
    SCREEN.blit(selection_area, selection_area_rect)

    pygame.display.flip()

def character_shop(state):
    global selected_character, owned_characters, player_coins

    scroll_offset = 0
    target_scroll = scroll_offset
    running = True

    smoothing_factor = 5.0

    while running:
        dt = clock.tick(60) / 1000.0

        scroll_diff = target_scroll - scroll_offset
        if abs(scroll_diff) < 1:
            scroll_offset = target_scroll
        else:
            scroll_offset += scroll_diff * min(dt * smoothing_factor, 1)

        draw_shop(scroll_offset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    target_scroll -= 50
                elif event.key == pygame.K_UP:
                    target_scroll += 50
                elif event.key == pygame.K_ESCAPE:
                    state["current"] = "menu"
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    target_scroll += 50
                elif event.button == 5:
                    target_scroll -= 50
                elif event.button == 1:
                    if event.button == 1 and close_rect.collidepoint(event.pos):
                        state["current"] = "menu"
                        running = False
                    else:
                        selection_width = shop_ui_rect.width - 40
                        selection_height = shop_ui_rect.height - 120
                        start_y = 20

                        seletion_area_rect = pygame.Rect(0, 0, selection_width, selection_height)
                        seletion_area_rect.center = (shop_ui_rect.centerx, shop_ui_rect.centery + 30)

                        local_click = (int(event.pos[0] - seletion_area_rect.x),
                                       int(event.pos[1] - seletion_area_rect.y))

                        for index, (name, image) in enumerate(character_images.items()):
                            y_pos = start_y + (index * 100) + scroll_offset

                            if y_pos < 0 or y_pos > selection_height - 70:
                                continue

                            character_rect = image.get_rect(center=(selection_width // 2, y_pos))

                            if character_rect.collidepoint(local_click):
                                if name in owned_characters:
                                    selected_character = name
                                else:
                                    if player_coins >= character_costs[name]:
                                        if confirm_purchase(name, character_costs[name]):
                                            player_coins -= character_costs[name]
                                            owned_characters.add(name)
                                            selected_character = name
                                        else:
                                            print("User declined purchase!!")
                                            pass
                                    else:
                                        print("Insufficient coins!!")
                                        pass

        min_scroll = -100 * (len(character_images) - 3)
        target_scroll = max(min(target_scroll, 25), min_scroll)

    return state