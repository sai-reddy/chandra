import logging

logger = logging.getLogger(__name__)

class FSM():
    """
    This object implements a Finite State Machine (FSM)

    An FSM is defined by tables of transitions. For a given input 
    the process() method uses these tables to decide what action to call and what
    the next state will be.The FSM maintains two tables of transitions:           
    a)     (input, current_state) --> (action, next_state)
       Where "action" is a function defined. The input and states can be any objects. 
    
    b)    (current_state) --> (action, next_state)
       In case for all or none of the input is not given, it is called as "Any" table

    When an action function is called it is passed a reference to the FSM. The
    action function may then access attributes of the FSM such as input,
    current_state.The processing sequence is as follows. The process() method is given an
    input to process. The FSM will search the table of transitions that associate:

            (input, current_state) --> (action, next_state)

    If the pair (input, current_state) is found then process() will call the
    associated action function and then set the current state to the next_state.
    If the FSM cannot find a match for (input, current_state) it will then
    search the table of transitions that associate:

            (current_state) --> (action, next_state)

    If the current_state is found then the process() method will call the
    associated action function and then set the current state to the next_state.
    Note: It is always checked after first searching the table for a specific
    (input, current_state).

    For the case where the FSM did not match either of the previous two cases the
    FSM will try to use the default transition. If the default transition is
    defined then the process() method will call the associated action function and
    then set the current state to the next_state. This lets define a default
    transition as a catch-all case like an exception handler. 
    There can be only one default transition.
    
    Finally, if none of the previous cases are defined for an input and
    current_state then the FSM will raise an exception. 
    """
    def __init__(self, initial_state):
        # Maps (input, current_state) --> (action, next_state)
        self.state_transitions = {}
        # Maps (current_state) --> (action, next_state)
        self.state_transitions_any = {}
        self.default_transition = None

        self.input = None
        self.initial_state = initial_state
        self.current_state = self.initial_state
        self.next_state = None
        self.action = None        

    def reset(self):
        """
        This sets the current_state to the initial_state and sets
        input to None.
        """
        self.current_state = self.initial_state
        self.input = None

    def addTransition(self, input, state, action=None, next_state=None):
        """
        This adds a transition that associates:

                (input, current_state) --> (action, next_state)

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged.
        """
        if next_state is None:
            next_state = state
        self.state_transitions[(input, state)] = (action, next_state)

    def addTransitionList(self, input_list, state, action=None, next_state=None):
        """
        This adds the same transition for a list of input.
        You can pass any iterator.

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged.
        """
        if next_state is None:
            next_state = state
        for input in input_list:
            self.add_transition (input, state, action, next_state)

    def addTransitionAny(self, state, action=None, next_state=None):
        """
        This adds a transition that associates:

                (current_state) --> (action, next_state)

        That is, any input symbol will match the current state.
        The process() method checks the "any" state associations after it first
        checks for an exact match of (input, current_state).

        The action may be set to None in which case the process() method will
        ignore the action and only set the next_state. The next_state may be
        set to None in which case the current state will be unchanged. 
        """
        if next_state is None:
            next_state = state
        self.state_transitions_any [state] = (action, next_state)

    def setDefaultTransition(self, action, next_state):
        """
        This sets the default transition. This defines an action and
        next_state if the FSM cannot find the input symbol and the current
        state in the transition list and if the FSM cannot find the
        current_state in the transition_any list. This is useful as a final
        fall-through state for catching errors and undefined states.
        """
        self.default_transition = (action, next_state)

    def getTransition(self, input, state):
        """
        This returns (action, next state) given an input and state.
        This does not modify the FSM state, so calling this method has no side
        effects. Normally you do not call this method directly. It is called by
        process().

        The sequence of steps to check for a defined transition goes from the
        most specific to the least specific.

        1. Check state_transitions[] that match exactly the tuple,
            (input, state)
        2. Check state_transitions_any[] that match (state) 
        3. Check if the default_transition is defined.
           This catches any input and any state.
           This is a handler for errors, undefined states, or defaults.
        4. No transition was defined raises an exception.
        """
        if self.state_transitions.has_key((input, state)):
            return self.state_transitions[(input, state)]
        elif self.state_transitions_any.has_key (state):
            return self.state_transitions_any[state]
        elif self.default_transition is not None:
            return self.default_transition
        else:
            raise Exception('Transition is undefined: (%s, %s).' %(str(input), str(state)))

    def process(self, input):
        """
        This is the main method that process input. This may cause the FSM to change state and call an action
        """
        self.input = input
        (self.action, self.next_state) = self.getTransition(self.input, self.current_state)
        if self.action is not None:
            self.action(self)
        self.current_state = self.next_state
        self.next_state = None

    def processList(self, input_list):
        """
        This takes a list and sends each element to process(). The list may
        be a string or any iterable object. 
        """
        for input in input_list:
            self.process(s)

