#!/usr/bin/env python


class Tank:
    def __init__(self, fid, width):  # pin_num - set in config file on pi
        self.fid = fid
        self.width = width
        self.side = None

    def decide(self, x, y, _ver='edge'):
        tmp_return = None
        if _ver is 'edge':
            if x < self.width/4 and not self.side == 'left':
                self.side = 'left'
                tmp_return = 'left'

            elif x > self.width*3/4 and not self.side == 'right':
                self.side = 'right'
                tmp_return = 'right'

        elif _ver is 'center':
            if (x > self.width * 3/8 and x < self.width * 5/8) and (y > self.width * 3/8 and y < self.width * 5/8):
                if self.side is 'out_center':
                    self.side = 'center'
                    tmp_return = 'center'
            else:
                self.side = 'out_center'
                tmp_return = 'out_center'

        return tmp_return
