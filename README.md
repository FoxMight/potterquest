# potterquest
Dive into Harry Potter universe, right on Discord!

##### Table of Contents
* [Abstract](#Abstract)
* [Getting Started](#getting-started)
    * [Configuration](#configuration)
    * [Running](#running)
    * [Closing](#closing)
  
 ## Abstract
 This bots main purpose is to server as a general fun, utility bot
 for playing a harrypotter like game directly inside of discords chat client!
 It allows users to create profiles, along with purchase items in shops with 
 coins they earn through various activities. There are also many other fun
 commands packed inside of which most users can see by using the bots help command!
 
 ## Getting started
 If you just want to be able to use the bot in your discord server, simply invite it 
 using this link: (Insert link here). Otherwise, if you want to run your own version of the bot
 first ensure you have python 3.7 or higher installed on your machine, then
 proceed go to your terminal to run pip install -r requirements.txt to install all of the dependencies of the bot 
 (ensure you are in the same directory as your requirements.txt file).
 
 
 ### Configuration
 Next we have to configure the files for your own instance of the bot. Go ahead and
 create an application at discordapp.com and get its secret key. You the must put that secret key inside 
 of secret.py inside of the quotes for "secret_token". You must also have your own mongodb atlas cluster to run
 the bot as well, as we store information in a mongo db atlas database. To make one, create a mongo
 db at last account, create a cluster and obtain a connection string. The connection string
 will have a large amount of text but within it there should be a \<password> portion. Replace
 that portion of the string with the password you created for a user in your cluster.
 Also ensure that you have IP whitelisted yourself within your database so you do not get blocked out.
 Once you change the link, put the new link into secret.py within the quotes for "secret_key".
 Once you do that, your all set to begin running!
 
 ### Running
 Running the bot once everything is set up is easy, go to your terminal and run python turn_on.py. You should see the 
 bot turn on in any server you invited it to! You can also choose to run it from a text editor or IDE, simply choose 
 turn_on.py as your startup file.
 
 ### Closing
 Closing is also fairly simple, from an IDE you can simple force the program to close using its tools, and from the
 terminal, you can simply enter ctrl + C.
 
 