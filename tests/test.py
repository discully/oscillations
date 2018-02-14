import unittest
import xmlrunner
import oscillations
import math


float_comp = 7
xml_output = True



class TestUnits (unittest.TestCase):
	
	def test_energyGigaelectronvolts(self):
		self.assertAlmostEqual(oscillations.units.GeV, 1e+9 * oscillations.units.eV, places=float_comp)
	
	def test_energyMegaelectronvolts(self):
		self.assertAlmostEqual(oscillations.units.MeV, 1e+6 * oscillations.units.eV, places=float_comp)
		
	def test_energyKiloelectronvolts(self):
		self.assertAlmostEqual(oscillations.units.keV, 1e+3 * oscillations.units.eV, places=float_comp)
		
	def test_energyMillielectronvolts(self):
		self.assertAlmostEqual(oscillations.units.meV, 1e-3 * oscillations.units.eV, places=float_comp)
	
	def test_energyGigaelectronvoltsMegaelectronvolts(self):
		self.assertAlmostEqual(oscillations.units.GeV, 1e+3 * oscillations.units.MeV, places=float_comp)
	
	def test_distanceKilomtres(self):
		self.assertAlmostEqual(oscillations.units.km, 1e+3 * oscillations.units.m, places=float_comp)
	
	def test_distanceCentimetres(self):
		self.assertAlmostEqual(oscillations.units.cm, 1e-2 * oscillations.units.m, places=float_comp)
	
	def test_distanceMillimetres(self):
		self.assertAlmostEqual(oscillations.units.mm, 1e-3 * oscillations.units.m, places=float_comp)
	
	def test_distanceCentimtresMillimetres(self):
		self.assertAlmostEqual(oscillations.units.cm, 1e+1 * oscillations.units.mm, places=float_comp)
	
	def test_angleDegreesRadians(self):
		self.assertAlmostEqual(
			oscillations.units.degrees,
			(math.pi/180.0) * oscillations.units.radians,
			places=float_comp)
	
	def test_massMillelectronvolts2Electronvolts2(self):
		self.assertAlmostEqual(
			oscillations.units.meV2,
			( pow(1e-3, 2) * oscillations.units.eV2 ),
			places=float_comp)
	
	def test_distancePerEnergy(self):
		self.assertAlmostEqual(
			oscillations.units.km_GeV,
			oscillations.units.km / oscillations.units.GeV,
			places=float_comp)



class TestNeutrinos (unittest.TestCase):
	
	def test_nuEIsNeutrino(self):
		self.assertTrue( oscillations.isNeutrino( oscillations.nu_e ) )
	
	def test_nuMuIsNeutrino(self):
		self.assertTrue( oscillations.isNeutrino( oscillations.nu_mu ) )
	
	def test_nuTauIsNeutrino(self):
		self.assertTrue( oscillations.isNeutrino( oscillations.nu_tau ) )
	
	def test_nuEBarIsNotNeutrino(self):
		self.assertFalse( oscillations.isNeutrino( oscillations.nu_e_bar ) )
	
	def test_nuMuBarIsNotNeutrino(self):
		self.assertFalse( oscillations.isNeutrino( oscillations.nu_mu_bar ) )
	
	def test_nuTauBarIsNotNeutrino(self):
		self.assertFalse( oscillations.isNeutrino( oscillations.nu_tau_bar ) )
	
	def test_nuEIsNotAntiNeutrino(self):
		self.assertFalse( oscillations.isAntiNeutrino( oscillations.nu_e ) )
	
	def test_nuMuIsNotAntiNeutrino(self):
		self.assertFalse( oscillations.isAntiNeutrino( oscillations.nu_mu ) )
	
	def test_nuTauIsNotAntiNeutrino(self):
		self.assertFalse( oscillations.isAntiNeutrino( oscillations.nu_tau ) )
	
	def test_nuEBarIsAntiNeutrino(self):
		self.assertTrue( oscillations.isAntiNeutrino( oscillations.nu_e_bar ) )
	
	def test_nuMuBarIsAntiNeutrino(self):
		self.assertTrue( oscillations.isAntiNeutrino( oscillations.nu_mu_bar ) )
	
	def test_nuTauBarIsAntiNeutrino(self):
		self.assertTrue( oscillations.isAntiNeutrino( oscillations.nu_tau_bar ) )
	
	def test_nuEIsMinusNuEBar(self):
		self.assertEqual( oscillations.nu_e, -oscillations.nu_e_bar )
		
	def test_nuMuIsMinusNuMuBar(self):
		self.assertEqual( oscillations.nu_mu, -oscillations.nu_mu_bar )
		
	def test_nuTauIsMinusNuTauBar(self):
		self.assertEqual( oscillations.nu_tau, -oscillations.nu_tau_bar )
	
	def test_thereAreThreeNeutrinos(self):
		self.assertEqual( len(oscillations.neutrinos), 3 )
	
	def test_thereAreThreeAntiNeutrinos(self):
		self.assertEqual( len(oscillations.anti_neutrinos), 3 )
	
	def test_allStatesAreUnique(self):
		for neutrino in oscillations.neutrinos:
			for anti_neutrino in oscillations.anti_neutrinos:
				self.assertNotEqual(neutrino, anti_neutrino)



