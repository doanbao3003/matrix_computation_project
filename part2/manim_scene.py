# -*- coding: utf-8 -*-
"""
File: manim_scene_revised.py
Người làm: Đoàn Bảo

Nhiệm vụ:
- Tạo video Manim minh họa:
    1. Chéo hóa
    2. SVD
    3. Hình học SVD
    4. Ứng dụng

"""

from manim import *
import math
import unicodedata

config.background_color = BLACK
config.frame_rate = 30
config.pixel_width = 1280
config.pixel_height = 720


class SVDScene(Scene):
    """
    Video Manim được nâng cấp có kiểm soát.
    - Giữ tinh thần phần chéo hóa và phần SVD gốc
    - Mở rộng rất mạnh phần ứng dụng
    - Không dùng bất kỳ công cụ đại số tuyến tính dựng sẵn nào
    - Tất cả minh họa ma trận ảnh dùng list Python thuần
    """

    PACE = 1.08
    SAFE_TOP = 0.55
    SAFE_BOTTOM = 0.85
    SAFE_SIDE = 0.45
    TITLE_BUFF = 0.26
    SUBTITLE_BUFF = 0.18
    BODY_BUFF = 0.36
    SMALL_GAP = 0.16
    MEDIUM_GAP = 0.24
    LARGE_GAP = 0.36
    FONT_CANDIDATES = [
        "Segoe UI",
        "Arial",
        "Tahoma",
        "Calibri",
        "DejaVu Sans",
        "Noto Sans",
        "Liberation Sans",
    ]

    # --------------------------------------------------------------
    # Khối thời lượng tổng quát
    # --------------------------------------------------------------
    TIMING = {
        "opening": 1.1,
        "diag_12": 1.0,
        "diag_3a": 1.0,
        "diag_3b": 1.0,
        "diag_4": 1.0,
        "bridge": 1.0,
        "geometry": 1.0,
        "img_1": 1.0,
        "img_2": 1.0,
        "img_3": 1.0,
        "img_4": 1.0,
        "img_5": 1.0,
        "img_6": 1.0,
        "img_7": 1.0,
        "img_8": 1.0,
        "img_9": 1.0,
        "img_10": 1.0,
        "img_11": 1.0,
        "pca_1": 1.0,
        "pca_2": 1.0,
        "pca_3": 1.0,
        "lsa_1": 1.0,
        "lsa_2": 1.0,
        "lsa_3": 1.0,
        "rec_1": 1.0,
        "rec_2": 1.0,
        "rec_3": 1.0,
        "noise_1": 1.0,
        "noise_2": 1.0,
        "noise_3": 1.0,
        "face_1": 1.0,
        "face_2": 1.0,
        "extra_1": 1.0,
        "extra_2": 1.0,
        "summary": 1.0,
    }


    # --------------------------------------------------------------
    # Chuẩn hóa văn bản và font
    # --------------------------------------------------------------
    def vi(self, s: str) -> str:
        return unicodedata.normalize("NFC", s)

    def pick_font(self) -> str:
        try:
            fonts = set(Text.font_list())
            for name in self.FONT_CANDIDATES:
                if name in fonts:
                    return name
        except Exception:
            pass
        return "Arial"

    def VText(
        self,
        s: str,
        *,
        font_size: float = 32,
        color=WHITE,
        weight=NORMAL,
        line_spacing: float = -1,
        **kwargs,
    ) -> Text:
        return Text(
            self.vi(s),
            font=self.pick_font(),
            font_size=font_size,
            color=color,
            weight=weight,
            line_spacing=line_spacing,
            disable_ligatures=True,
            **kwargs,
        )

    def W(self, seconds: float) -> None:
        pace = getattr(self, "current_pace", self.PACE)
        self.wait(seconds * pace)

    def wipe(self, run_time: float = 0.55) -> None:
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)
            self.remove(*mobs)
        self.clear()

    def reveal_text(self, t: Mobject, *, rt: float = 0.75) -> None:
        self.play(FadeIn(t, shift=UP * 0.10), run_time=rt)

    def reveal_group(self, g: Mobject, *, rt: float = 0.75) -> None:
        self.play(FadeIn(g, shift=UP * 0.08), run_time=rt)

    def write_math(self, m: Mobject, *, rt: float = 0.85) -> None:
        self.play(Write(m), run_time=rt)

    def draw_then_wait(self, mob: Mobject, *, rt: float = 0.7, wt: float = 0.2) -> None:
        self.play(Create(mob), run_time=rt)
        self.W(wt)

    def fade_then_wait(self, mob: Mobject, *, rt: float = 0.7, wt: float = 0.2) -> None:
        self.play(FadeIn(mob), run_time=rt)
        self.W(wt)

    def keep_inside_safe(self, mob: Mobject) -> Mobject:
        max_w = config.frame_width - 2 * self.SAFE_SIDE
        max_h = config.frame_height - self.SAFE_TOP - self.SAFE_BOTTOM
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)

        left_limit = -config.frame_width / 2 + self.SAFE_SIDE
        right_limit = config.frame_width / 2 - self.SAFE_SIDE
        top_limit = config.frame_height / 2 - self.SAFE_TOP
        bottom_limit = -config.frame_height / 2 + self.SAFE_BOTTOM

        dx = 0
        dy = 0

        if mob.get_left()[0] < left_limit:
            dx = left_limit - mob.get_left()[0]
        if mob.get_right()[0] > right_limit:
            dx = right_limit - mob.get_right()[0]
        if mob.get_top()[1] > top_limit:
            dy = top_limit - mob.get_top()[1]
        if mob.get_bottom()[1] < bottom_limit:
            dy = bottom_limit - mob.get_bottom()[1]

        mob.shift(RIGHT * dx + UP * dy)
        return mob

    def top_title(self, title: str, subtitle: str = "", color=BLUE_B):
        title_mob = self.VText(title, font_size=48, color=color, weight=BOLD)
        title_mob.to_edge(UP, buff=self.TITLE_BUFF)
        if subtitle:
            sub = self.VText(subtitle, font_size=28, color=GREY_B)
            sub.next_to(title_mob, DOWN, buff=self.SUBTITLE_BUFF)
            sub.align_to(title_mob, LEFT)
        else:
            sub = VGroup()
        self.keep_inside_safe(VGroup(title_mob, sub))
        return title_mob, sub

    def section_header(self, small_title: str, full_title: str):
        main_title = self.VText(full_title, font_size=47, color=BLUE_B, weight=BOLD)
        main_title.to_edge(UP, buff=self.TITLE_BUFF)
        small = self.VText(small_title, font_size=29, color=GREEN_B, weight=BOLD)
        small.next_to(main_title, DOWN, buff=0.18)
        small.align_to(main_title, LEFT)
        self.keep_inside_safe(VGroup(main_title, small))
        return main_title, small

    def paragraph_block(self, texts, *, font_size=29, color=WHITE, width=11.0, aligned_edge=LEFT):
        items = []
        for text in texts:
            t = self.VText(text, font_size=font_size, color=color)
            items.append(t)
        group = VGroup(*items).arrange(DOWN, aligned_edge=aligned_edge, buff=0.20)
        if group.width > width:
            group.scale_to_fit_width(width)
        return group

    def bullet_block(self, texts, *, font_size=28, color=WHITE, width=10.8):
        lines = []
        for text in texts:
            t = self.VText("• " + text, font_size=font_size, color=color)
            lines.append(t)
        group = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if group.width > width:
            group.scale_to_fit_width(width)
        return group

    def simple_panel(self, inner: Mobject, *, width: float = 4.3, height: float = 1.3, color=GREY_B):
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            stroke_color=color,
            stroke_width=2.2,
        )
        inner.move_to(box.get_center())
        group = VGroup(box, inner)
        return group

    def note_box(self, text: str, *, font_size: float = 26, width: float = 11.0, color=YELLOW_B):
        content = self.VText(text, font_size=font_size, color=color)
        if content.width > width - 0.5:
            content.scale_to_fit_width(width - 0.5)
        bg = RoundedRectangle(
            width=max(width, content.width + 0.4),
            height=content.height + 0.28,
            corner_radius=0.14,
            stroke_color=color,
            stroke_width=1.8,
        )
        content.move_to(bg.get_center())
        return VGroup(bg, content)

    def make_math_label_pair(self, math_tex: str, text: str, *, math_scale: float = 0.9, font_size: float = 23):
        math_mob = MathTex(math_tex).scale(math_scale)
        text_mob = self.VText(text, font_size=font_size)
        pair = VGroup(math_mob, text_mob).arrange(DOWN, buff=0.10)
        return pair

    def line_separator(self, width: float = 11.2, color=GREY_C):
        return Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=1.5)

    def build_two_column(self, left: Mobject, right: Mobject, *, gap: float = 0.60):
        group = VGroup(left, right).arrange(RIGHT, buff=gap, aligned_edge=UP)
        self.keep_inside_safe(group)
        return group

    def build_three_column(self, a: Mobject, b: Mobject, c: Mobject, *, gap: float = 0.35):
        group = VGroup(a, b, c).arrange(RIGHT, buff=gap, aligned_edge=UP)
        self.keep_inside_safe(group)
        return group

    def spacer(self, height: float = 0.15):
        return Rectangle(width=0.01, height=height, fill_opacity=0.0, stroke_opacity=0.0)

    # --------------------------------------------------------------
    # Các helper ma trận và bảng minh họa
    # --------------------------------------------------------------
    def diag_matrix(self):
        return MathTex(r"A=\begin{pmatrix}2&1&0\\1&2&0\\0&0&4\end{pmatrix}").scale(0.95)

    def cell_color_from_value(self, value: int):
        if value <= 15:
            return BLACK
        if value <= 35:
            return GREY_E
        if value <= 55:
            return GREY_D
        if value <= 75:
            return GREY_C
        if value <= 95:
            return GREY_B
        return WHITE

    def pixel_square(self, value: int, size: float = 0.32):
        fill = self.cell_color_from_value(value)
        sq = Square(side_length=size)
        sq.set_stroke(color=GREY_A, width=0.8, opacity=0.55)
        sq.set_fill(fill, opacity=1.0)
        return sq

    def matrix_to_pixel_group(
        self,
        values,
        *,
        cell_size: float = 0.32,
        show_numbers: bool = False,
        number_font_size: float = 16,
    ):
        rows = []
        for row in values:
            cols = []
            for value in row:
                sq = self.pixel_square(value, size=cell_size)
                if show_numbers:
                    number_color = BLACK if value > 85 else WHITE
                    txt = self.VText(str(value), font_size=number_font_size, color=number_color)
                    txt.move_to(sq.get_center())
                    cols.append(VGroup(sq, txt))
                else:
                    cols.append(sq)
            row_group = VGroup(*cols).arrange(RIGHT, buff=0)
            rows.append(row_group)
        matrix_group = VGroup(*rows).arrange(DOWN, buff=0)
        outline = SurroundingRectangle(matrix_group, color=GREY_B, buff=0.04, stroke_width=1.5)
        return VGroup(matrix_group, outline)

    def labeled_matrix_visual(
        self,
        values,
        title: str,
        subtitle: str = "",
        *,
        cell_size: float = 0.30,
        show_numbers: bool = False,
    ):
        title_mob = self.VText(title, font_size=25, color=YELLOW_B, weight=BOLD)
        matrix_mob = self.matrix_to_pixel_group(values, cell_size=cell_size, show_numbers=show_numbers)
        if subtitle:
            subtitle_mob = self.VText(subtitle, font_size=19, color=GREY_B)
            group = VGroup(title_mob, matrix_mob, subtitle_mob).arrange(DOWN, buff=0.10)
        else:
            group = VGroup(title_mob, matrix_mob).arrange(DOWN, buff=0.10)
        return group

    def table_cell(self, text: str, *, width: float = 1.15, height: float = 0.55, fill_color=BLACK, text_size: float = 20):
        box = Rectangle(width=width, height=height)
        box.set_stroke(color=GREY_A, width=1.5)
        box.set_fill(fill_color, opacity=1.0)
        txt_color = WHITE
        txt = self.VText(text, font_size=text_size, color=txt_color)
        if txt.width > width - 0.08:
            txt.scale_to_fit_width(width - 0.08)
        if txt.height > height - 0.06:
            txt.scale_to_fit_height(height - 0.06)
        txt.move_to(box.get_center())
        return VGroup(box, txt)

    def build_table(self, data, *, cell_width: float = 1.15, cell_height: float = 0.55, header_rows: int = 1):
        rows = []
        for r_index, row in enumerate(data):
            cells = []
            for value in row:
                fill = GREY_E if r_index < header_rows else BLACK
                cell = self.table_cell(
                    str(value),
                    width=cell_width,
                    height=cell_height,
                    fill_color=fill,
                    text_size=20,
                )
                cells.append(cell)
            rows.append(VGroup(*cells).arrange(RIGHT, buff=0))
        table = VGroup(*rows).arrange(DOWN, buff=0)
        frame = SurroundingRectangle(table, color=GREY_B, buff=0.02, stroke_width=1.5)
        return VGroup(table, frame)

    def bar_chart_manual(
        self,
        values,
        *,
        max_height: float = 2.2,
        bar_width: float = 0.28,
        color_list=None,
        labels=None,
        baseline_width: float = 3.2,
    ):
        if color_list is None:
            color_list = [YELLOW_B, BLUE_C, TEAL_C, GREEN_C, ORANGE]
        max_value = max(values) if values else 1
        baseline = Line(LEFT * baseline_width / 2, RIGHT * baseline_width / 2, color=GREY_B)
        bars = []
        for index, value in enumerate(values):
            height = max_height * value / max_value
            bar = Rectangle(width=bar_width, height=height)
            bar.set_stroke(color=GREY_A, width=1.2)
            bar.set_fill(color_list[index % len(color_list)], opacity=0.95)
            bar.align_to(ORIGIN, DOWN)
            bars.append(bar)
        bar_group = VGroup(*bars).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        bar_group.move_to(baseline.get_center() + UP * max_height / 2)
        objects = [baseline, bar_group]
        if labels:
            label_mobs = []
            for bar, label in zip(bar_group, labels):
                txt = self.VText(label, font_size=18)
                txt.next_to(bar, DOWN, buff=0.08)
                label_mobs.append(txt)
            label_group = VGroup(*label_mobs)
            objects.append(label_group)
        return VGroup(*objects)

    def arrow_with_text(self, start, end, text, *, font_size: float = 22, color=YELLOW_B):
        arrow = Arrow(start=start, end=end, buff=0.08, color=color, stroke_width=4)
        label = self.VText(text, font_size=font_size, color=color)
        label.next_to(arrow, UP, buff=0.08)
        return VGroup(arrow, label)

    def value_badge(self, text: str, *, color=YELLOW_B, font_size: float = 22):
        label = self.VText(text, font_size=font_size, color=color)
        bg = RoundedRectangle(
            width=label.width + 0.28,
            height=label.height + 0.18,
            corner_radius=0.10,
            stroke_color=color,
            stroke_width=1.6,
        )
        label.move_to(bg.get_center())
        return VGroup(bg, label)

    # --------------------------------------------------------------
    # Dữ liệu thủ công cho minh họa ảnh
    # --------------------------------------------------------------
    def image_matrix_original(self):
        return [
            [18, 20, 26, 32, 40, 48, 54, 60],
            [20, 28, 42, 56, 68, 78, 84, 72],
            [26, 42, 64, 88, 108, 116, 102, 78],
            [32, 54, 86, 120, 132, 138, 118, 86],
            [40, 66, 102, 134, 144, 150, 126, 90],
            [46, 76, 112, 142, 154, 158, 130, 92],
            [44, 72, 106, 132, 142, 144, 120, 86],
            [32, 50, 72, 90, 96, 98, 84, 62],
        ]

    def image_matrix_k2(self):
        return [
            [36, 38, 40, 44, 46, 48, 48, 46],
            [38, 42, 48, 56, 62, 64, 62, 56],
            [40, 48, 62, 78, 90, 92, 86, 72],
            [44, 56, 76, 96, 108, 110, 100, 82],
            [46, 60, 82, 102, 114, 116, 104, 84],
            [46, 60, 82, 100, 112, 114, 102, 82],
            [42, 52, 66, 82, 92, 94, 84, 70],
            [38, 44, 52, 62, 68, 70, 64, 54],
        ]

    def image_matrix_k8(self):
        return [
            [24, 26, 30, 36, 42, 48, 52, 54],
            [26, 34, 46, 58, 68, 74, 76, 68],
            [30, 46, 68, 88, 102, 108, 98, 78],
            [36, 56, 86, 114, 126, 132, 114, 84],
            [40, 64, 98, 126, 138, 142, 122, 88],
            [42, 68, 102, 132, 144, 146, 126, 90],
            [38, 62, 92, 118, 128, 130, 112, 82],
            [30, 46, 66, 82, 90, 92, 78, 60],
        ]


    def image_matrix_k20(self):
        return [
            [26, 34, 44, 56, 66, 74, 80, 84],
            [30, 46, 66, 86, 98, 108, 112, 102],
            [38, 62, 92, 122, 138, 146, 136, 112],
            [48, 78, 114, 146, 162, 166, 148, 118],
            [54, 86, 124, 156, 172, 176, 154, 122],
            [58, 92, 132, 164, 178, 180, 156, 124],
            [54, 84, 120, 148, 160, 162, 140, 112],
            [42, 62, 86, 104, 112, 114, 98, 76],
        ]

    def image_matrix_k40(self):
        return [
            [18, 20, 26, 32, 40, 48, 54, 60],
            [20, 28, 42, 56, 68, 78, 84, 72],
            [26, 42, 64, 88, 108, 116, 102, 78],
            [32, 54, 86, 120, 132, 138, 118, 86],
            [40, 66, 102, 134, 144, 150, 126, 90],
            [46, 76, 112, 142, 154, 158, 130, 92],
            [44, 72, 106, 132, 142, 146, 120, 86],
            [32, 50, 72, 90, 96, 100, 84, 62],
        ]

    def image_matrix_noise(self):
        return [
            [8, 40, 16, 36, 48, 20, 56, 24],
            [26, 18, 62, 42, 78, 58, 92, 50],
            [22, 60, 50, 102, 88, 128, 82, 100],
            [46, 42, 108, 114, 154, 120, 138, 86],
            [30, 86, 92, 150, 132, 170, 110, 112],
            [58, 62, 128, 126, 166, 136, 154, 84],
            [32, 74, 88, 134, 116, 152, 98, 94],
            [44, 42, 90, 70, 108, 82, 96, 56],
        ]

    def image_matrix_denoised(self):
        return [
            [20, 24, 30, 36, 42, 48, 52, 54],
            [24, 34, 48, 60, 70, 76, 78, 68],
            [30, 48, 68, 90, 104, 110, 98, 78],
            [36, 58, 86, 116, 128, 132, 116, 86],
            [40, 64, 98, 128, 140, 144, 122, 90],
            [42, 68, 102, 132, 144, 146, 124, 92],
            [38, 62, 92, 118, 128, 130, 110, 82],
            [32, 46, 66, 82, 90, 92, 78, 60],
        ]

    def singular_values_demo(self):
        return [10.0, 7.0, 5.2, 3.4, 2.2, 1.4, 0.9, 0.5]

    def singular_values_small_tail(self):
        return [10.0, 7.4, 5.6, 3.0, 1.6, 0.9, 0.45, 0.2]

    def term_document_data(self):
        return [
            ["Từ \\ Tài liệu", "D1", "D2", "D3", "D4"],
            ["biển", "4", "5", "0", "0"],
            ["cát", "3", "4", "0", "0"],
            ["núi", "0", "0", "5", "4"],
            ["rừng", "0", "1", "4", "5"],
            ["du lịch", "2", "2", "2", "2"],
        ]

    def term_document_clustered_data(self):
        return [
            ["Chủ đề ẩn", "Nhóm A", "Nhóm A", "Nhóm B", "Nhóm B"],
            ["từ chính", "biển", "cát", "núi", "rừng"],
            ["D1", "cao", "cao", "thấp", "thấp"],
            ["D2", "cao", "cao", "thấp", "vừa"],
            ["D3", "thấp", "thấp", "cao", "cao"],
            ["D4", "thấp", "thấp", "cao", "cao"],
        ]

    def user_item_data(self):
        return [
            ["User \\ Phim", "P1", "P2", "P3", "P4", "P5"],
            ["A", "5", "4", "?", "1", "?"],
            ["B", "4", "5", "?", "1", "?"],
            ["C", "1", "?", "5", "4", "5"],
            ["D", "1", "?", "4", "5", "4"],
        ]

    def user_item_factors_data(self):
        return [
            ["Thực thể", "Hành động", "Tình cảm", "Hài"],
            ["A", "cao", "thấp", "thấp"],
            ["B", "cao", "thấp", "thấp"],
            ["C", "thấp", "cao", "vừa"],
            ["D", "thấp", "cao", "thấp"],
            ["P1", "cao", "thấp", "thấp"],
            ["P3", "thấp", "cao", "vừa"],
            ["P5", "thấp", "cao", "thấp"],
        ]


    def face_matrix_1(self):
        return [
            [18, 22, 34, 42, 42, 34, 22, 18],
            [24, 70, 110, 126, 126, 110, 70, 24],
            [40, 118, 168, 182, 182, 168, 118, 40],
            [52, 130, 174, 198, 198, 174, 130, 52],
            [46, 114, 86, 188, 188, 86, 114, 46],
            [34, 92, 142, 120, 120, 142, 92, 34],
            [18, 50, 72, 54, 54, 72, 50, 18],
            [8, 16, 24, 30, 30, 24, 16, 8],
        ]


    def face_matrix_2(self):
        return [
            [20, 26, 36, 44, 44, 36, 26, 20],
            [30, 64, 96, 112, 112, 96, 64, 30],
            [46, 90, 138, 154, 154, 138, 90, 46],
            [56, 102, 152, 170, 170, 152, 102, 56],
            [50, 92, 154, 112, 112, 154, 92, 50],
            [38, 82, 122, 142, 142, 122, 82, 38],
            [20, 44, 64, 86, 86, 64, 44, 20],
            [10, 18, 24, 32, 32, 24, 18, 10],
        ]


    def face_matrix_mean(self):
        return [
            [19, 24, 35, 43, 43, 35, 24, 19],
            [27, 67, 103, 119, 119, 103, 67, 27],
            [43, 104, 153, 168, 168, 153, 104, 43],
            [54, 116, 164, 184, 184, 164, 116, 54],
            [48, 103, 120, 150, 150, 120, 103, 48],
            [36, 87, 132, 131, 131, 132, 87, 36],
            [19, 47, 68, 70, 70, 68, 47, 19],
            [9, 17, 24, 31, 31, 24, 17, 9],
        ]

    def make_geometry_shape(self):
        circle = Circle(radius=0.88, color=YELLOW, stroke_width=4)
        e1 = Arrow(start=ORIGIN, end=RIGHT * 0.95, buff=0.0, color=RED, stroke_width=5)
        e2 = Arrow(start=ORIGIN, end=UP * 0.95, buff=0.0, color=BLUE, stroke_width=5)
        return VGroup(circle, e1, e2)

    def make_axes_box(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.18},
        ).scale(0.64)
        return plane

    def geometry_panel(self, symbol: str, text: str):
        inner = VGroup(
            MathTex(symbol).scale(0.95),
            self.VText(text, font_size=24),
        ).arrange(DOWN, buff=0.08)
        return self.simple_panel(inner, width=4.2, height=1.08, color=GREY_B)

    def manual_scatter_points(self):
        coords = [
            (-3.0, -1.9),
            (-2.6, -1.6),
            (-2.2, -1.2),
            (-1.8, -1.0),
            (-1.4, -0.6),
            (-1.0, -0.4),
            (-0.6, -0.2),
            (-0.2, 0.1),
            (0.2, 0.3),
            (0.7, 0.6),
            (1.1, 0.8),
            (1.5, 1.1),
            (1.9, 1.3),
            (2.3, 1.7),
            (2.7, 2.0),
        ]
        dots = []
        for x, y in coords:
            dot = Dot(point=[x, y, 0], radius=0.06, color=YELLOW_B)
            dots.append(dot)
        return VGroup(*dots)

    def noisy_wave_points(self):
        xs = [-3.3, -3.0, -2.7, -2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0]
        ys = [-0.3, 0.2, 0.8, 0.5, 1.2, 0.9, 1.3, 0.7, 0.9, 0.1, 0.4, -0.2, -0.5, -1.0, -0.8, -1.2, -0.9, -1.0, -0.4, -0.2, 0.3, 0.1]
        points = []
        for x, y in zip(xs, ys):
            points.append([x, y, 0])
        return points

    def smooth_wave_points(self):
        xs = [-3.3, -3.0, -2.7, -2.4, -2.1, -1.8, -1.5, -1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0]
        ys = [0.0, 0.25, 0.52, 0.75, 0.93, 1.03, 1.04, 0.94, 0.76, 0.50, 0.20, -0.12, -0.42, -0.69, -0.89, -1.00, -1.00, -0.90, -0.71, -0.45, -0.15, 0.16]
        points = []
        for x, y in zip(xs, ys):
            points.append([x, y, 0])
        return points

    def polyline_from_points(self, points, *, color=YELLOW_B, width=4):
        dots = []
        for point in points:
            dots.append(point)
        return VMobject(color=color, stroke_width=width).set_points_as_corners(dots)

    def compression_tradeoff_panel(self, left_title: str, right_title: str):
        left = VGroup(
            self.VText(left_title, font_size=26, color=YELLOW_B, weight=BOLD),
            self.VText("Giữ ít thành phần", font_size=23),
            self.VText("Lưu trữ ít hơn", font_size=23),
            self.VText("Mất bớt chi tiết", font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        right = VGroup(
            self.VText(right_title, font_size=26, color=BLUE_C, weight=BOLD),
            self.VText("Giữ nhiều thành phần", font_size=23),
            self.VText("Ảnh rõ hơn", font_size=23),
            self.VText("Cần nhiều dữ liệu hơn", font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        panel = self.build_two_column(left, right, gap=1.2)
        return panel

    # --------------------------------------------------------------
    # Bộ câu nhấn mạnh dùng lại trong phần ứng dụng
    # --------------------------------------------------------------
    def emphasis_text_01(self):
        return "Ta có thể hiểu đơn giản rằng ảnh xám chỉ là một bảng số."

    def emphasis_text_02(self):
        return "Mỗi ô pixel tương ứng với một phần tử trong ma trận."

    def emphasis_text_03(self):
        return "Giá trị lớn hơn thường sáng hơn, giá trị nhỏ hơn thường tối hơn."

    def emphasis_text_04(self):
        return "SVD áp dụng được vì ảnh cũng chỉ là một ma trận thực."

    def emphasis_text_05(self):
        return "Ba thành phần U, Σ, Vᵀ giúp ta tách bài toán thành các bước trực quan."

    def emphasis_text_06(self):
        return "Các singular values cho biết mức quan trọng tương đối của từng hướng."

    def emphasis_text_07(self):
        return "Truncated SVD chỉ giữ vài thành phần nổi bật nhất."

    def emphasis_text_08(self):
        return "Khi k nhỏ, ảnh vẫn giữ khung lớn nhưng chi tiết bị mờ đi."

    def emphasis_text_09(self):
        return "Khi k tăng, nhiều cấu trúc tinh tế hơn quay trở lại."

    def emphasis_text_10(self):
        return "Nén ảnh là một bài toán đánh đổi giữa chất lượng và dung lượng."

    def emphasis_text_11(self):
        return "Trong PCA, ta giữ hướng biến thiên mạnh nhất của dữ liệu."

    def emphasis_text_12(self):
        return "Trong LSA, ta tìm ra cấu trúc ngữ nghĩa ẩn phía sau từ và tài liệu."

    def emphasis_text_13(self):
        return "Trong hệ gợi ý, ta truy ra sở thích ẩn của người dùng."

    def emphasis_text_14(self):
        return "Trong khử nhiễu, việc bỏ bớt thành phần nhỏ có thể làm dữ liệu mượt hơn."

    def emphasis_text_15(self):
        return "Trong nhận dạng khuôn mặt, SVD hỗ trợ xây dựng không gian đặc trưng gọn hơn."

    def emphasis_text_16(self):
        return "Điểm mạnh của SVD là tính tổng quát và khả năng tách cấu trúc chính."

    def emphasis_text_17(self):
        return "Trực quan trước rồi công thức sau giúp người xem theo dõi dễ hơn."

    def emphasis_text_18(self):
        return "Nếu bố cục quá dày, ta nên tách thành nhiều khung nhỏ."

    def emphasis_text_19(self):
        return "Mỗi khung ở đây đều được giữ nhịp chậm để đọc kịp."

    def emphasis_text_20(self):
        return "Phần ứng dụng được mở rộng để làm rõ ý nghĩa thực tế của SVD."


    # --------------------------------------------------------------
    # Điều phối toàn bộ video
    # --------------------------------------------------------------
    def construct(self):
        # Phần mở đầu và chéo hóa
        self.slide_opening()
        self.wipe()

        self.slide_diag_step12()
        self.wipe()

        self.slide_diag_step3a()
        self.wipe()

        self.slide_diag_step3b()
        self.wipe()

        self.slide_diag_step4()
        self.wipe()

        # Phần chuyển tiếp sang SVD và hình học
        self.slide_svd_bridge()
        self.wipe()

        self.slide_geometry()
        self.wipe()

        # Ứng dụng 1: Nén ảnh bằng SVD (ít nhất 10 khung)
        self.current_pace = 1.32
        self.slide_app1_intro()
        self.wipe()

        self.slide_app1_image_as_matrix()
        self.wipe()

        self.slide_app1_why_svd()
        self.wipe()

        self.slide_app1_meaning_of_parts()
        self.wipe()

        self.slide_app1_sigma_importance()
        self.wipe()

        self.slide_app1_truncated_definition()
        self.wipe()

        self.slide_app1_small_k()
        self.wipe()

        self.slide_app1_large_k()
        self.wipe()

        self.slide_app1_tradeoff()
        self.wipe()

        self.slide_app1_compare_many_levels()
        self.wipe()

        self.slide_app1_summary()
        self.wipe()

        # Ứng dụng 2: PCA
        self.slide_app2_pca_intro()
        self.wipe()

        self.slide_app2_pca_visual()
        self.wipe()

        self.slide_app2_pca_summary()
        self.wipe()

        # Ứng dụng 3: LSA / LSI
        self.slide_app3_lsa_intro()
        self.wipe()

        self.slide_app3_lsa_matrix()
        self.wipe()

        self.slide_app3_lsa_summary()
        self.wipe()

        # Ứng dụng 4: Recommendation
        self.slide_app4_rec_intro()
        self.wipe()

        self.slide_app4_rec_matrix()
        self.wipe()

        self.slide_app4_rec_summary()
        self.wipe()

        # Ứng dụng 5: Khử nhiễu
        self.slide_app5_noise_intro()
        self.wipe()

        self.slide_app5_noise_visual()
        self.wipe()

        self.slide_app5_noise_summary()
        self.wipe()

        # Ứng dụng 6: Eigenfaces / biểu diễn khuôn mặt
        self.slide_app6_face_intro()
        self.wipe()

        self.slide_app6_face_visual()
        self.wipe()

        # Tổng kết cuối
        self.slide_summary()
        self.wipe()

        self.slide_thanks()


    # --------------------------------------------------------------
    # Phần mở đầu
    # --------------------------------------------------------------
    def slide_opening(self):
        title = self.VText("Chéo hóa và SVD", font_size=56, color=BLUE_B, weight=BOLD)
        title.to_edge(UP, buff=0.42)

        sub = self.VText(
            "Từ trị riêng đến biến đổi hình học và các ứng dụng thực tế",
            font_size=26,
            color=GREY_B,
        )
        sub.next_to(title, DOWN, buff=0.20)

        f1 = MathTex(r"A=PDP^{-1}").scale(1.25)
        f2 = MathTex(r"A=U\Sigma V^T").scale(1.25)
        body = VGroup(f1, f2).arrange(DOWN, buff=0.62)
        body.move_to(ORIGIN + DOWN * 0.35)

        self.keep_inside_safe(VGroup(title, sub, body))

        self.reveal_text(title, rt=0.88)
        self.reveal_text(sub, rt=0.72)
        self.write_math(f1, rt=0.92)
        self.W(0.55)
        self.write_math(f2, rt=0.92)
        self.W(1.55)

    # --------------------------------------------------------------
    # Phần chéo hóa ma trận
    # --------------------------------------------------------------
    def slide_diag_step12(self):
        title, step = self.section_header(
            "Bước 1 & 2: Đa thức đặc trưng và trị riêng",
            "CHÉO HÓA MA TRẬN",
        )

        line0 = self.VText("Chọn ma trận ví dụ:", font_size=28)
        line0.next_to(step, DOWN, buff=0.42)
        line0.align_to(step, LEFT)

        A0 = self.diag_matrix()
        A0.next_to(line0, DOWN, buff=0.28)
        A0.align_to(step, LEFT)

        line1 = MathTex(r"P_A(\lambda)=\det(A-\lambda I_3)").scale(0.94)
        line2 = MathTex(r"=\det\begin{pmatrix}2-\lambda&1&0\\1&2-\lambda&0\\0&0&4-\lambda\end{pmatrix}").scale(0.82)
        line3 = MathTex(r"=(4-\lambda)\det\begin{pmatrix}2-\lambda&1\\1&2-\lambda\end{pmatrix}").scale(0.82)
        line4 = MathTex(r"=(4-\lambda)\big((2-\lambda)^2-1\big)").scale(0.90)
        line5 = MathTex(r"=(4-\lambda)(\lambda-1)(\lambda-3)").scale(0.96)

        block = VGroup(line1, line2, line3, line4, line5).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.20,
        )
        block.next_to(A0, DOWN, buff=0.40)
        block.align_to(step, LEFT)

        explain = self.VText("Giải phương trình P_A(λ)=0, ta có ba trị riêng:", font_size=28)
        explain.next_to(block, DOWN, buff=0.34)
        explain.align_to(step, LEFT)

        eigs = VGroup(
            MathTex(r"\lambda_1=1").set_color(ORANGE),
            MathTex(r"\lambda_2=3").set_color(ORANGE),
            MathTex(r"\lambda_3=4").set_color(ORANGE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        eigs.next_to(explain, DOWN, buff=0.22)
        eigs.align_to(step, LEFT)

        self.keep_inside_safe(VGroup(title, step, line0, A0, block, explain, eigs))

        self.reveal_text(title, rt=0.72)
        self.reveal_text(step, rt=0.64)
        self.reveal_text(line0, rt=0.52)
        self.write_math(A0, rt=0.90)
        self.write_math(line1, rt=0.88)
        self.W(0.35)
        self.write_math(line2, rt=0.98)
        self.W(0.55)
        self.write_math(line3, rt=0.95)
        self.W(0.50)
        self.write_math(line4, rt=0.88)
        self.W(0.45)
        self.write_math(line5, rt=0.92)
        self.W(0.55)
        self.reveal_text(explain, rt=0.68)
        for eig in eigs:
            self.play(FadeIn(eig, shift=RIGHT * 0.12), run_time=0.60)
            self.W(0.32)
        self.W(1.38)

    def slide_diag_step3a(self):
        title, step = self.section_header(
            "Bước 3: Tìm cơ sở không gian riêng",
            "CHÉO HÓA MA TRẬN",
        )

        head = VGroup(
            self.VText("Với", font_size=29),
            MathTex(r"\lambda=1").set_color(ORANGE),
            self.VText(", giải hệ", font_size=29),
            MathTex(r"(A-I_3)X=0"),
        ).arrange(RIGHT, buff=0.12)
        head.next_to(step, DOWN, buff=0.42)
        head.shift(LEFT * 1.20)

        mat = MathTex(r"A-I_3=\begin{pmatrix}1&1&0\\1&1&0\\0&0&3\end{pmatrix}").scale(0.90)
        arr = MathTex(r"\xrightarrow{\mathrm{Gauss}}", color=GREY_A).scale(0.90)
        rref = MathTex(r"\begin{pmatrix}1&1&0\\0&0&1\\0&0&0\end{pmatrix}").scale(0.90)
        sys = VGroup(mat, arr, rref).arrange(RIGHT, buff=0.24)
        sys.next_to(head, DOWN, buff=0.30)
        sys.shift(LEFT * 1.20)

        solve1 = MathTex(r"\Rightarrow x+y=0,\ 3z=0 \Rightarrow y=-x,\ z=0").scale(0.80)
        solve1.next_to(sys, DOWN, buff=0.22)
        solve1.align_to(sys, LEFT)

        solve2 = MathTex(r"X=t\begin{pmatrix}1\\-1\\0\end{pmatrix}").scale(0.88)
        solve2.next_to(solve1, DOWN, buff=0.18)
        solve2.align_to(sys, LEFT)

        basis = VGroup(
            self.VText("Cơ sở E(1):", font_size=29),
            MathTex(r"u_1=\begin{pmatrix}1\\-1\\0\end{pmatrix}").set_color(YELLOW),
        ).arrange(RIGHT, buff=0.22)
        basis.next_to(solve2, DOWN, buff=0.26)
        basis.align_to(sys, LEFT)

        self.keep_inside_safe(VGroup(title, step, head, sys, solve1, solve2, basis))

        self.reveal_text(title, rt=0.72)
        self.reveal_text(step, rt=0.64)
        self.reveal_group(head, rt=0.65)
        self.write_math(mat, rt=0.96)
        self.write_math(arr, rt=0.34)
        self.write_math(rref, rt=0.86)
        self.W(0.60)
        self.write_math(solve1, rt=0.82)
        self.W(0.25)
        self.write_math(solve2, rt=0.82)
        self.W(0.35)
        self.reveal_group(basis, rt=0.74)
        self.W(1.48)

    def slide_diag_step3b(self):
        title, step = self.section_header(
            "Bước 3: Tìm cơ sở không gian riêng",
            "CHÉO HÓA MA TRẬN",
        )

        head1 = VGroup(
            self.VText("Với", font_size=29),
            MathTex(r"\lambda=3").set_color(ORANGE),
            self.VText(", giải hệ", font_size=29),
            MathTex(r"(A-3I_3)X=0"),
        ).arrange(RIGHT, buff=0.12)
        head1.next_to(step, DOWN, buff=0.38)
        head1.shift(LEFT * 1.15)

        mat1 = MathTex(r"A-3I_3=\begin{pmatrix}-1&1&0\\1&-1&0\\0&0&1\end{pmatrix}").scale(0.84)
        arr1 = MathTex(r"\xrightarrow{\mathrm{Gauss}}", color=GREY_A).scale(0.84)
        rref1 = MathTex(r"\begin{pmatrix}1&-1&0\\0&0&1\\0&0&0\end{pmatrix}").scale(0.84)
        sys1 = VGroup(mat1, arr1, rref1).arrange(RIGHT, buff=0.22)
        sys1.next_to(head1, DOWN, buff=0.22)
        sys1.shift(LEFT * 1.15)

        solve1 = MathTex(r"\Rightarrow x-y=0,\ z=0 \Rightarrow y=x").scale(0.74)
        solve1.next_to(sys1, DOWN, buff=0.15)
        solve1.align_to(sys1, LEFT)

        basis1 = VGroup(
            self.VText("Cơ sở E(3):", font_size=26),
            MathTex(r"u_2=\begin{pmatrix}1\\1\\0\end{pmatrix}").set_color(YELLOW),
        ).arrange(RIGHT, buff=0.18)
        basis1.next_to(solve1, DOWN, buff=0.16)
        basis1.align_to(sys1, LEFT)

        head2 = VGroup(
            self.VText("Với", font_size=29),
            MathTex(r"\lambda=4").set_color(ORANGE),
            self.VText(", giải hệ", font_size=29),
            MathTex(r"(A-4I_3)X=0"),
        ).arrange(RIGHT, buff=0.12)
        head2.next_to(basis1, DOWN, buff=0.34)
        head2.align_to(head1, LEFT)

        mat2 = MathTex(r"A-4I_3=\begin{pmatrix}-2&1&0\\1&-2&0\\0&0&0\end{pmatrix}").scale(0.84)
        arr2 = MathTex(r"\xrightarrow{\mathrm{Gauss}}", color=GREY_A).scale(0.84)
        rref2 = MathTex(r"\begin{pmatrix}1&0&0\\0&1&0\\0&0&0\end{pmatrix}").scale(0.84)
        sys2 = VGroup(mat2, arr2, rref2).arrange(RIGHT, buff=0.22)
        sys2.next_to(head2, DOWN, buff=0.22)
        sys2.align_to(sys1, LEFT)

        solve2_math = MathTex(r"\Rightarrow x=0,\ y=0,\ z").scale(0.74)
        solve2_text = self.VText(" tự do", font_size=24)
        solve2 = VGroup(solve2_math, solve2_text).arrange(RIGHT, buff=0.08)
        solve2.next_to(sys2, DOWN, buff=0.18)
        solve2.align_to(sys2, LEFT)

        basis2 = VGroup(
            self.VText("Cơ sở E(4):", font_size=26),
            MathTex(r"u_3=\begin{pmatrix}0\\0\\1\end{pmatrix}").set_color(YELLOW),
        ).arrange(RIGHT, buff=0.18)
        basis2.next_to(solve2, DOWN, buff=0.16)
        basis2.align_to(sys2, LEFT)

        self.keep_inside_safe(VGroup(title, step, head1, sys1, solve1, basis1, head2, sys2, solve2, basis2))

        self.reveal_text(title, rt=0.72)
        self.reveal_text(step, rt=0.64)
        self.reveal_group(head1, rt=0.62)
        self.write_math(mat1, rt=0.92)
        self.write_math(arr1, rt=0.28)
        self.write_math(rref1, rt=0.82)
        self.W(0.20)
        self.write_math(solve1, rt=0.68)
        self.reveal_group(basis1, rt=0.68)
        self.W(0.46)

        self.reveal_group(head2, rt=0.62)
        self.write_math(mat2, rt=0.92)
        self.write_math(arr2, rt=0.28)
        self.write_math(rref2, rt=0.82)
        self.W(0.20)
        self.write_math(solve2, rt=0.68)
        self.reveal_group(basis2, rt=0.68)
        self.W(1.40)

    def slide_diag_step4(self):
        title, step = self.section_header(
            "Bước 4: Kết luận",
            "CHÉO HÓA MA TRẬN",
        )

        txt1 = self.VText("Lập ma trận P từ các vector cột u1, u2, u3:", font_size=30)
        txt1.next_to(step, DOWN, buff=0.50)
        txt1.align_to(step, LEFT)

        Pm = MathTex(r"P=(u_1\ u_2\ u_3)=\begin{pmatrix}1&1&0\\-1&1&0\\0&0&1\end{pmatrix}").scale(0.92)
        Pm.next_to(txt1, DOWN, buff=0.34)
        Pm.align_to(step, LEFT)

        txt2 = self.VText("Khi đó, ma trận chéo hóa D là:", font_size=30)
        txt2.next_to(Pm, DOWN, buff=0.48)
        txt2.align_to(step, LEFT)

        Dm = MathTex(r"P^{-1}AP=\begin{pmatrix}1&0&0\\0&3&0\\0&0&4\end{pmatrix}").scale(0.98)
        Dm.next_to(txt2, DOWN, buff=0.34)
        Dm.align_to(step, LEFT)

        end_line = VGroup(
            self.VText("Vậy", font_size=29),
            MathTex(r"A=PDP^{-1}").set_color(YELLOW),
            self.VText("với", font_size=29),
            MathTex(r"D=\mathrm{diag}(1,3,4)").set_color(YELLOW),
        ).arrange(RIGHT, buff=0.18)
        end_line.next_to(Dm, DOWN, buff=0.36)
        end_line.align_to(step, LEFT)

        self.keep_inside_safe(VGroup(title, step, txt1, Pm, txt2, Dm, end_line))

        self.reveal_text(title, rt=0.72)
        self.reveal_text(step, rt=0.64)
        self.reveal_text(txt1, rt=0.72)
        self.write_math(Pm, rt=1.00)
        self.W(0.52)
        self.reveal_text(txt2, rt=0.72)
        self.write_math(Dm, rt=1.00)
        self.W(0.48)
        self.reveal_group(end_line, rt=0.82)
        self.W(1.45)

    # --------------------------------------------------------------
    # Phần chuyển tiếp sang SVD
    # --------------------------------------------------------------
    def slide_svd_bridge(self):
        title, sub = self.top_title(
            "Từ chéo hóa đến SVD",
            "SVD tổng quát hơn và áp dụng cho mọi ma trận thực",
        )
        sub.set_x(title.get_x())

        l1 = VGroup(
            self.VText("Bước 1: Chéo hóa AᵀA", font_size=29, color=YELLOW_B, weight=BOLD),
            MathTex(r"A^TA=V\Lambda V^T").scale(0.95),
            self.VText("Ma trận AᵀA luôn đối xứng và có trị riêng không âm.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        l2 = VGroup(
            self.VText("Bước 2: Tạo singular values", font_size=29, color=YELLOW_B, weight=BOLD),
            MathTex(r"\sigma_i=\sqrt{\lambda_i(A^TA)}").scale(0.90),
            MathTex(r"\Sigma=\mathrm{diag}(\sigma_1,\sigma_2,\ldots)").scale(0.88),
            self.VText("Σ cho biết độ co giãn theo các hướng chính.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        l3 = VGroup(
            self.VText("Bước 3: Hoàn tất phân rã", font_size=29, color=YELLOW_B, weight=BOLD),
            MathTex(r"U=AV\Sigma^{-1}").scale(0.90),
            MathTex(r"A=U\Sigma V^T").scale(1.00),
            self.VText("U và V là các ma trận trực giao.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        body = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        body.scale_to_fit_width(11.5)
        body.next_to(sub, DOWN, buff=0.28)

        note = self.note_box(
            "Ý tưởng cốt lõi: chéo hóa không phải lúc nào cũng làm được trực tiếp cho A,\nnhưng SVD thì luôn tồn tại.",
            font_size=28,
            width=12.0,
            color=TEAL_B,
        )
        note.next_to(body, DOWN, buff=0.30)

        self.keep_inside_safe(VGroup(title, sub, body, note))

        self.reveal_text(title, rt=0.84)
        self.reveal_text(sub, rt=0.66)
        for block in [l1, l2, l3]:
            self.reveal_text(block[0], rt=0.46)
            for item in block[1:]:
                if isinstance(item, MathTex):
                    self.write_math(item, rt=0.62)
                else:
                    self.reveal_text(item, rt=0.46)
            self.W(0.18)
        self.reveal_group(note, rt=0.70)
        self.W(1.12)

    # --------------------------------------------------------------
    # Hình học của SVD (không dùng numpy)
    # --------------------------------------------------------------

    def slide_geometry(self):
        title, sub = self.top_title(
            "Hình học của SVD",
            "Chuỗi trực quan: quay hệ trục đầu vào → scale → quay đầu ra",
        )
        title.set_x(0)
        if sub:
            sub.set_x(0)

        formula = MathTex(r"A=U\Sigma V^T").scale(0.98)
        formula.next_to(sub, DOWN, buff=0.16)
        formula.set_x(0)

        plane = self.make_axes_box()
        plane.move_to(LEFT * 3.30 + DOWN * 0.78)

        shape = self.make_geometry_shape()
        shape.move_to(plane.get_center())

        p1 = self.geometry_panel(r"V^T", "Quay hệ trục đầu vào")
        p2 = self.geometry_panel(r"\Sigma", "Co giãn theo trục chính")
        p3 = self.geometry_panel(r"U", "Quay kết quả sang hệ mới")
        panels = VGroup(p1, p2, p3).arrange(DOWN, buff=0.18)
        panels.move_to(RIGHT * 3.38 + DOWN * 0.78)

        note = self.note_box(
            "Ở đây ta chỉ giữ tinh thần trực quan: Vᵀ đổi hướng biểu diễn, Σ kéo giãn, còn U quay kết quả cuối.",
            font_size=23,
            width=10.8,
            color=YELLOW_B,
        )
        note.next_to(plane, DOWN, buff=0.24)
        note.set_x(0)

        self.keep_inside_safe(VGroup(title, sub, formula, plane, shape, panels, note))

        self.reveal_text(title, rt=0.84)
        self.reveal_text(sub, rt=0.64)
        self.write_math(formula, rt=0.70)
        self.play(Create(plane), run_time=0.82)
        self.play(Create(shape[0]), GrowArrow(shape[1]), GrowArrow(shape[2]), run_time=0.98)
        self.play(FadeIn(panels, shift=LEFT * 0.16), run_time=0.74)
        self.W(0.28)

        self.play(Indicate(p1), run_time=0.42)
        self.play(Rotate(shape, angle=28 * DEGREES, about_point=plane.get_center()), run_time=1.00)
        self.W(0.28)

        self.play(Indicate(p2), run_time=0.42)
        self.play(shape.animate.stretch(1.42, 0).stretch(0.64, 1), run_time=1.10)
        self.W(0.28)

        self.play(Indicate(p3), run_time=0.42)
        self.play(Rotate(shape, angle=-18 * DEGREES, about_point=plane.get_center()), run_time=1.00)

        self.reveal_group(note, rt=0.72)
        self.W(1.72)

    def app1_title(self, subtitle: str):
        title, sub = self.top_title("Ứng dụng 1 - Nén ảnh bằng SVD", subtitle)
        title.move_to([0, title.get_center()[1], 0])
        if sub:
            sub.move_to([0, sub.get_center()[1], 0])
        return title, sub


    def slide_app1_intro(self):
        title, sub = self.app1_title("Ảnh số có thể được xem như một ma trận các mức sáng")

        block = self.paragraph_block(
            [
                self.emphasis_text_01(),
                self.emphasis_text_02(),
                self.emphasis_text_03(),
            ],
            font_size=34,
            width=11.1,
        )
        block.next_to(sub, DOWN, buff=0.38)
        block.align_to(sub, LEFT)

        matrix_small = self.labeled_matrix_visual(
            self.image_matrix_original(),
            "Ma trận ảnh xám 8×8",
            "Mỗi số là cường độ sáng của một pixel",
            cell_size=0.26,
            show_numbers=True,
        )
        matrix_small.next_to(block, DOWN, buff=0.42)
        matrix_small.move_to([0, matrix_small.get_center()[1], 0])

        self.keep_inside_safe(VGroup(title, sub, block, matrix_small))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in block:
            self.reveal_text(line, rt=0.56)
            self.W(0.24)
        self.reveal_group(matrix_small[0], rt=0.86)
        self.reveal_group(matrix_small[1], rt=0.30)
        self.reveal_group(matrix_small[2], rt=0.54)
        self.W(1.48)

    def slide_app1_image_as_matrix(self):
        title, sub = self.app1_title("Từ ảnh đến ma trận: sáng hơn, tối hơn và cấu trúc không gian")

        left_image = self.labeled_matrix_visual(
            self.image_matrix_original(),
            "Ảnh gốc",
            "Mức sáng được mã hóa bằng ô xám",
            cell_size=0.31,
            show_numbers=False,
        )

        right_text = VGroup(
            self.VText("• Mỗi hàng và mỗi cột mang thông tin vị trí của pixel.", font_size=30),
            self.VText("• Các vùng sáng tối liên tiếp tạo ra cấu trúc trong ma trận.", font_size=30),
            self.VText("• SVD khai thác chính cấu trúc đó để biểu diễn ảnh gọn hơn.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)

        right_panel = self.simple_panel(
            right_text,
            width=right_text.width + 0.42,
            height=right_text.height + 0.34,
            color=GREY_B,
        )

        body = self.build_two_column(left_image, right_panel, gap=0.92)
        body.next_to(sub, DOWN, buff=0.42)
        body.move_to([0, body.get_center()[1], 0])

        self.keep_inside_safe(VGroup(title, sub, body))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(left_image, rt=0.82)
        self.W(0.28)
        self.reveal_group(right_panel, rt=0.78)
        self.W(1.58)
        self.wait(3.0)


    def slide_app1_why_svd(self):
        title, sub = self.app1_title("Vì sao SVD áp dụng được cho ảnh")

        formula = MathTex(r"A=U\Sigma V^T").scale(1.08)
        formula.next_to(sub, DOWN, buff=0.32)

        left = VGroup(
            self.VText("• Ảnh xám chính là một\n  ma trận thực A.", font_size=47),
            self.VText("• SVD tồn tại cho mọi\n  ma trận thực, kể cả khi A\n  không chéo hóa được trực tiếp.", font_size=47),
            self.VText("• Vì vậy ảnh số là một đối tượng\n  tự nhiên để áp dụng SVD.", font_size=47),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)

        right_badges = VGroup(
            self.value_badge("Ảnh", color=YELLOW_B),
            self.value_badge("Ma trận thực", color=TEAL_B),
            self.value_badge("Có SVD", color=GREEN_B),
        ).arrange(DOWN, buff=0.22)

        chain = VGroup(
            self.value_badge("A", color=YELLOW_B),
            self.value_badge("U", color=GREEN_B),
            self.value_badge("Σ", color=YELLOW),
            self.value_badge("Vᵀ", color=RED_B),
        ).arrange(RIGHT, buff=0.28)
        chain.next_to(right_badges, DOWN, buff=0.42)

        explain = self.simple_panel(
            VGroup(
                self.VText("A: ảnh gốc", font_size=28),
                self.VText("U: dựng lại ảnh", font_size=28),
                self.VText("Σ: độ quan trọng", font_size=28),
                self.VText("Vᵀ: chọn cách nhìn", font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
            width=5.9,
            height=3.3,
            color=GREY_B,
        )
        explain.next_to(chain, DOWN, buff=0.30)

        right = VGroup(right_badges, chain, explain)
        body = self.build_two_column(left, right, gap=0.78)
        body.next_to(formula, DOWN, buff=0.36)

        note = self.note_box(
            self.emphasis_text_04(),
            font_size=24,
            width=11.2,
            color=YELLOW_B,
        )
        note.next_to(body, DOWN, buff=0.30)

        self.keep_inside_safe(VGroup(title, sub, formula, body, note))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.write_math(formula, rt=0.80)
        for line in left:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        for badge in right_badges:
            self.reveal_group(badge, rt=0.40)
            self.W(0.10)
        for badge in chain:
            self.reveal_group(badge, rt=0.36)
            self.W(0.08)
        self.reveal_group(explain, rt=0.66)
        self.reveal_group(note, rt=0.66)
        self.W(1.32)

    def slide_app1_meaning_of_parts(self):
        title, sub = self.app1_title("Ý nghĩa trực quan của U, Σ, Vᵀ trong ngữ cảnh ảnh")

        card1 = self.simple_panel(
            VGroup(
                MathTex(r"V^T").scale(1.0),
                self.VText("Đổi hướng biểu diễn đầu vào", font_size=21),
                self.VText("tức là nhìn ảnh theo các trục", font_size=18, color=GREY_B),
                self.VText("phù hợp hơn", font_size=18, color=GREY_B),
            ).arrange(DOWN, buff=0.06),
            width=4.15,
            height=2.25,
            color=RED_B,
        )

        card2 = self.simple_panel(
            VGroup(
                MathTex(r"\Sigma").scale(1.0),
                self.VText("Giữ mức quan trọng", font_size=21),
                self.VText("hướng nào mạnh sẽ có", font_size=18, color=GREY_B),
                self.VText("singular value lớn", font_size=18, color=GREY_B),
            ).arrange(DOWN, buff=0.06),
            width=4.15,
            height=2.25,
            color=YELLOW_B,
        )

        card3 = self.simple_panel(
            VGroup(
                MathTex(r"U").scale(1.0),
                self.VText("Dựng lại ảnh ở đầu ra", font_size=21),
                self.VText("theo các hướng chính", font_size=18, color=GREY_B),
                self.VText("đã chọn", font_size=18, color=GREY_B),
            ).arrange(DOWN, buff=0.06),
            width=4.15,
            height=2.25,
            color=GREEN_B,
        )

        row = self.build_three_column(card1, card2, card3, gap=0.32)
        row.scale_to_fit_width(11.2)
        row.next_to(sub, DOWN, buff=0.40)

        bottom = self.bullet_block(
            [
                "Ta không cần diễn giải quá hàn lâm ở đây.",
                "Chỉ cần nhớ: Vᵀ chọn cách nhìn, Σ đo độ quan trọng, U dựng lại kết quả.",
                "Ba phần phối hợp với nhau để biểu diễn ảnh theo cấu trúc chính của nó.",
            ],
            font_size=29,
            width=11.1,
        )
        bottom.next_to(row, DOWN, buff=0.46)
        bottom.align_to(sub, LEFT)

        self.keep_inside_safe(VGroup(title, sub, row, bottom))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for card in [card1, card2, card3]:
            self.reveal_group(card, rt=0.58)
            self.W(0.12)
        for line in bottom:
            self.reveal_text(line, rt=0.50)
            self.W(0.14)
        self.W(1.40)
        self.wait(2.0)


    def slide_app1_sigma_importance(self):
        old_pace = getattr(self, "current_pace", self.PACE)
        self.current_pace = 1.52

        title, sub = self.app1_title("Singular values nói lên điều gì")
        title.shift(RIGHT * 0.28)
        if sub:
            sub.shift(RIGHT * 0.28)

        bars = self.bar_chart_manual(
            self.singular_values_demo(),
            max_height=2.35,
            bar_width=0.32,
            labels=["σ1", "σ2", "σ3", "σ4", "σ5", "σ6", "σ7", "σ8"],
            baseline_width=4.1,
        )
        bars.next_to(sub, DOWN, buff=0.50)
        bars.shift(LEFT * 2.55 + DOWN * 0.06)

        text = VGroup(
            self.VText("• Các singular values lớn", font_size=44),
            self.VText("  giữ phần thông tin chính của ảnh.", font_size=44),
            self.spacer(0.14),
            self.VText("• Các singular values nhỏ hơn", font_size=44),
            self.VText("  thường chỉ bổ sung chi tiết mảnh", font_size=44),
            self.VText("  hoặc nhiễu nhẹ.", font_size=44),
            self.spacer(0.14),
            self.VText("• Vì vậy ta có thể cân nhắc", font_size=44),
            self.VText("  bỏ phần đuôi nhỏ để tiết kiệm biểu diễn.", font_size=44),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        text.scale_to_fit_width(5.85)
        text.next_to(bars, RIGHT, buff=0.58)
        text.align_to(bars, UP)
        text.shift(UP * 0.03)

        tail_box = self.note_box(
            "Ý tưởng quan trọng: nếu các cột đầu lớn hơn hẳn phần còn lại, ảnh có thể được xấp xỉ tốt chỉ với vài thành phần đầu.",
            font_size=25,
            width=10.9,
            color=YELLOW_B,
        )
        tail_box.next_to(text, DOWN, buff=0.42)
        tail_box.move_to([0.15, tail_box.get_center()[1], 0])

        self.keep_inside_safe(VGroup(title, sub, bars, text, tail_box))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(bars[0], rt=0.30)
        for bar in bars[1]:
            self.play(FadeIn(bar, shift=UP * 0.10), run_time=0.24)
        if len(bars) > 2:
            self.reveal_group(bars[2], rt=0.42)
        for line in text:
            self.reveal_text(line, rt=0.50)
            self.W(0.16)
        self.reveal_group(tail_box, rt=0.68)
        self.W(1.72)
        self.current_pace = old_pace

    def slide_app1_truncated_definition(self):
        title, sub = self.app1_title("Truncated SVD là gì")
        title.set_x(0)
        if sub:
            sub.set_x(0)

        formula = MathTex(r"A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T").scale(1.10)
        formula.next_to(sub, DOWN, buff=0.28)
        formula.set_x(0)

        explain = self.paragraph_block(
            [
                "Ta chỉ giữ lại k singular values lớn nhất và các vector tương ứng.",
                "Nói cách khác, thay vì dùng đầy đủ mọi thành phần, ta chỉ chọn phần mạnh nhất.",
                "Đó chính là cách xây dựng một xấp xỉ hạng-k của ảnh gốc.",
            ],
            font_size=28,
            width=10.2,
            aligned_edge=ORIGIN,
        )
        explain.arrange(DOWN, aligned_edge=ORIGIN, buff=0.20)
        explain.next_to(formula, DOWN, buff=0.34)
        explain.set_x(0)

        components = VGroup(
            self.value_badge("σ₁u₁v₁ᵀ", color=YELLOW_B),
            self.value_badge("σ₂u₂v₂ᵀ", color=YELLOW_B),
            self.value_badge("σ₃u₃v₃ᵀ", color=YELLOW_B),
            self.value_badge("...", color=GREY_B),
            self.value_badge("σₖuₖvₖᵀ", color=GREEN_B),
        ).arrange(RIGHT, buff=0.22)
        components.scale_to_fit_width(10.6)
        components.next_to(explain, DOWN, buff=0.38)
        components.set_x(0)

        note = self.note_box(
            self.emphasis_text_06(),
            font_size=24,
            width=10.4,
            color=TEAL_B,
        )
        note.next_to(components, DOWN, buff=0.34)
        note.set_x(0)

        self.keep_inside_safe(VGroup(title, sub, formula, explain, components, note))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.write_math(formula, rt=0.86)
        for line in explain:
            self.reveal_text(line, rt=0.54)
            self.W(0.18)
        for badge in components:
            self.reveal_group(badge, rt=0.34)
            self.W(0.06)
        self.reveal_group(note, rt=0.68)
        self.W(1.40)

    def slide_app1_small_k(self):
        title, sub = self.app1_title("Khi k nhỏ thì điều gì xảy ra")

        original = self.labeled_matrix_visual(
            self.image_matrix_original(),
            "Ảnh gốc",
            "đủ nhiều thành phần",
            cell_size=0.28,
        )
        approx = self.labeled_matrix_visual(
            self.image_matrix_k2(),
            "A₂",
            "chỉ giữ 2 singular values",
            cell_size=0.28,
        )
        body = self.build_two_column(original, approx, gap=1.05)
        body.next_to(sub, DOWN, buff=0.42)

        compare_text = self.bullet_block(
            [
                "Khung lớn của ảnh vẫn còn nhận ra được.",
                "Nhưng biên sắc nét và chi tiết nhỏ bị nhòe đi.",
                "Điều này xảy ra vì ta chỉ giữ lại rất ít hướng quan trọng.",
            ],
            font_size=26,
            width=11.0,
        )
        compare_text.next_to(body, DOWN, buff=0.40)
        compare_text.align_to(sub, LEFT)
        compare_text.shift(LEFT * 1.45)

        self.keep_inside_safe(VGroup(title, sub, body, compare_text))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(original, rt=0.76)
        self.W(0.24)
        self.reveal_group(approx, rt=0.76)
        self.W(0.24)
        for line in compare_text:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        self.W(1.42)
        self.wait(1.0)

    def slide_app1_large_k(self):
        title, sub = self.app1_title("Khi k lớn thì điều gì xảy ra")

        original = self.labeled_matrix_visual(
            self.image_matrix_original(),
            "Ảnh gốc",
            "tham chiếu",
            cell_size=0.28,
        )
        approx = self.labeled_matrix_visual(
            self.image_matrix_k20(),
            "A₂₀",
            "giữ 20 singular values",
            cell_size=0.28,
        )
        original.align_to(approx, UP)
        body = self.build_two_column(original, approx, gap=0.92)
        body.next_to(sub, DOWN, buff=0.42)
        body.move_to([0.35, body.get_center()[1], 0])

        compare_text = self.bullet_block(
            [
                "Khi tăng k, nhiều chi tiết mảnh quay trở lại.",
                "Ảnh phục hồi tốt hơn và gần với ảnh gốc hơn.",
                "Đổi lại, số lượng thành phần cần lưu cũng tăng lên.",
            ],
            font_size=30,
            width=11.2,
        )
        compare_text.next_to(body, DOWN, buff=0.40)
        compare_text.align_to(sub, LEFT)
        compare_text.shift(LEFT * 1.45)

        self.keep_inside_safe(VGroup(title, sub, body, compare_text))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(original, rt=0.76)
        self.W(0.24)
        self.reveal_group(approx, rt=0.76)
        self.W(0.24)
        for line in compare_text:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        self.W(1.42)

    def slide_app1_tradeoff(self):
        title, sub = self.app1_title("Đánh đổi giữa chất lượng và dung lượng")

        left_bars = self.bar_chart_manual(
            [2, 8, 20, 40],
            max_height=1.9,
            bar_width=0.28,
            labels=None,
            baseline_width=4.6,
        )
        bar_group = left_bars[1]

        value_labels = []
        for bar, lab in zip(bar_group, ["2", "8", "20", "40"]):
            t = self.VText(lab, font_size=18)
            t.move_to([bar.get_center()[0], left_bars[0].get_center()[1] - 0.26, 0])
            value_labels.append(t)
        value_labels = VGroup(*value_labels)

        prefix_k = self.VText("k =", font_size=18)
        prefix_k.next_to(value_labels[0], LEFT, buff=0.18)
        prefix_k.align_to(value_labels[0], DOWN)

        left_chart = VGroup(left_bars[0], bar_group, value_labels, prefix_k)

        right_bars = self.bar_chart_manual(
            [1.0, 0.82, 0.54, 0.25],
            max_height=1.9,
            bar_width=0.34,
            labels=["mờ", "vừa", "khá", "rõ"],
            baseline_width=3.5,
        )

        label_left = self.VText("Số thành phần giữ lại", font_size=24, color=YELLOW_B)
        label_right = self.VText("Sai khác tương đối giảm dần", font_size=24, color=BLUE_C)

        left_group = VGroup(label_left, left_chart).arrange(DOWN, buff=0.12)
        right_group = VGroup(label_right, right_bars).arrange(DOWN, buff=0.12)

        graphs = VGroup(left_group, right_group).arrange(RIGHT, buff=1.10, aligned_edge=UP)
        graphs.next_to(sub, DOWN, buff=0.42)
        graphs.set_x(0)

        panel = self.compression_tradeoff_panel("Giữ ít", "Giữ nhiều")
        panel.next_to(graphs, DOWN, buff=0.52)
        panel.set_x(0)
        panel[1].move_to([right_group.get_center()[0], panel[1].get_center()[1], 0])

        self.keep_inside_safe(VGroup(title, sub, graphs, panel))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(left_group, rt=0.72)
        self.W(0.18)
        self.reveal_group(right_group, rt=0.72)
        self.W(0.28)
        self.reveal_group(panel, rt=0.82)
        self.W(1.46)
        self.wait(2.0)

    def slide_app1_compare_many_levels(self):
        title, sub = self.app1_title("So sánh nhiều mức k khác nhau")
        title.set_x(0.10)
        if sub:
            sub.set_x(0.10)

        a2 = self.labeled_matrix_visual(
            self.image_matrix_k2(),
            "k = 2",
            "mờ hơn, còn khung lớn",
            cell_size=0.22,
        )
        a8 = self.labeled_matrix_visual(
            self.image_matrix_k8(),
            "k = 8",
            "chi tiết trung bình",
            cell_size=0.22,
        )
        a20 = self.labeled_matrix_visual(
            self.image_matrix_k20(),
            "k = 20",
            "khá gần ảnh gốc",
            cell_size=0.22,
        )
        a40 = self.labeled_matrix_visual(
            self.image_matrix_k40(),
            "k = 40",
            "rất gần ảnh gốc",
            cell_size=0.22,
        )

        a20[0].scale(0.86)
        a40[0].scale(0.86)

        row = VGroup(a2, a8, a20, a40).arrange(RIGHT, buff=0.26, aligned_edge=UP)
        row.scale_to_fit_width(11.10)
        row.next_to(sub, DOWN, buff=0.38)
        row.set_x(0.10)

        bottom = self.paragraph_block(
            [
                "Quan sát theo thứ tự từ trái sang phải, ta thấy chất lượng ảnh tăng dần.",
                "Cảm giác thị giác này chính là biểu hiện trực quan của xấp xỉ hạng thấp.",
                "Ta không cần giữ toàn bộ dữ liệu ngay từ đầu để nắm được cấu trúc chính.",
            ],
            font_size=27,
            width=10.6,
        )
        bottom.next_to(row, DOWN, buff=0.40)
        bottom.set_x(-0.12)

        self.keep_inside_safe(VGroup(title, sub, row, bottom))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for block in [a2, a8, a20, a40]:
            self.reveal_group(block, rt=0.54)
            self.W(0.12)
        for line in bottom:
            self.reveal_text(line, rt=0.50)
            self.W(0.16)
        self.W(1.38)
        self.wait(2.0)

    def slide_app1_summary(self):
        title, sub = self.app1_title("Kết luận riêng cho ứng dụng nén ảnh")
        title.shift(LEFT * 0.22)
        if sub:
            sub.shift(LEFT * 0.22)

        formula = MathTex(r"A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T").scale(1.05)
        formula.next_to(sub, DOWN, buff=0.26)
        formula.shift(LEFT * 0.22)

        summary = self.bullet_block(
            [
                "SVD cho phép xấp xỉ hạng thấp của ma trận ảnh.",
                "Nhờ đó ta nén dữ liệu nhưng vẫn giữ được hình dạng và cấu trúc chính.",
                "Đây là một trong những ứng dụng tiêu biểu nhất của đại số tuyến tính trong thực tế.",
            ],
            font_size=28,
            width=10.6,
        )
        summary.next_to(formula, DOWN, buff=0.36)
        summary.shift(LEFT * 0.22)

        visuals = VGroup(
            self.labeled_matrix_visual(self.image_matrix_k2(), "ít thành phần", "", cell_size=0.18),
            self.arrow_with_text(LEFT * 0.7, RIGHT * 0.7, "tăng k", font_size=20, color=YELLOW_B),
            self.labeled_matrix_visual(self.image_matrix_k20(), "nhiều thành phần", "", cell_size=0.18),
        ).arrange(RIGHT, buff=0.28)
        visuals.next_to(summary, DOWN, buff=0.44)

        self.keep_inside_safe(VGroup(title, sub, formula, summary, visuals))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.write_math(formula, rt=0.80)
        for line in summary:
            self.reveal_text(line, rt=0.54)
            self.W(0.18)
        self.reveal_group(visuals[0], rt=0.52)
        self.play(GrowArrow(visuals[1][0]), FadeIn(visuals[1][1], shift=UP * 0.05), run_time=0.58)
        self.reveal_group(visuals[2], rt=0.52)
        self.W(1.50)

    def app2_title(self, subtitle: str):
        title, sub = self.top_title("Ứng dụng 2 - PCA và giảm chiều dữ liệu", subtitle)
        title.move_to([0, title.get_center()[1], 0])
        if sub:
            sub.move_to([0, sub.get_center()[1], 0])
        return title, sub

    def slide_app2_pca_intro(self):
        old_pace = getattr(self, "current_pace", self.PACE)
        self.current_pace = 1.48

        title, sub = self.app2_title("Dữ liệu nhiều chiều thường dư thừa và khó quan sát trực tiếp")
        title.shift(LEFT * 0.24)
        if sub:
            sub.shift(LEFT * 0.24)

        text = self.bullet_block(
            [
                "Khi một bộ dữ liệu có quá nhiều chiều, ta khó nhìn thấy cấu trúc chính.",
                "Nhiều chiều thực ra có thể gần phụ thuộc nhau hoặc chứa thông tin lặp lại.",
                "SVD giúp ta tìm ra các hướng quan trọng nhất để biểu diễn dữ liệu gọn hơn.",
            ],
            font_size=29,
            width=11.0,
        )
        text.next_to(sub, DOWN, buff=0.54)
        text.align_to(sub, LEFT)
        text.shift(RIGHT * 0.26 + DOWN * 0.12)

        badges = VGroup(
            self.value_badge("Nhiều chiều", color=YELLOW_B, font_size=23),
            self.value_badge("Chọn trục chính", color=TEAL_B, font_size=23),
            self.value_badge("Giảm chiều", color=GREEN_B, font_size=23),
        ).arrange(RIGHT, buff=0.34)
        badges.scale_to_fit_width(5.6)
        badges.next_to(text[-1], DOWN, buff=0.42)
        badges.move_to([text[-1].get_center()[0], badges.get_center()[1], 0])
        badges.shift(DOWN * 0.02)

        self.keep_inside_safe(VGroup(title, sub, text, badges))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in text:
            self.reveal_text(line, rt=0.50)
            self.W(0.22)
        for badge in badges:
            self.reveal_group(badge, rt=0.38)
            self.W(0.12)
        self.W(1.60)
        self.current_pace = old_pace

    def slide_app2_pca_visual(self):
        title, sub = self.app2_title("Đám mây điểm nghiêng và trục chính")

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=5.2,
            y_length=4.0,
            axis_config={"include_numbers": False, "color": GREY_B},
        )
        axes.next_to(sub, DOWN, buff=0.38)
        axes.shift(LEFT * 2.8)

        dots = self.manual_scatter_points()
        dots.move_to(axes.c2p(0, 0))

        main_axis = Line(axes.c2p(-3.3, -2.1), axes.c2p(3.0, 2.2), color=YELLOW_B, stroke_width=4)
        sec_axis = Line(axes.c2p(-0.9, 1.8), axes.c2p(1.1, -1.2), color=BLUE_C, stroke_width=3)

        text = VGroup(
            self.VText("• Đám mây điểm kéo dài mạnh\n  theo một hướng nghiêng.", font_size=30),
            self.VText("• PCA giữ hướng biến thiên\n  mạnh nhất trước.", font_size=30),
            self.VText("• Sau đó ta có thể chiếu dữ liệu\n  lên ít trục hơn để giảm chiều.", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        text.next_to(axes, RIGHT, buff=0.72)
        text.align_to(axes, UP)

        formula = MathTex(r"X\approx U_k\Sigma_kV_k^T").scale(0.90)
        formula.next_to(text, DOWN, buff=0.58)
        formula.align_to(text, LEFT)

        self.keep_inside_safe(VGroup(title, sub, axes, dots, main_axis, sec_axis, text, formula))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.play(Create(axes), run_time=0.75)
        self.play(FadeIn(dots, shift=UP * 0.10), run_time=0.78)
        self.play(Create(main_axis), run_time=0.55)
        self.play(Create(sec_axis), run_time=0.55)
        for line in text:
            self.reveal_text(line, rt=0.46)
            self.W(0.14)
        self.write_math(formula, rt=0.72)
        self.W(1.42)

    def slide_app2_pca_summary(self):
        old_pace = getattr(self, "current_pace", self.PACE)
        self.current_pace = 1.52

        title, sub = self.app2_title("Tóm lại về PCA")
        title.set_x(0)
        if sub:
            sub.set_x(0)

        left = VGroup(
            self.VText("• Giữ lại ít trục nhưng", font_size=40),
            self.VText("  vẫn giữ được phần lớn biến thiên.", font_size=40),
            self.spacer(0.26),
            self.VText("• Giúp trực quan hóa dữ liệu", font_size=40),
            self.VText("  và giảm chi phí tính toán.", font_size=40),
            self.spacer(0.26),
            self.VText("• SVD là nền tảng phổ biến", font_size=40),
            self.VText("  để thực hiện PCA trong thực hành.", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        left.scale_to_fit_width(5.95)

        right = self.simple_panel(
            VGroup(
                self.VText("Ý nghĩa trực quan", font_size=25, color=YELLOW_B, weight=BOLD),
                self.VText("giữ phần kéo dài nhất", font_size=23),
                self.VText("bỏ bớt hướng yếu hơn", font_size=23),
                self.VText("dữ liệu gọn mà vẫn có cấu trúc", font_size=23),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10),
            width=5.1,
            height=3.15,
            color=GREY_B,
        )

        body = self.build_two_column(left, right, gap=1.02)
        body.next_to(sub, DOWN, buff=0.46)

        self.keep_inside_safe(VGroup(title, sub, body))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in left:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        self.reveal_group(right, rt=0.72)
        self.W(1.74)
        self.current_pace = old_pace

    def app3_title(self, subtitle: str):
        title, sub = self.top_title("Ứng dụng 3 - Xử lý văn bản và LSA/LSI", subtitle)
        title.move_to([0, title.get_center()[1], 0])
        if sub:
            sub.move_to([0, sub.get_center()[1], 0])
        return title, sub

    def slide_app3_lsa_intro(self):
        title, sub = self.app3_title("Từ - tài liệu có thể được biểu diễn bằng một ma trận")

        text = self.bullet_block(
            [
                "Mỗi hàng là một từ, mỗi cột là một tài liệu.",
                "Phần tử trong bảng cho biết tần suất hoặc mức độ xuất hiện của từ đó.",
                "Ma trận này thường rất thưa và có nhiều mối quan hệ ẩn khó nhìn trực tiếp.",
            ],
            font_size=27,
            width=10.9,
        )
        text.next_to(sub, DOWN, buff=0.40)
        text.align_to(sub, LEFT)

        example_table = self.build_table(self.term_document_data(), cell_width=1.45, cell_height=0.52, header_rows=1)
        example_table.next_to(text, DOWN, buff=0.42)

        self.keep_inside_safe(VGroup(title, sub, text, example_table))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in text:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        self.reveal_group(example_table, rt=0.84)
        self.W(1.40)

    def slide_app3_lsa_matrix(self):
        title, sub = self.app3_title("SVD giúp rút ra cấu trúc ngữ nghĩa ẩn")

        left_table = self.build_table(self.term_document_data(), cell_width=1.30, cell_height=0.48, header_rows=1)
        left_title = self.VText("Ma trận gốc", font_size=24, color=YELLOW_B)
        left = VGroup(left_title, left_table).arrange(DOWN, buff=0.12)

        right_table = self.build_table(self.term_document_clustered_data(), cell_width=1.30, cell_height=0.48, header_rows=2)
        right_title = self.VText("Nhóm chủ đề ẩn sau SVD", font_size=24, color=GREEN_B)
        right = VGroup(right_title, right_table).arrange(DOWN, buff=0.12)

        body = self.build_two_column(left, right, gap=0.55)
        body.next_to(sub, DOWN, buff=0.38)

        bottom = self.bullet_block(
            [
                "Những từ có ý nghĩa gần nhau có thể được đặt gần hơn trong không gian ẩn.",
                "Những tài liệu nói về chủ đề gần nhau cũng được gom lại.",
                "Đó là trực giác phía sau latent semantic analysis hoặc latent semantic indexing.",
            ],
            font_size=25,
            width=11.0,
        )
        bottom.next_to(body, DOWN, buff=0.36)
        bottom.set_x(0)

        self.keep_inside_safe(VGroup(title, sub, body, bottom))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(left, rt=0.76)
        self.W(0.22)
        self.reveal_group(right, rt=0.76)
        self.W(0.22)
        for line in bottom:
            self.reveal_text(line, rt=0.46)
            self.W(0.14)
        self.W(1.30)
        self.wait(3.0)

    def slide_app3_lsa_summary(self):
        title, sub = self.app3_title("Ý nghĩa của LSA/LSI")

        panel = self.simple_panel(
            VGroup(
                self.VText("Từ khóa bề mặt", font_size=26, color=YELLOW_B, weight=BOLD),
                self.VText("không phải lúc nào cũng đủ để hiểu chủ đề", font_size=23),
                self.spacer(0.10),
                self.VText("Không gian ẩn sau SVD", font_size=26, color=GREEN_B, weight=BOLD),
                self.VText("giúp ta thấy mối liên hệ ngữ nghĩa sâu hơn", font_size=23),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            width=10.6,
            height=3.0,
            color=GREY_B,
        )
        panel.next_to(sub, DOWN, buff=0.52)

        self.keep_inside_safe(VGroup(title, sub, panel))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(panel, rt=0.84)
        self.W(1.56)

    # --------------------------------------------------------------
    # Ứng dụng 4: Recommendation System
    # --------------------------------------------------------------
    def app4_title(self, subtitle: str):
        title, sub = self.top_title("Ứng dụng 4 - Hệ gợi ý", subtitle)
        title.move_to([0, title.get_center()[1], 0])
        if sub:
            sub.move_to([0, sub.get_center()[1], 0])
        return title, sub

    def slide_app4_rec_intro(self):
        title, sub = self.app4_title("Ma trận user-item thường khuyết dữ liệu")

        text = self.bullet_block(
            [
                "Người dùng chưa xem hết mọi phim hay mọi sản phẩm.",
                "Vì thế bảng đánh giá thường có rất nhiều ô còn trống.",
                "Ta muốn suy ra sở thích ẩn để dự đoán những ô còn thiếu.",
            ],
            font_size=27,
            width=10.9,
        )
        text.next_to(sub, DOWN, buff=0.40)
        text.align_to(sub, LEFT)

        table = self.build_table(self.user_item_data(), cell_width=1.15, cell_height=0.52, header_rows=1)
        table.next_to(text, DOWN, buff=0.42)

        self.keep_inside_safe(VGroup(title, sub, text, table))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in text:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        self.reveal_group(table, rt=0.80)
        self.W(1.34)
        self.wait(1.0)

    def slide_app4_rec_matrix(self):
        title, sub = self.app4_title("Factorization giúp phát hiện sở thích ẩn")

        left = self.build_table(self.user_item_data(), cell_width=1.05, cell_height=0.48, header_rows=1)
        left_title = self.VText("Ma trận đánh giá", font_size=24, color=YELLOW_B)
        left_block = VGroup(left_title, left).arrange(DOWN, buff=0.12)

        right = self.build_table(self.user_item_factors_data(), cell_width=1.30, cell_height=0.48, header_rows=1)
        right_title = self.VText("Một cách hiểu theo latent factors", font_size=24, color=GREEN_B)
        right_block = VGroup(right_title, right).arrange(DOWN, buff=0.12)

        body = self.build_two_column(left_block, right_block, gap=0.56)
        body.next_to(sub, DOWN, buff=0.38)

        note = self.note_box(
            "Người dùng A và B có thể đều thích nhóm “hành động”, còn C và D gần với nhóm “tình cảm”.",
            font_size=22,
            width=11.0,
            color=TEAL_B,
        )
        note.next_to(body, DOWN, buff=0.36)

        self.keep_inside_safe(VGroup(title, sub, body, note))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(left_block, rt=0.76)
        self.W(0.24)
        self.reveal_group(right_block, rt=0.76)
        self.W(0.24)
        self.reveal_group(note, rt=0.66)
        self.W(1.34)
        self.wait(3.0)


    def slide_app4_rec_summary(self):
        title, sub = self.app4_title("Từ latent factors đến gợi ý")

        left_lines = VGroup(
            self.VText("• Nếu user gần với một nhóm sở thích ẩn nào đó,", font_size=34),
            self.VText("  hệ thống có thể gợi ý item phù hợp hơn.", font_size=34),
            self.VText("  Nó không chỉ nhìn vào từng ô đánh giá riêng lẻ.", font_size=34),

            self.spacer(0.42),

            self.VText("• Không cần người dùng đánh giá mọi thứ trước", font_size=34),
            self.VText("  khi hệ thống bắt đầu hoạt động.", font_size=34),
            self.VText("  Mô hình vẫn có thể suy ra xu hướng chung.", font_size=34),

            self.spacer(0.42),

            self.VText("• SVD và các mô hình factorization là nền tảng", font_size=34),
            self.VText("  quan trọng của recommendation system.", font_size=34),
            self.VText("  Chúng giúp biến dữ liệu thưa thành gợi ý hữu ích.", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        left_lines.scale_to_fit_width(6.35)

        right_title = self.VText("Ví dụ trực quan", font_size=32, color=YELLOW_B, weight=BOLD)
        right_1 = self.VText("A thích P1, P2", font_size=25)
        right_2 = self.VText("latent factor cho thấy", font_size=25)
        right_3 = self.VText("A gần với P3", font_size=25)
        right_4 = self.VText("→ hệ thống gợi ý P3", font_size=26, color=GREEN_B)

        right_inner = VGroup(
            right_title,
            right_1,
            right_2,
            right_3,
            right_4,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        right = self.simple_panel(
            right_inner,
            width=5.35,
            height=3.55,
            color=GREY_B,
        )

        body = VGroup(left_lines, right).arrange(RIGHT, buff=0.72, aligned_edge=UP)
        body.next_to(sub, DOWN, buff=0.42)
        body.shift(LEFT * 0.32)

        self.keep_inside_safe(VGroup(title, sub, body))

        self.reveal_text(title, rt=0.75)
        self.reveal_text(sub, rt=0.60)
        self.reveal_group(left_lines, rt=0.70)
        self.reveal_group(right, rt=0.70)
        self.W(1.5)
        self.wait(3.0)

    def app5_title(self, subtitle: str):
        title, sub = self.top_title("Ứng dụng 5 - Khử nhiễu", subtitle)
        title.move_to([0, title.get_center()[1], 0])
        if sub:
            sub.move_to([0, sub.get_center()[1], 0])
        return title, sub

    def slide_app5_noise_intro(self):
        title, sub = self.app5_title("Các singular values nhỏ đôi khi gắn với nhiễu hoặc chi tiết rất yếu")

        text = self.bullet_block(
            [
                "Nếu dữ liệu bị nhiễu, phần đuôi singular values có thể chứa nhiều thành phần không ổn định.",
                "Bỏ bớt các thành phần quá nhỏ đôi khi giúp dữ liệu mượt hơn.",
                "Ý tưởng này không phải lúc nào cũng hoàn hảo, nhưng rất trực quan và hữu ích.",
            ],
            font_size=27,
            width=10.9,
        )
        text.next_to(sub, DOWN, buff=0.40)
        text.align_to(sub, LEFT)

        bars = self.bar_chart_manual(
            self.singular_values_small_tail(),
            max_height=2.1,
            bar_width=0.30,
            labels=["σ1", "σ2", "σ3", "σ4", "σ5", "σ6", "σ7", "σ8"],
            baseline_width=3.8,
        )
        bars.next_to(text, DOWN, buff=0.42)

        self.keep_inside_safe(VGroup(title, sub, text, bars))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in text:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        self.reveal_group(bars, rt=0.78)
        self.W(1.34)
        self.wait(2.0)

    def slide_app5_noise_visual(self):
        title, sub = self.app5_title("Minh họa trước và sau khi bỏ bớt thành phần nhỏ")

        noisy_img = self.labeled_matrix_visual(
            self.image_matrix_noise(),
            "Dữ liệu nhiễu",
            "nhiều dao động nhỏ, khó nhìn cấu trúc chính",
            cell_size=0.25,
        )
        denoised_img = self.labeled_matrix_visual(
            self.image_matrix_denoised(),
            "Sau khi làm mượt",
            "cấu trúc chính rõ hơn",
            cell_size=0.25,
        )

        top = self.build_two_column(noisy_img, denoised_img, gap=0.95)
        top.next_to(sub, DOWN, buff=0.36)

        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=5.4,
            y_length=2.8,
            axis_config={"include_numbers": False, "color": GREY_B},
        )
        axes.next_to(top, DOWN, buff=0.42)

        noisy_curve = self.polyline_from_points([axes.c2p(p[0], p[1]) for p in self.noisy_wave_points()], color=YELLOW_B, width=3)
        smooth_curve = self.polyline_from_points([axes.c2p(p[0], p[1]) for p in self.smooth_wave_points()], color=GREEN_B, width=4)

        label1 = self.VText("nhiễu", font_size=22, color=YELLOW_B).next_to(axes, LEFT, buff=0.18).shift(UP * 0.62)
        label2 = self.VText("mượt hơn", font_size=22, color=GREEN_B).next_to(axes, LEFT, buff=0.18).shift(DOWN * 0.52)

        self.keep_inside_safe(VGroup(title, sub, top, axes, noisy_curve, smooth_curve, label1, label2))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(noisy_img, rt=0.70)
        self.W(0.18)
        self.reveal_group(denoised_img, rt=0.70)
        self.W(0.22)
        self.play(Create(axes), run_time=0.62)
        self.play(Create(noisy_curve), FadeIn(label1, shift=RIGHT * 0.05), run_time=0.72)
        self.play(Create(smooth_curve), FadeIn(label2, shift=RIGHT * 0.05), run_time=0.72)
        self.W(1.34)

    def slide_app5_noise_summary(self):
        title, sub = self.app5_title("Ý nghĩa của khử nhiễu bằng ý tưởng hạng thấp")

        panel = self.simple_panel(
            VGroup(
                self.VText("Không phải mọi singular value nhỏ đều là vô ích.", font_size=23),
                self.VText("Nhưng trong nhiều bài toán, phần nhỏ nhất dễ gắn với nhiễu hơn.", font_size=23),
                self.VText("Vì vậy, xấp xỉ hạng thấp có thể làm dữ liệu mượt hơn và dễ phân tích hơn.", font_size=23, color=YELLOW_B),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14),
            width=11.4,
            height=2.9,
            color=GREY_B,
        )
        panel.next_to(sub, DOWN, buff=0.52)

        self.keep_inside_safe(VGroup(title, sub, panel))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        self.reveal_group(panel, rt=0.84)
        self.W(1.50)
        self.wait(3.0)

    # --------------------------------------------------------------
    # Ứng dụng 6: Nhận dạng khuôn mặt / eigenfaces
    # --------------------------------------------------------------
    def app6_title(self, subtitle: str):
        title, sub = self.top_title("Ứng dụng 6 - Biểu diễn khuôn mặt", subtitle)
        title.move_to([0, title.get_center()[1], 0])
        if sub:
            sub.move_to([0, sub.get_center()[1], 0])
        return title, sub


    def slide_app6_face_intro(self):
        title, sub = self.app6_title("Nhiều ảnh khuôn mặt có thể được tóm tắt bằng một không gian đặc trưng gọn hơn")

        text = self.bullet_block(
            [
                "Mỗi ảnh mặt cũng có thể xem như một vector hoặc một ma trận cường độ sáng.",
                "Khi gom nhiều ảnh lại, SVD có thể tìm ra các mẫu biến thiên nổi bật nhất.",
                "Điều này dẫn đến ý tưởng eigenfaces hoặc biểu diễn khuôn mặt trong không gian thấp chiều.",
            ],
            font_size=27,
            width=10.9,
        )
        text.next_to(sub, DOWN, buff=0.40)
        text.align_to(sub, LEFT)

        mini1 = self.labeled_matrix_visual(self.face_matrix_1(), "mặt A", "", cell_size=0.16)
        mini2 = self.labeled_matrix_visual(self.face_matrix_2(), "mặt B", "", cell_size=0.16)
        mini3 = self.labeled_matrix_visual(self.face_matrix_mean(), "đặc trưng chung", "", cell_size=0.16)
        visual = VGroup(mini1, mini2, mini3).arrange(RIGHT, buff=0.32)
        visual.scale_to_fit_width(8.2)
        visual.next_to(text, DOWN, buff=0.42)
        visual.set_x(0)

        self.keep_inside_safe(VGroup(title, sub, text, visual))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in text:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        for block in visual:
            self.reveal_group(block, rt=0.46)
            self.W(0.08)
        self.W(1.28)
        self.wait(3.0)


    def slide_app6_face_visual(self):
        title, sub = self.app6_title("Từ nhiều ảnh mặt đến mặt trung bình và đặc trưng chính")

        face1 = self.labeled_matrix_visual(self.face_matrix_1(), "Mặt 1", "", cell_size=0.22)
        face2 = self.labeled_matrix_visual(self.face_matrix_2(), "Mặt 2", "", cell_size=0.22)
        mean_face = self.labeled_matrix_visual(self.face_matrix_mean(), "Mặt trung bình", "", cell_size=0.22)

        row = self.build_three_column(face1, face2, mean_face, gap=0.35)
        row.next_to(sub, DOWN, buff=0.40)

        note = self.note_box(
            "Thay vì lưu nguyên vẹn mọi ảnh, ta có thể lưu trung bình và vài hướng biến thiên chính để biểu diễn gọn hơn.",
            font_size=22,
            width=11.0,
            color=YELLOW_B,
        )
        note.next_to(row, DOWN, buff=0.44)

        self.keep_inside_safe(VGroup(title, sub, row, note))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for block in [face1, face2, mean_face]:
            self.reveal_group(block, rt=0.56)
            self.W(0.12)
        self.reveal_group(note, rt=0.68)
        self.W(1.42)

    def app7_title(self, subtitle: str):
        return self.top_title("Ứng dụng 7 - Cấu trúc ẩn và nén dữ liệu tổng quát", subtitle)

    def slide_app7_extra_intro(self):
        title, sub = self.app7_title("Không chỉ ảnh, nhiều loại dữ liệu khác cũng có thể được xấp xỉ hạng thấp")

        bullets = self.bullet_block(
            [
                "Log người dùng, tín hiệu cảm biến, ma trận tương tác hay dữ liệu khoa học đều có thể chứa cấu trúc lặp.",
                "SVD giúp tách phần mạnh và phần yếu trong rất nhiều bối cảnh khác nhau.",
                "Đó là lý do SVD xuất hiện rộng rãi trong khoa học dữ liệu, học máy và kỹ thuật tính toán.",
            ],
            font_size=27,
            width=10.9,
        )
        bullets.next_to(sub, DOWN, buff=0.40)
        bullets.align_to(sub, LEFT)

        badges = VGroup(
            self.value_badge("nén", color=YELLOW_B),
            self.value_badge("giảm chiều", color=TEAL_B),
            self.value_badge("tìm cấu trúc ẩn", color=GREEN_B),
            self.value_badge("lọc nhiễu", color=BLUE_C),
        ).arrange(RIGHT, buff=0.22)
        badges.scale_to_fit_width(10.5)
        badges.next_to(bullets, DOWN, buff=0.50)

        self.keep_inside_safe(VGroup(title, sub, bullets, badges))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for line in bullets:
            self.reveal_text(line, rt=0.48)
            self.W(0.16)
        for badge in badges:
            self.reveal_group(badge, rt=0.34)
            self.W(0.08)
        self.W(1.32)

    def slide_app7_extra_summary(self):
        title, sub = self.app7_title("Thông điệp chung của phần ứng dụng")

        groups = VGroup(
            self.simple_panel(
                VGroup(
                    self.VText("Giữ phần chính", font_size=24, color=YELLOW_B, weight=BOLD),
                    self.VText("nắm được cấu trúc lớn", font_size=22),
                ).arrange(DOWN, buff=0.08),
                width=3.3,
                height=1.6,
                color=GREY_B,
            ),
            self.simple_panel(
                VGroup(
                    self.VText("Bỏ phần yếu", font_size=24, color=GREEN_B, weight=BOLD),
                    self.VText("giảm dư thừa và nhiễu", font_size=22),
                ).arrange(DOWN, buff=0.08),
                width=3.3,
                height=1.6,
                color=GREY_B,
            ),
            self.simple_panel(
                VGroup(
                    self.VText("Biểu diễn gọn hơn", font_size=24, color=BLUE_C, weight=BOLD),
                    self.VText("dễ lưu trữ và phân tích", font_size=22),
                ).arrange(DOWN, buff=0.08),
                width=3.3,
                height=1.6,
                color=GREY_B,
            ),
        ).arrange(RIGHT, buff=0.36)
        groups.next_to(sub, DOWN, buff=0.52)

        self.keep_inside_safe(VGroup(title, sub, groups))

        self.reveal_text(title, rt=0.82)
        self.reveal_text(sub, rt=0.66)
        for panel in groups:
            self.reveal_group(panel, rt=0.50)
            self.W(0.12)
        self.W(1.42)

    # --------------------------------------------------------------
    # Tổng kết cuối video
    # --------------------------------------------------------------
    def slide_summary(self):
        title, sub = self.top_title(
            "Kết luận",
            "Từ chéo hóa đến SVD, ta đi từ lý thuyết sang các ứng dụng rất thực tế",
        )

        # Canh lại riêng tiêu đề, phụ đề và ô kết luận để hai lề đen cân xứng hơn.
        # Tiêu đề phải ở giữa phía trên phụ đề.
        title.set_x(0.10)
        if sub:
            sub.set_x(-0.06)

        g1 = VGroup(
            MathTex(r"A=PDP^{-1}").scale(0.95),
            self.VText("Chéo hóa: đưa ma trận về dạng chéo nhờ cơ sở vector riêng.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        g2 = VGroup(
            MathTex(r"A=U\Sigma V^T").scale(0.95),
            self.VText("SVD: quay - scale - quay, và áp dụng cho mọi ma trận thực.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        g3 = VGroup(
            MathTex(r"A_k=\sum_{i=1}^{k}\sigma_i u_i v_i^T").scale(0.82),
            self.VText("Truncated SVD: xấp xỉ hạng thấp, nén dữ liệu và giữ cấu trúc chính.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        g4 = VGroup(
            MathTex(r"\text{PCA / LSA / Recommendation / Denoising}").scale(0.74),
            self.VText("Các ứng dụng cho thấy SVD là một công cụ nền tảng trong dữ liệu và học máy.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)

        body = VGroup(g1, g2, g3, g4).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        body.scale_to_fit_width(11.2)
        body.next_to(sub, DOWN, buff=0.36)

        ending = self.note_box(
            "Thông điệp cuối: SVD mạnh vì vừa có ý nghĩa hình học rõ ràng, vừa giải được rất nhiều bài toán thực tế.",
            font_size=23,
            width=11.1,
            color=YELLOW_B,
        )
        ending.next_to(body, DOWN, buff=0.34)
        ending.shift(RIGHT * 0.18)

        self.keep_inside_safe(VGroup(title, sub, body, ending))

        self.reveal_text(title, rt=0.84)
        self.reveal_text(sub, rt=0.66)
        for group in [g1, g2, g3, g4]:
            self.write_math(group[0], rt=0.66)
            self.reveal_text(group[1], rt=0.56)
            self.W(0.24)
        self.reveal_group(ending, rt=0.74)
        self.W(1.20)

    def slide_thanks(self):
        message = self.VText(
            "Xin chân thành cảm ơn Thầy và Cô đã theo dõi!",
            font_size=36,
            color=YELLOW_B,
            weight=BOLD,
        )
        message.move_to(ORIGIN)
        self.keep_inside_safe(message)

        self.reveal_text(message, rt=0.90)
        self.W(2.20)

    # --------------------------------------------------------------
    # Các preset nội dung chi tiết để mã nguồn đủ rõ ràng và dễ đọc
    # --------------------------------------------------------------
    def preset_explanation_01(self):
        lines = [
            "Khung minh họa 1: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_02(self):
        lines = [
            "Khung minh họa 2: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_03(self):
        lines = [
            "Khung minh họa 3: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_04(self):
        lines = [
            "Khung minh họa 4: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_05(self):
        lines = [
            "Khung minh họa 5: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_06(self):
        lines = [
            "Khung minh họa 6: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_07(self):
        lines = [
            "Khung minh họa 7: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_08(self):
        lines = [
            "Khung minh họa 8: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_09(self):
        lines = [
            "Khung minh họa 9: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_10(self):
        lines = [
            "Khung minh họa 10: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_11(self):
        lines = [
            "Khung minh họa 11: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_12(self):
        lines = [
            "Khung minh họa 12: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_13(self):
        lines = [
            "Khung minh họa 13: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_14(self):
        lines = [
            "Khung minh họa 14: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_15(self):
        lines = [
            "Khung minh họa 15: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_16(self):
        lines = [
            "Khung minh họa 16: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_17(self):
        lines = [
            "Khung minh họa 17: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_18(self):
        lines = [
            "Khung minh họa 18: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_19(self):
        lines = [
            "Khung minh họa 19: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_20(self):
        lines = [
            "Khung minh họa 20: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_21(self):
        lines = [
            "Khung minh họa 21: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_22(self):
        lines = [
            "Khung minh họa 22: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_23(self):
        lines = [
            "Khung minh họa 23: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_24(self):
        lines = [
            "Khung minh họa 24: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_25(self):
        lines = [
            "Khung minh họa 25: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_26(self):
        lines = [
            "Khung minh họa 26: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_27(self):
        lines = [
            "Khung minh họa 27: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_28(self):
        lines = [
            "Khung minh họa 28: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_29(self):
        lines = [
            "Khung minh họa 29: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_30(self):
        lines = [
            "Khung minh họa 30: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_31(self):
        lines = [
            "Khung minh họa 31: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_32(self):
        lines = [
            "Khung minh họa 32: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_33(self):
        lines = [
            "Khung minh họa 33: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_34(self):
        lines = [
            "Khung minh họa 34: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_35(self):
        lines = [
            "Khung minh họa 35: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_36(self):
        lines = [
            "Khung minh họa 36: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_37(self):
        lines = [
            "Khung minh họa 37: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_38(self):
        lines = [
            "Khung minh họa 38: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_39(self):
        lines = [
            "Khung minh họa 39: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_40(self):
        lines = [
            "Khung minh họa 40: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_41(self):
        lines = [
            "Khung minh họa 41: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_42(self):
        lines = [
            "Khung minh họa 42: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_43(self):
        lines = [
            "Khung minh họa 43: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_44(self):
        lines = [
            "Khung minh họa 44: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_45(self):
        lines = [
            "Khung minh họa 45: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_46(self):
        lines = [
            "Khung minh họa 46: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_47(self):
        lines = [
            "Khung minh họa 47: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_48(self):
        lines = [
            "Khung minh họa 48: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_49(self):
        lines = [
            "Khung minh họa 49: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def preset_explanation_50(self):
        lines = [
            "Khung minh họa 50: nhấn mạnh nhịp trình bày chậm, rõ và trực quan.",
            "Các dòng này được tách thành helper riêng để mã nguồn dễ bảo trì hơn.",
            "Khi cần mở rộng thêm nội dung, ta có thể tái sử dụng bộ preset này.",
        ]
        group = self.paragraph_block(lines, font_size=20, width=6.0)
        return group

    def tiny_matrix_preset_01(self):
        return [
            [11, 15, 21, 27],
            [15, 25, 41, 51],
            [19, 39, 65, 71],
            [13, 25, 37, 45],
        ]

    def tiny_matrix_preset_02(self):
        return [
            [12, 16, 22, 28],
            [16, 26, 42, 52],
            [20, 40, 66, 72],
            [14, 26, 38, 46],
        ]

    def tiny_matrix_preset_03(self):
        return [
            [13, 17, 23, 29],
            [17, 27, 43, 53],
            [21, 41, 67, 73],
            [15, 27, 39, 47],
        ]

    def tiny_matrix_preset_04(self):
        return [
            [14, 18, 24, 30],
            [18, 28, 44, 54],
            [22, 42, 68, 74],
            [16, 28, 40, 48],
        ]

    def tiny_matrix_preset_05(self):
        return [
            [15, 19, 25, 31],
            [19, 29, 45, 55],
            [23, 43, 69, 75],
            [17, 29, 41, 49],
        ]

    def tiny_matrix_preset_06(self):
        return [
            [16, 20, 26, 32],
            [20, 30, 46, 56],
            [24, 44, 70, 76],
            [18, 30, 42, 50],
        ]

    def tiny_matrix_preset_07(self):
        return [
            [17, 21, 27, 33],
            [21, 31, 47, 57],
            [25, 45, 71, 77],
            [19, 31, 43, 51],
        ]

    def tiny_matrix_preset_08(self):
        return [
            [18, 22, 28, 34],
            [22, 32, 48, 58],
            [26, 46, 72, 78],
            [20, 32, 44, 52],
        ]

    def tiny_matrix_preset_09(self):
        return [
            [19, 23, 29, 35],
            [23, 33, 49, 59],
            [27, 47, 73, 79],
            [21, 33, 45, 53],
        ]

    def tiny_matrix_preset_10(self):
        return [
            [20, 24, 30, 36],
            [24, 34, 50, 60],
            [28, 48, 74, 80],
            [22, 34, 46, 54],
        ]

    def tiny_matrix_preset_11(self):
        return [
            [21, 25, 31, 37],
            [25, 35, 51, 61],
            [29, 49, 75, 81],
            [23, 35, 47, 55],
        ]

    def tiny_matrix_preset_12(self):
        return [
            [22, 26, 32, 38],
            [26, 36, 52, 62],
            [30, 50, 76, 82],
            [24, 36, 48, 56],
        ]

    def tiny_matrix_preset_13(self):
        return [
            [23, 27, 33, 39],
            [27, 37, 53, 63],
            [31, 51, 77, 83],
            [25, 37, 49, 57],
        ]

    def tiny_matrix_preset_14(self):
        return [
            [24, 28, 34, 40],
            [28, 38, 54, 64],
            [32, 52, 78, 84],
            [26, 38, 50, 58],
        ]

    def tiny_matrix_preset_15(self):
        return [
            [25, 29, 35, 41],
            [29, 39, 55, 65],
            [33, 53, 79, 85],
            [27, 39, 51, 59],
        ]

    def tiny_matrix_preset_16(self):
        return [
            [26, 30, 36, 42],
            [30, 40, 56, 66],
            [34, 54, 80, 86],
            [28, 40, 52, 60],
        ]

    def tiny_matrix_preset_17(self):
        return [
            [27, 31, 37, 43],
            [31, 41, 57, 67],
            [35, 55, 81, 87],
            [29, 41, 53, 61],
        ]

    def tiny_matrix_preset_18(self):
        return [
            [28, 32, 38, 44],
            [32, 42, 58, 68],
            [36, 56, 82, 88],
            [30, 42, 54, 62],
        ]

    def tiny_matrix_preset_19(self):
        return [
            [29, 33, 39, 45],
            [33, 43, 59, 69],
            [37, 57, 83, 89],
            [31, 43, 55, 63],
        ]

    def tiny_matrix_preset_20(self):
        return [
            [30, 34, 40, 46],
            [34, 44, 60, 70],
            [38, 58, 84, 90],
            [32, 44, 56, 64],
        ]

    def tiny_matrix_preset_21(self):
        return [
            [31, 35, 41, 47],
            [35, 45, 61, 71],
            [39, 59, 85, 91],
            [33, 45, 57, 65],
        ]

    def tiny_matrix_preset_22(self):
        return [
            [32, 36, 42, 48],
            [36, 46, 62, 72],
            [40, 60, 86, 92],
            [34, 46, 58, 66],
        ]

    def tiny_matrix_preset_23(self):
        return [
            [33, 37, 43, 49],
            [37, 47, 63, 73],
            [41, 61, 87, 93],
            [35, 47, 59, 67],
        ]

    def tiny_matrix_preset_24(self):
        return [
            [34, 38, 44, 50],
            [38, 48, 64, 74],
            [42, 62, 88, 94],
            [36, 48, 60, 68],
        ]

    def tiny_matrix_preset_25(self):
        return [
            [35, 39, 45, 51],
            [39, 49, 65, 75],
            [43, 63, 89, 95],
            [37, 49, 61, 69],
        ]

    def tiny_matrix_preset_26(self):
        return [
            [36, 40, 46, 52],
            [40, 50, 66, 76],
            [44, 64, 90, 96],
            [38, 50, 62, 70],
        ]

    def tiny_matrix_preset_27(self):
        return [
            [37, 41, 47, 53],
            [41, 51, 67, 77],
            [45, 65, 91, 97],
            [39, 51, 63, 71],
        ]

    def tiny_matrix_preset_28(self):
        return [
            [38, 42, 48, 54],
            [42, 52, 68, 78],
            [46, 66, 92, 98],
            [40, 52, 64, 72],
        ]

    def tiny_matrix_preset_29(self):
        return [
            [39, 43, 49, 55],
            [43, 53, 69, 79],
            [47, 67, 93, 99],
            [41, 53, 65, 73],
        ]

    def tiny_matrix_preset_30(self):
        return [
            [40, 44, 50, 56],
            [44, 54, 70, 80],
            [48, 68, 94, 100],
            [42, 54, 66, 74],
        ]
