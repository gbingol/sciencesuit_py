from .fluid import Fluid

import sqlite3 as sql

class Refrigerant(Fluid):
    """
    Base class thermodynamic properties of refrigerants
    """

    def __init__(self) -> None:
        super().__init__()
    


class SaturatedRefrigerant(Refrigerant):
    """
    FluidName: Name of the fluid
    PropertyName: Any property (P, T, vf, vg, sf, sg, hf, hg)
    Value: A numeric value of the property
    """

    s_DataBasePath = "/datafiles/Fluids.db"

    def __init__(self, FluidName:str, PropertyName:str, Value:float) -> None:
        super().__init__()
        
        self.m_FluidName = FluidName
        self.m_PropertyName = PropertyName
        self.m_Value = Value

        self.m_Connection = sql.connect(self.s_DataBasePath)

        cursor = self.m_Connection.cursor()

        #Check if the parameter FluidName is valid
        PlaceHolderTxt = FluidName
        QueryString = "SELECT Type FROM MAINTABLE where TYPE=?"
        rows = cursor.execute(QueryString , (PlaceHolderTxt,)).fetchall()

        if(len(rows) == 0):
            raise Exception(FluidName + " does not exist")
