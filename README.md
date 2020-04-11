# Auto-Whatsapp

This is a simple selenium based framework for creating whatsapp bots. It interacts with whatsapp web to read messages and send them. The major problem with this approach is speed/performance.

## Installation  

### Core Dependancies:  
selenium, splinter, base64, bs4  

### Extra Bot Specific Dependancies:  
spotipy, nltk (with extra data)  

Chromedriver has to be installed and in your path.  
If using spotipy, you'll have to register on the spotify dev website, and sort out authentication yourself (i.e set path variables etc)

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
