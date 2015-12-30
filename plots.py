"""
Examples of the oscillation module in use, being used to generate the
oscillation plots from my PhD thesis.

Expects PyROOT to be installed and loaded.
"""


import ROOT
import oscillations
import math



def colour(nu):
	"""Return the line colour to use for a given neutrino flavour."""
	if( abs(nu) == oscillations.nu_e   ): return ROOT.kBlue + 3
	if( abs(nu) == oscillations.nu_mu  ): return ROOT.kRed - 3
	if( abs(nu) == oscillations.nu_tau ): return ROOT.kGreen - 5
	raise ValueError("Invalid neutrino/anti-neutrino enum.")



def style(nu):
	"""Return the line style to use for a given neutrino flavour."""
	if oscillations.isNeutrino(nu):
		return 1
	elif oscillations.isAntiNeutrino(nu):
		return 7
	else:
		raise ValueError("Invalid neutrino/anti-neutrino enum.")



def styleHierarchy(dm2_31):
	"""Return the line style to use for a given mass hierarchy.
	dm2_31 : (Delta m^2)_31.
	"""
	if( dm2_31 > 0 ): return 1
	else: return 7



def name(nu):
	"""Return a ROOT text representation of a given neutrino flavour."""
	if( nu == oscillations.nu_e ):       return "#nu_{e}"
	if( nu == oscillations.nu_mu ):      return "#nu_{#mu}"
	if( nu == oscillations.nu_tau ):     return "#nu_{#tau}"
	if( nu == oscillations.nu_e_bar ):   return "#bar{#nu}_{e}"
	if( nu == oscillations.nu_mu_bar ):  return "#bar{#nu}_{#mu}"
	if( nu == oscillations.nu_tau_bar ): return "#bar{#nu}_{#tau}"
	raise ValueError("Invalid neutrino/anti-neutrino enum.")



def colourDelta(delta_cp):
	"""Return the line colour to use for a given value of delta_cp."""
	if( delta_cp == 0 ):                        return ROOT.kBlack
	elif( delta_cp > 0.0 and delta_cp <= 180 ): return ROOT.kBlue - 3
	else:                                       return ROOT.kBlue + 3



def styleDelta(delta_cp):
	"""Return the line style to use for a given value of delta_cp."""
	if( math.fabs(delta_cp) == 0 ): return 1
	if( math.fabs(delta_cp) == 45 ): return 7
	if( math.fabs(delta_cp) == 90 or math.fabs(delta_cp) == 270 ): return 2
	if( math.fabs(delta_cp) == 180 ): return 1
	raise ValueError("Unsupported value of delta_cp.")



def styleTheta23(theta_23):
	"""Return the line style to use for a given value of theta_23."""
	if( theta_23 == 45 ): return 1
	if( theta_23 == 40 ): return 7
	if( theta_23 == 35 ): return 2
	raise ValueError("Unsupported value of theta_23.")



def styleDM32(delta_m2_32):
	"""Return the line style to use for a given value of (Delta m^2)_32."""
	if( delta_m2_32 == 2.3e-3 ): return 1
	if( delta_m2_32 == 2.0e-3 ): return 7
	if( delta_m2_32 == 2.6e-3 ): return 2
	raise ValueError("Unsupported value of delta_m2_23.")



def styleTheta13(theta_13):
	"""Return the line style to use for a given value of theta_13."""
	if( theta_13 ==  7 ): return 2
	if( theta_13 ==  9 ): return 1
	if( theta_13 == 11 ): return 7
	raise ValueError("Unsupported value of theta_13.")



