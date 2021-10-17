-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org

-- 1) The compositional data was downloaded from USDA NAL website (given below) as an Excel file.
-- https://www.ars.usda.gov/northeast-area/beltsville-md/beltsville-human-nutrition-research-center/nutrient-data-laboratory/docs/sr28-download-files/
-- 2) Some of the characters such as & and , was replaced with empty characters for food names.
-- 3) Acronyms such as W/ and WO/ was replaced with with and without, respectively.
-- 4) Compositional Data (water, CHO, protein, total lipids, ash) was read from the Excel file into database/USDANALSR28.db SQLite file.


require( "iuplua" )


local std <const> =std
local iup <const> =iup


local function GetScientificRep(num)
	local exp=math.floor(math.log10(math.abs(num)))
	local base=num*math.pow(10,-1*exp)
		
	local strexp=""
	if(math.abs(exp)<10) then
		if(exp<0) then
			strexp="-0"..tostring(math.abs(exp))
		else
			strexp="+0"..tostring(exp)
		end
		
	else
		strexp=tostring(exp)
			
	end
	
	return string.format("%.3f",tostring(base)).."E"..strexp
end


local function WriteValues(Food, txtRho, txtCp, txtK, txtAlpha)
	local f_rho=Food:rho(); 
	local f_cp=Food:cp();  
	local f_k=Food:k();  
	local f_thermdif=f_k/(f_rho*(f_cp*1000))
	
	assert(type(f_rho)=="number" and  type(f_cp)=="number" and type(f_k)=="number","ERROR: Predictions did not yield a number")
	
	txtRho.value=string.format("%.2f",tostring(f_rho))
	txtCp.value=string.format("%.3f",tostring(f_cp))
	txtK.value=string.format("%.4f",tostring(f_k))
	txtAlpha.value=GetScientificRep(f_thermdif)
end


