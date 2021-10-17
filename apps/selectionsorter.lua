-- Author:	Gokhan Bingol (gbingol@sciencesuit.org)
-- License: Subject to end-user license agreement conditions available at www.sciencesuit.org


require( "iuplua" )


local std <const> =std
local iup <const> =iup


local function Reverse(Tbl)
	
	local retTbl={}
	local key=#Tbl
	
	for k,v in pairs(Tbl) do
		retTbl[key]=v

		key=key-1
	end
	
	return retTbl
end
		


local function CheckRange(ARange)

	local r, c=std.size(ARange)
	
	if(r*c==1) then 
		return false
	end
	

	local HasData=false

	for i=1,r do
		for j=1,c do
			
			if (ARange(i,j)~="")  then 
				HasData=true 
				
				break
			end 

		end
	end


	return HasData
end


local function RangeSorter()
		
	local rng=std.activeworksheet():selection()
	
	if(rng==nil) then 
		iup.Message("ERROR","A selection must be made to run this command.") 
		
		return 
	end
	
	local row, col=std.size(rng)
	
	if(CheckRange(rng)==false) then 
		iup.Message("ERROR","Ther is no data available in the selected region.") 
		
		return 
	end
	
	local tbl={}
	local topleft, bottomright=rng:coords()
	
	for i=col,1,-1 do
		local HasValue=CheckRange(rng:col(i))
		
		if(HasValue) then
			local str=string.char(topleft.c+(i-1)+65-1)
			
			table.insert(tbl,"Column "..str)
		end

	end
	
	
	tbl=Reverse(tbl)


	local m_Label=iup.label{title="Sort by:"}
	local m_SortType= iup.list {"A-Z", "Z-A"; dropdown="YES", value=1}
	local m_Columns=iup.list{value=1,dropdown="YES",table.unpack(tbl)}
	local m_CaseSensitive=iup.toggle{title="Case Sensitive"}
	
	
	local BtnSort=iup.button{title="Sort", size="30x12"}
	local BtnClose=iup.button{title="Close",size="30x12"}

	local AllLayout=iup.vbox{iup.hbox{m_Label, m_Columns, m_SortType ,m_CaseSensitive,alignment = "ACENTER"},
							iup.hbox{iup.fill{}, BtnSort, BtnClose,alignment = "ACENTER"}}


	local icon=std.gui.makeicon(std.const.exedir.."apps/images/sort.jpg")

	local MainDlg = iup.dialog{AllLayout; title = "Sort", margin="10x10", gap="10", resize="NO", icon=icon}
	
	
	MainDlg:show()
	
		

	function BtnSort:action( )
		
		local SortType="A"
		if(m_SortType.value== "2") then 
			SortType="D" 
		end
		
		local IsCaseSensitive=false
		if(m_CaseSensitive.value=="ON") then 
			IsCaseSensitive=true 
		end
		
		
		rng:sort(m_Columns.value, SortType,IsCaseSensitive)

	end 
	
	function BtnClose:action()
		MainDlg:hide()
	end
	
	
end



std.app.RangeSorter=RangeSorter
