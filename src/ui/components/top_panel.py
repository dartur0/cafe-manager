from __future__ import annotations
import pygame

from ui.components.progress_bar import ProgressBar


class TopPanel:

    def __init__(
        self,
        screen,
        title_font,
        font,
        small_font,
        star_icon,
    ):

        self.screen = screen

        self.title_font = title_font
        self.font = font
        self.small_font = small_font

        self.star_icon = star_icon

        width = screen.get_width()

        self.progress_bar = ProgressBar(
            width - 530,
            45,
            420,
            18
        )

    def draw(
        self,
        day_number,
        time_left,
        money,
        state
    ):

        served_count = 0
        quality_progress = 0.0

        if state is not None:

            served_count = state.served_count

            if served_count > 0:
                quality_progress = state._patience_sum / served_count

        quality_progress = max(
            0.0,
            min(1.0, quality_progress)
        )

        bar_rect = self.progress_bar.rect

        day_text = self.title_font.render(
            f"Day {day_number}",
            True,
            (217, 2, 192)
        )

        day_rect = day_text.get_rect(
            midright=(
                bar_rect.x - 20,
                bar_rect.centery
            )
        )

        self.screen.blit(
            day_text,
            day_rect
        )

        self.progress_bar.draw(
            self.screen,
            quality_progress,
            1.0
        )

        star_ratios = [
            0.25,
            0.50,
            0.75,
        ]

        for ratio in star_ratios:

            x = bar_rect.x + int(bar_rect.width * ratio)
            y = bar_rect.y + bar_rect.height // 2

            star_rect = self.star_icon.get_rect(
                center=(
                    x,
                    y
                )
            )

            self.screen.blit(
                self.star_icon,
                star_rect
            )

        timer_text = self.font.render(
            f"{int(time_left)}s",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            timer_text,
            (
                105,
                30
            )
        )

        money_text = self.font.render(
            f"${int(money)}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            money_text,
            (
                105,
                68
            )
        )

        served_text = self.small_font.render(
            f"served: {served_count}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            served_text,
            (
                bar_rect.x,
                bar_rect.y + 28
            )
        )
