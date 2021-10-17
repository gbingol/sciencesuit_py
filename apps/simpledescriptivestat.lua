-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org


require( "iuplua" )


local std <const> =std
local iup <const> =iup


local function  DescriptiveStat()

	
	local SampleLayout=iup.radio{iup.vbox{InOneCol, InTwoCol}, value=InTwoCol}

	local lblInput=iup.label{title="Input:"}
	local txtInput=std.gui.gridtext()

	local InputInCols = iup.toggle{title="Treat columns separately"}

	local Inputs=iup.vbox{alignment="ALEFT", iup.hbox{lblInput, txtInput}, InputInCols}
							
	
	local chkAll=iup.toggle{title="All"}
	local chkMean = iup.toggle{title= "Mean"}
	local chkSE =iup.toggle{title= "Standard Error"}
	local chkMedian = iup.toggle{title="Median"}
	local chkMode = iup.toggle{title="Mode"}
	
	local chkSD = iup.toggle{title="Standard Deviation"}
	local chkSampleVar = iup.toggle{title="Sample Variance"}
	local chkRange = iup.toggle{title="Range"}
	local chkMin = iup.toggle{title="Minimum"}
	local chkMaximum = iup.toggle{title="Maximum"}

	local chkSum = iup.toggle{title="Sum"}
	local chkCount = iup.toggle{title="Count"}
	local chkSkew = iup.toggle{title="Skewness"}
	local chkKurtosis = iup.toggle{title="Kurtosis"}

	local col1=iup.vbox{chkAll, chkMean,chkSE,chkMedian,chkMode}
	local col2=iup.vbox{chkSD,chkSampleVar,chkRange,chkMin,chkMaximum}
	local col3=iup.vbox{chkSum,chkCount,chkSkew,chkKurtosis}


	local Options=iup.hbox{col1,col2,col3}
	local OutputFrame=std.gui.frmOutput()
	

	--main dialog
	
	local BtnOK=iup.button{title="OK", size="30x12"}
	local BtnCancel=iup.button{title="Cancel",size="30x12"}

	local AllLayout=iup.vbox{Inputs, Options,	OutputFrame , 
							iup.hbox{iup.fill{}, BtnOK, BtnCancel,alignment = "ACENTER"}}


	local icon=std.gui.makeicon(std.const.exedir.."apps/images/descriptivestat.jpg")

	local MainDlg = iup.dialog{AllLayout; title = "Descriptive Statistics", margin="10x10", resize="yes", icon=icon}
	
	txtInput:setOwner(MainDlg)
	OutputFrame:setOwner(MainDlg)
	
	MainDlg:show()
	
	std.gui.PrepareAppForPreSelection(txtInput)
	
	

	local function SE(elem) -- Standard Error
		return std.stdev(elem)/std.sqrt(std.size(elem))
	end

	local selList={{chkMean, std.mean, "Mean"},
                  {chkSE, SE, "Standard Error"},
                  {chkMedian, std.median, "Median"},
                  {chkMode, std.mode, "Mode"},
                  {chkSD , std.stdev, "Standard Deviation"},
                  {chkSampleVar, std.var, "Variance"},
                  {chkRange, std.range, "Range"},
                  {chkMin, std.min, "Minimum"},
                  {chkMaximum, std.max, "Maximum"},
                  {chkSum , std.sum, "Sum"},
                  {chkCount, std.size, "Count"},
                  {chkSkew, std.skew,"Skewness"},
                  {chkKurtosis, std.kurt, "Kurtosis"}}

	
	function chkAll:action(state)
		
		for i=1,#selList do
			selList[i][1].value=state
		end
	end


	function chkMean:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkSE:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkMedian:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkMode:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkSD:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkSampleVar:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkRange:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkMin:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkMaximum:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkSum:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkCount:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkSkew:action(state)
		if(state==0) then chkAll.value=0 end
	end

	function chkKurtosis:action(state)
		if(state==0) then chkAll.value=0 end
	end


	function BtnCancel:action()
		MainDlg:hide()
	end
	
	
	
	function BtnOK:action()
		
		if(txtInput.value=="") then
			iup.Message("ERROR","A selection has not been done yet.")
			
			return
		end
		
		
		local InputRange=std.Range.new(txtInput.value)
		
		
		local outRng=OutputFrame:GetRange()
		
		
		local row, col=1, 1
		local WS=nil 
		
		if(outRng~=nil)  then 
			row=outRng:coords().r 
			col=outRng:coords().c
			WS=outRng:parent() 
		else
			WS=std.appendworksheet()
		end
		
		local function PrinttoWS(ARange,ARow, ACol, PrintInfo)
			for i=1, #selList do
				if(selList[i][1].value=="ON") then
					
					if(PrintInfo) then
						WS[ARow][ACol]={value=selList[i][3], style="italic"}
					end
					
					
					local func=selList[i][2]
					local success, OutputVal=pcall(func,ARange)
									
					if(OutputVal==nil) then 
						OutputVal="N/A" 
					end 
					
					
					if(type(OutputVal)=="number" ) then
						WS[ARow][ACol+1]=std.misc.tostring(OutputVal)
					
					elseif(type(OutputVal)=="table") then
						local str=""
						for i=1,#OutputVal do
							str=str..std.misc.tostring(OutputVal[i])..","
						end
						WS[ARow][ACol+1]=str
						
					else
						WS[ARow][ACol+1]={value=OutputVal, style="italic", fgcolor="255 0 0"} 
					end
					
					
					
					ARow=ARow+1
				end
			end
			
			return row
		end
		
		
		if(InputInCols.value=="ON") then
			local DescInfo=true
			local nrows,ncols=std.size(InputRange)
			for i=1,ncols do
				local v=std.util.tovector(InputRange:col(i))
				
				PrinttoWS(v,row, col+(i-1), DescInfo)
				
				DescInfo=DescInfo and false
			end
			
		else
			PrinttoWS(std.util.tovector(InputRange),row, col, true)
		end
		
	end


end --MainDialog


std.app.DescriptiveStat=DescriptiveStat



