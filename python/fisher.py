from scipy.stats import fisher_exact
def fisher(a, b, overlap):
	universe = 22000
	_, p = fisher_exact([[overlap,a], [b, universe]])
	return p

print fisher(269,604,168)
print fisher(325,124,23)
print fisher(254,414,77)
print fisher(395,578,71)
print fisher(155,145,40)
print fisher(145,96,19)
print fisher(290,604,160)
print fisher(181,578,94)
print fisher(365,578,82)
print fisher(340,74,5)
print fisher(545,105,35)
print fisher(104,127,7)
print fisher(674,127,27)
print fisher(970,127,29)
print fisher(361,234,62)
print fisher(145,234,40)
