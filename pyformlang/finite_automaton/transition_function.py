class TransitionFunction(object):
    """ A transition function in a finite automaton.

    This is a deterministic transition function.

    Parameters
    ----------

    Attributes
    ----------
    _transitions : dict
        A dictionary which contains the transitions of a finite automaton


    """

    def __init__(self):
        self._transitions = dict()

    def add_transition(self, s_from, by, s_to):
        """ Adds a new transition to the function

        Parameters
        ----------
        s_from : State
            The source state
        by : Symbol
            The transition symbol
        s_to : State
            The destination state


        Returns
        --------
        done : int
            Always 1

        Raises
        --------
        DuplicateTransitionError
            If the transition already exists
        """
        if s_from in self._transitions:
            if by in self._transitions[s_from]:
                if self._transitions[s_from][by] != s_to:
                    raise DuplicateTransitionError(s_from,
                                                   by,
                                                   s_to,
                                                   self._transitions[s_from][by])
            else:
                self._transitions[s_from][by] = s_to
        else:
            self._transitions[s_from] = dict()
            self._transitions[s_from][by] = s_to
        return 1

    def remove_transition(self, s_from, by, s_to):
        """ Removes a transition to the function

        Parameters
        ----------
        s_from : State
            The source state
        by : Symbol
            The transition symbol
        s_to : State
            The destination state


        Returns
        --------
        done : int
            1 is the transition was found, 0 otherwise

        """
        if s_from in self._transitions and \
                by in self._transitions[s_from] and \
                s_to == self._transitions[s_from][by]:
            del self._transitions[s_from][by]
            return 1
        return 0

    def get_number_transitions(self):
        """ Gives the number of transitions describe by the function

        Returns
        ----------
        n_transitions : int
            The number of transitions

        """
        counter = 0
        for s_from in self._transitions:
            counter += len(self._transitions[s_from])
        return counter

    def __call__(self, s_from, by):
        """ Calls the transition function as a real function

        Parameters
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State`
            The source state
        by : :class:`~pyformlang.finite_automaton.Symbol`
            The transition symbol

        Returns
        ----------
        s_from : :class:`~pyformlang.finite_automaton.State` or None
            The destination state or None if it does not exists

        """
        if s_from in self._transitions:
            if by in self._transitions[s_from]:
                return self._transitions[s_from][by]
        return None



class DuplicateTransitionError(Exception):
    """ Signals a duplicated transition

    Parameters
    ----------
    s_from : :class:`~pyformlang.finite_automaton.State`
        The source state
    by : :class:`~pyformlang.finite_automaton.Symbol`
        The transition symbol
    s_to : :class:`~pyformlang.finite_automaton.State`
        The wanted new destination state
    s_to_old : :class:`~pyformlang.finite_automaton.State`
        The old destination state

    Attributes
    ----------
    message : str
        An error message summarising the information

    """

    def __init__(self, s_from, by, s_to, s_to_old):
        self.message = "Transition from " + str(s_from) + " by " + str(by) +\
            " goes to " + str(s_to_old) + " not " + str(s_to)
        self._s_from = s_from
        self._by = by
        self._s_to = s_to
        self._s_to_old = s_to_old