def plotLOverE(mode = "short"):
	"""Plot P(nu_mu -> nu) for all flavours as a function of L/E.
	
	mode : Specifies either 'short' or 'long' range plot.
	"""
	n = 4000
	
	if( mode == "short" ):
		le_max = 4000.0
	elif( mode == "long" ):
		le_max = 40000.0
	else:
		raise ValueError("Mode must be either 'short' or 'long'.")
	
	le_min = 0.0
	le_step = (le_max - le_min) / float(n)
	
	graphs = {}
	graphs[oscillations.nu_e]   = ROOT.TGraph(n+1)
	graphs[oscillations.nu_mu]  = ROOT.TGraph(n+1)
	graphs[oscillations.nu_tau] = ROOT.TGraph(n+1)
	
	osc = oscillations.Oscillations()
	
	for i in range(n+1):
		le = le_min + (i * le_step)
		osc.setLOverE( le * oscillations.units.km_GeV )
		
		p_e   = 100 * osc.p(oscillations.nu_mu, oscillations.nu_e)
		p_mu  = 100 * osc.p(oscillations.nu_mu, oscillations.nu_mu)
		p_tau = 100 * osc.p(oscillations.nu_mu, oscillations.nu_tau)
		
		graphs[oscillations.nu_e  ].SetPoint(i, le, p_e)
		graphs[oscillations.nu_mu ].SetPoint(i, le, p_mu)
		graphs[oscillations.nu_tau].SetPoint(i, le, p_tau)
	
	c = ROOT.TCanvas("c", "c", 800, 800)
	f = c.DrawFrame(0.0, 0.0, le_max, 100)
	
	l = ROOT.TLegend(0.91, 0.65, 1.0, 0.9)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Neutrino Oscillations")
	f.GetXaxis().SetTitle("L / E_{#nu}  [ km GeV ^{-1} ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{#alpha} )  [ % ]   ")
	
	for nu in [oscillations.nu_tau, oscillations.nu_mu, oscillations.nu_e]:
		graph = graphs[nu]
		graph.SetLineColor( colour(nu) )
		graph.SetLineStyle( style(nu)  )
		
		if( mode == "short" ):
			graph.SetLineWidth(5)
		elif( mode == "long" ):
			graph.SetLineWidth(3)
		
		graph.Draw()
		
		l.AddEntry(graph, name(nu), "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-le-" + mode + ".png")



def plotDeltaCP(e_range):
	"""Plot P(nu_mu -> nu_e) as a function of E for different values of delta_cp."""
	n = 300
	
	deltas = [0, 90, 180, 270]
	
	e_min = e_range[0]
	e_max = e_range[1]
	e_step = (e_max - e_min) / float(n)
	
	graphs = {}
	
	nu_i = oscillations.nu_mu
	nu_f = oscillations.nu_e
	
	osc = oscillations.Oscillations()
	
	for dcp in deltas:
		graphs[dcp] = ROOT.TGraph(n+1)
		
		osc.setDeltaCP( dcp * oscillations.units.degrees )
		
		for i in range(n+1):
			e = e_min + (i * e_step)
			osc.setE( e * oscillations.units.GeV )
			
			p   = 100.0 * osc.p(nu_i, nu_f)
			
			graphs[dcp].SetPoint(i, e, p)
	
	c = ROOT.TCanvas("c", "c", 800, 800)
	f = c.DrawFrame(e_min, 0.0, e_max, 10)
	
	l = ROOT.TLegend(0.69, 0.69, 0.89, 0.89)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Effect of #delta_{CP} on P(#nu_{#mu} #rightarrow #nu_{e})")
	f.GetXaxis().SetTitle("E_{#nu}  [ GeV ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{e} )  [ % ]   ")
	
	for dcp in deltas:
		graph = graphs[dcp]
		graph.SetLineColor(colourDelta(dcp))
		graph.SetLineStyle(styleDelta(dcp))
		graph.SetLineWidth(3)
		graph.Draw()
		
		l.AddEntry(graph, "#delta_{CP} = " + str(dcp) + "#circ", "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-dcp-e.png")



