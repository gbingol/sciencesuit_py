from scisuit.stats import quantile

def median(x, sorted=False):
      return quantile(x, 0.5, sorted)