local function FoodDatabase()

	local SearchStr=""
	
	local m_Food=nil
	
	--Design of Page1
	
	local m_List=iup.list{expand="yes"}
	local m_SearchText=std.gui.initvaltext{value="Start Typing to Search..."}
	
	local page1=iup.vbox{m_List, m_SearchText}

	page1.tabtitle="Search"
	--page1.color="255 0 0"
	
	--Design of Page2
	
	local lblWater=iup.label{title="Water"}
	local txtWater=iup.text{readonly="yes"}
	
	local lblCHO=iup.label{title="CHO"}
	local txtCHO=iup.text{readonly="yes"}
	
	local lblProtein=iup.label{title="Protein"}
	local txtProtein=iup.text{readonly="yes"}
	
	local lblLipid=iup.label{title="Lipid"}
	local txtLipid=iup.text{readonly="yes"}
	
	local lblAsh=iup.label{title="Ash"}
	local txtAsh=iup.text{readonly="yes"}
    
	local GridboxLeft=iup.gridbox{lblWater, txtWater,
										lblCHO, txtCHO,
										lblProtein, txtProtein,
										lblLipid, txtLipid,
										lblAsh, txtAsh,
								numdiv=2, HOMOGENEOUSCOL="yes",CGAPLIN=10, CGAPCOL=5, orientation="HORIZONTAL"}
	
	
	local lblT=iup.label{title="T(C): "}
	local txtT=std.gui.numtext{min=0, max=50, value=20}
	
	local lblRho=iup.label{title="rho"}
	local txtRho=iup.text{readonly="yes"}
	local lblRhoUnit=iup.label{title="kg/m\xB3"}
	
	local lblK=iup.label{title="k"} --Thermal conductivity
	local txtK=iup.text{readonly="yes"}
	local lblKUnit=iup.label{title="W/m\xB7C"} 
	
	local lblCp=iup.label{title="Cp"}
	local txtCp=iup.text{readonly="yes"}
	local lblCpUnit=iup.label{title="kJ/kg\xB7C"}
	
	local lblAlpha=iup.label{title="alpha"}
	local txtAlpha=iup.text{readonly="yes"}
	local lblAlphaUnit=iup.label{title="m\xB2/s"} 
	
	local GridboxRight=iup.gridbox{lblRho, txtRho, lblRhoUnit,
										lblK, txtK, lblKUnit,
										lblCp, txtCp, lblCpUnit,
										lblAlpha, txtAlpha, lblAlphaUnit,
								numdiv=3,CGAPLIN=10, CGAPCOL=10}
	
	
	local Inputs=iup.hbox{lblT,txtT}
	local Outputs=iup.hbox{GridboxLeft,iup.fill{}, GridboxRight,iup.fill{10}}
	local page2=iup.vbox{Inputs,iup.label{}, Outputs}

	
	page2.tabtitle="Composition and ThermoPhysical Prop"
	local m_tabs=iup.tabs{page1,page2}
	
	local icon=std.gui.makeicon(std.const.exedir.."apps/images/fooddatabase.jpg")
	
	local dlgFoodDatabase = iup.dialog{m_tabs, title="Search Food Database File - SR 28 (Offline)", size="250x150", icon=icon}
	
	
	local db=std.Database.new()
	db:open(std.const.exedir.."/datafiles/USDANALSR28.db") 

	dlgFoodDatabase:show()
	
	function m_SearchText:valuechanged_cb()
            
		local SearchStr=m_SearchText.value
		if(SearchStr==" " or  #SearchStr<3) then return end

		m_List[1]=nil --remove all items
		
		local  QueryString=""
		
		local tokens=std.util.tokenize(SearchStr)
		local firstToken=true
		
		for i=1,#tokens do
			local token=tokens[i]
			
			if(token~="") then
			
				if(firstToken) then
					QueryString=QueryString.." SELECT * FROM Composition where FoodName like\"%"..token.."%".."\""
					firstToken=false
				else
					QueryString=QueryString.." INTERSECT SELECT * FROM Composition where FoodName like\"%"..token.."%".."\""
				end
				
			end
		end
		

		local t,r,c=db:sql(QueryString)		
		if(r==nil) then return end
            
		for i=1,r do
			m_List[i]=t[i][2]
		end
	
	end
	
	
	
	function m_List:action(text, item, state)
	
		local SelectedFoodName=text
		local QueryString="SELECT * FROM Composition where FoodName=\'"..SelectedFoodName.."\'";
		local t=db:sql(QueryString)

		txtWater.value=t[1][3]
		txtProtein.value=t[1][4]
		txtLipid.value=t[1][5]
		txtCHO.value=t[1][6]
		txtAsh.value=t[1][7]

		m_Food=nil
		m_Food=std.Food.new({Water=tonumber(t[1][3]), Protein=tonumber(t[1][4]), Lipid=tonumber(t[1][5]), CHO=tonumber(t[1][6]), Ash=tonumber(t[1][7])})
		txtT.value=20
		
		if(m_Food==nil) then 
			iup.Message("ERROR","Could not create the food variable")
			return 
		end
         
		WriteValues(m_Food,txtRho, txtCp, txtK, txtAlpha)
	
	end
	
	function m_List:button_cb(button, pressed, x, y, status)
		
		if(button==iup.BUTTON3 ) then -- right mouse button
			if(m_Food==nil) then return end
			
			local varName=iup.GetText("Export as Lua Variable","")
			_G[varName]=m_Food
			
		end
	end
	
	
	function txtT:valuechanged_cb()
		local val=txtT.value
		if(val=="") then return end
		
		local temperature=tonumber(val)
		if(temperature==nil) then return end
		
		if(temperature>50 or temperature<1) then
			iup.Message("Warning", "At temperatures below 1C and above 50C, predictions might not work well.")
		end
		
		m_Food:T(temperature)
		
		WriteValues(m_Food, txtRho, txtCp, txtK, txtAlpha)
	end
	
end

std.app.FoodDatabase=FoodDatabase
