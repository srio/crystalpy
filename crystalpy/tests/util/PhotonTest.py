"""
Unittest for Photon class.
"""

import unittest

from crystalpy.util.Photon import Photon
from crystalpy.util.Vector import Vector


class PhotonTest(unittest.TestCase):

    def testConstructorByDefault(self):
        photon = Photon()

        self.assertIsInstance(photon, Photon)
        self.assertEqual(photon.energy(), 1000.0)
        self.assertTrue(photon.unitDirectionVector() == Vector(0.0, 1.0, 0.0))

    def testConstructor(self):
        photon = Photon(4000, Vector(0, 0, 1))

        self.assertIsInstance(photon, Photon)
        self.assertEqual(photon.energy(), 4000)
        self.assertTrue(photon.unitDirectionVector() == Vector(0, 0, 1))

    def testEnergy(self):
        photon = Photon(4000, Vector(0, 0, 1))
        photon.setEnergy(8000.0)
        self.assertEqual(photon.energy(), 8000)

    def testWavelength(self):
        # Test data in eV : m.
        test_data = {   3: 413.28 * 1e-9,
                        4: 309.96 * 1e-9,
                        8: 154.98 * 1e-9,
                     5000: 2.4797 * 1e-10,
                    10000: 1.2398 * 1e-10}

        for energy, wavelength in test_data.items():
            photon = Photon(energy, Vector(0, 0, 1))
            # print("Energy=%f, Wavelength=%f A (reference = %f A)"%(energy,1e10*photon.wavelength(),1e10*wavelength))
            self.assertAlmostEqual(1e10*photon.wavelength(),1e10*wavelength,places=1)

    def testWavenumber(self):
        # Test data in eV : m^-1.
        test_data = {   3: 15203192.28,
                        4: 20270923.03,
                        8: 40541846.07,
                     5000: 25338653792.67,
                    10000: 50677307585.34}

        for energy, wavenumber in test_data.items():
            photon = Photon(energy, Vector(0, 0, 1))
            self.assertAlmostEqual(photon.wavenumber(),
                                   wavenumber, places=1)

    def testWavevector(self):
        direction = Vector(0, 0, 1)
        photon = Photon(5000.0, direction)

        wavevector = photon.wavevector()

        self.assertAlmostEqual(wavevector.norm(),
                               25338653792.67, places=1)

        self.assertEqual(wavevector.getNormalizedVector(),
                         direction)

    def testUnitDirectionVector(self):
        photon = Photon(4000, Vector(0, 0, 5))

        self.assertTrue(photon.unitDirectionVector() == Vector(0, 0, 1))

    def testSetUnitDirectionVector(self):
        photon = Photon(4000, Vector(0, 0, 5))
        photon.setUnitDirectionVector(Vector(1,2,3))

        self.assertTrue(photon.unitDirectionVector() == Vector(1, 2, 3).getNormalizedVector())

    def testOperatorEqual(self):
        photon_one = Photon(4000, Vector(0, 0, 5))
        photon_two = Photon(4000, Vector(0, 1, 1))
        photon_three = Photon(2000, Vector(0, 0, 5))

        self.assertTrue(photon_one == photon_one)
        self.assertFalse(photon_one == photon_two)
        self.assertFalse(photon_one == photon_three)
        self.assertFalse(photon_two == photon_three)

    def testOperatorNotEqual(self):
        photon_one = Photon(4000, Vector(0, 0, 5))
        photon_two = Photon(4000, Vector(0, 1, 1))
        photon_three = Photon(2000, Vector(0, 0, 5))

        self.assertFalse(photon_one != photon_one)
        self.assertTrue(photon_one != photon_two)
        self.assertTrue(photon_one != photon_three)
        self.assertTrue(photon_two != photon_three)

    def testDuplicate(self):
        photon_one = Photon(4000, Vector(0, 0, 5))
        photon_two = photon_one.duplicate()


        self.assertTrue( photon_one == photon_two )

        photon_one.setEnergy(1000.0)
        self.assertFalse( photon_one == photon_two )