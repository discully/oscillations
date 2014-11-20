# oscillations

Calculate neutrino oscillation probabilities easily

## Example

Here's a basic example of how to use the module:

```python
import oscillations

osc = oscillations.Oscillations()

osc.setTheta23( 90.0 * oscillations.units.degrees )
osc.setE( 1.0 * oscillations.units.GeV )
osc.setL( 3000.0 * oscillations.units.km )

print "P(nu_mu -> nu_e) = ", osc.p(oscillations.nu_mu, oscillations.nu_e)

print "Parameters used:"
print osc
```

Remember to always use the oscillations.units constants to convert to the
correct units whenever you call the set parameter methods of Oscillations.

## More Examples

There are multiple examples of the use of the module in plots.py, which
includes the code used to generate all the [oscillations plots in my PhD
thesis](http://danielscully.co.uk/thesis/neutrinos.html#section-oscillation-measurment).

To run plots.py, you will need to have PyROOT installed and loaded.
