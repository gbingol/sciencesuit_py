-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org

require( "iuplua" ) 


local std <const> =std
local iup <const> =iup


local function ASSERT(exp, msg)

	if(not exp) then
		error(msg, 0)
	end

end



local function ANOVASingleFactor()
	
	local lblResponses=iup.label{title="Response Variables Range:"} 
	local txtResponses=std.gui.gridtext()
	
	local lblFactors=iup.label{title="Factors:", active="NO"}
	local txtFactors=std.gui.gridtext()
	
	local lblConfidence=iup.label{title="Confidence Level:"}
	local txtConfidence=std.gui.numtext{min=0, max=100, value=95}
	
	txtFactors.active="NO"
	
	local chkStacked = iup.toggle{title = "My data is stacked"}
	
	local chkTukeyTest = iup.toggle{title = "Tukey's Test", value="ON"}
	
	local Input=iup.gridbox{lblResponses, txtResponses,
								lblFactors, txtFactors,
								lblConfidence, txtConfidence,
								chkStacked, iup.fill{},
								chkTukeyTest, iup.fill{},
								numdiv=2, HOMOGENEOUSCOL="yes",CGAPLIN=10, CGAPCOL=5, orientation="HORIZONTAL"}
	
	
	
	local OutputFrm=std.gui.frmOutput()
	
	local btnOK=iup.button{title="  OK  "}
	local btnCancel=iup.button{title="Cancel"}
	local btns=iup.hbox{btnOK,btnCancel}
	
	local vbox=iup.vbox{Input,OutputFrm,btns}
	
	
	local icon=std.gui.makeicon(std.const.exedir.."apps/images/anovasinglefactor.png")
	
	local dlgAnova=iup.dialog{vbox; margin="10x10",title="One-Way ANOVA", icon=icon}
	
	OutputFrm:setOwner(dlgAnova)
	txtResponses:setOwner(dlgAnova)
	txtFactors:setOwner(dlgAnova)
	
	dlgAnova:show()
	
	
	std.gui.PrepareAppForPreSelection({txt=txtResponses, row=1,col=1, nrows=-1, ncols=-1})
	
	
	function btnCancel:action()
		dlgAnova:hide()
	end
	
	
	
	local IsStacked=false
	
	
	function chkStacked:action( state)
		if(state==1) then
			IsStacked=true
			
			lblFactors.active="YES"
			txtFactors.active="YES"
		
			lblResponses.title="Response Variable Range:"
		
		elseif(state==0) then
			IsStacked=false
			
			lblFactors.active="NO"
			txtFactors.active="NO"
			
			lblResponses.title="Response Variables Range:"
		end
		
	end
	

	
	
	local function OnCompute()
		
		ASSERT(txtResponses.value~="","Response range cannot be empty, a selection must be made.")
		
		if(IsStacked) then
			ASSERT(txtFactors.value=="", "ERROR","Factors range cannot be empty, a selection must be made")
		end
			
		
		local Alpha=(100-tonumber(txtConfidence.value))/100
            
		local Row, Col=0, 0
		local WS=nil 
		
		local rngResponses=std.Range.new(txtResponses.value)
		
		local outRng=OutputFrm:GetRange()
		
		if(outRng~=nil)  then 
			Row=outRng:coords().r 
			Col=outRng:coords().c
			WS=outRng:parent() 
		else
			WS=std.appendworksheet()
			Row=1
			Col=1
		end
           
           
		local pvalue, AnovaTable=0 , {}
		
		if(not IsStacked) then 
			local tbl={}
			
			for i=1,rngResponses:ncols() do
				tbl[i]=std.util.tovector(rngResponses:col(i))
			end
			
			pvalue, AnovaTable= std.anova(table.unpack(tbl)) 
		end
		
		
		if(IsStacked) then
			rngFactors=std.Range.new(txtFactors.value)
			
			ASSERT(rngFactors:ncols()==1 and rngResponses:ncols()==1, "The factors or the responses must be in a single column") 
			
			local responses, NonNum=std.util.tovector(rngResponses:col(1))
			
			ASSERT(responses~=nil and NonNum==0, "There is none-numeric data in the selected response range") 
				
			
			local factors=std.util.tovector(rngFactors:col(1))
			local uniquefactors=factors[{}]
			uniquefactors:unique()
			
			
			local tblVecFactors={}
			for i=1, #uniquefactors do 
				tblVecFactors[i]=std.Vector.new(0) 
			end
			
			for i=1,  #factors do
				local j=0

				repeat
					j=j+1
				until uniquefactors(j)==factors(i)
				
				tblVecFactors[j]:push_back(responses(i))
			end 
			
			pvalue, AnovaTable=std.anova(table.unpack(tblVecFactors)) 
		end --if(DataIsStacked)
             
             
		--Prepare headers for output 
		local Headers_Col={ "Source", "df","SS", "MS","F", "P"}
		for j=1,#Headers_Col do
			WS[Row][Col+j-1]=Headers_Col[j]
		end
		
		local Headers_Row={"Treatment",  "Error","Total"}
		for i=1,#Headers_Row do
			WS[Row+i][Col]=Headers_Row[i]
		end


		Row=Row+1

		local OutputTbl={{AnovaTable.DF_Treatment, AnovaTable.SS_Treatment, AnovaTable.MS_Treatment, AnovaTable.Fvalue , AnovaTable.pvalue},
				{AnovaTable.DF_Error, AnovaTable.SS_Error, AnovaTable.MS_Error},
				{AnovaTable.DF_Total, AnovaTable.SS_Total}}
				
		
		for i=1,#OutputTbl do
			
			local Entry=OutputTbl[i]
			
			for j=1,#Entry do
				WS[Row][Col+j]=std.misc.tostring(Entry[j])
			end
			
			Row=Row+1
		end
		
		
		if(chkTukeyTest.value=="ON") then
			Row=Row+3
			WS[Row][Col]="Tukey's Test"
			
			Row=Row+2
			
			local TukeyTable=std.anova.tukey(AnovaTable, Alpha)
			
			local Headers={"Pairwise Diff", "Difference (i-j)", "Tukey Interval", "Conclusion"}
			
			Col=1
			for j=1,#Headers do
				WS[Row][Col+j-1]=Headers[j]
			end

			for i=1,#TukeyTable do
				WS[Row+i][Col]=tostring(TukeyTable[i].a).."-"..tostring(TukeyTable[i].b)
				WS[Row+i][Col+1]=std.misc.tostring(TukeyTable[i].MeanValueDiff)
				
				local CILow=std.misc.tostring(TukeyTable[i].CILow)
				local CIHigh=std.misc.tostring(TukeyTable[i].CIHigh)
				
				WS[Row+i][Col+2]=CILow.." , "..CIHigh
				
				if(TukeyTable[i].CILow *TukeyTable[i].CIHigh<0) then
					WS[Row+i][Col+3]="NS"
				else
					WS[Row+i][Col+3]="Reject"
				end

			end

		end --if(chkTukeyTest
	
		
	end --function OnCompute




	function btnOK:action()
		local status, err=pcall(OnCompute)
		
		if(not status)  then 
			iup.Message("ERROR",err) 
		end
	
	end

      
end


std.app.ANOVASingleFactor=ANOVASingleFactor

