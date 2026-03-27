"""
File: manim_scene.py
Người làm: Đoàn Bảo

Nhiệm vụ:
- Tạo video Manim minh họa:
    1. Intro
    2. Diagonalization
    3. SVD geometry
    4. Application
"""

from manim import *


class SVDScene(Scene):

    def construct(self):
        """
        TODO:
        - Gọi lần lượt các scene nhỏ
        """
        self.intro_scene()
        self.diagonalization_scene()
        self.svd_geometry_scene()
        self.application_scene()


    def intro_scene(self):
        """
        TODO:
        - Hiển thị matrix A
        - Giới thiệu bài toán
        """
        pass


    def diagonalization_scene(self):
        """
        TODO:
        - Hiển thị:
            A^T A = V Λ V^T
        - Giải thích eigenvalues, eigenvectors

        Lưu ý:
        - Có thể hardcode ví dụ matrix nhỏ
        """
        pass


    def svd_geometry_scene(self):
        """
        TODO:
        - Minh họa:
            rotate → scale → rotate

        Gợi ý:
        - bắt đầu từ Circle()
        - transform thành ellipse
        """
        pass


    def application_scene(self):
        """
        TODO:
        - Minh họa ứng dụng:
            + nén ảnh (đơn giản)
            hoặc
            + transform shape

        - Có thể chỉ cần demo concept
        """
        pass
