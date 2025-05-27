from manim import *
import numpy as np 

def crear_plano_complejo():
    template = TexTemplate()
    template.add_to_preamble(r"\usepackage{amssymb}")
    plane = ComplexPlane(
            x_range = [-4,4,1], 
            y_range = [-4,4,1],
            background_line_style ={
                "stroke_opacity": 0.2,
            }
            ).add_coordinates()
    
    annulus = Annulus(
        inner_radius= 0.5,
        outer_radius= 1.5, 
        fill_opacity= 0.3,
        fill_color = RED,
        stroke_color = RED,
        stroke_width= 2
        )

    domain_name = MathTex("\mathbb{C}", tex_template = template).next_to(plane,UP + LEFT)
    annulus_name = Tex("D").move_to(plane.coords_to_point(-1.5,1.5))
    enclosing = Square(side_length= 8).move_to(plane.get_center() + [-0.1, 0.12,0])
    domain = VGroup(enclosing, plane, annulus, annulus_name, domain_name)
    domain.move_to(LEFT * 4) 
    return domain

class StyledCPlane(VGroup):
    def __init__(self):
        super().__init__()
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{amssymb}")
        
        self.plane = ComplexPlane(
            x_range=[-4,4,1],
            y_range=[-4,4,1],
            background_line_style={
                "stroke_opacity": 0.2,
            }
        ).add_coordinates()
        
        self.enclosing = Square(side_length=8).move_to(self.plane.get_center() + [-0.1, 0.12, 0])
        
        # Añadimos los elementos al VGroup (self)
        self.add(self.plane, self.enclosing)
    
    def get_plane(self):
        return self.plane

