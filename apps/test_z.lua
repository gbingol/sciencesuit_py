-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org


require( "iuplua" )

local std <const> =std
local iup <const> =iup



local function dlgTestZ()

	
	local lblVar1=iup.label{title="Variable range:"}
	local txtVar1=std.gui.gridtext()

	local lblMu=iup.label{title="Test mean:"}
	local txtMu=std.gui.numtext()
	
	local lblSigma=iup.label{title="Sigma:"}
	local txtSigma=std.gui.numtext{min=0}

	local lblConfLevel=iup.label{title="Confidence level:"}
	local txtConfLevel=std.gui.numtext{min=0, max=100, value=95}


	local GridboxInput=iup.gridbox{lblVar1, txtVar1,
							lblMu, txtMu,
							lblSigma,txtSigma,
							lblConfLevel, txtConfLevel,
							numdiv=2, HOMOGENEOUSCOL="yes",CGAPLIN=10, CGAPCOL=30, orientation="HORIZONTAL"}
							
	
	local lblAlternative=iup.label{title="Alternative: "}
	local listAlternative = iup.list {"less than", "not equal", "greater than"; value = 2, DROPDOWN="yes"}


	local OutputFrame=std.gui.frmOutput()
	
	
	std.gui.PrepareAppForPreSelection({txt=txtVar1, row=1,col=1, nrows=-1, ncols=1})

	--main dialog
	
	local BtnOK=iup.button{title="OK", size="30x12"}
	local BtnCancel=iup.button{title="Cancel",size="30x12"}

	local AllLayout=iup.vbox{GridboxInput,
							iup.hbox{lblAlternative,listAlternative;alignment = "ACENTER"},
							iup.space{size="x5"},
							OutputFrame , 
							iup.hbox{iup.fill{}, BtnOK, BtnCancel;alignment = "ACENTER"}}


	local icon=std.gui.makeicon(std.const.exedir.."apps/images/test_z.png")
	
	local MainDlg = iup.dialog{AllLayout; title = "1-sample z-test", margin="10x10", resize="yes", icon=icon}
	
	txtVar1:setOwner(MainDlg)
	OutputFrame:setOwner(MainDlg)
	
	MainDlg:show()

	
	function BtnCancel:action()
		MainDlg:hide()
	end
	
	
	
	local alternative="two.sided"
	function listAlternative:action(text, item, state)
		local alt={"less", "two.sided", "greater"}
		alternative=alt[item]
	end 


	function BtnOK:action()

		if(txtVar1.value=="") then
			iup.Message("ERROR","A range must be selected for the variable.")
			
			return
		end
		
		if(txtMu.value=="") then
			iup.Message("ERROR","A value must be entered for the test mean.")
			
			return
		end

		if(txtSigma.value=="") then
			iup.Message("ERROR","A value must be entered for sigma.")
			return
		end

		
		local conflevel=tonumber(txtConfLevel.value)/100
		local Mu=tonumber(txtMu.value)

		local sigma=tonumber(txtSigma.value)
		
		 
		local rng1=std.Range.new(txtVar1.value)

		if(rng1:ncols()>1) then 
			iup.Message("ERROR","The selected range for Variable #1 must be a single column.") 
			return 
		end
			
		
		local OutputRng=OutputFrame:GetRange()
		
		local WS=nil
		local row, col=0, 0
		
		if(OutputRng~=nil)  then 
			row=OutputRng:coords().r 
			col=OutputRng:coords().c
			WS=OutputRng:parent() 
		else
			WS=std.appendworksheet()
			row=1
			col=1
		end
		
		
		local pval,ztable=nil, nil
		local v1, v2=nil
		
		
		local v1 =std.util.tovector(rng1) 
		if(v1==nil or #v1<3) then 
			iup.Message("ERROR","Either there is none or less than 3 valid numeric data in the selected range of Variable #1.") 
			return 
		end
			
		
		pval,ztable=std.test_z{x=v1,alternative=alternative,  mu=Mu, conflevel=conflevel, sd=sigma}
		
		local vals={{"N",ztable.N, false},
					{"Average", ztable.mean, true},
					{"stdev",ztable.stdev, true},
					{"SE Mean", ztable.SE, true},
					{"z",ztable.zcritical, true},
					{"p value", pval, true}}
					
			
		
		for i=1,#vals do
			WS[row][col+i-1]=vals [i][1]
			
			if(vals [i][3]) then
				WS[row+1][col+i-1]=std.misc.tostring(vals [i][2])
			else
				WS[row+1][col+i-1]=vals [i][2]
			end
			
		end

		row=row + rng1:ncols() + 2
		
		WS[row][col]=tostring(conflevel*100).." Confidence Interval for "..alternative
		
		if(alternative=="less") then
			WS[row+1][col]="(-inf, "..std.misc.tostring(ztable.CI_upper)..")"
			
		elseif(alternative=="greater") then
			WS[row+1][col]="("..std.misc.tostring(ztable.CI_lower)..", inf)"
			
		else
			WS[row+1][col]="("..std.misc.tostring(ztable.CI_lower).." , "..std.misc.tostring(ztable.CI_upper)..")"
		end

	end 
	
	

end --MainDialog


std.app.test_z=dlgTestZ