def plotDeltaCPSecond(e_range):
	"""Plot P(nu_mu -> nu_e) as a function of E for different values of delta_cp.
	The energy range (x-axis) is extended low enough to see the second oscillation peak.
	"""
	n = 300
	
	deltas = [0, 90, 180, 270]
	
	e_min = e_range[0]
	e_max = e_range[1]
	e_step = (e_max - e_min) / float(n)
	
	graphs = {}
	
	nu_i = oscillations.nu_mu
	nu_f = oscillations.nu_e
	
	osc = oscillations.Oscillations()
	
	for dcp in deltas:
		graphs[dcp] = ROOT.TGraph(n+1)
		
		osc.setDeltaCP( dcp * oscillations.units.degrees )
		
		for i in range(n+1):
			e = e_min + (i * e_step)
			osc.setE( e * oscillations.units.GeV )
			
			p   = 100.0 * osc.p(nu_i, nu_f)
			
			graphs[dcp].SetPoint(i, e, p)
	
	c = ROOT.TCanvas("c", "c", 1200, 800)
	f = c.DrawFrame(e_min, 0.0, e_max, 11)
	
	l = ROOT.TLegend(0.69, 0.69, 0.89, 0.89)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Effect of #delta_{CP} on P(#nu_{#mu} #rightarrow #nu_{e})")
	f.GetXaxis().SetTitle("E_{#nu}  [ GeV ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{e} )  [ % ]   ")
	
	for dcp in deltas:
		graph = graphs[dcp]
		graph.SetLineColor(colourDelta(dcp))
		graph.SetLineStyle(styleDelta(dcp))
		graph.SetLineWidth(3)
		graph.Draw()
		l.AddEntry(graph, "#delta_{CP} = " + str(dcp) + "#circ", "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-dcp-e2.png")



def plotDeltaCPAnti(e_range):
	"""Plot P(nu_mu -> nu_e) and the anti-neutrino equivalent with delta_cp = 0 and 90degrees"""
	n = 300
	
	deltas = [0, 90]
	
	e_min = e_range[0]
	e_max = e_range[1]
	e_step = (e_max - e_min) / float(n)
	
	graphs = {}
	
	nu_is = [oscillations.nu_mu, oscillations.nu_mu_bar]
	nu_fs = [oscillations.nu_e,  oscillations.nu_e_bar]
	
	osc = oscillations.Oscillations()
	
	for dcp in deltas:
		osc.setDeltaCP( dcp * oscillations.units.degrees )
		
		for nu_i,nu_f in zip(nu_is,nu_fs):
			graphs[ (dcp,nu_f) ] = ROOT.TGraph(n+1)
			
			for i in range(n+1):
				e = e_min + (i * e_step)
				osc.setE( e * oscillations.units.GeV )
				
				p   = 100.0 * osc.p(nu_i, nu_f)
				
				graphs[(dcp,nu_f)].SetPoint(i, e, p)
	
	c = ROOT.TCanvas("c", "c", 800, 800)
	f = c.DrawFrame(e_min, 0.0, e_max, 10)
	
	l = ROOT.TLegend(0.69, 0.69, 0.89, 0.89)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Effect of #delta_{CP} on P(#nu_{#mu} #rightarrow #nu_{e}) and  P(#bar{#nu}_{#mu} #rightarrow #bar{#nu}_{e})")
	f.GetXaxis().SetTitle("E_{#nu}  [ GeV ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{e} ) or P( #bar{#nu}_{#mu} #rightarrow #bar{nu}_{e} )  [ % ]   ")
	
	for nu_f in [oscillations.nu_e_bar, oscillations.nu_e]:
		for dcp in deltas:
			
			if( dcp == 0 and nu_f == oscillations.nu_e_bar ):
				continue # When delta_cp = 0, the two graphs are identical
			
			graph = graphs[(dcp,nu_f)]
			graph.SetLineColor(colourDelta(dcp))
			graph.SetLineStyle(style(nu_f))
			graph.SetLineWidth(3)
			graph.Draw()
			
			if( dcp == 0 ):
				l.AddEntry(graph, "#delta_{CP} = " + str(dcp) + "#circ", "L")
			else:
				l.AddEntry(graph, "#delta_{CP} = " + str(dcp) + "#circ " + name(nu_f), "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-dcp-anti.png")



