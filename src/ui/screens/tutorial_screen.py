from __future__ import annotations
import os
import pygame

from ui.components.button import Button


class TutorialScreen:

    def __init__(self, screen, steps, current_step: int = 0,):

        self.screen = screen
        self.steps = steps
        self.current_step = current_step

        self.width = screen.get_width()
        self.height = screen.get_height()

        self.background_color = (255, 235, 250)
        self.panel_color = (255, 245, 255)
        self.border_color = (217, 2, 192)
        self.text_color = (82, 26, 75)
        self.shadow_color = (130, 70, 120)

        self.title_font = pygame.font.Font("assets/fonts/title_font.ttf", 120)

        self.header_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 42)

        self.text_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 26)

        self.small_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 22)

        self.tiny_font = pygame.font.Font("assets/fonts/Pacifico.ttf", 18)

        self.next_button = Button("Next", self.width - 260, self.height - 110, 190, 60)

        self.back_button = Button("Back", 70, self.height - 110, 190, 60)

        self.skip_button = Button("Skip", self.width - 180, 40, 120, 45)

        self.image_cache = {}

    def update_step(self, current_step: int):

        self.current_step = current_step

    def get_current_step_data(self) -> dict:

        step = self.steps[self.current_step]

        return {**step, "is_first": self.current_step == 0, "is_last": self.current_step == len(self.steps) - 1, "progress": f"{self.current_step + 1} / {len(self.steps)}",}

    def handle_event(self, event):

        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        if event.button != 1:
            return None

        step_data = self.get_current_step_data()

        if self.skip_button.is_clicked(event):
            return "skip"

        if not step_data["is_first"]:
            if self.back_button.is_clicked(event):
                return "back"

        if self.next_button.is_clicked(event):
            return "next"

        return None

    def load_tutorial_image(self, image_name: str):

        if image_name in self.image_cache:
            return self.image_cache[image_name]

        possible_paths = [f"assets/images/tutorial/{image_name}.png",
            f"assets/images/tutorial/{image_name}.jpg",
            f"assets/images/{image_name}.png",
            f"assets/images/{image_name}.jpg",]

        for path in possible_paths:

            if os.path.exists(path):

                image = pygame.image.load(path).convert_alpha()

                self.image_cache[image_name] = image

                return image

        self.image_cache[image_name] = None

        return None

    def draw(self):

        step_data = self.get_current_step_data()

        self.screen.fill(self.background_color)

        self.draw_title()

        self.draw_main_panel(step_data)

        self.draw_image_area(step_data)

        self.draw_text_area(step_data)

        self.draw_progress(step_data)

        self.draw_buttons(step_data)

    def draw_title(self):

        shadow = self.title_font.render("Tutorial", True, self.shadow_color)

        title = self.title_font.render("Tutorial", True, self.border_color)

        shadow_rect = shadow.get_rect(center=(self.width // 2, 75))

        title_rect = title.get_rect(center=(self.width // 2, 72))

        self.screen.blit(shadow, shadow_rect)

        self.screen.blit(title, title_rect)

    def draw_main_panel(self, step_data: dict):

        panel_rect = pygame.Rect(90, 130, self.width - 180, self.height - 270)

        pygame.draw.rect(self.screen, self.panel_color, panel_rect, border_radius=28)

        pygame.draw.rect(self.screen, self.border_color, panel_rect, width=4, border_radius=28)

        step_number_text = self.small_font.render(f"Step {step_data['progress']}", True, self.text_color)

        self.screen.blit(step_number_text, (panel_rect.x + 35, panel_rect.y + 20))

    def draw_image_area(self, step_data: dict):

        image_rect = pygame.Rect(130, 220, 500, 360)

        pygame.draw.rect(self.screen, (255, 255, 255), image_rect, border_radius=22)

        pygame.draw.rect(self.screen, self.border_color, image_rect, width=3, border_radius=22)

        image_name = step_data.get("image")

        image = None

        if image_name is not None:
            image = self.load_tutorial_image(image_name)

        if image is not None:

            image = pygame.transform.smoothscale(image,(image_rect.width - 30, image_rect.height - 30))

            self.screen.blit(image, (image_rect.x + 15, image_rect.y + 15))

        else:

            self.draw_placeholder_image(image_rect, step_data)

    def draw_placeholder_image(self, image_rect, step_data: dict):

        highlight = step_data.get("highlight")

        if highlight is None:
            label = "LEFT NO CRUMBS"
        else:
            label = highlight.replace("_", " ").upper()

        text = self.header_font.render(label, True, self.text_color)

        text_rect = text.get_rect(center=image_rect.center)

        self.screen.blit(text, text_rect)

        hint = self.tiny_font.render("image placeholder", True,self.shadow_color)

        hint_rect = hint.get_rect(center=(image_rect.centerx, image_rect.centery + 50))

        self.screen.blit(hint, hint_rect)

    def draw_text_area(self, step_data: dict):

        title_text = step_data.get("title", "")

        body_text = step_data.get("text", "")

        title_surface = self.header_font.render(title_text, True, self.text_color)

        self.screen.blit(title_surface, (690, 230))

        lines = self.wrap_text(body_text, self.text_font, 600)

        y = 310

        for line in lines:

            text_surface = self.text_font.render(line, True, self.text_color)

            self.screen.blit(text_surface, (690, y))

            y += 42

        highlight = step_data.get("highlight")

        if highlight is not None:

            highlight_text = self.small_font.render(f"Focus: {highlight.replace('_', ' ')}", True, self.border_color)

            self.screen.blit(highlight_text, (690, y + 35))

    def draw_progress(self, step_data: dict):

        progress_text = self.small_font.render(step_data["progress"], True, self.text_color)

        progress_rect = progress_text.get_rect(center=(self.width // 2, self.height - 82))

        self.screen.blit(progress_text, progress_rect)

        dot_start_x = self.width // 2 - 70
        dot_y = self.height - 45

        for i in range(len(self.steps)):

            if i == self.current_step:
                color = self.border_color
                radius = 9
            else:
                color = (180, 150, 175)
                radius = 6

            pygame.draw.circle(self.screen, color, (dot_start_x + i * 28, dot_y), radius)

    def draw_buttons(self, step_data: dict):

        if not step_data["is_first"]: self.back_button.draw(self.screen)

        if step_data["is_last"]:

            finish_text = "Finish"

            old_text = self.next_button.text
            self.next_button.text = finish_text

            self.next_button.draw(self.screen)

            self.next_button.text = old_text

        else:

            self.next_button.draw(self.screen)

        self.skip_button.draw(self.screen)

    def wrap_text(self, text: str, font, max_width: int):

        words = text.split()
        lines = []
        current_line = ""

        for word in words:

            test_line = word if current_line == "" else current_line + " " + word

            test_width = font.size(test_line)[0]

            if test_width <= max_width:

                current_line = test_line

            else:

                if current_line:
                    lines.append(current_line)

                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
