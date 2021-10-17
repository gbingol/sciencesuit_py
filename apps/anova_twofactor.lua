-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org

require( "iuplua" ) 

local std <const> =std
local iup <const> =iup


local function ANOVATwoFactor()  
 
	local lblResponse=iup.label{title="Response:"}
	local txtResponse=std.gui.gridtext()
	
	local lblFactor1=iup.label{title="Factor 1:"}
	local txtFactor1=std.gui.gridtext()
	
	local lblFactor2=iup.label{title="Factor 2:"}
	local txtFactor2=std.gui.gridtext()
	
	local lblConfidence=iup.label{title="Confidence Level:"}
	local txtConfidence=std.gui.numtext{min=0, max=100, value=95}
	
	
	local Input=iup.gridbox{lblResponse, txtResponse,
								lblFactor1, txtFactor1,
								lblFactor2, txtFactor2,
								lblConfidence, txtConfidence,
								numdiv=2, HOMOGENEOUSCOL="yes",CGAPLIN=10, CGAPCOL=5, orientation="HORIZONTAL"}
	
	
	
	local OutputFrm=std.gui.frmOutput()
	
	local btnOK=iup.button{title="  OK  "}
	local btnCancel=iup.button{title="Cancel"}
	local btns=iup.hbox{btnOK,btnCancel}
	
	local vbox=iup.vbox{Input,OutputFrm,btns}
	
	
	local icon=std.gui.makeicon(std.const.exedir.."apps/images/anova2factor.png")
	
	local dlgAnova=iup.dialog{vbox; size="220x160", margin="10x10",title="Two-factor ANOVA", icon=icon}
	
	OutputFrm:setOwner(dlgAnova)
	txtResponse:setOwner(dlgAnova)
	txtFactor1:setOwner(dlgAnova)
	txtFactor2:setOwner(dlgAnova)
	
	dlgAnova:show()
	
	

	std.gui.PrepareAppForPreSelection(
										{txt=txtResponse, row=1,col=1, nrows=-1, ncols=1},
										{txt=txtFactor1, row=1,col=2, nrows=-1, ncols=1},
										{txt=txtFactor2, row=1,col=3, nrows=-1, ncols=1})
	
	
	
	
	local function OnCompute()
		local pvalue, AnovaTable=0 , {}
		
		if(txtResponse.value=="") then
			wx.wxMessageBox("Response range cannot be empty, a selection must be made")
			return
		end
            
		if(txtFactor1.value=="" or txtFactor2.value=="") then
			iup.Message("ERROR","Factor #1 or #2 range cannot be empty, a selection must be made")
			return
		end
            
		local Row, Col=0, 0
		
		local rngResponse=std.Range.new(txtResponse.value)
		local rngFactor1=std.Range.new(txtFactor1.value) 
		local rngFactor2=std.Range.new(txtFactor2.value) 
		
		
		if(rngResponse:ncols()>1 or rngFactor1:ncols()>1 or rngFactor2:ncols()>1) then 
			iup.Message("ERROR","Each of Response, Factor #1 and #2 must be in a single column.") 
			
			return 
		end


		local outRng=OutputFrm:GetRange()
		
		local WS=nil
		
		if(outRng~=nil)  then 
			Row=outRng:coords().r 
			Col=outRng:coords().c
			WS=outRng:parent() 
			
		else
		
			WS=std.appendworksheet()
			Row=1
			Col=1
		end


		local vecResponse, NonNum=std.util.tovector(rngResponse)
		if(vecResponse==nil or NonNum>0) then 
			iup.Message("ERROR","Response range contains non-numeric data.") 
			
			return 
		end
		
	
		if((rngFactor1:nrows() - rngFactor2:nrows())~=0 ) then 
			iup.Message("ERROR","Factor 1 and 2 must contain equal number of entries") 
			return 
		end
		
		if((rngFactor1:nrows() - rngResponse:nrows())~=0 ) then 
			iup.Message("ERROR","Factors and response must contain equal number of entries") 
			return 
		end

		local pvalue, AnovaTable=std.anova2(vecResponse ,std.util.tovector(rngFactor1), std.util.tovector(rngFactor2) )
		
		if(pvalue==nil) then 
			iup.Message("ERROR",AnovaTable) 
			return 
		end 
		
		--Prepare headers for output 
		local Headers={"Source", "DF", "SS", "MS", "F-value", "p-value"}
		for i=1,#Headers do
			WS[Row][Col+i-1]=Headers[i]
		end

		
		Row=Row+1
		
		Headers={"Factor #1","Factor #2",  "Interaction", "Error","","", "Total"}
		for i=1,#Headers do
			WS[Row+i-1][Col]=Headers[i]
		end
		
		
		--Write the calculated values

		local Fact1={AnovaTable.DFFact1, AnovaTable.SSFact1, AnovaTable.MSFact1, AnovaTable.FvalFact1, pvalue(1)}
		local Fact2={AnovaTable.DFFact2, AnovaTable.SSFact2, AnovaTable.MSFact2, AnovaTable.FvalFact2, pvalue(2)}
		local Interact={AnovaTable.DFinteract, AnovaTable.SSinteract, AnovaTable.MSinteract, AnovaTable.Fvalinteract, pvalue(3)}
		local Err={AnovaTable.DFError, AnovaTable.SSError, AnovaTable.MSError}
		
		local Vals={Fact1,Fact2, Interact,  Err}
		
		for i=1, #Vals do
			local tbl=Vals[i]
			
			for j=1, #tbl do
				local val=tonumber(tbl[j])
				
				if(val<1) then
					WS[Row][Col+j]=string.format("%.4f",val)
				else
					WS[Row][Col+j]=string.format("%.2f",val)
				end
			end
			
			Row=Row+1
		end
		
		--Total

		Row=Row+2
		local SStotal= AnovaTable.SSFact1+ AnovaTable.SSFact2+AnovaTable.SSinteract+ AnovaTable.SSError
		local DFtotal=AnovaTable.DFFact1+AnovaTable.DFFact2+AnovaTable.DFinteract+AnovaTable.DFError
		WS[Row][Col+1]=DFtotal
		WS[Row][Col+2]=string.format("%.2f",SStotal)

	end

	function btnOK:action()
		local status, err=pcall(OnCompute)
		
		if(not status) then 
			iup.Message("ERROR",err) 
		end
	end 
	
	function btnCancel:action()
		dlgAnova:hide()
	end

end

std.app.ANOVATwoFactor=ANOVATwoFactor
