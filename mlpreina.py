from manim import *
from manim.utils.space_ops import rotate_vector

class MLPReina(Scene):
    def construct(self):
        t = ValueTracker(0)

        title = Text("Por qué usar complejos", font_size=38).to_edge(UP).shift(DOWN * 0.2)
        self.play(Write(title))

        freq = list(range(-2, 4))
        circle_group = VGroup()
        arrows = VGroup()  

        for n in freq:
            radius = 0.45 if abs(n) != 3 else 0.3
            circle = Circle(radius=radius, color=BLUE, stroke_width=1.5)

            freq_label = MathTex(str(n), color=YELLOW, font_size=30)
            formula = MathTex(f"c_{{{n}}} e^{{{n}2\\pi it}}", font_size=26)

            bloque_temp = VGroup(freq_label, circle, formula).arrange(DOWN, buff=0.15)
            bloque = VGroup(bloque_temp)
            circle_group.add(bloque)

        circle_group.arrange(RIGHT, buff=0.7)
        circle_group.move_to(UP * 1.5)

        for i, n in enumerate(freq):
            bloque_temp = circle_group[i][0]
            circle = [m for m in bloque_temp if isinstance(m, Circle)][0]
            radius = circle.radius

            def get_arrow(c=circle, n=n, r=radius):
                return Arrow(
                    start=c.get_center(),
                    end=c.get_center() + rotate_vector(RIGHT * r, TAU * n * t.get_value()),
                    buff=0,
                    stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.2,
                )

            arrow = always_redraw(get_arrow)
            arrows.add(arrow)

        self.play(LaggedStart(*[Create(c) for c in circle_group], lag_ratio=0.1))
        self.play(FadeIn(arrows)) 

        self.add(*arrows) 

        general_formula = MathTex("c_n e^{n \\cdot 2\\pi i t}", font_size=32)
        general_formula.next_to(circle_group, LEFT * 2)
        self.play(Write(general_formula))

        plano = ComplexPlane(
            x_range=[-3.5, 3.5, 1],
            y_range=[-2.5, 2.5, 1],
            axis_config={
                "color": WHITE,
                "stroke_width": 1.5,
                "include_ticks": False,
                "include_numbers": False,
            },
            background_line_style={
                "stroke_color": WHITE,
                "stroke_opacity": 0.2,
                "stroke_width": 1,
            }
        ).scale(1.1).move_to(DOWN * 2)

        self.play(Create(plano))

        etiquetas_reales = VGroup()
        for x in [-3, -2, -1, 1, 2, 3]:
            label = MathTex(str(x), font_size=28).next_to(plano.c2p(x, 0), DOWN, buff=0.2)
            etiquetas_reales.add(label)

        etiquetas_imaginarias = VGroup()
        for y in [-2, -1, 1, 2]:
            texto = f"{'' if y > 0 else '-'}{abs(y)}i"
            label = MathTex(texto, font_size=28).next_to(plano.c2p(0, y), LEFT, buff=0.2)
            etiquetas_imaginarias.add(label)

        self.play(Write(etiquetas_reales), Write(etiquetas_imaginarias))

        self.play(t.animate.set_value(1), run_time=6, rate_func=linear)
        self.wait()

        self.play(
            *[FadeOut(mob) for mob in circle_group],
            *[FadeOut(arrow) for arrow in arrows],
            FadeOut(general_formula),
            run_time=2
        )

        t = ValueTracker(0)
        n_val = ValueTracker(1)

        main_circle = Circle(radius=1, color=BLUE, stroke_width=2)
        main_circle.move_to(plano.c2p(0, 0))
        self.play(Create(main_circle))

        ecuacion_general = MathTex("c_", "n", " e^{2\\pi i ", "n", " t}", font_size=36)
        ecuacion_general.next_to(title, DOWN, buff=0.5)
        self.play(Write(ecuacion_general))
        self.wait()

        subscript_n_label = ecuacion_general[1]
        exponent_n_label = ecuacion_general[3]

        # Función para actualizar n en la fórmula
        def update_n_label(new_n):
            nuevo_label = MathTex(str(int(new_n)), font_size=36)

            nuevo_sub = nuevo_label.copy().move_to(subscript_n_label)
            nuevo_exp = nuevo_label.copy().move_to(exponent_n_label)

            self.play(
                Transform(subscript_n_label, nuevo_sub),
                Transform(exponent_n_label, nuevo_exp),
                run_time=0.5
            )

        rotating_vector = always_redraw(lambda: Arrow(
            start=plano.c2p(0, 0),
            end=plano.c2p(
                np.cos(TAU * n_val.get_value() * t.get_value()),
                np.sin(TAU * n_val.get_value() * t.get_value())
            ),
            buff=0,
            stroke_width=3,
            color=YELLOW
        ))
        self.add(rotating_vector)

        self.play(n_val.animate.set_value(1), run_time=0.5)
        update_n_label(1)
        self.play(t.animate.set_value(1), run_time=3, rate_func=linear)
        self.wait(1)

        self.play(n_val.animate.set_value(2), run_time=0.5)
        update_n_label(2)
        self.play(t.animate.set_value(2), run_time=3, rate_func=linear)
        self.wait(1)
        self.remove(rotating_vector)

        cn_label = MathTex("c_n", font_size=36)
        exp_label = MathTex("e^{2\\pi i n t}", font_size=36)

        # Agrupar como fórmula completa
        formula_cn = VGroup(cn_label, exp_label).arrange(RIGHT, buff=0.2)
        formula_cn.move_to(title.get_center() + DOWN * 1.5)

        self.play(Write(formula_cn))

        cn_label = formula_cn[0]

        def update_cn_label(new_latex, shift=ORIGIN):
            nuevo_label = MathTex(new_latex, font_size=36)
            nuevo_label.move_to(formula_cn[0].get_center() + shift)
            self.play(ReplacementTransform(formula_cn[0], nuevo_label), run_time=1)
            formula_cn[0] = nuevo_label


        update_cn_label("2 e^{i \\pi / 3}", shift=LEFT * 0.4)
        cn_radius = 2
        cn_angle =  PI / 3

        new_circle = Circle(radius=cn_radius, color=BLUE, stroke_width=2).move_to(plano.c2p(0, 0))
        self.play(Transform(main_circle, new_circle))

        # Crea el vector la primera vez y guarda referencia
        vector_cn = Arrow(
            start=plano.c2p(0, 0),
            end=plano.c2p(
                cn_radius * np.cos(cn_angle),
                cn_radius * np.sin(cn_angle)
            ),
            buff=0,
            stroke_width=3,
            color=YELLOW
        )
        self.play(Create(vector_cn))

        # --- Cambiar c_n = 0.5 e^{iπ/2} ---
        update_cn_label("0.5 e^{i \\pi / 2}", shift=LEFT * 0)
        cn_radius = 0.5
        cn_angle = PI / 2

        new_circle = Circle(radius=cn_radius, color=BLUE, stroke_width=2).move_to(plano.c2p(0, 0))
        self.play(Transform(main_circle, new_circle))

        new_vector = Arrow(
            start=plano.c2p(0, 0),
            end=plano.c2p(
                cn_radius * np.cos(cn_angle),
                cn_radius * np.sin(cn_angle)
            ),
            buff=0,
            stroke_width=3,
            color=YELLOW
        )
        self.play(Transform(vector_cn, new_vector))
        self.wait()
        self.play(FadeOut(*self.mobjects))