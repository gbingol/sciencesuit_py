import math

from SCISUITSYSTEM import Array, Matrix, Polynomial, Vector

from .mathfuncs import Copy_CallObjectMethod

from .cumsum import cumsum

from .minmax import minmax


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