"""
Module for Calculating neutrino oscillation probabilities easily.

class Oscillations is the primary interface, which allows you to set the
various parameters and calculate oscillation probabilities.

The 'units' object provides pre-defined constants to ensure parameters
provided to Oscillations are in the correct units.

An enumeration of the 6 neutrino/anti-neutrino flavours is provided in
the form of nu_e, nu_mu, nu_tau, nu_e_bar, nu_mu_bar and nu_tau_bar.

For convenience, groups of those enumerations (neutrinos and anti_neutrinos)
are provided, as are some functions (isNeutrino() and isAntiNeutrino())for
testing them.
"""


import math
import cmath



#
# Units
#



class Units:
	"""Various factors for keeping units of physical quantities internally consistent.
	
	Here's how to set in a value in a given units:
	one_kilometer = 1.0 * units.km
	
	Here's how to get a value in a given units:
	print "1km = ", one_kilometer / units.mm, "mm"
	"""
	
	def __init__(self):
		# Energy
		self.GeV = 1.0
		self.eV  = 1.0e-09 * self.GeV
		self.meV = 1.0e-03 * self.eV
		self.keV = 1.0e+03 * self.eV
		self.MeV = 1.0e+06 * self.eV
		self.TeV = 1.0e+12 * self.eV
		# Distance
		self.m  = 5.07e+15 / self.GeV
		self.km = 1.0e+03 * self.m
		self.mm = 1.0e-03 * self.m
		self.cm = 1.0e-02 * self.m
		# Angle
		self.radians = 1.0
		self.degrees = (math.pi/180.0) * self.radians;
		# For mass-squared differences
		self.eV2  = pow(self.eV,  2)
		self.meV2 = pow(self.meV, 2)
		# For L/E
		self.km_GeV = self.km / self.GeV
units = Units()



#
# Neutrino / Anti-Neutrino definitions
#



# Enumeration of possible neutrino/anti-neutrino states.
# Should be used when calling Oscillations::p().
nu_e = 1
nu_mu = 2
nu_tau = 3
nu_e_bar = -nu_e
nu_mu_bar = -nu_mu
nu_tau_bar = -nu_tau


# Convenience collections of the neutrino/anti-neutrino states.
neutrinos = (nu_e, nu_mu, nu_tau)
anti_neutrinos = (nu_e_bar, nu_mu_bar, nu_tau_bar)


def isNeutrino(state):
	"""Returns True if state is a valid neutrino enum, or False otherwise."""
	return (state in neutrinos)


def isAntiNeutrino(state):
	"""Returns True if state is a valid anti-neutrino enum, or False otherwise."""
	return (state in anti_neutrinos)



#
# Oscillation calculations
#



