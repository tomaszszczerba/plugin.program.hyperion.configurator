import json


class LedChain:
    def __init__(self, no_of_leds):
        self.number_of_leds = no_of_leds
        self.leds = []
        self.offset = 0

    def generate(self, nol_horizontal, nol_vertical, horizontal_depth, vertical_depth):
        self.nol_horizontal = nol_horizontal
        self.nol_vertical = nol_vertical
        area_top_coordinate = 0.0
        area_bottom_coordinate = 0.0
        area_left_coordinate = 0.0
        area_right_coordinate = 0.0

        self.vertical_segment = 1.0 / nol_vertical
        self.horizontal_segment = 1.0 / nol_horizontal
        for i in range(0, self.number_of_leds):
            if i < nol_vertical:  # right
                vertical_position = i + 1
                area_top_coordinate = (1 - (self.vertical_segment * vertical_position))
                area_left_coordinate = 1 - horizontal_depth;
                area_right_coordinate = 1
                area_bottom_coordinate = area_top_coordinate + self.vertical_segment
            elif i >= nol_vertical and i < nol_vertical + nol_horizontal:  # top
                horizontal_position = nol_horizontal - (i - nol_vertical) - 1
                area_left_coordinate = horizontal_position * self.horizontal_segment
                area_top_coordinate = 0.0
                area_bottom_coordinate = vertical_depth
                area_right_coordinate = area_left_coordinate + self.horizontal_segment
            elif i >= nol_vertical + nol_horizontal and i < nol_vertical + nol_horizontal + nol_vertical:  # left
                vertical_position = i - nol_vertical - nol_horizontal
                area_top_coordinate = (0 + (self.vertical_segment * vertical_position))
                area_left_coordinate = 0.0
                area_right_coordinate = horizontal_depth
                area_bottom_coordinate = area_top_coordinate + self.vertical_segment
            else:  # bottom
                horizontal_position = i - nol_vertical - nol_horizontal - nol_vertical
                area_top_coordinate = (1 - vertical_depth)
                area_left_coordinate = horizontal_position * self.horizontal_segment
                area_right_coordinate = area_left_coordinate + self.horizontal_segment
                area_bottom_coordinate = 1

            led = Led()
            led.setCoordinates(area_left_coordinate, area_right_coordinate, area_top_coordinate, area_bottom_coordinate)
            led.position = i
            self.leds.append(led)
        self.original_chain = list(self.leds)  # make a copy of initial setup

    def setOverlap(self, overlap_pct):
        self.horizontal_overlap = (overlap_pct / 100.0) * self.horizontal_segment
        self.vertical_overlap = (overlap_pct / 100.0) * self.vertical_segment
        for led in self.leds:
            led.x_start = max(led.x_start - self.horizontal_overlap, 0)
            led.x_end = min(led.x_end + self.horizontal_overlap, 1)
            led.y_start = max(led.y_start - self.vertical_overlap, 0)
            led.y_end = min(led.y_end + self.vertical_overlap, 1)

    def reverseDirection(self):
        self.leds.reverse()

    def setOffset(self, offset_value):
        if offset_value > 0:
            for i in range(offset_value):
                self.leds.append(self.leds.pop(0))
        elif offset_value < 0:
            for i in range((-1) * offset_value):
                self.leds.insert(0, self.leds.pop(self.number_of_leds - 1))

    def addExtraLeds(self, no_of_extra_leds):
        for i in range(0, no_of_extra_leds):
            led = Led()
            led.position = self.number_of_leds + i
            self.leds.append(led)


class Led:
    def __init__(self):
        self.x_start = 0
        self.x_end = 0
        self.y_start = 0
        self.y_end = 0
        self.position = 0
        self.color = bytearray([0, 0, 0])

    def setCoordinates(self, in_x_start, in_x_end, in_y_start, in_y_end):
        self.x_start = in_x_start
        self.x_end = in_x_end
        self.y_start = in_y_start
        self.y_end = in_y_end

    def hscanToDict(self):
        return dict(minimum=round(self.x_start, 4), maximum=round(self.x_end, 4))

    def vscanToDict(self):
        return dict(minimum=round(self.y_start, 4), maximum=round(self.y_end, 4))

    def setColor(self, red, green, blue):
        if red > 255 or red < 0 or green > 255 or green < 0 or blue > 255 or blue < 0:
            raise "Incorrect values (must be between <0,255>"
        else:
            self.color = bytearray([red, green, blue])
