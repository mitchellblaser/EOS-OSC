class Boundary():
    def __init__(self, startX, startY, endX, endY):
        self.sx = startX
        self.sy = startY
        self.ex = endX
        self.ey = endY
        self.width = endX-startX
        self.height = endY-startY

Elements_MainWindow = {
    "Toolbar_Menu": Boundary(237, 3, 317, 47),
    "FaderBox_1": Boundary(5, 55, 315, 95),
    "FaderBox_2": Boundary(5, 100, 315, 140),
    "FaderBox_3": Boundary(5, 145, 315, 185),
    "FaderBox_4": Boundary(5, 190, 315, 230),
    "FaderBox_5": Boundary(5, 235, 315, 275),
    "Encoder_1": Boundary(2, 302, 158, 388),
    "Encoder_2": Boundary(2, 392, 158, 478),
    "Encoder_3": Boundary(162, 302, 318, 388),
    "Encoder_4": Boundary(162, 392, 318, 478)
}

Elements_MenuWindow = {
    "Toolbar_Menu_Exit": Boundary(237, 3, 317, 47),
    "MyIP_1_Up": Boundary(30, 85, 80, 135),
    "MyIP_1_Center": Boundary(30, 136, 80, 184),
    "MyIP_1_Down": Boundary(30, 185, 80, 235),
    "MyIP_2_Up": Boundary(100, 85, 150, 135),
    "MyIP_2_Center": Boundary(100, 136, 150, 184),
    "MyIP_2_Down": Boundary(100, 185, 150, 235),
    "MyIP_3_Up": Boundary(170, 85, 220, 135),
    "MyIP_3_Center": Boundary(170, 136, 220, 184),
    "MyIP_3_Down": Boundary(170, 185, 220, 235),
    "MyIP_4_Up": Boundary(240, 85, 290, 135),
    "MyIP_4_Center": Boundary(240, 136, 290, 184),
    "MyIP_4_Down": Boundary(240, 185, 290, 235),
    "ConsoleIP_1_Up": Boundary(30, 265, 80, 315),
    "ConsoleIP_1_Center": Boundary(30, 316, 80, 364),
    "ConsoleIP_1_Down": Boundary(30, 365, 80, 415),
    "ConsoleIP_2_Up": Boundary(100, 265, 150, 315),
    "ConsoleIP_2_Center": Boundary(100, 316, 150, 364),
    "ConsoleIP_2_Down": Boundary(100, 365, 150, 415),
    "ConsoleIP_3_Up": Boundary(170, 265, 220, 315),
    "ConsoleIP_3_Center": Boundary(170, 316, 220, 364),
    "ConsoleIP_3_Down": Boundary(170, 365, 220, 415),
    "ConsoleIP_4_Up": Boundary(240, 265, 290, 315),
    "ConsoleIP_4_Center": Boundary(240, 316, 290, 364),
    "ConsoleIP_4_Down": Boundary(240, 365, 290, 415)
}