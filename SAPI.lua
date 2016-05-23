--[[
	Created By Sublimus, you can modify it, redistribute it all you like, just don't take credit for the original.
	
	Please check out SublimusAPI.us.to:69 for usage, as well as source code.
	
	Note: There is a limit of 500 requests per server per minute, if you exceed this, the entire httpService will stall for 30 seconds.
	
	Note2: If there is an error, such as the user doesn't exist or an id that doesn't exist is entered, the functions will all return nil.  You can modify the return value if you wish.
	
	Be sure to click on HttpService in Explorer and make sure HttpEnabled is true.
	
	To use this module-script add this code to your script:
		sapi = require(game.Workspace.SublimusAPI) -- Or whatever the location is
		
	Add then to make a call to one of the functions:
		sapi.getUsernameById(1234) -- Example call to the getUsernameById function
--]]

--[[
	List of APIs:
		getUsernameById(id) -- Get username by ID
			Returns Username as String
			
		getIdByUsername(username) -- Get ID by username
			Returns ID as integer
			
		userCanManageAsset(userID, assetID) -- Returns whether the user can manage the given asset
			Returns boolean
			
		userHasAsset(userID, assetID) -- Returns whether the user has the given asset
			Returns boolean
			
		getMarketplaceInfo(assetID) -- Returns the properties of the given catalog item
			Returns table with the following tree:
				{
					["AssetID"] = long,
					["ProductID"] = long,
					["Name"] = string,
					["Description"] = string,
					["AssetTypeId"] = integer,
					["Creator"] = {
									["Id"] = integer,
									["Name"] = string
								  }
					["IconImageAssetId"] = long,
					["Created"] = string,
					["Updated"] = string,
					["PriceInRobux"] = integer,
					["PriceInTickets"] = null, -- Deprecated
					["Sales"] = integer,
					["IsNew"] = boolean,
					["IsForSale"] = boolean,
					["IsPublicDomain"] = boolean,
					["IsLimited"] = boolean,
					["IsLimitedUnique"] = boolean,
					["Remaining"] = integer or null,
					["MinimumMembershipLevel"] = integer,
					["ContentRatingTypeId"] = integer
				 }
				
		getClanByUser(userID) -- Returns the properties of the given user's clan
			Returns table with the following tree:
				{
					["Id"] = integer,
					["Name"] = string or null,
					["EmblemAssetId"] = long
				}
				
		getClanById(clanID) -- Returns the properties of the given clan
			Returns table with the following tree:
				{
					["Id"] = integer,
					["Name"] = string or null,
					["EmblemAssetId"] = long
				}
		
		getFriendsOfUser(userID,page) -- Returns the list of friends of a user on the given page
			Returns table with the following tree:
				{
					{
						["Id"] = long,
						["Username"] = string,
						["AvatarUri"] = string,
						["AvatarFinal"] = boolean,
						["IsOnline"] = boolean
					}
					-- And so on for remaining users
				}
--]]
local module = {}

local http = game:getService("HttpService")

function module.getUsernameById(id)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/getUsernameById/"..id)
	local json = http:JSONDecode(response)
	if json["response"] ~= 200 then
		return nil
	end
	return json["username"]
end

function module.getIdByUsername(username)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/getIdByUsername/"..username)
	local json = http:JSONDecode(response)
	if json["response"] ~= 200 then
		return nil
	end
	return json["id"]
end

function module.userCanManageAsset(uid,aid)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/userCanManageAsset/"..uid.."/"..aid)
	local json = http:JSONDecode(response)
	if json["response"] ~= 200 then
		return nil
	end
	return json["manage"]
end

function module.userHasAsset(uid,aid)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/userHasAsset/"..uid.."/"..aid)
	local json = http:JSONDecode(response)
	if json["response"] ~= 200 then
		return nil
	end
	return json["has"]
end

function module.getMarketplaceInfo(aid)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/getMarketplaceInfo/"..aid)
	local json = http:JSONDecode(response)
	if json["response"] ~= 200 then
		return nil
	end
	local item = http:JSONDecode(json["info"])
	return item
end

function module.getClanByUser(uid)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/getClanByUser/"..uid)
	local json = http:JSONDecode(response)
	if json["response"] ~= 200 then
		return nil
	end
	local clan = http:JSONDecode(json["info"])
	return clan
end

function module.getClanById(cid)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/getClanById/"..cid)
	local json = http:JSONDecode(response)
	if json["response"] ~= 200 then
		return nil
	end
	local clan = http:JSONDecode(json["info"])
	return clan
end

function module.getFriendsOfUser(uid,page)
	local response = http:GetAsync("http://SublimusAPI.us.to:69/apis/getFriendsOfUser/"..uid.."/"..page)
	local json = http:JSONDecod(response)
	if json["response"] ~= 200 then
		return nil
	end
	local friendList = http:JSONDecode(json["info"])
	return friendList
end

return module
