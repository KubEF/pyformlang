""" Tests the CFG """

import unittest

from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon

class TestCFG(unittest.TestCase):
    """ Tests the production """

    def test_creation(self):
        """ Tests creatin of CFG """
        v0 = Variable(0)
        t0 = Terminal("a")
        p0 = Production(v0, [t0, Terminal("A"), Variable(1)])
        cfg = CFG({v0}, {t0}, v0, {p0})
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.get_number_variables(), 2)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 1)
        self.assertTrue(cfg.is_empty())

        cfg = CFG()
        self.assertIsNotNone(cfg)
        self.assertEqual(cfg.get_number_variables(), 0)
        self.assertEqual(cfg.get_number_terminals(), 0)
        self.assertEqual(cfg.get_number_productions(), 0)
        self.assertTrue(cfg.is_empty())

    def test_generating_object(self):
        """ Test the finding of CFGObject """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(start, [ter_a])
        p2 = Production(var_A, [ter_b])
        cfg = CFG({var_A, var_B, start}, {ter_a, ter_b}, start, {p0, p1, p2})
        self.assertEqual(cfg.get_number_variables(), 3)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 3)
        self.assertEqual(cfg.get_generating_symbols(), {var_A, ter_a, ter_b, start})

        p3 = Production(var_B, [Epsilon()])

        cfg = CFG({var_A, var_B, start}, {ter_a, ter_b}, start, {p0, p1, p2, p3})
        self.assertEqual(cfg.get_number_variables(), 3)
        self.assertEqual(cfg.get_number_terminals(), 2)
        self.assertEqual(cfg.get_number_productions(), 4)
        self.assertEqual(cfg.get_generating_symbols(), {var_A, var_B, ter_a,
                                                        ter_b, start})

    def test_reachable_object(self):
        """ Test the finding of reachable objects """
        var_A = Variable("A")
        var_B = Variable("B")
        var_C = Variable("C")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(start, [ter_a])
        p2 = Production(var_A, [ter_b])
        p3 = Production(var_C, [ter_c])
        p4 = Production(var_A, [Epsilon()])
        cfg = CFG({var_A, var_B, start, var_C},
                  {ter_a, ter_b, ter_c},
                  start, {p0, p1, p2, p3, p4})
        self.assertEqual(cfg.get_reachable_symbols(), {var_A, ter_a, var_B,
                                                       ter_b, start})

    def test_useless_removal(self):
        """ Test the removal of useless symbols """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(start, [ter_a])
        p2 = Production(var_A, [ter_b])
        cfg = CFG({var_A, var_B, start}, {ter_a, ter_b}, start, {p0, p1, p2})
        new_cfg = cfg.remove_useless_symbols()
        self.assertEqual(new_cfg.get_number_variables(), 1)
        self.assertEqual(new_cfg.get_number_terminals(), 1)
        self.assertEqual(new_cfg.get_number_productions(), 1)
        self.assertFalse(cfg.is_empty())

    def test_nullable_object(self):
        """ Tests the finding of nullable objects """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(var_A, [ter_a, var_A, var_A])
        p2 = Production(var_A, [Epsilon()])
        p3 = Production(var_B, [ter_b, var_B, var_B])
        p4 = Production(var_B, [Epsilon()])
        cfg = CFG({var_A, var_B, start},
                  {ter_a, ter_b},
                  start, {p0, p1, p2, p3, p4})
        self.assertEqual(cfg.get_nullable_symbols(),
                         {var_A, var_B, start})

    def test_remove_epsilon(self):
        """ Tests the removal of epsilon """
        var_A = Variable("A")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        start = Variable("S")
        p0 = Production(start, [var_A, var_B])
        p1 = Production(var_A, [ter_a, var_A, var_A])
        p2 = Production(var_A, [Epsilon()])
        p3 = Production(var_B, [ter_b, var_B, var_B])
        p4 = Production(var_B, [])
        cfg = CFG({var_A, var_B, start},
                  {ter_a, ter_b},
                  start, {p0, p1, p2, p3, p4})
        new_cfg = cfg.remove_epsilon()
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 9)
        self.assertEqual(len(new_cfg.get_nullable_symbols()), 0)
        self.assertFalse(cfg.is_empty())

    def test_unit_pair(self):
        """ Test the finding of unit pairs """
        var_I = Variable("I")
        var_F = Variable("F")
        var_E = Variable("E")
        var_T = Variable("T")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_I, [ter_a]),
                       Production(var_I, [ter_b]),
                       Production(var_I, [var_I, ter_a]),
                       Production(var_I, [var_I, ter_b]),
                       Production(var_I, [var_I, ter_0]),
                       Production(var_I, [var_I, ter_1]),
                       Production(var_F, [var_I]),
                       Production(var_F, [ter_par_open, var_E, ter_par_close]),
                       Production(var_T, [var_F]),
                       Production(var_T, [var_T, ter_mult, var_F]),
                       Production(var_E, [var_T]),
                       Production(var_E, [var_E, ter_plus, var_T])}
        cfg = CFG({var_I, var_F, var_E, var_T},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_E,
                  productions)
        self.assertEqual(cfg.get_unit_pairs(),
                         {(var_E, var_E),
                          (var_E, var_T),
                          (var_E, var_F),
                          (var_E, var_I),
                          (var_T, var_T),
                          (var_T, var_F),
                          (var_T, var_I),
                          (var_F, var_F),
                          (var_F, var_I),
                          (var_I, var_I)})
        new_cfg = cfg.eliminate_unit_productions()
        self.assertEqual(new_cfg.get_number_productions(), 30)

    def test_cnf(self):
        """ Tests the conversion to CNF form """
        var_I = Variable("I")
        var_F = Variable("F")
        var_E = Variable("E")
        var_T = Variable("C#CNF#1")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_0 = Terminal("0")
        ter_1 = Terminal("1")
        ter_par_open = Terminal("(")
        ter_par_close = Terminal(")")
        ter_mult = Terminal("*")
        ter_plus = Terminal("+")
        productions = {Production(var_I, [ter_a]),
                       Production(var_I, [ter_b]),
                       Production(var_I, [var_I, ter_a]),
                       Production(var_I, [var_I, ter_b]),
                       Production(var_I, [var_I, ter_0]),
                       Production(var_I, [var_I, ter_1]),
                       Production(var_F, [var_I]),
                       Production(var_F, [ter_par_open, var_E, ter_par_close]),
                       Production(var_T, [var_F]),
                       Production(var_T, [var_T, ter_mult, var_F]),
                       Production(var_E, [var_T]),
                       Production(var_E, [var_E, ter_plus, var_T])}
        cfg = CFG({var_I, var_F, var_E, var_T},
                  {ter_a, ter_b, ter_0, ter_1, ter_par_open,
                   ter_par_close, ter_mult, ter_plus},
                  var_E,
                  productions)
        new_cfg = cfg.to_normal_form()
        self.assertEqual(new_cfg.get_number_variables(), 15)
        self.assertEqual(new_cfg.get_number_terminals(), 8)
        self.assertEqual(new_cfg.get_number_productions(), 41)
        self.assertFalse(cfg.is_empty())

    def test_substitution(self):
        """ Tests substitutions in a CFG """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.substitute({ter_a: cfg})
        self.assertEqual(new_cfg.get_number_variables(), 2)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 4)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_a, ter_b, ter_a, ter_b, ter_b, ter_b]))

    def test_union(self):
        """ Tests the union of two cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.union(cfg)
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 6)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_b, ter_b]))

    def test_concatenation(self):
        """ Tests the concatenation of two cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.concatenate(cfg)
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 5)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_b, ter_b, ter_a, ter_b]))

    def test_closure(self):
        """ Tests the closure of a cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [ter_c])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.get_closure()
        self.assertEqual(new_cfg.get_number_variables(), 2)
        self.assertEqual(new_cfg.get_number_terminals(), 3)
        self.assertEqual(new_cfg.get_number_productions(), 5)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([]))
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b,
                                          ter_a, ter_c, ter_b]))

    def test_pos_closure(self):
        """ Tests the closure of a cfg """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [ter_c])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.get_positive_closure()
        self.assertEqual(new_cfg.get_number_variables(), 3)
        self.assertEqual(new_cfg.get_number_terminals(), 3)
        self.assertEqual(new_cfg.get_number_productions(), 6)
        self.assertFalse(new_cfg.is_empty())
        self.assertFalse(new_cfg.contains([]))
        self.assertTrue(new_cfg.contains([ter_a, ter_a, ter_c, ter_b, ter_b,
                                          ter_a, ter_c, ter_b]))

    def test_reverse(self):
        """ Test the reversal of a CFG """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        new_cfg = cfg.reverse()
        self.assertEqual(new_cfg.get_number_variables(), 1)
        self.assertEqual(new_cfg.get_number_terminals(), 2)
        self.assertEqual(new_cfg.get_number_productions(), 2)
        self.assertFalse(new_cfg.is_empty())
        self.assertTrue(new_cfg.contains([ter_b, ter_b, ter_a, ter_a]))

    def test_emptiness(self):
        """ Tests the emptiness of a CFG """
        var_S = Variable("S")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        p0 = Production(var_S, [ter_a, var_S, ter_b])
        p1 = Production(var_S, [])
        cfg = CFG({var_S}, {ter_a, ter_b}, var_S, {p0, p1})
        self.assertFalse(cfg.is_empty())

    def test_membership(self):
        """ Tests the membership of a CFG """
        var_useless = Variable("USELESS")
        var_S = Variable("S")
        var_B = Variable("B")
        ter_a = Terminal("a")
        ter_b = Terminal("b")
        ter_c = Terminal("c")
        p0 = Production(var_S, [ter_a, var_S, var_B])
        p1 = Production(var_useless, [ter_a, var_S, var_B])
        p2 = Production(var_S, [var_useless])
        p4 = Production(var_B, [ter_b])
        p5 = Production(var_useless, [])
        cfg0 = CFG({var_useless, var_S}, {ter_a, ter_b}, var_S, {p0, p1, p2, p4, p5})
        self.assertTrue(cfg0.contains([Epsilon()]))
        self.assertTrue(cfg0.contains([ter_a, ter_b]))
        self.assertTrue(cfg0.contains([ter_a, ter_a, ter_b, ter_b]))
        self.assertTrue(cfg0.contains([ter_a, ter_a, ter_a, ter_b, ter_b, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_b, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_b, ter_c, ter_b]))
        self.assertFalse(cfg0.contains([ter_a, ter_a, ter_a, ter_b, ter_b]))

        p3 =  Production(var_S, [ter_c])
        cfg0 = CFG({var_S}, {ter_a, ter_b, ter_c}, var_S, {p0, p3})
        self.assertFalse(cfg0.contains([Epsilon()]))

        var_A = Variable("A")
        p6 = Production(var_S, [var_A, var_B])
        p7 = Production(var_A, [var_A, var_B])
        p8 = Production(var_A, [ter_a])
        p9 = Production(var_B, [ter_b])
        cfg1 = CFG({var_A, var_B, var_S},
                   {ter_a, ter_b},
                   var_S,
                   {p6, p7, p8, p9})
        self.assertTrue(cfg1.contains([ter_a, ter_b, ter_b]))
