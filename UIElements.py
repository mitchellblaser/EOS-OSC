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
    "Toolbar_Menu_Exit": Boundary(237, 3, 317, 47)
}