from __SCISUIT import STATS as stat

#binomial
dbinom = stat.dbinom
pbinom = stat.pbinom
qbinom = stat.qbinom
rbinom = stat.rbinom


#chisq
dchisq = stat.dchisq
pchisq = stat.pchisq
qchisq = stat.qchisq
rchisq = stat.rchisq


#F-dist
df = stat.df
pf = stat.pf
qf = stat.qf
rf = stat.rf


#normal dist
dnorm = stat.dnorm
pnorm = stat.pnorm
qnorm = stat.qnorm
rnorm = stat.rnorm


#Poisson dist
dpois = stat.dpois
ppois = stat.ppois
qpois = stat.qpois
rpois = stat.rpois


#t-dist
dt = stat.dt
pt = stat.pt
qt = stat.qt
rt = stat.rt


#unif dist
dunif = stat.dunif
punif = stat.punif
qunif = stat.qunif
runif = stat.runif


#sign rank dist
dsignrank = stat.dsignrank
psignrank = stat.psignrank
qsignrank = stat.qsignrank
rsignrank = stat.rsignrank



cor = stat.cor
cov = stat.cov
test_norm_ad = stat.test_norm_ad



#as of this point import modules which might depend on the core stat

from .mean import mean
from .kurt import kurt
from .var import var, stdev
from .linregress import linregress