""" Tests the PDA """

import unittest

from pyformlang.pda import PDA, State, StackSymbol, Symbol, Epsilon

class TestPDA(unittest.TestCase):
    """ Tests the pushdown automata """

    def test_creation(self):
        """ Test of creation """
        pda = PDA()
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 0)

        pda = PDA(start_state=State("A"))
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 0)

        pda = PDA(final_states={State("A"), State("A"), State("B"),
                                Symbol("B")})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 3)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 0)

        pda = PDA(input_symbols={Symbol("A"), Symbol("B"),
                                 Symbol("A"), State("A")})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 3)
        self.assertEqual(pda.get_number_stack_symbols(), 0)

        pda = PDA(start_stack_symbol=StackSymbol("A"))
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 1)

        pda = PDA(stack_alphabet={StackSymbol("A"), StackSymbol("A"),
                                  StackSymbol("B"),
                                  State("B")})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 0)
        self.assertEqual(pda.get_number_stack_symbols(), 3)

        pda = PDA(input_symbols={Epsilon()})
        self.assertIsNotNone(pda)
        self.assertEqual(pda.get_number_states(), 0)
        self.assertEqual(pda.get_number_input_symbols(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 0)
        self.assertEqual(pda.get_number_transitions(), 0)

    def test_transition(self):
        """ Tests the creation of transition """
        pda = PDA()
        pda.add_transition(State("from"),
                           Symbol("input symbol"),
                           StackSymbol("stack symbol"),
                           State("to"),
                           [StackSymbol("A"), StackSymbol("B")])
        self.assertEqual(pda.get_number_states(), 2)
        self.assertEqual(pda.get_number_input_symbols(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 3)
        self.assertEqual(pda.get_number_transitions(), 1)
        pda.add_transition(State("from"),
                           Epsilon(),
                           StackSymbol("stack symbol"),
                           State("to"),
                           [StackSymbol("A"), StackSymbol("B")])
        self.assertEqual(pda.get_number_states(), 2)
        self.assertEqual(pda.get_number_input_symbols(), 1)
        self.assertEqual(pda.get_number_stack_symbols(), 3)
        self.assertEqual(pda.get_number_transitions(), 2)

    def test_example62(self):
        """ Example from the book """
        q0 = State("q0")
        q1 = State("q1")
        q2 = State("q2")
        s_zero = Symbol("0")
        s_one = Symbol("1")
        ss_zero = StackSymbol("0")
        ss_one = StackSymbol("1")
        ss_z0 = StackSymbol("Z0")
        pda = PDA(states={q0, q1, q2},
                  input_symbols={s_zero, s_one},
                  stack_alphabet={ss_zero, ss_one, ss_z0},
                  start_state=q0,
                  start_stack_symbol=ss_z0,
                  final_states={q2})
        self.assertEqual(pda.get_number_states(), 3)
        self.assertEqual(pda.get_number_input_symbols(), 2)
        self.assertEqual(pda.get_number_stack_symbols(), 3)
        self.assertEqual(pda.get_number_transitions(), 0)

        pda.add_transition(q0, s_zero, ss_z0, q0, [ss_zero, ss_z0])
        pda.add_transition(q0, s_one, ss_z0, q0, [ss_one, ss_z0])

        pda.add_transition(q0, s_zero, ss_zero, q0, [ss_zero, ss_zero])
        pda.add_transition(q0, s_one, ss_one, q0, [ss_zero, ss_one])
        pda.add_transition(q0, s_one, ss_zero, q0, [ss_one, ss_zero])
        pda.add_transition(q0, s_one, ss_one, q0, [ss_one, ss_one])

        pda.add_transition(q0, Epsilon(), ss_z0, q1, [ss_z0])
        pda.add_transition(q0, Epsilon(), ss_zero, q1, [ss_zero])
        pda.add_transition(q0, Epsilon(), ss_one, q1, [ss_one])

        pda.add_transition(q1, s_zero, ss_zero, q1, [])
        pda.add_transition(q1, s_one, ss_one, q1, [])

        pda.add_transition(q1, Epsilon(), ss_z0, q2, [ss_z0])

        self.assertEqual(pda.get_number_transitions(), 12)