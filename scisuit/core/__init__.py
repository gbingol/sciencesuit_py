import math

from __SCISUIT import CORE as __scicore

Array = __scicore.Array
Matrix = __scicore.Matrix
Polynomial = __scicore.Polynomial 
Vector = __scicore.Vector

arange =  __scicore.arange
det = __scicore.det
diag = __scicore.diag
diff = __scicore.diff
eig = __scicore.eig
eigvals = __scicore.eigvals
expfit = __scicore.expfit
eye = __scicore.eye
inv = __scicore.inv
linspace = __scicore.linspace
logfit = __scicore.logfit
lu = __scicore.lu
meshgrid = __scicore.meshgrid
null = __scicore.null
polyfit = __scicore.polyfit
powfit = __scicore.powfit
qr = __scicore.qr
rank = __scicore.rank
svd = __scicore.svd
trans = __scicore.trans



from .mathfuncs import Copy_CallObjectMethod

from .cumsum import cumsum

from .minmax import minmax

from .sum import sum

def abs(entry):     
      return Copy_CallObjectMethod(entry, "abs")


def acos(entry):     
      return Copy_CallObjectMethod(entry, "acos")


def asin(entry):     
      return Copy_CallObjectMethod(entry, "asin")


def atan(entry):     
      return Copy_CallObjectMethod(entry, "atan")


def ceil(entry):     
      return Copy_CallObjectMethod(entry, "ceil")


def cos(entry):     
      return Copy_CallObjectMethod(entry, "cos")


def cosh(entry):     
      return Copy_CallObjectMethod(entry, "cosh")


def exp(entry):     
      return Copy_CallObjectMethod(entry, "exp")


def floor(entry):     
      return Copy_CallObjectMethod(entry, "floor")


def log(entry, base):     
      return Copy_CallObjectMethod(entry, "log", base)


def ln(entry):     
      return Copy_CallObjectMethod(entry, "log", math.exp(1.0))


def log10(entry):     
      return Copy_CallObjectMethod(entry, "log", 10.0)


def pow(entry, exponent):     
      return Copy_CallObjectMethod(entry, "pow", exponent)


def sqrt(entry):     
      return Copy_CallObjectMethod(entry, "sqrt")


def sin(entry):     
      return Copy_CallObjectMethod(entry, "sin")


def sinh(entry):     
      return Copy_CallObjectMethod(entry, "sinh")


def tan(entry):     
      return Copy_CallObjectMethod(entry, "tan")


def tanh(entry):     
      return Copy_CallObjectMethod(entry, "tanh")