class TestOscillations (unittest.TestCase):
	
	def setUp(self):
		# Example experiment oscillations
		self.osc = oscillations.Oscillations()
		self.osc.setL(295.0 * oscillations.units.km )
		self.osc.setE(0.6   * oscillations.units.GeV)
		self.osc.setDeltaM21( 7.50e-5 * oscillations.units.eV2 )
		self.osc.setDeltaM32( 2.32e-3 * oscillations.units.eV2 )
		self.osc.setTheta12( 33.9 * oscillations.units.degrees )
		self.osc.setTheta13(  9.1 * oscillations.units.degrees )
		self.osc.setTheta23( 45.0 * oscillations.units.degrees )
		self.osc.setDeltaCP(  0.0 * oscillations.units.degrees )
		# get an index which does not represent a neutrino or anti-neutrino
		non_nu = 1
		while( oscillations.isNeutrino(non_nu) or oscillations.isAntiNeutrino(non_nu) ):
			non_nu += 1
		self.non_neutrino = non_nu
	
	def test_setERaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setE, "a")
	
	def test_setERaisesValueErrorForNegativeValue(self):
		self.assertRaises(ValueError, self.osc.setE, -3.3)
	
	def test_setLRaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setL, "b")
	
	def test_setLRaisesValueErrorForNegativeValue(self):
		self.assertRaises(ValueError, self.osc.setL, -2.4)
	
	def test_setLOverERaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setLOverE, "c")
	
	def test_setLOverERaisesValueErrorForNegativeValue(self):
		self.assertRaises(ValueError, self.osc.setLOverE, -8.1)
	
	def test_setLOverESucceedsInSettingValue(self):
		new_l_over_e = 1.3
		self.osc.setLOverE(new_l_over_e)
		self.assertAlmostEqual( self.osc.lOverE(), new_l_over_e, places=float_comp )
	
	def test_setDeltaM32RaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setDeltaM32, "d")
	
	def test_setDeltaM21RaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setDeltaM21, "e")
	
	def test_setTheta12RaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setTheta12, "f")
	
	def test_setTheta23RaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setTheta23, "g")
	
	def test_setTheta13RaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setTheta13, "h")
	
	def test_setDeltaCPRaisesValueErrorForNonFloat(self):
		self.assertRaises(ValueError, self.osc.setDeltaCP, "i")
	
	def test_oscillationsOccur(self):
		for initial in oscillations.neutrinos:
			for final in oscillations.neutrinos:
				p = self.osc.p(initial, final)
				self.assertGreater( p , 0.0 )
				self.assertLessEqual( p, 1.0 )
	
	def test_unitarity(self):
		total = 0.0
		for neutrino in oscillations.neutrinos:
			total += self.osc.p(oscillations.nu_mu, neutrino)
		self.assertAlmostEqual( total, 1.0, places=float_comp )
	
	def test_noCPViolationIfDeltaIsZero(self):
		self.osc.setDeltaCP(0.0)
		self.assertAlmostEqual(
			self.osc.p(oscillations.nu_mu, oscillations.nu_e),
			self.osc.p(oscillations.nu_mu_bar, oscillations.nu_e_bar),
			places=float_comp)
	
	def test_noCPViolationIfTheta13IsZero(self):
		self.osc.setTheta13(0.0)
		self.assertAlmostEqual(
			self.osc.p(oscillations.nu_mu, oscillations.nu_e),
			self.osc.p(oscillations.nu_mu_bar, oscillations.nu_e_bar),
			places=float_comp)
	
	def test_cpViolationIfDeltaNonZero(self):
		self.osc.setTheta13(9.1  * oscillations.units.degrees)
		self.osc.setDeltaCP(35.0 * oscillations.units.degrees)
		self.assertNotAlmostEqual(
			self.osc.p(oscillations.nu_mu, oscillations.nu_e),
			self.osc.p(oscillations.nu_mu_bar, oscillations.nu_e_bar),
			places=float_comp)
	
	def test_noOscillationsAtDistanceZero(self):
		self.osc.setL(0.0)
		self.assertEqual( self.osc.p(oscillations.nu_e, oscillations.nu_e  ), 1.0)
		self.assertEqual( self.osc.p(oscillations.nu_e, oscillations.nu_mu ), 0.0)
		self.assertEqual( self.osc.p(oscillations.nu_e, oscillations.nu_tau), 0.0)
	
	def test_noOscillationsAtEnergyZero(self):
		self.osc.setE(0.0)
		self.assertEqual( self.osc.p(oscillations.nu_e, oscillations.nu_e  ), 1.0)
		self.assertEqual( self.osc.p(oscillations.nu_e, oscillations.nu_mu ), 0.0)
		self.assertEqual( self.osc.p(oscillations.nu_e, oscillations.nu_tau), 0.0)
	
	def test_noOscillationsBetweenNeutrinosAndAntiNeutrions(self):
		for neutrino in oscillations.neutrinos:
			for anti_neutrino in oscillations.anti_neutrinos:
				self.assertEqual( self.osc.p(neutrino, anti_neutrino), 0.0 )
				self.assertEqual( self.osc.p(anti_neutrino, neutrino), 0.0 )
	
	def test_noOscillationsIfNoMassDifferences(self):
		self.osc.setDeltaM21(0.0)
		self.osc.setDeltaM32(0.0)
		self.assertAlmostEqual( self.osc.p(oscillations.nu_mu,oscillations.nu_e  ), 0.0, places=float_comp )
		self.assertAlmostEqual( self.osc.p(oscillations.nu_mu,oscillations.nu_mu ), 1.0, places=float_comp )
		self.assertAlmostEqual( self.osc.p(oscillations.nu_mu,oscillations.nu_tau), 0.0, places=float_comp )
	
	def test_noOscillationsIfNoMixing(self):
		self.osc.setTheta12(0.0)
		self.osc.setTheta23(0.0)
		self.osc.setTheta13(0.0)
		self.assertAlmostEqual( self.osc.p(oscillations.nu_mu,oscillations.nu_e  ), 0.0, places=float_comp )
		self.assertAlmostEqual( self.osc.p(oscillations.nu_mu,oscillations.nu_mu ), 1.0, places=float_comp )
		self.assertAlmostEqual( self.osc.p(oscillations.nu_mu,oscillations.nu_tau), 0.0, places=float_comp )
	
	def test_pRaisesValueErrorForInvalidInitialState(self):
		self.assertRaises(ValueError, self.osc.p, self.non_neutrino, oscillations.nu_mu)
	
	def test_pRaisesValueErrorForInvalidFinalState(self):
		self.assertRaises(ValueError, self.osc.p, oscillations.nu_mu, self.non_neutrino)



def main():
	if( xml_output ):
		import xmlrunner	
		unittest.main(
			testRunner=xmlrunner.XMLTestRunner(),
			failfast=False,
			buffer=False,
			catchbreak=False
			)
	else:
		unittest.main()
	
if __name__ == "__main__":
	main()
