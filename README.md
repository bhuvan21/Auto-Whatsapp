# Auto-Whatsapp

This is a simple selenium based framework for creating whatsapp bots. It interacts with whatsapp web to both read and send messages. The major problem with this approach is speed/performance. Unfortunately, until whatsapp provides us with a public API, this is the best we can get.

## Installation  
First install the following dependancies.

### Core Dependancies:  
selenium, splinter, base64, bs4  

### Extra Bot Specific Dependancies:  
spotipy, nltk (with extra data)  

Chromedriver has to be installed and in your path.  
If using spotipy, you'll have to register on the spotify dev website, and sort out authentication yourself (i.e set path variables etc)
Finally, clone this repository. Now you'll have to customise the options for your whatsapp setup.
Replace the sample chat names in chats.json with the chat names you want these bots to be active on.
Customise the bottom part of main.py to choose which bots you would like to be active.
Now just run main.py, scan the authorisation QR code and the bots should start to work!

## Usage
After following the previous installation instructions, commands can be run by anyone by sending a message on the relevant chat as follows:
`!command-name parameter1 parameter2 . . .`
e.g.
`roll d20` will roll a 20 sided dice.

## Progress

### Current Available Commands are:
spotify - searches spotify for your query
youtube - searches youtube for your query
spongebob - selectively capitalizes text for comedic effect
remindme - sends a reminder message after a specific period of time
thesaurize - changes every word replaced by a synonym from a thesaurus
aboutme - gives information about this bot framework
help - gives syntax help about the specified command
roll - rolls a variable sided dice

### ToDo Commands are:  
mal  
poll (vote etc.)  
