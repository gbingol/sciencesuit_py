-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org


require( "iuplua" )

local std <const> =std
local iup <const> =iup



local function  dlgTwoSample2Test()


	local lblVar1=iup.label{title="Variable 1 range:"}
	local txtVar1=std.gui.gridtext()

	local lblVar2=iup.label{title="Variable 2 range:"}
	local txtVar2=std.gui.gridtext()

	local lblConfLevel=iup.label{title="Confidence level:"}
	local txtConfLevel=std.gui.numtext{min=0, max=100, value=95}


	local lblDiff=iup.label{title="Assumed mean difference:"}
	local txtDiff=iup.text{value=0,expand="HORIZONTAL"}
	
	local lblAlternative=iup.label{title="Alternative: "}
	local listAlternative = iup.list {"less than", "not equal", "greater than"; value = 2, DROPDOWN="yes"}
	
	local chkEqualVar=iup.toggle{title = "Assume Equal Variances", tip="You can run F-test to see if the variances are equal or not"}
	
	local chkInOneCol=iup.toggle{title = "Samples in one column"}
	
	chkInOneCol.tip="If you have data pairs  in the format of (Subscripts, data) such as (A,10), (B,20) and \n subscripts are stacked in 1 column and data stacked in another column select this option"
	

	local GridboxInput=iup.gridbox{lblVar1, txtVar1,
							lblVar2, txtVar2,
							lblConfLevel, txtConfLevel,
							lblDiff, txtDiff,
							lblAlternative,listAlternative,
							chkInOneCol,chkEqualVar,
							numdiv=2, HOMOGENEOUSCOL="yes",CGAPLIN=10, CGAPCOL=20, orientation="HORIZONTAL"}
							

	local OutputFrame=std.gui.frmOutput()
	

	--main dialog
	
	local BtnOK=iup.button{title="OK", size="30x12"}
	local BtnCancel=iup.button{title="Cancel",size="30x12"}

	local AllLayout=iup.vbox{GridboxInput,
							iup.space{size="x5"},
							OutputFrame , 
							iup.hbox{iup.fill{}, BtnOK, BtnCancel;alignment = "ACENTER"}}


	local icon=std.gui.makeicon(std.const.exedir.."apps/images/t_test2sample.png")

	local MainDlg = iup.dialog{AllLayout; title = "Two-sample t-test", margin="10x10", size="225x195", resize="yes", icon=icon}
	
	txtVar1:setOwner(MainDlg)
	txtVar2:setOwner(MainDlg)
	OutputFrame:setOwner(MainDlg)
	
	MainDlg:show()
	
	iup.Refresh(MainDlg)
	
	
	std.gui.PrepareAppForPreSelection({txt=txtVar1, row=1,col=1, nrows=-1, ncols=1}, {txt=txtVar2, row=1,col=2, nrows=-1, ncols=1})

	
	function BtnCancel:action()
		MainDlg:hide()
	end
	
	
	local SamplesInTwoCol=true
	
	function chkInOneCol:action(value)
		if(value==1) then
			lblVar1.title="Samples range:"
			lblVar2.title="Subscripts range:"
		
			SamplesInTwoCol=false
		else
			lblVar1.title="Variable 1 range:"
			lblVar2.title="Variable 2 range:"
			
			SamplesInTwoCol=true
		end
	end
	
	local alternative="two.sided"
	function listAlternative:action(text, item, state)
		local alt={"less", "two.sided", "greater"}
		alternative=alt[item]
	end 




	local function PerformTTest2Sample()

		assert(txtVar1.value~="" and txtVar2.value~="","A range must be selected for both variable 1 and 2.")
			
		
		local conflevel=tonumber(txtConfLevel.value)/100
		local Mu=tonumber(txtDiff.value)
		local varequal=false
		
		if(chkEqualVar.value=="ON") then
			varequal=true
		end
		 
		local rng1=std.Range.new(txtVar1.value)
		local rng2=std.Range.new( txtVar2.value)

		
		assert(rng1:ncols()==1 and rng2:ncols()==1,"The selected range for Variable #1 and Variable #2 must be a single column.") 
		
		
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
		local v1, v2=nil, nil
		
		
		if(SamplesInTwoCol) then
			v1 , v2=std.util.tovector(rng1) , std.util.tovector(rng2)
			
			assert(v1~=nil and #v1>=3, "Either there is none or less than 3 valid numeric data in the selected range of Variable #1.") 
			assert(v2~=nil and #v2>=3, "Either there is none or less than 3 valid numeric data in the selected range of Variable #2.") 	
			
		end
		
		
		
		local uniquesubscripts=nil
		if (not SamplesInTwoCol) then
		
			local samples , subscripts=std.util.tovector(rng1) , std.util.toarray(rng2)
			
			uniquesubscripts=subscripts:clone()
			uniquesubscripts:unique()
			
			assert(#uniquesubscripts==2, "Number of codes pertaining to factors in the subscripts range must be exactly 2")  
			
			
			v1, v2=std.Vector.new(0), std.Vector.new(0)
			
			for i=1,  #subscripts do
				if(subscripts[i]==uniquesubscripts[1]) then
					v1:push_back(samples(i))
				
				elseif(subscripts[i]==uniquesubscripts[2]) then
					v2:push_back(samples(i))
				end
			end
	
		end 
			
			
			
			
		pval,ttable=std.test_t{x=v1,y=v2,alternative=alternative, varequal=varequal, mu=Mu, conflevel=conflevel, paired=false}
		
		
		
		--Outputting the results
		
		local header1, header2="Variable 1", "Variable 2"
		
		if(SamplesInTwoCol) then
			if(tonumber(rng1(1,1))==nil and tonumber(rng2(1,1))==nil) then
				header1=rng1(1,1)
				header2=rng2(1,1)
			end
		
		elseif(not SamplesInTwoCol) then
			header1=uniquesubscripts[1]
			header2=uniquesubscripts[2]
		end
		

		WS[row][col+1]=header1;   WS[row][col+2]=header2 ; 
		row=row+1
		
		WS[row][col]="Observation"; WS[row][col+1]=ttable.n1;WS[row][col+2]=ttable.n2; 
		row=row+1
		
		WS[row][col]="Mean"; WS[row][col+1]=std.misc.tostring(ttable.xaver); WS[row][col+2]=std.misc.tostring(ttable.yaver);
		row=row+1
		
		WS[row][col]="Standard Deviation"; WS[row][col+1]=std.misc.tostring(ttable.s1);WS[row][col+2]=std.misc.tostring(ttable.s2); 
		row=row+1

		row=row+1--Leave one space so that following analysis does not seem to belong variable 1
		if(varequal) then 
			WS[row][col]="Pooled variance" 
			WS[row][col+1]=std.misc.tostring(ttable.sp)
			row=row+1
		end

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
	
	
	function BtnOK:action()
		local status, err=pcall(PerformTTest2Sample)
		
		if(status==false) then
			iup.Message("ERROR", err)
			
			return
		end
	end
	

end --MainDialog


std.app.TTest2Sample=dlgTwoSample2Test



