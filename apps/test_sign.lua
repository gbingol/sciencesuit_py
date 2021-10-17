-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org


require( "iuplua" )


local std <const> =std
local iup <const> =iup


local function  dlgSignTest()

	
	local lblVar1=iup.label{title="Variable range:"}
	local txtVar1=std.gui.gridtext()

	local lblVar2=iup.label{title="Second sample range:", active="NO"}
	local txtVar2=std.gui.gridtext()
	txtVar2.active="NO"

	local lblConfLevel=iup.label{title="Confidence level:"}
	local txtConfLevel=std.gui.numtext{min=0, max=100, value=95}


	local lblAssumedMedian=iup.label{title="Test median:"}
	local txtAssumedMedian=iup.text{value=0,expand="HORIZONTAL"}
	

	local GridboxInput=iup.gridbox{lblVar1, txtVar1,
							lblVar2, txtVar2,
							lblConfLevel, txtConfLevel,
							lblAssumedMedian, txtAssumedMedian,
							numdiv=2, HOMOGENEOUSCOL="yes",CGAPLIN=10, CGAPCOL=30,orientation="HORIZONTAL"}
							
	
	local lblAlternative=iup.label{title="Alternative: "}
	local listAlternative = iup.list {"less than", "not equal", "greater than"; value = 2, DROPDOWN="yes"}
	
	local chkPairedTest=iup.toggle{title = "Paired test", value="OFF"}


	local OutputFrame=std.gui.frmOutput()
	

	--main dialog
	
	local BtnOK=iup.button{title="OK", size="30x12"}
	local BtnCancel=iup.button{title="Cancel",size="30x12"}

	local AllLayout=iup.vbox{	GridboxInput,
							iup.hbox{lblAlternative,listAlternative;alignment = "ACENTER"},
							iup.space{size="x5"},
							chkPairedTest,
							iup.space{size="x5"},
							OutputFrame , 
							iup.hbox{iup.fill{}, BtnOK, BtnCancel;alignment = "ACENTER"}}

	
	local icon=std.gui.makeicon(std.const.exedir.."apps/images/test_sign.png")


	local MainDlg = iup.dialog{AllLayout; title = "Sign test", margin="10x10", size="220x190", resize="yes", icon=icon}
	
	txtVar1:setOwner(MainDlg)
	txtVar2:setOwner(MainDlg)
	OutputFrame:setOwner(MainDlg)
	
	
	MainDlg:show()
	
	
	
	std.gui.PrepareAppForPreSelection({txt=txtVar1, row=1,col=1, nrows=-1, ncols=1})

	
	function BtnCancel:action()
		MainDlg:hide()
	end
	
	
	
	local alternative="two.sided"
	local AlternativeSign="<>"
	
	function listAlternative:action(text, item, state)
		alternative=({"less", "two.sided", "greater"})[item]
		
		AlternativeSign=({"<", "<>", ">"})[item]
	end 


	local IsPaired=false
	
	function chkPairedTest:action(v)
		if(v==1) then
			lblVar1.title="First sample range:"
			
			lblVar2.active="YES"
			txtVar2.active="YES"
			
			IsPaired=true
		
		elseif(v==0) then
			lblVar1.title="Variable range:"
			
			lblVar2.active="NO"
			txtVar2.active="NO"
			
			IsPaired=false
		end
		
		iup.Refresh(MainDlg)

	end  


	function BtnOK:action()

		if(txtVar1.value=="" ) then
			iup.Message("ERROR","A range must be selected for variable 1.")
			
			return
		end

		
		local rng1, rng2=std.Range.new(txtVar1.value), nil
		
		if(rng1:ncols()>1 ) then 
			iup.Message("ERROR","The selected range for Variable #1 must be a single column.") 
			
			return 
		end
		 
		 
		
		local xvec, yvec=std.util.tovector(rng1), nil
		
		 
		if(IsPaired) then
			
			if(txtVar2.value=="") then
				iup.Message("ERROR","If paired option is selected a range must be selected for variable 2.")
				
				return
			end


			rng2=std.Range.new(txtVar2.value)
			
			if(rng2:ncols()>1) then 
				iup.Message("ERROR","The selected range for Variable #2 must be a single column.") 
				
				return 
			end


			yvec=std.util.tovector(rng2)
			
			if(#xvec~=#yvec) then
				iup.Message("ERROR","If paired test is selected, then both variables must be of same size.")
				
				return
			end

		end --if(IsPaired)


		local conflevel=tonumber(txtConfLevel.value)/100
		
		local AssumedMedian=tonumber(txtAssumedMedian.value)
		



		local OutputRng=OutputFrame:GetRange()
		
		local WS=nil
		local row, col=1, 1
		
		if(OutputRng~=nil)  then 
			WS=OutputRng:parent()
			
			row=OutputRng:coords().r 
			col=OutputRng:coords().c
		else
			WS=std.appendworksheet()
		end
		
		
		
		
		local Median=nil
		
		local pvalue, retTable=nil, nil
		
		if(not IsPaired) then
			Median=std.median(xvec)
			
			pvalue, retTable=std.test_sign{x=xvec, md=AssumedMedian, alternative=alternative, conflevel=conflevel}
			
		else
			Median=std.median(xvec-yvec)
			
			pvalue, retTable=std.test_sign{x=xvec, y=yvec, md=AssumedMedian, alternative=alternative, conflevel=conflevel}
		end
			
			
			
		--print output
		local GenInfo={{"N",std.size(xvec)}, 
						{"Number>"..tostring(AssumedMedian), retTable.ngreater},
						{"Number="..tostring(AssumedMedian), retTable.nequal},
						{"",""},
						{"Median", Median}}
						
		for i=1,#GenInfo do
			WS[row+i][col]={value=GenInfo[i][1], style="italic"}
			WS[row+i][col+1]=GenInfo[i][2]
		end
			
		row=row+#GenInfo+2
		
		WS[row][col]="Median="..tostring(AssumedMedian).." vs Median"..AlternativeSign..tostring(AssumedMedian)
		
		row=row+1
		
		WS[row][col]={value="p-value", style="italic"}
		WS[row][col+1]=pvalue
		
		row=row+2
		
		WS[row][col]={value="CONFIDENCE INTERVALS", fgcolor="255 0 0"}
		
		local CI={{"Lower Achieved", retTable.lower.prob, retTable.lower.CILow, retTable.lower.CIHigh},
				{"Interpolated", retTable.interpolated.prob, retTable.interpolated.CILow, retTable.interpolated.CIHigh},
				{"Upper Achieved", retTable.upper.prob, retTable.upper.CILow, retTable.upper.CIHigh}}
				
		for i=1, #CI do
			local tbl=CI[i]
			
			for j=1, #tbl do
				local entry=tbl[j]
				
				if(type(entry)=="number") then
					WS[row+i][col+j-1]=std.misc.tostring(entry)
				else
					WS[row+i][col+j-1]={value=entry, style="italic"}
				end

			end--j

		end--i


	end --function BtnOK:action()
	
	

end --MainDialog


std.app.SignTest=dlgSignTest



