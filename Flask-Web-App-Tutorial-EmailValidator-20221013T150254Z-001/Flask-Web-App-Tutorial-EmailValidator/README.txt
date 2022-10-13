Hello, our program is an attempt to imitate a Regular Expression Denial of Service Attack (ReDoS)
targeted at a web server running on flask framework with python backend.

To compile the program, just run:
$python main.py

This will run the web server on the local address http://127.0.0.1:5000/
To access the website just open up a browser and enter the address above.

You will be greeted with a login page, and you may also click on the sign up tab located on the
upper left corner. Head to the sign up page.

#####	The Vulnerability	#############################################################################
The evil regex is actually used to validate the email entered by the user, in this case
the evil regex mention is as follows:
^([a-zA-Z0-9])(([\-.]|[_]+)?([a-zA-Z0-9]+))*(@){1}[a-z0-9]+[.]{1}(([a-z]{2,3})|([a-z]{2,3}[.]{1}[a-z]{2,3}))$

It is a well known email validating regex that results in catastrophic backtracking if given a
long invalid email input, such as:
aaaaaaaaaaaaaaaaaaaa@aaa.aa1

Catastrophic backtracking occurs when the regex reaches the end of the email and encounters the number 1,
which results in an invalid match. The regex will now attempt to backtrack in order to find if another
group will match the intended pattern, due to this part within the evil regex:
(([\-.]|[_]+)?([a-zA-Z0-9]+))*

As a result, the regex will keep backtracking all the a's within the invalid email as it divides them into
more and more groups, ultimately resulting in catastrophic backtracking.

#############################################################################################################

-How to conduct the ReDoS attack:

To demonstrate this, in the sign up page, enter all the other relevant details, but instead of inputting an email, enter the malicious
string 'aaaaaaaaaaaaaaaaaaaa@aaa.aa1' into the email field instead. Then, click "submit".

You will find out that after pressing submit, the entire webpage becomes stuck on the sign up page. The values
such as email and name can still be altered but clicking submit or login will not do anything. This signifies
that the ReDoS attack has succeeded, and the website is stuck evaluating the evil regex.

Open another tab and attempt to load the webpage http://127.0.0.1:5000/. It will not be able to load, demonstrating
the effect of the ReDos attack and how it prevents users from accessing a website that has been attacked.

To stop the attack, simply close the browser and enter CTRL + C in your terminal.

#####	The Patch	#############################################################################
There are two ways we can attempt to patch the program.
1. Replace the evil regex with a safe one, such as the one below:
	^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$
   This regex avoids the nested quantifier present in the evil regex, and hence will not attempt
   to divide the matched pattern into different groups when backtracking. This avoids catastrophic
   backtracking.

2. Do not use regex at all.
   There are numerous libraries out there such as email-validator that performs email validation
   through syntax validation and deliverability validation. The library not only validates whether
   or not the syntax of the email is correct, it also checks to see whether or not the email entered
   can actually send and receive emails.By doing so, not only is the risk of an evil regex nullified
   completely but you will also be able to check the authenticity of the email with only one function
   call: validate_email()
   
#####################################################################################################