def plotTheta23(e_range):
	"""Plot P(nu_mu -> nu_mu) as a function of E for different values of theta_23."""
	n = 300
	
	thetas = [35, 40, 45]
	
	e_min = e_range[0]
	e_max = e_range[1]
	e_step = (e_max - e_min) / float(n)
	
	graphs = {}
	
	nu_i = oscillations.nu_mu
	nu_f = oscillations.nu_mu
	
	osc = oscillations.Oscillations()
	
	for t in thetas:
		graphs[t] = ROOT.TGraph(n+1)
		
		osc.setTheta23( t * oscillations.units.degrees )
		
		for i in range(n+1):
			e = e_min + (i * e_step)
			osc.setE( e * oscillations.units.GeV )
			
			p   = 100.0 * osc.p(nu_i, nu_f)
			
			graphs[t].SetPoint(i, e, p)
	
	c = ROOT.TCanvas("c", "c", 800, 800)
	f = c.DrawFrame(e_min, 0.0, e_max, 100)
	
	l = ROOT.TLegend(0.69, 0.26, 0.89, 0.39)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Effect of #theta_{23} on  P(#nu_{#mu} #rightarrow #nu_{#mu})")
	f.GetXaxis().SetTitle("E_{#nu}  [ GeV ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{#mu} )  [ % ]   ")
	
	for t in thetas:
		graph = graphs[t]
		graph.SetLineColor(colour(nu_f))
		graph.SetLineStyle(styleTheta23(t))
		graph.SetLineWidth(3)
		graph.Draw()
		
		l.AddEntry(graph, "#theta_{23} = " + str(t) + "#circ", "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-t23.png")



def plotDM32(e_range):
	n = 300
	
	dms = [(2.0e-3), (2.3e-3), (2.6e-3)]
	
	e_min = e_range[0]
	e_max = e_range[1]
	e_step = (e_max - e_min) / float(n)
	
	graphs = {}
	
	nu_i = oscillations.nu_mu
	nu_f = oscillations.nu_mu
	
	osc = oscillations.Oscillations()
	
	for dm in dms:
		graphs[dm] = ROOT.TGraph(n+1)
		
		osc.setDeltaM32( dm * oscillations.units.eV2 )
		
		for i in range(n+1):
			e = e_min + (i * e_step)
			osc.setE( e * oscillations.units.GeV )
			
			p   = 100.0 * osc.p(nu_i, nu_f)
			
			graphs[dm].SetPoint(i, e, p)
	
	c = ROOT.TCanvas("c", "c", 800, 800)
	f = c.DrawFrame(e_min, 0.0, e_max, 100)
	
	l = ROOT.TLegend(0.59, 0.19, 0.89, 0.39)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Effect of #Deltam^{2}_{32} on P(#nu_{#mu} #rightarrow #nu_{#mu})")
	f.GetXaxis().SetTitle("E_{#nu}  [ GeV ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{#mu} )  [ % ]   ")
	
	for dm in dms:
		graph = graphs[dm]
		graph.SetLineColor(colour(nu_f))
		graph.SetLineStyle(styleDM32(dm))
		graph.SetLineWidth(3)
		graph.Draw()
		
		l.AddEntry(graph, "#Deltam^{2}_{32} = " + str(dm) + " eV^{2}", "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-dm32.png")



