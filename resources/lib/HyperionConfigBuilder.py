import json
from collections import OrderedDict


class HyperionConfigSettings:
    def __init__(self):
        pass

    deviceType = ""
    deviceRate = ""
    deviceColorOrderSet = False
    deviceColorOrder = ""

    horizontal = 0
    horizontalDepth = ""

    vertical = 0
    verticalDepth = ""

    startPoint = ""
    offset = 0

    grabberEnabled = False
    grabberType = ""
    grabberPriority = ""
    grabberVideoStandard = ""
    grabberBlueSignalWhenSourceIsOff = False

    REDThreshold = ""
    REDGamma = ""
    REDBlack = ""
    REDWhite = ""

    GREENThreshold = ""
    GREENGamma = ""
    GREENBlack = ""
    GREENWhite = ""

    BLUEThreshold = ""
    BLUEGamma = ""
    BLUEBlack = ""
    BLUEWhite = ""

    smoothingType = ""
    smoothingTime = ""
    smoothingFreq = ""

    blackBorderDetectorEnabled = ""
    blackBorderDetectorThreshold = ""

    amlGrabberRequired = False


class HyperionConfigBuilder:
    ws2801 = "Lightberry HD GPIO (ws2801)"
    apa102 = "Lightberry HD GPIO (apa102)"
    adalight = "Lightberry HD USB (ws2801)"
    adalightapa102 = "Lightberry HD USB (apa102)"
    lightberryXL = "Lightberry XL"

    startRB = "Right/bottom corner and goes up"
    startLB = "Left/bottom corner and goes up"
    startCBr = "Center/bottom and goes right"
    startCBl = "Center/bottom and goes left"

    grabberUTV = "utv007"
    grabberSTK = "stk1160"

    grabberPAL = "PAL"
    grabberNTSC = "NTSC"

    def __init__(self):
        self.settings = HyperionConfigSettings()

    def buildJSON(self):
        configDict = OrderedDict()

        self.__buildDevice(configDict)
        self.__buildV4LGrabber(configDict)
        self.__buildGrabber(configDict)
        self.__buildBlackBorderDetection(configDict)
        self.__buildColor(configDict)
        self.__buildBootsequence(configDict)
        self.__buildVideoChecker(configDict)
        self.__buildServers(configDict)
        self.__buildEffects(configDict)
        self.__buildLeds(configDict)

        configDict["endOfJson"] = "endOfJson";

        return json.dumps(configDict, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)

    @staticmethod
    def getTypes(isGPIOAvailable):
        if isGPIOAvailable:
            return [HyperionConfigBuilder.adalightapa102, HyperionConfigBuilder.adalight,
                    HyperionConfigBuilder.lightberryXL]
        else:
            return [HyperionConfigBuilder.adalightapa102, HyperionConfigBuilder.adalight,
                    HyperionConfigBuilder.ws2801, HyperionConfigBuilder.apa102,
                    HyperionConfigBuilder.lightberryXL]

    @staticmethod
    def getStartPoints():
        return [HyperionConfigBuilder.startRB,
                HyperionConfigBuilder.startLB,
                HyperionConfigBuilder.startCBr,
                HyperionConfigBuilder.startCBl]

    def setStartPoint(self, startPoint, offset):
        self.settings.startPoint = startPoint
        self.settings.offset = int(offset)

    def setDevice(self, param):
        self.settings.deviceType = param

    def setAmlGrabber(self):
        self.settings.amlGrabberRequired = True

    def setHorizontal(self, param):
        self.settings.horizontal = int(param)

    def setHorizontalDepth(self, param):
        self.settings.horizontalDepth = param

    def setVertical(self, param):
        self.settings.vertical = int(param)

    def setVerticalDepth(self, param):
        self.settings.verticalDepth = param

    def setGrabberEnabled(self, param):
        self.settings.grabberEnabled = True
        self.settings.grabberType = param

    def setDeviceRate(self, param):
        self.settings.deviceRate = param

    def setDeviceColorOrder(self, param):
        self.settings.deviceColorOrderSet = True
        self.settings.deviceColorOrder = param

    def setColorRED(self, threshold, gamma, black, white):
        self.settings.REDThreshold = threshold
        self.settings.REDGamma = gamma
        self.settings.REDBlack = black
        self.settings.REDWhite = white

    def setColorGREEN(self, threshold, gamma, black, white):
        self.settings.GREENThreshold = threshold
        self.settings.GREENGamma = gamma
        self.settings.GREENBlack = black
        self.settings.GREENWhite = white

    def setColorBLUE(self, threshold, gamma, black, white):
        self.settings.BLUEThreshold = threshold
        self.settings.BLUEGamma = gamma
        self.settings.BLUEBlack = black
        self.settings.BLUEWhite = white

    def setSmoothing(self, sType, time, freq):
        self.settings.smoothingType = sType
        self.settings.smoothingTime = time
        self.settings.smoothingFreq = freq

    def setBlackborderDetection(self, bbdEnabled, bbdTreshold):
        self.settings.blackBorderDetectorEnabled = bbdEnabled
        self.settings.blackBorderDetectorThreshold = bbdTreshold

    def setGrabberBlueSignalWhenSourceIsOff(self):
        self.settings.grabberBlueSignalWhenSourceIsOff = True

    def setGrabberPriority(self, param):
        self.settings.grabberPriority = param

    def setGrabberVideoStandard(self, param):
        self.settings.grabberVideoStandard = param

    def __buildDevice(self, configDict):
        configDict["device"] = {
            "name": "lightberry",
            "rate": self.settings.deviceRate,
            "colorOrder": "rgb"
        }
        if self.settings.deviceType == self.ws2801:
            configDict["device"]["type"] = "ws2801"
            configDict["device"]["output"] = "/dev/spidev0.0"
        if self.settings.deviceType == self.adalight:
            configDict["device"]["type"] = "adalight"
            configDict["device"]["output"] = "/dev/ttyACM0"
        elif self.settings.deviceType == self.lightberryXL:
            configDict["device"]["type"] = "adalight"
            configDict["device"]["output"] = "/dev/ttyACM0"
            configDict["device"]["colorOrder"] = "brg"
        elif self.settings.deviceType == self.apa102:
            configDict["device"]["type"] = "apa102"
            configDict["device"]["output"] = "/dev/spidev0.0"
            configDict["device"]["colorOrder"] = "bgr"
        elif self.settings.deviceType == self.adalightapa102:
            configDict["device"]["type"] = "adalightapa102"
            configDict["device"]["output"] = "/dev/ttyACM0"
            configDict["device"]["colorOrder"] = "bgr"

        if self.settings.deviceColorOrderSet:
            configDict["device"]["colorOrder"] = self.settings.deviceColorOrder

    def __buildLeds(self, configDict):
        leds = []

        verticalSpan = 1.0 / self.settings.vertical
        horizontalSpan = 1.0 / self.settings.horizontal

        for i in range(0, self.__getNumberOfLedsTotal()):
            if i < self.settings.vertical:  # right
                verticalPosition = i + 1
                leds.append({
                    "vscan": {
                        "minimum": (1 - verticalSpan * verticalPosition),  #area_top_coordinate
                        "maximum": (1 - verticalSpan * (verticalPosition + 1))  #area_bottom_coordinate
                    },
                    "hscan": {
                        "minimum": 1.0,  #area_right_coordinate
                        "maximum": 1 - self.settings.horizontalDepth  #area_left_coordinate
                    }
                })

            elif self.settings.vertical <= i < self.settings.vertical + self.settings.horizontal:  # top
                horizontalPosition = self.settings.horizontal - (i - self.settings.vertical) - 1
                leds.append({
                    "vscan": {
                        "minimum": 0.0,  #area_top_coordinate
                        "maximum": self.settings.verticalDepth  #area_bottom_coordinate
                    },
                    "hscan": {
                        "minimum": horizontalSpan * (horizontalPosition + 1), #area_right_coordinate
                        "maximum": horizontalSpan * horizontalPosition #area_left_coordinate
                    }
                })

            elif self.settings.vertical + self.settings.horizontal <= i < self.settings.vertical + self.settings.horizontal + self.settings.vertical:  # left
                verticalPosition = i - self.settings.vertical - self.settings.horizontal
                leds.append({
                    "vscan": {
                        "minimum": verticalSpan * verticalPosition,  #area_top_coordinate
                        "maximum": verticalSpan * (verticalPosition + 1)  #area_bottom_coordinate
                    },
                    "hscan": {
                        "minimum": self.settings.horizontalDepth,  #area_right_coordinate
                        "maximum": 0.0  #area_left_coordinate
                    }
                })

            else:  # bottom
                horizontalPosition = i - self.settings.vertical - self.settings.horizontal - self.settings.vertical
                leds.append({
                    "vscan": {
                        "minimum": 1 - self.settings.verticalDepth,  #area_top_coordinate
                        "maximum": 1.0  #area_bottom_coordinate
                    },
                    "hscan": {
                        "minimum": horizontalSpan * (horizontalPosition + 1),  #area_right_coordinate
                        "maximum": horizontalSpan * horizontalPosition  #area_left_coordinate
                    }
                })

        if self.settings.startPoint == self.startLB:
            leds.reverse()
            self.__setLedsOffset(leds, self.settings.horizontal)
        elif self.settings.startPoint == self.startCBl or self.settings.startPoint == self.startCBr:
            if self.startCBr == 2:
                self.__setLedsOffset(leds, -1 * self.settings.offset)
            else:
                leds.reverse()
                self.__setLedsOffset(leds, self.settings.offset)

        for i in range(self.__getNumberOfLedsTotal(), self.__getNumberOfLedsTotal() + self.__getNumberOfLedsOff()):
            leds.append({
                "vscan": {
                    "minimum": 1.0,
                    "maximum": 1.0
                },
                "hscan": {
                    "minimum": 1.0,
                    "maximum": 1.0
                }
            })

        for i in range(0, leds.__len__()):
            leds[i]["index"] = i

        configDict["leds"] = leds

    def __setLedsOffset(self, leds, offset_value):
        if offset_value > 0:
            for i in range(offset_value):
                leds.append(leds.pop(0))
        elif offset_value < 0:
            for i in range((-1) * offset_value):
                leds.insert(0, leds.pop(self.__getNumberOfLedsTotal() - 1))

    def __buildV4LGrabber(self, configDict):
        if not self.settings.grabberEnabled:
            return

        configDict["grabber-v4l2"] = {
            "cropLeft": 46,
            "cropTop": 20,
            "cropRight": 42,
            "cropBottom": 37,
            "width": 720,
            "height": 576,
            "sizeDecimation": 8,
            "frameDecimation": 2,
            "blueSignalThreshold": 0.2,
            "redSignalThreshold": 0.2,
            "greenSignalThreshold": 0.2,
            "priority": 880,
            "mode": "2D",
            "device": "/dev/video0",
            "input": 0,
            "standard": self.settings.grabberVideoStandard
        }

        if self.settings.grabberType == self.grabberSTK:
            configDict["grabber-v4l2"]["width"] = 180
            configDict["grabber-v4l2"]["height"] = \
                144 if self.settings.grabberVideoStandard == self.grabberPAL else 120
            configDict["grabber-v4l2"]["frame_decimation"] = 2
            configDict["grabber-v4l2"]["size_decimation"] = 2
        else:
            configDict["grabber-v4l2"]["width"] = 720
            configDict["grabber-v4l2"]["height"] = \
                576 if self.settings.grabberVideoStandard == self.grabberPAL else 480
            configDict["grabber-v4l2"]["frame_decimation"] = 2
            configDict["grabber-v4l2"]["size_decimation"] = 8

        if self.settings.grabberBlueSignalWhenSourceIsOff:
            configDict["grabber-v4l2"]["blueSignalThreshold"] = 1.0
            configDict["grabber-v4l2"]["redSignalThreshold"] = 0.1
            configDict["grabber-v4l2"]["greenSignalThreshold"] = 0.1

    def __buildGrabber(self, configDict):
        configDict["amlgrabber" if self.settings.amlGrabberRequired else "framegrabber"] = {
            "width": 64,
            "frequency_Hz": 10.0,
            "height": 64
        }

    def __buildBlackBorderDetection(self, configDict):
        configDict["blackborderdetector"] = {
            "threshold": self.settings.blackBorderDetectorThreshold,
            "enable": True
        }

    def __buildColor(self, configDict):
        configDict["color"] = {
            "transform": [self.__buildLedTransformations()]
            if self.__getNumberOfLedsOff() == 0 else
            [self.__buildLedTransformations(), self.__buildLedOFFTransformations()],
            "smoothing": {
                "updateFrequency": self.settings.smoothingFreq,
                "time_ms": self.settings.smoothingTime,
                "type": self.settings.smoothingType
            }
        }

    def __getNumberOfLedsTotal(self):
        return (self.settings.horizontal + self.settings.vertical) * 2

    def __getNumberOfLedsOff(self):
        """ 150 is assumed max number of LEDs in typical sets """
        return 150 - self.__getNumberOfLedsTotal() \
            if 150 - self.__getNumberOfLedsTotal() > 0 else 0

    def __buildLedTransformations(self):
        transform = {
            "id": "leds",
            "leds": "0-" + str(self.__getNumberOfLedsTotal() - 1),
            "red": {
                "threshold": self.settings.REDThreshold,
                "blacklevel": self.settings.REDBlack,
                "whitelevel": self.settings.REDWhite,
                "gamma": self.settings.REDGamma
            },
            "green": {
                "threshold": self.settings.GREENThreshold,
                "blacklevel": self.settings.GREENBlack,
                "whitelevel": self.settings.GREENWhite,
                "gamma": self.settings.GREENGamma
            },
            "blue": {
                "threshold": self.settings.BLUEThreshold,
                "blacklevel": self.settings.BLUEBlack,
                "whitelevel": self.settings.BLUEWhite,
                "gamma": self.settings.BLUEGamma
            },
            "hsv": {
                "saturationGain": 1.0,
                "valueGain": 1.0
            }
        }
        return transform

    def __buildLedOFFTransformations(self):
        transform = {
            "id": "ledsOff",
            "leds": str(self.__getNumberOfLedsTotal()) + "-" +
                    str(self.__getNumberOfLedsTotal() + self.__getNumberOfLedsOff() - 1),
            "red": {
                "threshold": 1,
                "blacklevel": 0,
                "whitelevel": 0,
                "gamma": 2.2
            },
            "green": {
                "threshold": 1,
                "blacklevel": 0,
                "whitelevel": 0,
                "gamma": 2.2
            },
            "blue": {
                "threshold": 1,
                "blacklevel": 0,
                "whitelevel": 0,
                "gamma": 2.2
            },
            "hsv": {
                "saturationGain": 0,
                "valueGain": 0
            }
        }
        return transform

    def __buildBootsequence(self, configDict):
        configDict["bootsequence"] = {
            "duration_ms": 3000,
            "effect": "Rainbow swirl fast"
        }

    def __buildServers(self, configDict):
        configDict["protoServer"] = {
            "port": 19445
        }

        configDict["jsonServer"] = {
            "port": 19444
        }

    def __buildEffects(self, configDict):
        configDict["effects"] = {
            "paths": [
                "/storage/hyperion/effects",
                "/usr/share/hyperion/effects"
            ]
        }

    def __buildVideoChecker(self, configDict):
        configDict["xbmcVideoChecker"] = {
            "grabVideo": True,
            "grabPictures": True,
            "xbmcTcpPort": 9090,
            "grabAudio": True,
            "grabMenu": False,
            "enable3DDetection": True,
            "xbmcAddress": "127.0.0.1",
            "grabScreensaver": True
        }
