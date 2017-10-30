import xbmc
import sys
import xbmcaddon
import xbmcgui
import time
import os
import subprocess
from resources.lib.SystemHelper import SystemHelper
from resources.lib.SystemConfig import SystemConfig
from resources.lib.HyperionConfigBuilder import HyperionConfigBuilder
from resources.lib.Arrow import Arrow

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')


def getAddonRoot():
    return xbmc.translatePath(addon.getAddonInfo('path'))


def openAdvancedSettings():
    try:
        addon.openSettings()
    except KeyboardInterrupt:
        sys.exit(0)


def checkAndInstallPrerequisities():
    result = SystemHelper.testSystemRequirements()

    if result == SystemHelper.NoHyperion:
        if SystemHelper.isOSMC():
            xbmcgui.Dialog().ok(addonname, "Hyperion installation was not detected. Please install manually.")
            sys.exit()
        xbmcgui.Dialog().ok(addonname, "Hyperion installation was not detected. Installing...")
        rc = SystemHelper.installHyperion(getAddonRoot())
        if rc == -2:
            xbmcgui.Dialog().ok(addonname,
                                "Hyperion installation failed. Install script download failed. Please install manually.")
            sys.exit()
        elif rc != 0:
            xbmcgui.Dialog().ok(addonname, "Installation error. Please install manually.")
            sys.exit()

    if result == SystemHelper.NoSystemUtils:
        if SystemHelper.isOSMC():
            if xbmcgui.Dialog().yesno(addonname,
                                      "System utilities missing - lsusb and killall. " +
                                      "Select Yes to have them installed. No will exit the wizard."):
                pDialog = xbmcgui.DialogProgress()
                pDialog.create('Installing...', 'Please wait. it can take few minutes...')
                subprocess.call(["sudo", "apt-get", "install", "-y", "psmisc", "usbutils"])
                pDialog.close()
            else:
                sys.exit()
        else:
            xbmcgui.Dialog().ok(addonname, "System utilities missing. Please install  - lsusb and killall.")
            sys.exit()


def setDefaults():
    builder.setHorizontalDepth(0.08)
    builder.setVerticalDepth(0.1)
    builder.setDeviceRate(int(addon.getSetting("rate")))
    if addon.getSetting("colorOrder").lower() != "default":
        builder.setDeviceColorOrder(addon.getSetting("colorOrder").lower())

    if addon.getSetting("recommendedColorSettings") == "true":
        builder.setRecommendedColorSettings()
    else:
        builder.setColorRED(float(addon.getSetting("redThreshold")),
                            float(addon.getSetting("redGamma")),
                            float(addon.getSetting("redBlacklevel")),
                            float(addon.getSetting("redWhitelevel")))

        builder.setColorGREEN(float(addon.getSetting("greenThreshold")),
                              float(addon.getSetting("greenGamma")),
                              float(addon.getSetting("greenBlacklevel")),
                              float(addon.getSetting("greenWhitelevel")))

        builder.setColorBLUE(float(addon.getSetting("blueThreshold")),
                             float(addon.getSetting("blueGamma")),
                             float(addon.getSetting("blueBlacklevel")),
                             float(addon.getSetting("blueWhitelevel")))

    builder.setSmoothing(addon.getSetting("smoothingType"),
                         int(addon.getSetting("smoothingTime")),
                         int(addon.getSetting("smoothingFreq")))

    builder.setBlackborderDetection((addon.getSetting("bbdEnabled") == "true"), float(addon.getSetting("bbdThreshold")))

    if addon.getSetting("colorWhenSourceIsOff") == "BLUE":
        builder.setGrabberBlueSignalWhenSourceIsOff()

    builder.setGrabberPriority(int(float(addon.getSetting("grabberPriority"))))
    builder.setGrabberVideoStandard(addon.getSetting("videoStandard"))


def selectDevice():
    availableDevices = HyperionConfigBuilder.getTypes(SystemHelper.isGpioAvailable())
    selectedIndex = xbmcgui.Dialog().select("Select your led device:", availableDevices)
    return availableDevices[selectedIndex]


def getStartPoint():
    availableStartPoints = HyperionConfigBuilder.getStartPoints()
    selectedIndex = xbmcgui.Dialog().select("Select where the led chain starts:", availableStartPoints)
    return availableStartPoints[selectedIndex]


def getOffset(startPoint):
    offset = 0
    if startPoint == HyperionConfigBuilder.startCBr or \
            startPoint == HyperionConfigBuilder.startCBl:
        offset = xbmcgui.Dialog().input("How many leds from the center to the corner or the screen?", "15",
                                        xbmcgui.INPUT_NUMERIC)
    return offset


