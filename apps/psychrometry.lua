-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org



require( "iuplua" )

local std <const> =std
local iup <const> =iup


local function Psychrometry()

	local chkP = iup.toggle{title = "P"}
	local lblP=iup.label{title="Pressure"}
	local txtP=std.gui.numtext{min=40*1000, max=1555*1000} --theoretically it is lower but practically it does not yield stable results
	local lblP_unit=iup.label{title="Pa"}


	local lblPw=iup.label{title="Pw"}
	local txtPw=iup.text{readonly="yes"}
	local lblPw_unit=iup.label{title="Pa"} 


	local lblPws=iup.label{title="Pws"}
	local txtPws=iup.text{readonly="yes"}
	local lblPws_unit=iup.label{title="Pa"}


	local chkT = iup.toggle{title = "Tdb"}
	local lblT=iup.label{title="Dry-bulb \nTemperature"}
	local txtT=std.gui.numtext{min=-100, max=200}
	local lblT_unit=iup.label{title="\xB0 C"}

	local chkTwb = iup.toggle{title = "Twb"}
	local lblTwb=iup.label{title="Wet-bulb \nTemperature"}
	local txtTwb=std.gui.numtext{min=-100, max=200}
	local lblTwb_unit=iup.label{title="\xB0 C"}

	local chkTdp = iup.toggle{title = "Tdp"}
	local lblTdp=iup.label{title="Dew point \nTemperature"}
	local txtTdp=std.gui.numtext{min=-100, max=200}
	local lblTdp_unit=iup.label{title="\xB0 C"}

	local GridboxLeft=iup.gridbox{chkP, lblP, txtP, lblP_unit,
								iup.label{}, lblPw,  txtPw,lblPw_unit,
								iup.label{}, lblPws,  txtPws,lblPws_unit,
								chkT, lblT, txtT, lblT_unit,
								chkTwb, lblTwb, txtTwb, lblTwb_unit,
								chkTdp, lblTdp, txtTdp, lblTdp_unit,
								numdiv=4, HOMOGENEOUSCOL="yes",CGAPLIN=15, CGAPCOL=7, orientation="HORIZONTAL"}



	local chkW = iup.toggle{title = "W"}
	local lblW=iup.label{title="Absolute Humidity"}
	local txtW=std.gui.numtext{min=0, max=1}
	local lblW_unit=iup.label{title="kg / kg dry air"}


	local lblWs=iup.label{title="Ws"}
	local txtWs=iup.text{readonly="yes"}
	local lblWs_unit=iup.label{title="kg / kg dry air"}

	local chkH = iup.toggle{title = "H"}
	local lblH=iup.label{title="Enthalpy"}
	local txtH=std.gui.numtext{min=0}
	local lblH_unit=iup.label{title="kJ / kg dry air"}

	local chkRH = iup.toggle{title = "RH"}
	local lblRH=iup.label{title="Relative Humidity"}
	local txtRH=std.gui.numtext{min=0, max=100}
	local lblRH_unit=iup.label{title="%"}

	local chkV = iup.toggle{title = "v"}
	local lblV=iup.label{title="Specific Volume"}
	local txtV=std.gui.numtext{min=0}
	local lblV_unit=iup.label{title="m\xB3 /kg"}


	local GridboxRight=iup.gridbox{chkW, lblW, txtW, lblW_unit,
								iup.label{}, lblWs, txtWs, lblWs_unit,
								chkH, lblH, txtH, lblH_unit,
								chkRH, lblRH, txtRH, lblRH_unit,
								chkV, lblV, txtV, lblV_unit,
								numdiv=4, CGAPLIN=15, CGAPCOL=7, orientation="HORIZONTAL"}


	local HBox=iup.hbox{GridboxLeft,GridboxRight}

	local BtnCalc=iup.button{title="Calculate", active="NO"}


	local AllLayout=iup.vbox{HBox, BtnCalc, alignment="acenter"}


	local icon=std.gui.makeicon(std.const.exedir.."apps/images/psychrometry.bmp")
	
	--menu
	local item_exportresults = iup.item {title = "Export to Worksheet", active="NO"}
	local menu_file = iup.menu {item_exportresults}
	local submenu_file = iup.submenu {menu_file; title = "File"}
	local menu = iup.menu {submenu_file}

	local dlg = iup.dialog{AllLayout; title = "Psychrometry", margin="10x10", resize="yes", menu=menu, icon=icon}
	dlg:showxy(iup.CENTER, iup.CENTER)

	--
	local ChkBoxes={chkP, chkT,chkTwb,  chkTdp, chkW, chkH,chkRH,chkV}

	local function EnableAllCheckBoxes()
		for i=1,8 do
			ChkBoxes[i].active="YES"
		end
	end

	local function DisableUncheckedBoxes()
		for i=1,8 do
			if(ChkBoxes[i].value=="OFF") then  --unchecked
				ChkBoxes[i].active="NO"
			end
		end
	end



	local function CheckToAllowStateChange()
		local NumberofCheckedBoxes=0
		local chkBox=nil

		--Find number of checked boxes
		for i=1,8 do
			chkBox=ChkBoxes[i]
			if(chkBox.value=="ON") then
				NumberofCheckedBoxes=NumberofCheckedBoxes+1
			end
		end

		--If the number is 3, then disable unchecked boxes and allow calculation
		if(NumberofCheckedBoxes>=3) then
			DisableUncheckedBoxes()
			BtnCalc.active="YES"
		else
			EnableAllCheckBoxes()
			BtnCalc.active="NO"
		end
	end


	function chkP:action(v)
		CheckToAllowStateChange()
	end  
	

	function chkT:action(v)
		CheckToAllowStateChange()
	end

	function chkTwb:action(v)
		CheckToAllowStateChange()
	end

	function chkTdp:action(v)
		CheckToAllowStateChange()
	end

	function chkW:action(v)
		CheckToAllowStateChange()
	end

	function chkH:action(v)
		CheckToAllowStateChange()
	end

	function chkRH:action(v)
		CheckToAllowStateChange()
	end

	function chkV:action(v)
		CheckToAllowStateChange()
	end



	local PsyInputValues, PsyOutputValues={}, {}


	function BtnCalc:action()

		--reset the tables
		PsyInputValues={}
		PsyOutputValues={}
		
		local function Check()
			local control={{chkP,txtP,"pressure"},
							{chkT, txtT, "dry-bulb temperature"},
							{chkTwb, txtTwb, "wet-bulb temperature"},
							{chkTdp, txtTdp, "dew point temperature"},
							{chkW, txtW, "humidity"},
							{chkH, txtH, "enthalpy"},
							{chkRH, txtRH, "relative humidity"},
							{chkV, txtV, "specific volume"}}
				
				
						
							
			for i=1,#control do
				
				if(control[i][1].value=="ON") then 
					if(control[i][2].value=="") then
						iup.Message("ERROR","A numeric value must be entered for "..control[i][3]..".") 
						
						return false;
					end
				end
				 
			end 
			
		end --function check
		
		
		
		if(Check()==false) then
			return
		end 
				

		if (chkP.value=="ON") then
			PsyInputValues.P=tonumber(txtP.value)/1000 --Pa to kPa
		end


		if (chkT.value=="ON") then
			PsyInputValues.Tdb=tonumber(txtT.value)
		end

		if (chkTwb.value=="ON") then
			PsyInputValues.Twb=tonumber(txtTwb.value)
		end

		if (chkTdp.value=="ON") then
			PsyInputValues.Tdp=tonumber(txtTdp.value)
		end

		if (chkW.value=="ON") then
			PsyInputValues.W=tonumber(txtW.value)
		end

		if (chkH.value=="ON") then
			PsyInputValues.H=tonumber(txtH.value)
		end

		if (chkRH.value=="ON") then
			PsyInputValues.RH=tonumber(txtRH.value)
		end

		if (chkV.value=="ON") then
			PsyInputValues.V=tonumber(txtV.value)
		end

		local stat=nil

		stat, PsyOutputValues=pcall(std.fluid.psychrometry,PsyInputValues)

		if(stat==false) then
			iup.Message("ERROR", PsyOutputValues)
			
			return
		end




		--Output to textboxes
		if (chkP.value=="OFF")  then 
			txtP.value=string.format("%.0f",tostring(PsyOutputValues.P*1000)) --kPa to Pa 
		end
		
		txtPw.value=string.format("%.0f",tostring(PsyOutputValues.Pw*1000)) --kPa to Pa
		txtPws.value=string.format("%.0f",tostring(PsyOutputValues.Pws*1000)) --kPa to Pa

		if (chkT.value=="OFF") then 
			txtT.value=string.format("%.2f",tostring(PsyOutputValues.Tdb)) 
		end
		
		if (chkTwb.value=="OFF") then 
			txtTwb.value=string.format("%.2f",tostring(PsyOutputValues.Twb)) 
		end
		
		if (chkTdp.value=="OFF")  then 
			txtTdp.value=string.format("%.2f",tostring(PsyOutputValues.Tdp)) 
		end
		
		
		if (chkW.value=="OFF") then 
			txtW.value=string.format("%.4f",tostring(PsyOutputValues.W)) 
		end
		
		if(PsyOutputValues.Ws~=nil) then 
			txtWs.value=string.format("%.4f",tostring(PsyOutputValues.Ws)) 
		else 
			txtWs.value="NA"
		end
		
		if (chkH.value=="OFF") then 
			txtH.value=string.format("%.2f",tostring(PsyOutputValues.H)) 
		end 
		
		if (chkRH.value=="OFF") then 
			txtRH.value=string.format("%.2f",tostring(PsyOutputValues.RH)) 
		end 
		
		if (chkV.value=="OFF") then 
			txtV.value=string.format("%.4f",tostring(PsyOutputValues.V)) 
		end 

		
		--enable export results menu item
		item_exportresults.active="YES"

	end


	function item_exportresults:action()
		
		local Units={Tdb=" C", Twb=" C", Tdp=" C", P="kPa", Pws="kPa", Pw="kPa", RH="%", H="kJ/ kg da", 
					W="kg / kg da", Ws="kg / kg da", V="m3 /kg"}
		
		local date=os.date("*t")
		local hour=date.hour
		local min=date.min
		if(min<=9) then 
			min="0"..min
		end

		local sec=date.sec
		if(sec<=9) then
			sec="0"..sec
		end

		local ws=std.appendworksheet("Psychrometry "..hour..min..sec)
		
		local row=1
		
		ws[row][1]={value="Selected Combination", fgcolor=std.const.color.red}
		
		for key,value in pairs(PsyInputValues) do
			row=row+1
			
			ws[row][1]={value=key, style="italic"}
			ws[row][2]=value --dont format the value
			ws[row][3]=Units[key]
			
		end

		row=row+2
		
		ws[row][1]={value="Results", fgcolor=std.const.color.blue_royal}
		
		for key, value in pairs(PsyOutputValues) do
			local IsKeyEqual=false
			
			for in_key,in_value in pairs(PsyInputValues) do
				
				if(key==in_key) then 
					IsKeyEqual=true 
					
					break
				end 
			end
			
			if(not IsKeyEqual) then
				row=row+1
				
				ws[row][1]={value=key, style="italic"}
				ws[row][2]=std.misc.tostring(value)
				ws[row][3]=Units[key]
			end
		end
		
		
		return iup.DEFAULT
	end


end --local function psychrometry


std.app.Psychrometry=Psychrometry