class EgFunction(MovingCameraScene):
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{amssymb}")

        self.camera.frame.set(width=22)
        plane = ComplexPlane(
            x_range = [-4,4,1], 
            y_range = [-4,4,1],
            background_line_style ={
                "stroke_opacity": 0.2,
            }
            ).add_coordinates()
    
        annulus = Annulus(
            inner_radius= 0.5,
            outer_radius= 1.5, 
            fill_opacity= 0.3,
            fill_color = RED,
            stroke_color = RED,
            stroke_width= 2
            )

        domain_name = MathTex("\mathbb{C}", tex_template = template).next_to(plane,UP + LEFT)
        annulus_name = Tex("D").move_to(plane.coords_to_point(-1.5,1.5))
        enclosing = Square(side_length= 8).move_to(plane.get_center() + [-0.1, 0.12,0])
        domain = VGroup(enclosing, plane, annulus, annulus_name, domain_name)
        domain.move_to(LEFT * 6)
        
        #circulo unitario
        unit_circle = DashedVMobject(Circle(radius=1, color= GREEN), num_dashes= 60)
        unit_circle.move_to(plane.coords_to_point(0,0))
        domain = VGroup(domain, unit_circle)
        print(plane.get_center())
        
        def create_plane():
            self.play(Create(VGroup(enclosing, plane, domain_name)), run_time= 3)
            self.play(Create(VGroup(annulus, annulus_name)), run_time = 3)
            self.wait(1)
            self.play(Create(unit_circle))
            self.play(domain.animate.move_to(LEFT*6))
            self.wait(2)
            return 
        
        #parametrizacion
        parameter = MathTex("z = e^{it}, \; t \; \epsilon \; [-\pi,\pi]")
        parameter.scale(1.5)
        parameter.move_to(RIGHT * 4)

        tex1 = Tex("f(z) analítica en D")
        tex2 = MathTex(r"f(z) = \sum_{n=-\infty}^{\infty} a_n z^n", tex_template = template)
        tex3 = Tex("Representación en Serie de ", "Laurent:", tex_to_color_map={"Laurent:": YELLOW})
        textos = VGroup(tex1,tex3,tex2).arrange(DOWN)
        textos.move_to(RIGHT * 4)

        def explanation():
            self.play(Create(tex1))
            self.wait(1)
            self.play(Create(tex3))
            self.wait(1)
            self.play(Create(tex2), run_time = 3)
            self.wait(1)
            self.play(textos.animate.shift(UP*3))
            self.play(Write(parameter))

        # Slider
        slider_line = Line(start=[0,0,0], end=[5,0,0], color=GREEN)
        slide_dot = Dot(slider_line.point_from_proportion(0), color=BLUE, radius=0.1)

        # Coordenadas de inicio y fin del slider
        slider_start = slider_line.get_start()
        slider_end = slider_line.get_end()

        # Marca izquierda (-pi)
        tick_left = Line(
            start=slider_start + UP * 0.1,
            end=slider_start + DOWN * 0.1,
            color=GREEN
        )

        # Marca derecha (pi)
        tick_right = Line(
            start=slider_end + UP * 0.1,
            end=slider_end + DOWN * 0.1,
            color=GREEN
        )
        slider = VGroup(slider_line, slide_dot, tick_left, tick_right).next_to(parameter, DOWN*2)
        label_left = MathTex(r"-\pi").scale(0.7).next_to(tick_left, DOWN, buff=0.1)
        label_right = MathTex(r"\pi").scale(0.7).next_to(tick_right, DOWN, buff=0.1)
        

        # Tracker para ángulo t
        t_tracker = ValueTracker(-PI)

        # Arrow dinámico
        vector = always_redraw(lambda: Arrow(
            start=plane.number_to_point(0),
            end=plane.number_to_point(np.exp(1j * t_tracker.get_value())),
            color=BLUE,
            buff=0
        ))
        
        # Punto que se mueve con el slider
        moving_dot = always_redraw(lambda: slide_dot.move_to(
            slider_line.point_from_proportion((t_tracker.get_value() + PI )/ (2*PI))
        ))

        moving_t_text = always_redraw(
                lambda: DecimalNumber(
                    t_tracker.get_value(),
                    num_decimal_places=4,
                    include_sign=True
                ).scale(0.5).next_to(moving_dot, UP, buff=0.1)
        )

        
        def slider_animation():
            self.play(Create(slider), Create(vector))
            self.play(Create(VGroup(label_left,label_right)))
            self.wait(2)

            self.play(Indicate(VGroup(slider, vector), run_time = 1.5))
            #Cambio del track value
            self.play(t_tracker.animate.set_value(PI), run_time=4, rate_func=linear)

        

        def demonstration_animation():
            self.play(FadeOut(VGroup(tex1,tex2,tex3)))
            self.play(VGroup(parameter,slider).animate.shift(UP * 4))
            tex5 = Tex("Dado que $f(e^{it}) := F(t)$")
            tex4 = MathTex("F(t) = \sum_{n = -\infty}^{\infty} a_n e^{int}", tex_template = template)
            tex6 = Tex("Esta es la representación de Fourier de nuestra f(z),\\\\ ya que tiene perido $2\\pi$.")
            textos = VGroup(tex2,tex5,tex4,tex6).arrange(DOWN)
            textos.next_to(slider, DOWN)
            self.play(Write(tex2))
            self.play(Write(tex5))
            self.play(Write(tex4))
            self.play(Write(tex6))
        #-------------------- EJECUCIÓN ---------------------
        #self.add(domain) #en cambio de create_plane()
        create_plane()
        explanation()
        slider_animation()
        slider = VGroup(slider, label_left, label_right)
        self.wait(1)
        #self.play(FadeOut(VGroup(tex1,tex2,tex3)))
        demonstration_animation()


class MobiusEg(MovingCameraScene):
    def construct(self):
        self.camera.frame.set(width=18)
        domain = crear_plano_complejo()

        for elem in domain:
            self.play(Create(elem))

        pos_domain = domain.get_center()
        new_pos = np.array([pos_domain[0], pos_domain[1] / 2, pos_domain[2]])

        mobius_styled = StyledCPlane()
        mobius_styled.scale(0.5)
        mobius_styled.move_to(domain.get_top() + RIGHT * 8 + DOWN * 2.5)
        self.play(Create(mobius_styled))
        self.wait(2)
    