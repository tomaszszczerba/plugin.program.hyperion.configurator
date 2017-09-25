from lib.HyperionConfigBuilder import HyperionConfigBuilder
import unittest
import json

class TestHyperionConfigBuilder(unittest.TestCase):

    def test_devicebuilder(self):
        out = HyperionConfigBuilder()

        out.setHorizontal(20)
        out.setHorizontalDepth(0.1)
        out.setVertical(20)
        out.setVerticalDepth(0.1)

        out.setDevice(out.adalightapa102)
        out.setDeviceRate(123456789)
        out.setDeviceColorOrder("brg")

        result = out.buildJSON()
        deserialized = json.loads(result)
        self.assertIn("device", deserialized)
        self.assertEqual(deserialized["device"]["rate"], 123456789)
        self.assertEqual(deserialized["device"]["colorOrder"], "brg")

    def test_grabberbuilder_on1(self):
        out = HyperionConfigBuilder()

        out.setHorizontal(20)
        out.setHorizontalDepth(0.1)
        out.setVertical(20)
        out.setVerticalDepth(0.1)

        out.setGrabberEnabled(out.grabberSTK)
        out.setGrabberPriority(9999)
        out.setGrabberVideoStandard(out.grabberNTSC)
        out.setGrabberBlueSignalWhenSourceIsOff()

        result = out.buildJSON()
        deserialized = json.loads(result)
        self.assertIn("grabber-v4l2", deserialized)
        self.assertEqual(deserialized["grabber-v4l2"]["standard"], out.grabberNTSC)
        self.assertEqual(deserialized["grabber-v4l2"]["height"], 120)
        self.assertEqual(deserialized["grabber-v4l2"]["blueSignalThreshold"], 1.0)

    def test_grabberbuilder_on2(self):
        out = HyperionConfigBuilder()

        out.setHorizontal(20)
        out.setHorizontalDepth(0.1)
        out.setVertical(20)
        out.setVerticalDepth(0.1)

        out.setGrabberEnabled(out.grabberUTV)

        result = out.buildJSON()
        deserialized = json.loads(result)
        self.assertIn("grabber-v4l2", deserialized)
        self.assertEqual(deserialized["grabber-v4l2"]["width"], 720)
        self.assertEqual(deserialized["grabber-v4l2"]["blueSignalThreshold"], 0.2)

    def test_grabberbuilder_off(self):
        out = HyperionConfigBuilder()

        out.setHorizontal(20)
        out.setHorizontalDepth(0.1)
        out.setVertical(20)
        out.setVerticalDepth(0.1)

        result = out.buildJSON()
        deserialized = json.loads(result)
        self.assertNotIn("grabber-v4l2", deserialized)


if __name__ == '__main__':
    unittest.main()
