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
    "FaderBox_5": Boundary(5, 235, 315, 275)
}

Elements_MenuWindow = {
    "Toolbar_Menu_Exit": Boundary(237, 3, 317, 47)
}