def plotHierarchy(e_range):
	"""Plot P(nu_mu -> nu_e) as a function of E for the two choices of mass hierarchy."""
	n = 300
	
	dms = [(2.3e-3), (-2.3e-3)] # (Delta m^2)_31 for normal and inverted hierarchy
	
	e_min = e_range[0]
	e_max = e_range[1]
	e_step = (e_max - e_min) / float(n)
	
	graphs = {}
	
	nu_i = oscillations.nu_mu
	nu_f = oscillations.nu_e
	
	osc = oscillations.Oscillations()
	
	for dm in dms:
		graphs[dm] = ROOT.TGraph(n+1)
		
		osc.setDeltaM32( dm * oscillations.units.eV2 )
		
		for i in range(n+1):
			e = e_min + (i * e_step)
			osc.setE( e * oscillations.units.GeV )
			
			p   = 100.0 * osc.p(nu_i, nu_f)
			
			graphs[dm].SetPoint(i, e, p)
	
	c = ROOT.TCanvas("c", "c", 800, 800)
	f = c.DrawFrame(e_min, 0.0, e_max, 10)
	
	l = ROOT.TLegend(0.49, 0.79, 0.89, 0.89)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Effect of Mass Hierarchy on  P(#nu_{#mu} #rightarrow #nu_{e})")
	f.GetXaxis().SetTitle("E_{#nu}  [ GeV ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{e} )  [ % ]   ")
	
	for dm in dms:
		graph = graphs[dm]
		graph.SetLineColor(colour(nu_f))
		graph.SetLineStyle(styleHierarchy(dm))
		graph.SetLineWidth(3)
		graph.Draw()
		
		if( dm > 0 ):
			l.AddEntry(graph, "Mass Hierarchy = Normal", "L")
		else:
			l.AddEntry(graph, "Mass Hierarchy = Inverted", "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-hierarchy.png")



def plotTheta13(e_range):
	"""Plot P(nu_mu -> nu_e) as a function of E for different values of theta_13."""
	n = 300
	
	thetas = [11, 9, 7]
	
	e_min = e_range[0]
	e_max = e_range[1]
	e_step = (e_max - e_min) / float(n)
	
	graphs = {}
	
	nu_i = oscillations.nu_mu
	nu_f = oscillations.nu_e
	
	osc = oscillations.Oscillations()
	
	for t in thetas:
		graphs[t] = ROOT.TGraph(n+1)
		
		osc.setTheta13( t * oscillations.units.degrees )
		
		for i in range(n+1):
			e = e_min + (i * e_step)
			osc.setE( e * oscillations.units.GeV )
			
			p   = 100.0 * osc.p(nu_i, nu_f)
			
			graphs[t].SetPoint(i, e, p)
	
	c = ROOT.TCanvas("c", "c", 800, 800)
	f = c.DrawFrame(e_min, 0.0, e_max, 10)
	
	l = ROOT.TLegend(0.69, 0.76, 0.89, 0.89)
	l.SetFillColor(ROOT.kWhite)
	l.SetBorderSize(0)
	
	f.SetTitle("Effect of #theta_{13} on  P(#nu_{#mu} #rightarrow #nu_{e})")
	f.GetXaxis().SetTitle("E_{#nu}  [ GeV ]")
	f.GetYaxis().SetTitle("P( #nu_{#mu} #rightarrow #nu_{e} )  [ % ]   ")
	
	for t in thetas:
		graph = graphs[t]
		graph.SetLineColor( colour(nu_f) )
		graph.SetLineStyle( styleTheta13(t) )
		graph.SetLineWidth(3)
		graph.Draw()
		
		l.AddEntry(graph, "#theta_{13} = " + str(t) + "#circ", "L")
	
	c.Update()
	
	l.Draw()
	c.Update()
	
	raw_input("continue?")
	c.SaveAs("figure-osc-t13.png")



def main():
	
	e_range = (0.3, 3.0)
	
	ROOT.gStyle.SetOptTitle(0)
	plotLOverE("short")
	plotLOverE("long")
	plotDeltaCP(e_range)
	plotDeltaCPSecond( (0.15,1.0) )
	plotDeltaCPAnti(e_range)
	plotTheta23(e_range)
	plotDM32(e_range)
	plotTheta13(e_range)
	plotHierarchy(e_range)
	
if __name__ == "__main__":
	main()
