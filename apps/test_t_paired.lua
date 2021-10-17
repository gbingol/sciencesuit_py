-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org


require( "iuplua" )

local std <const> =std
local iup <const> =iup



local function  dlgPairedttest()

	local lblSample1=iup.label{title="First sample range:"}
	local txtSample1=std.gui.gridtext()

	local lblSample2=iup.label{title="Second sample range:"}
	local txtSample2=std.gui.gridtext()

	local lblConfLevel=iup.label{title="Confidence level:"}
	local txtConfLevel=std.gui.numtext{min=0, max=100, value=95}


	local lblMu=iup.label{title="Assumed mean difference:"}
	local txtMu=iup.text{value=0,expand="HORIZONTAL"}
	

	local GridboxInput=iup.gridbox{lblSample1, txtSample1,
							lblSample2, txtSample2,
							lblConfLevel, txtConfLevel,
							lblMu, txtMu,
							numdiv=2, HOMOGENEOUSCOL="yes",CGAPLIN=10, CGAPCOL=30, orientation="HORIZONTAL"}
							
	
	local lblAlternative=iup.label{title="Alternative: "}
	local listAlternative = iup.list {"less than", "not equal", "greater than"; value = 2, DROPDOWN="yes"}
	
	local OutputFrame=std.gui.frmOutput()
	

	
	
	local BtnOK=iup.button{title="OK", size="30x12"}
	local BtnCancel=iup.button{title="Cancel",size="30x12"}

	local AllLayout=iup.vbox{GridboxInput,
							iup.hbox{lblAlternative,listAlternative;alignment = "ACENTER"},
							iup.space{size="x5"},
							OutputFrame , 
							iup.hbox{iup.fill{}, BtnOK, BtnCancel;alignment = "ACENTER"}}


	local icon=std.gui.makeicon(std.const.exedir.."apps/images/t_testpaired.png")

	local MainDlg = iup.dialog{AllLayout; title = "Paired t-test", margin="10x10", resize="yes", icon=icon}
	
	txtSample1:setOwner(MainDlg)
	txtSample2:setOwner(MainDlg)
	OutputFrame:setOwner(MainDlg)
	
	MainDlg:show()
	
	
	std.gui.PrepareAppForPreSelection({txt=txtSample1, row=1,col=1, nrows=-1, ncols=1}, {txt=txtSample2, row=1,col=2, nrows=-1, ncols=1})
	

	--main dialog
	
	function BtnCancel:action()
		MainDlg:hide()
	end
	
	
	
	local alternative="two.sided"
	function listAlternative:action(text, item, state)
		local alt={"less", "two.sided", "greater"}
		alternative=alt[item]
	end 


	function BtnOK:action()

		if(txtSample1.value=="" or txtSample2.value=="") then
			iup.Message("ERROR","A range must be selected for both sample 1 and 2.")
			return
		end

		
		local conflevel=tonumber(txtConfLevel.value)/100
		local Mu=tonumber(txtMu.value)
		 
		local rng1=std.Range.new(txtSample1.value)
		local rng2=std.Range.new(txtSample2.value)

		if(rng1:ncols()>1 or rng2:ncols()>1) then 
			iup.Message("ERROR","The selected range for Sample #1 and Sample #2 must be a single column.") 
			
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
		
		
		local pval,ttable=nil, nil
		local sample1, sample2=std.util.tovector(rng1), std.util.tovector(rng2)
		
		if(sample1==nil or #sample1<3) then 
			iup.Message("ERROR","Either there is none or less than 3 valid numeric data in the selected range of Sample #1.") 
			return 
		end
			
		if(sample2==nil or #sample1<3) then 
			iup.Message("ERROR","Either there is none or less than 3 valid numeric data in the selected range of Sample #2.")  
			return 
		end

		--note that if status==false then pval is the error message	
		status, pval,ttable=pcall(std.test_t,{x=sample1, y=sample2,alternative=alternative, mu=Mu, conflevel=conflevel, paired=true})
		
		if(not status)  then 
			iup.Message("ERROR",pval) 
			
			return
		end
		
		local Rows={"Sample 1","Sample 2","Difference"}
		for i=1,#Rows do
			WS[row+i][col]=Rows[i]
		end
		
		
		local Headers={"N", "Mean", "StDev", "SE Mean"}
		for j=1,#Headers do
			WS[row][col+j]=Headers[j]
		end

		
		local SE1, SE2=std.misc.tostring(ttable.s1/math.sqrt(ttable.n1)), std.misc.tostring(ttable.s2/math.sqrt(ttable.n2))
		
		local Values={
						{ttable.n1,std.misc.tostring(ttable.xaver), std.misc.tostring(ttable.s1), SE1},
						{ttable.n2, std.misc.tostring(ttable.yaver), std.misc.tostring(ttable.s2),SE2},
						{ttable.N, std.misc.tostring(ttable.mean), std.misc.tostring(ttable.stdev), std.misc.tostring(ttable.SE)}
					}
		
		for i=1,#Values do
			local vals=Values[i]
			
			for j=1, #vals do
				WS[row+i][col+j]=vals[j]
			end
		end
		
		row=row+#Values+2

		WS[row][col]="t critical" 
		WS[row][col+1]=std.misc.tostring(ttable.tcritical)
		row=row+1
		
		WS[row][col]="p-value" 
		WS[row][col+1]=std.misc.tostring(pval); 
		row=row+2
		
		WS[row][col]=tostring(conflevel*100).." Confidence Interval for "..alternative
		
		if(alternative=="less") then
			WS[row+1][col]="(-inf, "..std.misc.tostring(ttable.CI_upper)..")"
		elseif(alternative=="greater") then
			WS[row+1][col]="("..std.misc.tostring(ttable.CI_lower)..", inf)"
		else
			WS[row+1][col]="("..std.misc.tostring(ttable.CI_lower).." , "..std.misc.tostring(ttable.CI_upper)..")"
		end

	end 

end --MainDialog


std.app.TTestPaired=dlgPairedttest



