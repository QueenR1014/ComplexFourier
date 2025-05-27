from manim import *
import numpy as np

class FourierApproximation(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0,2.5],
            y_range=[-1.5, 1.5],
            x_length=10,
            y_length=4,
            axis_config={"include_tip": True},
            
        ).add_coordinates()
        self.add(axes)
        #plantilla pa no perdernos 
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{amssymb}")

        series = MathTex(r"f(x) \sim \sum_{n=1}^{\infty} \frac{4}{n\pi} \sin(n\pi x)")
        series.to_corner(UR)


        # Define the target function f(x)
        # Define each part separately to preserve the jump
        f1 = axes.plot(lambda x: 1, x_range=[0, 1], color=RED)
        f2 = axes.plot(lambda x: -1, x_range=[1, 2], color=BLUE)
        # Optional: show jump with dots
        dot_left = Dot(axes.c2p(1, 1), color=RED)     # left limit
        dot_right = Dot(axes.c2p(1, -1), color=BLUE)   # right limit
        discontinuity = DashedLine(dot_left.get_center(),dot_right.get_center(), color = WHITE).set_opacity(0.5)
        end_fun = DashedLine(axes.c2p(2,-1), axes.c2p(2,0), color = WHITE).set_opacity(0.5)
        f_graph = VGroup(f1,f2)

        function = MathTex(
            r"""
            f(x) = \left\{
            \begin{array}{ll}
            1, & \text{si } 0 \leq x \leq 1 \\
            -1, & \text{si } 1 < x < 2
            \end{array}
            \right.
            """,
            tex_template=template
        )
        function.next_to(series, LEFT)
        self.play(Write(function))

        self.play(Succession(Create(f1),FadeIn(dot_left),Create(discontinuity), FadeIn(dot_right), Create(f2), Create(end_fun)), run_time = 2)
        self.wait(5)
        self.play(Transform(function, series))
        self.wait(2)


        # Define partial Fourier sums
        def fourier_approx(n_terms):
            def g(x):
                sum = 0
                for n in range(1, n_terms * 2, 2):  # only odd n
                    sum += (4 / (n * np.pi)) * np.sin(n * np.pi * x)
                return sum
            return axes.plot(g, x_range=[0,2],color=BLUE)
        
        
        # Animate growing Fourier approximations
        rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        label = MathTex("n=").to_corner(UL)
        self.play(Write(label))
        self.play(FadeOut(VGroup(dot_left,dot_right)))
        for k in range(1, 30):
            color = rainbow_colors[k % len(rainbow_colors)]
            approx = fourier_approx(k).set_color(color)
            
            number = MathTex(f"{2 * k - 1}").next_to(label, RIGHT)
            
            # Fix fill issue: use stroke and no fill
            memory_graph = f_graph.copy()
            memory_graph.set_fill(opacity=0)
            memory_graph.set_stroke(opacity=0.1, width=2)

            self.add(memory_graph)

            self.play(Transform(f_graph, approx), Write(number))
            self.wait(0.1)
            
            self.remove(number)
        self.add(number)
        self.wait(2)
