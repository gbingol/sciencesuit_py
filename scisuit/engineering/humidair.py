
import __SCISUIT as SCI




class psychrometry:

      """
      <p>A class to compute thermodynamic properties of humid-air. </p>

      <p><b>Example</b>:</p>
      >>p=psychrometry(P=100, Tdb=50, RH=60) <br>
      >>res=p.compute() <br>
      >>res.H # access to enthalpy
      
      """

     
      def __init__(self, **kwargs):
            self.m_Params = kwargs
            

      def compute(self):
            """
            returns PsychrometryResult class
            """
            res = SCI.psychrometry(**self.m_Params)
           
            return self.PsychrometryResult(res)


      
      class PsychrometryResult:
            """
            <p>Computation results of psychrometry class. </p>

            >>result = psy.compute() <br>
            >>result.P #access to pressure
            """

            def __init__(self, psyresult):
                  self.m_Results = psyresult

            def __str__(self) -> str:
                  retStr=""

                  if(len(self.m_Results)==0):
                        return retStr

                  retStr += "P=" + str(round(self.P, 2)) + " kPa" + "\n"

                  retStr += "Tdb=" + str(round(self.Tdb, 2)) + " C" + "\n"
                  
                  retStr += "Twb=" + str(round(self.Twb, 2)) + " C" + "\n"
                  
                  retStr += "Tdp=" + str(round(self.Tdp, 2)) +  " C" + "\n"
                  
                  retStr += "H=" + str(round(self.H, 2)) + " kJ/kg da" + "\n"
                  
                  retStr += "RH=" + str(round(self.RH, 2)) + " %" + "\n"
                  
                  retStr += "W=" + str(round(self.W, 4)) +  " kg/kg da" + "\n"
                  
                  retStr += "V=" + str(round(self.V,3)) +  " m3/kg da" + "\n"

                  return retStr


            
            @property
            def P(self): 
                  """Pressure in kPa"""
                  
                  return self.m_Results.get("P")


            @property
            def Tdb(self): 
                  """
                  Dry bulb temperature in Celcius
                  """
                  return self.m_Results.get("Tdb")

            @property
            def Twb(self): 
                  """
                  Wet bulb temperature in Celcius
                  """
                  return self.m_Results.get("Twb")

            @property
            def Tdp(self): 
                  """
                  Dew point temperature in Celcius
                  """
                  return self.m_Results.get("Tdp")

            @property
            def H(self):
                  """
                  Enthalpy in kJ/kg da
                  """ 
                  return self.m_Results.get("H")

            @property
            def RH(self): 
                  """
                  Relative Humidity in %
                  """
                  return self.m_Results.get("RH")

            @property
            def W(self):
                  """
                  Absolute Humidity in kg/kg da
                  """ 
                  return self.m_Results.get("W")

            @property
            def V(self): 
                  """
                  Specific volume in m3/kg da
                  """
                  return self.m_Results.get("V")

            @property
            def Pws(self):
                  """
                  water vapor pressure at saturation in kPa
                  """
                  return self.m_Results.get("Pws")

            @property
            def Pw(self):
                  """
                  water vapor pressure in kPa
                  """
                  return self.m_Results.get("Pw")

            @property
            def Ws(self):
                  """
                  Absolute humidity at saturation kg/kg da
                  """
                  return self.m_Results.get("Ws")
      

      