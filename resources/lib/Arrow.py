from HyperionConfigBuilder import HyperionConfigBuilder
import xbmcgui
import os


class Arrow:

    def __init__(self, workingDir):
        self.workingDir = workingDir
        self.left = os.path.join(workingDir, "/resources/img/arrowLEFT.png")
        self.right = os.path.join(workingDir, "/resources/img/arrowRIGHT.png")
        self.down = os.path.join(workingDir, "/resources/img/arrowDOWN.png")
        self.up = os.path.join(workingDir, "/resources/img/arrowUP.png")
        self.sizex = 144
        self.sizey = 144
        self.screenx = 1280
        self.screeny = 720
        pass

    def getControlImageStartPoint(self, startPoint):
        if startPoint == HyperionConfigBuilder.startCBl or startPoint == HyperionConfigBuilder.startCBr:
            return xbmcgui.ControlImage(self.screenx/2 - self.sizex/2,
                                        self.screeny - self.sizey,
                                        self.sizex,
                                        self.sizey,
                                        self.workingDir + self.down)
        elif startPoint == HyperionConfigBuilder.startLB:
            return xbmcgui.ControlImage(0,
                                        self.screeny - self.sizey,
                                        self.sizey,
                                        self.sizex,
                                        self.workingDir + self.left)
        elif startPoint == HyperionConfigBuilder.startRB:
            return xbmcgui.ControlImage(self.screenx - self.sizex,
                                        self.screeny - self.sizey,
                                        self.sizey,
                                        self.sizex,
                                        self.workingDir + self.right)
