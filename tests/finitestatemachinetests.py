import unittest
from finitestatemachine import FSM

MOCK_STATE_1, MOCK_STATE_2, MOCK_STATE_3, MOCK_STATE_4, MOCK_STATE_5 = (1,2,3,4,5)

class MockActions():
    def __init__(self):
        self.recent_input = None

    def action1(self, fsm):
        self.recent_input = fsm.input

class FSMTests(unittest.TestCase):
    def setUp(self):
       self.fsm = FSM(MOCK_STATE_1)
       self.mock_actions = MockActions()

    def test_default_transition(self):
        self.fsm.setDefaultTransition(self.mock_actions.action1, MOCK_STATE_5)
        self.fsm.process("mockinput")
        self.assertEqual(self.mock_actions.recent_input, "mockinput")
        self.assertEqual(self.fsm.current_state, MOCK_STATE_5)        

    def test_process(self):
        self.fsm.addTransition("mockinput", MOCK_STATE_1, self.mock_actions.action1, MOCK_STATE_2)
        self.fsm.process("mockinput")
        self.assertEqual(self.mock_actions.recent_input, "mockinput")
        self.assertEqual(self.fsm.current_state, MOCK_STATE_2)

    def test_process_exception(self):
        self.assertRaises(Exception, self.fsm.process, ("mockinput"))

    def test_reset(self):
        self.fsm.addTransition("mockinput", MOCK_STATE_1, self.mock_actions.action1, MOCK_STATE_3)
        self.fsm.process("mockinput")
        self.fsm.reset()
        self.assertEqual(self.fsm.current_state, MOCK_STATE_1)
        self.assertEqual(self.fsm.input, None)

