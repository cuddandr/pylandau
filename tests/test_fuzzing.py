''' Check pylandau with random inputs
'''
import unittest

from hypothesis import given, seed, assume
import hypothesis.extra.numpy as nps
import hypothesis.strategies as st
from hypothesis.extra.numpy import unsigned_integer_dtypes
import numpy as np
from scipy.integrate import quad as integrate

import pylandau
from tests import constrains


class Test(unittest.TestCase):

    @given(st.floats(constrains.LANDAU_MIN_MPV,
                     constrains.LANDAU_MAX_MPV,
                     allow_nan=False,
                     allow_infinity=False))
    def test_landau_mpv(self, mpv):
        ''' Check Landau MPV position '''
        # https://github.com/SiLab-Bonn/pyLandau/issues/11
        assume(abs(mpv) > 1e-3)
        x = np.linspace(mpv - 10, mpv + 10, 1000)
        y = pylandau.landau(x, mpv=mpv, eta=1., A=1.)
        delta = x[1] - x[0]
        self.assertAlmostEqual(x[np.argmax(y)], mpv, delta=delta)

    @given(st.floats(constrains.LANGAU_MIN_MPV,
                     constrains.LANGAU_MAX_MPV,
                     allow_nan=False,
                     allow_infinity=False))
    def test_langau_mpv(self, mpv):
        ''' Check Langau MPV position '''
        # https://github.com/SiLab-Bonn/pyLandau/issues/11
        assume(abs(mpv) > 1e-3)
        x = np.linspace(mpv - 10, mpv + 10, 1000)
        y = pylandau.langau(x, mpv=mpv, eta=1., sigma=1., A=1.)
        delta = x[1] - x[0]
        self.assertAlmostEqual(x[np.argmax(y)], mpv, delta=delta)

    @given(st.floats(constrains.LANDAU_MIN_A,
                     constrains.LANDAU_MAX_A,
                     allow_nan=False,
                     allow_infinity=False))
    def test_landau_A(self, A):
        ''' Check Landau amplitude '''
        mpv = 1.
        x = np.linspace(mpv - 10, mpv + 10, 1000)
        y = pylandau.landau(x, mpv=mpv, eta=1., A=A)
        self.assertAlmostEqual(y.max(), A, delta=1e-4 * A)

    @given(st.floats(constrains.LANGAU_MIN_A,
                     constrains.LANGAU_MAX_A,
                     allow_nan=False,
                     allow_infinity=False))
    def test_langau_A(self, A):
        ''' Check Langau amplitude '''
        mpv = 1.
        x = np.linspace(mpv - 10, mpv + 10, 1000)
        y = pylandau.langau(x, mpv=mpv, eta=1., sigma=1., A=A)
        self.assertAlmostEqual(y.max(), A, delta=1e-4 * A)

    @given(st.tuples(
        # mpv
        st.floats(constrains.LANDAU_MIN_MPV,
                  constrains.LANDAU_MAX_MPV,
                  allow_nan=False,
                  allow_infinity=False),
        # eta
        st.floats(constrains.LANDAU_MIN_ETA,
                  constrains.LANDAU_MAX_ETA,
                  allow_nan=False,
                  allow_infinity=False),
        # A
        st.floats(constrains.LANDAU_MIN_A,
                  constrains.LANDAU_MAX_A,
                  allow_nan=False,
                  allow_infinity=False),)
           )
    def test_landau_stability(self, pars):
        ''' Check Landau outputs for same intput parameters '''
        (mpv, eta, A) = pars
        x = np.linspace(mpv - 5 * eta, mpv + 5 * eta, 1000)
        y_1 = pylandau.landau(x, mpv=mpv, eta=eta, A=A)
        y_2 = pylandau.landau(x, mpv=mpv, eta=eta, A=A)
        self.assertTrue(np.all(y_1 == y_2))

    @given(st.tuples(
        # mpv
        st.floats(constrains.LANGAU_MIN_MPV,
                  constrains.LANGAU_MAX_MPV,
                  allow_nan=False,
                  allow_infinity=False),
        # eta
        st.floats(constrains.LANGAU_MIN_ETA,
                  constrains.LANGAU_MAX_ETA,
                  allow_nan=False,
                  allow_infinity=False),
        # sigma
        st.floats(constrains.LANGAU_MIN_SIGMA,
                  constrains.LANGAU_MAX_SIGMA,
                  allow_nan=False,
                  allow_infinity=False),
        # A
        st.floats(constrains.LANGAU_MIN_A,
                  constrains.LANGAU_MAX_A,
                  allow_nan=False,
                  allow_infinity=False),)
           )
    def test_langau_stability(self, pars):
        ''' Check Langau outputs for same intput parameters '''

        (mpv, eta, sigma, A) = pars
        # Correct input to avoid oscillations
        if sigma > 100 * eta:
            sigma = eta
        assume(sigma * eta < constrains.LANGAU_MAX_ETA_SIGMA)
        x = np.linspace(mpv - 5 * sigma * eta, mpv + 5 * sigma * eta, 1000)
        y_1 = pylandau.langau(x, mpv=mpv, eta=eta, sigma=sigma, A=A)
        y_2 = pylandau.langau(x, mpv=mpv, eta=eta, sigma=sigma, A=A)
        self.assertTrue(np.all(y_1 == y_2))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
