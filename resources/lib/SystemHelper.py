import os
import subprocess


class SystemHelper:
    NoHyperion = "HYPERION_NOT_INSTALLED"
    NoSystemUtils = "SYSTEM_UTILS_NOT_INSTALLED"
    OK = "OK"

    GrabberUTV = "GRABBER_UTV007"
    GrabberSTK = "GRABBER_STK1160"
    GrabberMISSING = "GRABBER_MISSING"
    GrabberMISSINGDEVICE = "GRABBER_MISSING_DEVICE"

    @staticmethod
    def isWetek():
        if "Amlogic" in open("/proc/cpuinfo").read():
            return True
        else:
            return False

    @staticmethod
    def isOSMC():
        if "osmc" in open("/proc/version").read():
            return True
        else:
            return False

    @staticmethod
    def testSystemRequirements():
        if not SystemHelper.isHyperionInstalled():
            return SystemHelper.NoHyperion
        try:
            subprocess.call(["lsusb"])
            subprocess.call(["killall", "-help"])
        except Exception, e:
            return SystemHelper.NoSystemUtils
        return SystemHelper.OK

    @staticmethod
    def isHyperionInstalled():
        if os.path.isdir("/storage/hyperion/bin") \
                or os.path.isdir("/opt/hyperion") \
                or os.path.isdir("/usr/share/hyperion"):
            return True
        else:
            return False

    @staticmethod
    def installHyperion(workRoot):
        if SystemHelper.isOSMC():
            return -1
        rc = subprocess.call(["curl", "-L", "--output", os.path.join(workRoot,
                             "install_hyperion.sh"), "--get",
                              "https://raw.githubusercontent.com/tvdzwan/hyperion/master/bin/install_hyperion.sh"])
        if rc != 0:
            return -2
        return subprocess.call(["sh", os.path.join(workRoot, "install_hyperion.sh")])

    @staticmethod
    def isGpioAvailable():
        return SystemHelper.isWetek() or "spidev" not in subprocess.check_output(['ls', '/dev'])

    @staticmethod
    def isGrabberAvailable():
        lsusb_output = subprocess.check_output('lsusb')
        result = SystemHelper.GrabberMISSING
        if "1b71:3002" in lsusb_output:
            result = SystemHelper.GrabberUTV
        elif "05e1:0408" in lsusb_output:
            result = SystemHelper.GrabberSTK

        if result != SystemHelper.GrabberMISSING and "video0" in subprocess.check_output(['ls', '/dev']):
            return result
        else:
            return SystemHelper.GrabberMISSINGDEVICE
    @staticmethod
    def __runProcess(cmd):
        if SystemHelper.isSudoRequired():
            su = ["sudo"]
            su.extend(cmd)
            subprocess.Popen(su)
        else:
            subprocess.Popen(cmd)

    @staticmethod
    def processStart(cmd):
        subprocess.Popen(cmd)

    @staticmethod
    def processKill(processName):
        subprocess.Popen(["killall", processName])

    @staticmethod
    def isSudoRequired():
        return False

    @staticmethod
    def saveFile(hyperiondConfigTemp, configFileContent):
        with open(hyperiondConfigTemp, "w+", 0777) as f:
            f.write(configFileContent)