class Oscillations:
	"""Making PMNS neutrino oscillation calculations.
	
	Methods are provided to set the PMNS parameters, mass-squared differences,
	and experimental energy and baseline.
	Oscillation probabilities can than be calculated for given initial
	and final neutrino states.
	
	Matter effects are not currently supported.
	"""
	
	def __init__(self):
		"""Constructs with initial parameters approximate to PDG (2013) and the T2K experiment."""
		self.L = 295.0 * units.km  # T2K approximate baseline
		self.E =   0.6 * units.GeV # T2K approximate peak nu_mu energy
		
		self.delta_m2_21 = (7.50e-5) * units.eV2
		self.delta_m2_32 = (2.32e-3) * units.eV2
		self._updateMasses()
		
		self.theta_12 = 33.9 * units.degrees
		self.theta_13 =  9.1 * units.degrees
		self.theta_23 = 45.0 * units.degrees
		self.delta_cp =  0.0 * units.degrees
		self._updateMatrix()
	
	
	def lOverE(self):
		"""Return the value of L/E."""
		if( self.E > 0.0 ):
			return (self.L / self.E)
		else:
			return 0.0
	
	
	def setE(self, energy):
		"""Set the neutrino energy.
		
		Raises ValueError if energy cannot be converted to a float.
		Raises ValueError if energy is negative.
		"""
		energy = float(energy) * units.GeV
		if( energy < 0.0 ):
			raise ValueError("Neutrino energy must be positive.")
		self.E = energy
	
	
	def setL(self, baseline):
		"""Set the oscillation baseline.
		
		Raises ValueError if baseline cannot be converted to a float.
		Raises ValueError if baseline is negative.
		"""
		baseline = float(baseline)
		if( baseline < 0.0 ):
			raise ValueError("Oscillation baseline must be positive.")
		self.L = baseline
	
	
	def setLOverE(self, l_over_e):
		"""Overrides the current L and E to set the ratio L/E.
		
		No guarantees are made about what L or E will be set to in order to achieve this.
		Raises ValueError if l_over_e cannot be converted to a float.
		Raises ValueError if l_over_e is negative.
		"""
		l_over_e = float(l_over_e)
		if( l_over_e < 0.0 ):
			raise ValueError("L/E must be positive.")
		self.L = self.E * l_over_e
	
	
	def setDeltaM32(self, dm2):
		"""Set the neutrino mass-squared difference (Delta m^2)_32.
		
		(Delta m^2)_32 = (m_3)^2 - (m_2)^2
		Raises ValueError if dm2 cannot be converted to a float.
		"""
		self.delta_m2_32 = float(dm2)
		self._updateMasses()
	
	
	def setDeltaM21(self, dm2):
		"""Set the neutrino mass-squared difference (Delta m^2)_21.
		
		(Delta m^2)_21 = (m_2)^2 - (m_1)^2
		Raises ValueError if dm2 cannot be converted to a float.
		"""
		self.delta_m2_21 = float(dm2)
		self._updateMasses()
	
	
	def setTheta12(self, theta):
		"""Set the PMNS mixing angle theta_12.
		
		Raises ValueError is theta_radians cannot be converted to a float.
		"""
		self.theta_12 = float(theta)
		self._updateMatrix()
	
	
	def setTheta23(self, theta):
		"""Set the PMNS mixing angle theta_23.
		
		Raises ValueError is theta cannot be converted to a float.
		"""
		self.theta_23 = float(theta)
		self._updateMatrix()
	
	
	def setTheta13(self, theta):
		"""Set the PMNS mixing angle theta_13.
		
		Raises ValueError is theta cannot be converted to a float.
		"""
		self.theta_13 = float(theta)
		self._updateMatrix()
	
	
	def setDeltaCP(self, delta):
		"""Set the PMNS CP-violating phase delta_cp.
		
		Raises ValueError is delta cannot be converted to a float.
		"""
		self.delta_cp = float(delta)
		self._updateMatrix()
	
	
	def _updateMatrix(self):
		"""Updates the PMNS matrix and its complex conjugate.
		
		Must be called by the class each time one of the PMNS matrix parameters are changed.
		"""
		zero = complex( 0.0, 0.0 )
		c12  = complex( math.cos( self.theta_12 ), 0.0 )
		c13  = complex( math.cos( self.theta_13 ), 0.0 )
		c23  = complex( math.cos( self.theta_23 ), 0.0 )
		s12  = complex( math.sin( self.theta_12 ), 0.0 )
		s13  = complex( math.sin( self.theta_13 ), 0.0 )
		s23  = complex( math.sin( self.theta_23 ), 0.0 )
		eid  = cmath.exp( complex(0.0,  self.delta_cp) ) # e^( i * delta_cp)
		emid = cmath.exp( complex(0.0, -self.delta_cp) ) # e^(-i * delta_cp)
		
		self.matrix      = [[zero,zero,zero],[zero,zero,zero],[zero,zero,zero]]
		self.anti_matrix = [[zero,zero,zero],[zero,zero,zero],[zero,zero,zero]]
		
		self.matrix[0][0] = c12 * c13
		self.matrix[0][1] = s12 * c13
		self.matrix[0][2] = s13 * emid
		
		self.matrix[1][0] = (zero - s12*c23 ) - ( c12*s23*s13*eid )
		self.matrix[1][1] = ( c12*c23 ) - ( s12*s23*s13*eid )
		self.matrix[1][2] = s23*c13
		
		self.matrix[2][0] = ( s12*s23 ) - ( c12*c23*s13*eid)
		self.matrix[2][1] = ( zero - c12*s23 ) - ( s12*c23*s13*eid )
		self.matrix[2][2] = c23*c13
		
		for i in range(3):
			for j in range(3):
				self.anti_matrix[i][j] = self.matrix[i][j].conjugate()
	
	
	def _updateMasses(self):
		"""Updates the neutrino masses (squared).
		
		Must be called by the class each time one of the mass-squared differences are changed.
		"""
		# Remember oscillations are insensitive to the absolute scale of the masses.
		# Here, we assume the smallest mass is 0.
		m2_2 = max(self.delta_m2_21, self.delta_m2_32)
		m1_2 = m2_2 - self.delta_m2_21
		m3_2 = m2_2 + self.delta_m2_32
		self.mass_squared = [m1_2, m2_2, m3_2]
	
	
	def p(self, initial, final):
		"""Returns the oscillation probability.
		
		initial : The initial state neutrino
		final : The final state neutrino
		
		Raises ValueError if initial/final is not neutrino/anti-neutrino enum as defined in this module.
		If initial and final are not both neutrinos/anti-neutrinos, 1.0 is returned.
		If L or E is 0.0, then 0.0 is returned, or 1.0 if initial == final.
		"""
		
		if( not isNeutrino(initial) and not isAntiNeutrino(initial) ):
			raise ValueError("Invalid value for initial neutrino state.")
		elif( not isNeutrino(final) and not isAntiNeutrino(final) ):
			raise ValueError("Invalid value for final neutrino state.")
		
		if( isNeutrino(initial) and isAntiNeutrino(final) ):
			return 0.0 # probability of nu -> anti_nu oscillation
		elif( isAntiNeutrino(initial) and isNeutrino(final) ):
			return 0.0 # probability of anti_nu ->nu oscillation
		
		L = self.L
		E = self.E
		# Oscillations with E = 0 or don't really make sense,
		# but if you're plotting graphs these are the values you'll want.
		if( E == 0.0 or L == 0.0 ):
			if( initial == final ):
				return 1.0
			else:
				return 0.0
		
		if( isNeutrino(initial) ):
			U = self.matrix      # Use PMNS matrix
		else:
			U = self.anti_matrix # Use complex-conjugate of PMNS matrix
		
		a = abs(initial) - 1 # index of initial neutrino state
		b = abs(final)   - 1 # index of final neutrino state
		m2 = self.mass_squared
		i = complex(0,1)
		
		s = complex(0.0,0.0)
		for x in range(3):
			s += U[a][x].conjugate() * U[b][x] * cmath.exp( (-i*m2[x]*L)/(2.0*E) )
		
		return pow(abs(s), 2)
	
	
	def __str__(self):
		s  = "theta_12 = {:.2f} degrees\n".format(self.theta_12/units.degrees)
		s += "theta_23 = {:.2f} degrees\n".format(self.theta_23/units.degrees)
		s += "theta_13 = {:.2f} degrees\n".format(self.theta_13/units.degrees)
		m2 = self.mass_squared
		s += "(Delta m^2)_21 = {:.2f} meV^2\n".format( (m2[1] - m2[0] )/units.meV2 )
		s += "(Delta m^2)_32 = {:.2f} meV^2\n".format( (m2[2] - m2[1] )/units.meV2 )
		s += "(Delta m^2)_31 = {:.2f} meV^2\n".format( (m2[2] - m2[0] )/units.meV2 )
		s += "L   = {:} km \n".format(self.L/units.km )
		s += "E   = {:} GeV\n".format(self.E/units.GeV)
		s += "L/E = {:.2f} km/GeV".format((self.L/units.km) / (self.E/units.GeV))
		return s
