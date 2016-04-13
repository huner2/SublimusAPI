var error = document.getElementById("hook").innerHTML;
var errors = new Array();
errors["page_not_found"] = ["Page Not Found", "The page or service you requested does not exist. Please check your spelling or the change log."];
errors["server_error"] = ["Server Error", "The server is experiencing a heavy load, there is something wrong with my code, or your request may be malformed.  Try your request again and then verify it is formed correctly.  Please report it as a bug if your request is correct."]

var title = document.getElementById("etitle");
var desc = document.getElementById("edesc");

title.innerHTML = "Error - " + errors[error][0];
desc.innerHTML = errors[error][1];