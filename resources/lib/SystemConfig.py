import os
from SystemHelper import SystemHelper


class SystemConfig:
    def __init__(self, workRoot):
        # openelec based systems
        self.hyperiondCommand = "/storage/hyperion/bin/hyperiond"
        self.hyperiondConfig = "/storage/.config/hyperion.config.json"
        self.hyperiondConfigTemp = os.path.join(workRoot, "hyperion.config.json.temp")
        self.hyperionRemotePath = "/storage/hyperion/bin/hyperion-remote.sh"

        if SystemHelper.isOSMC():
            self.hyperiondCommand = "hyperiond"
            self.hyperionRemotePath = "hyperion-remote"

    def getRunCommandTemp(self):
        return [self.hyperiondCommand, self.hyperiondConfigTemp]

    def getRunCommand(self):
        return [self.hyperiondCommand, self.hyperiondConfig]

    def getProcessName(self):
        return "hyperiond"

    def getShowTestImageCommand(self, testImagePath):
        return [self.hyperionRemotePath, "-i", testImagePath]

    def getClearLedsCommand(self):
        return [self.hyperionRemotePath, "--clearall"]

