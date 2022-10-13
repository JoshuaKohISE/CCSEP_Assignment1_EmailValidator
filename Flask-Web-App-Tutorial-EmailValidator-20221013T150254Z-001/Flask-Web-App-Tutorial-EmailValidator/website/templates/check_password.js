function CheckPassword(username, password) 
{ 
	var rePattern =  username;
	if(password.value.match(rePattern) != null) 
	{ 
		alert("Password must not contain your username!");
		return true;
	}
	else
	{ 
		alert("Valid Password.");
		return false;
	}
}
