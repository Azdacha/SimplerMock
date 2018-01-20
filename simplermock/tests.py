
import unittest

from simplermock import SimplerMock


class ASimplerMock(SimplerMock):

    def aMethod(self):
        pass


class BSimplerMock(SimplerMock):

    def bMethod(self):
        pass


class SlackBotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(SlackBotTests, cls).setUpClass()

        cls.mc = ASimplerMock()
        cls.mc_b = BSimplerMock()
        cls.mc_c = ASimplerMock()

        cls.mc.aMethod()
        cls.mc.unknownMethod()

        cls.mc_b.bMethod()
        cls.mc_c.anotherMethod()

    def test_existing(self):
        '''Should test existing methods.'''
        assert self.mc.was_called('ASimplerMock.aMethod')

    def test_unkown(self):
        '''Should test unknown methods.'''
        assert self.mc.was_called('ASimplerMock.unknownMethod')

    def test_other_class(self):
        '''Should test unicity from other class.'''
        assert self.mc.was_called('BSimplerMock.bMethod')
        assert not self.mc.was_called('ASimplerMock.bMethod')

    def test_other_object(self):
        '''Should test same class share entity.'''
        assert self.mc.was_called('ASimplerMock.anotherMethod')

    # note : tests seem to run in alphabetical order
    # hence _Zreset so we don't reset other tests
    def test_zreset(self):
        '''Should test reset.'''
        self.mc.reset()
        assert len(self.mc.attrs) == 0


if __name__ == '__main__':
    unittest.main()