def setGrabber():
    grabberStatus = SystemHelper.isGrabberAvailable()
    if grabberStatus == SystemHelper.GrabberMISSING:
        xbmcgui.Dialog().ok(addonname, "We have not detected the HDMI Kit. It will not be added to the config file.")
    elif grabberStatus == SystemHelper.GrabberMISSINGDEVICE:
        xbmcgui.Dialog().ok(addonname,
                            "HDMI Kit has been detected but video0 does not exist. " +
                            "Please install drivers or use different distribution")
    else:
        if xbmcgui.Dialog().yesno(addonname, "Compatible HDMI Kit has been detected. Do you want to enable it in hyperion?"):
            if grabberStatus == SystemHelper.GrabberUTV:
                builder.setGrabberEnabled(builder.grabberUTV)
            elif grabberStatus == SystemHelper.GrabberSTK:
                builder.setGrabberEnabled(builder.grabberSTK)


def showSettings():
    line1 = "Welcome!"
    line2 = "We are about to prepare your hyperion config file in this step-by-step wizard."
    line3 = "You must complete all steps to have the config file generated. Let\'s start!"
    return xbmcgui.Dialog().yesno(addonname, line1, line2, line3, "Let's start!", "Advanced settings")


def showTestImage(startPoint):
    arrowHelper = Arrow(getAddonRoot())

    xbmcgui.Dialog().ok(addonname, "For the next 10 seconds you will see test image. " +
                        "The leds should adjust to that image. " +
                        "Check if the leds are showing the right colors in the right places." +
                        " If not, start this wizard again and " +
                        "correct the numbers of leds horizontally and vertically." +
                        "Arrow points to the start point.")

    testImagePath = os.path.join(getAddonRoot(), "resources/img/test_picture.png")
    window = xbmcgui.WindowDialog(xbmcgui.getCurrentWindowId())
    image = xbmcgui.ControlImage(0, 0, 1280, 720, testImagePath)
    arrow = arrowHelper.getControlImageStartPoint(startPoint)

    window.addControl(image)
    window.addControl(arrow)
    window.show()
    SystemHelper.processStart(config.getShowTestImageCommand(testImagePath))

    time.sleep(10)
    window.close()

    SystemHelper.processStart(config.getClearLedsCommand())


def setHorizontalAndVerticalLedNumber():
    xbmcgui.Dialog().ok(addonname, "In the next two steps please provide a number of leds at the top edge of" +
                        "  tv (horizontally) and a number of leds at the side of your tv " +
                        "(count the leds at single side only) - horizontally")

    nolHorizontal = xbmcgui.Dialog().input("Select the number of leds horizontally", "29", xbmcgui.INPUT_NUMERIC)
    builder.setHorizontal(nolHorizontal)

    nolVertical = xbmcgui.Dialog().input("Select the number of leds vertically", "16", xbmcgui.INPUT_NUMERIC)
    builder.setVertical(nolVertical)


def bye():
    xbmcgui.Dialog().ok(addonname, "Enjoy!", "If you'd like to fine tune advanced parameters, "
                                             "please modify addon advanced settings before running it",
                        "You may need to restart your system.")


try:
    config = SystemConfig(getAddonRoot())

    if showSettings():
        addon.openSettings()

    checkAndInstallPrerequisities()

    builder = HyperionConfigBuilder()
    setDefaults()

    selectedDevice = selectDevice()
    builder.setDevice(selectedDevice)

    setHorizontalAndVerticalLedNumber()

    startPoint = getStartPoint()
    offset = getOffset(startPoint)
    builder.setStartPoint(startPoint, offset)

    setGrabber()

    xbmcgui.Dialog().ok(addonname, "Now we will attempt to restart hyperion...")

    configFileContent = builder.buildJSON()
    SystemHelper.saveFile(config.hyperiondConfigTemp, configFileContent)
    SystemHelper.processKill(config.getProcessName())
    SystemHelper.processStart(config.getRunCommandTemp())

    if not xbmcgui.Dialog().yesno(addonname, "Have you seen the rainbow swirl? " +
                                             "(sometimes it does not appear, if you're sure that correct led type " +
                                             "is selected but the answer YES anyway, save config as default and reboot)"):
        xbmcgui.Dialog().ok(addonname, "Please try running hyperion from command line to see the error. " +
                                       "(" + config.getRunCommandTemp() + ")")
        sys.exit()

    showTestImage(startPoint)

    if xbmcgui.Dialog().yesno(addonname, "Do you want to save this config as your default one?",
                              "(if you select No, changes will be lost after hyperion/system restart)"):
        SystemHelper.saveFile(config.hyperiondConfig, configFileContent)
    elif xbmcgui.Dialog().yesno(addonname, "Hyperion is now running with the newly created config. ",
                                           "Would you like to restart hyperion with previous config?"):
        SystemHelper.processStart(config.getRunCommand())

    bye()

except Exception, e:
        xbmcgui.Dialog().ok(addonname, repr(e), "Please report an error at github issue list")


