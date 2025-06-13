class GraphicAttributes:
    def __init__(self, foreground:str, background:str, font:str, font_size:int,
                 alignment:str, padding_x:int, padding_y:int):
        self.foreground = foreground
        self.background = background
        self.font = (font, font_size)
        self.alignment = alignment
        self.padding_x = padding_x
        self.padding_y = padding_y
    