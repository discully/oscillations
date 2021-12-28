# oscillations

Calculate neutrino oscillation probabilities easily.

## Installation

You can install oscillations from PyPI in the usual way...

```
pip install oscillations
```

## Example

Here's a basic example of how to use the module:

```python
import oscillations

osc = oscillations.Oscillations()

osc.setTheta23( 90.0 * oscillations.units.degrees )
osc.setE( 1.0 * oscillations.units.GeV )
osc.setL( 3000.0 * oscillations.units.km )

p = osc.p(oscillations.nu_mu, oscillations.nu_e)
print("P(nu_mu -> nu_e) = ", p)

print("Parameters used:")
print(osc)
```

Remember to always use the oscillations.units constants to convert to the
correct units whenever you call the set parameter methods of Oscillations.

## More Examples

There are multiple examples of the use of the module in plots.py, which
includes the code used to generate all the [oscillations plots in my PhD
thesis](https://danielscully.uk/thesis/neutrinos.html#section-oscillation-measurment).

To run plots.py, you will need to have PyROOT installed and loaded.

## Physics

The module uses the standard PMNS matrix calculation for neutrino oscillations
in a vacuum.

Neither matter effects nor sterile neutrinos are currently included.

## Unit Tests

Some basic unit testing is conducted in test.py, which uses Python's unittest module (PyUnit).
