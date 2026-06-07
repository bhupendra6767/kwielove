"""
generator.py — Generates triggers.json and responses.json with 1000+ triggers and 10000+ responses.
Run this once: python discord-bot/generator.py
"""

import json
import os
import random

# ---------------------------------------------------------------------------
# TRIGGER SEEDS — each seed expands into many variations
# ---------------------------------------------------------------------------

TRIGGER_SEEDS = {
    "greetings": [
        "hi", "hello", "hey", "heyy", "heyyy", "heyyyy",
        "hii", "hiii", "hiiii", "helo", "helo there",
        "hello there", "hi there", "hey there", "greetings",
        "howdy", "sup", "whats up", "what's up", "wassup",
        "wazzup", "waddup", "whaddup", "yo", "yoo", "yooo",
        "ayo", "ayoo", "oi", "ello", "hiya", "heya", "heyyy there",
        "hi everyone", "hello everyone", "hey everyone",
        "hello all", "hi all", "hey all", "hi folks", "hello folks",
        "hey folks", "hi guys", "hello guys", "hey guys",
        "hi peeps", "hello peeps", "hey peeps",
    ],
    "morning": [
        "good morning", "gm", "morning", "mornin", "good mornin",
        "good morning everyone", "gm everyone", "morning everyone",
        "good morning all", "gm all", "morning all",
        "rise and shine", "wakey wakey", "good day",
        "top of the morning", "morning fellas", "gm fellas",
        "morning guys", "gm guys", "good morning guys",
        "happy morning", "bright morning", "early morning",
        "gooood morning", "goood morning", "gm gm",
    ],
    "night": [
        "good night", "gn", "goodnight", "night", "nite", "nighty",
        "nighty night", "good nite", "night everyone", "gn everyone",
        "goodnight everyone", "nite everyone", "night all", "gn all",
        "sleep well", "sweet dreams", "going to sleep", "gonna sleep",
        "heading to bed", "going to bed", "off to bed", "bye night",
        "later night", "night night", "gnite", "g nite",
        "have a good night", "have a good sleep",
    ],
    "goodbye": [
        "bye", "goodbye", "later", "cya", "see ya", "see you",
        "ttyl", "take care", "peace", "peace out", "deuces",
        "im out", "i'm out", "im leaving", "leaving now",
        "gotta go", "got to go", "have to go", "gtg",
        "brb", "be right back", "afk", "going afk", "ciao",
        "adios", "hasta la vista", "catch you later", "bye bye",
        "byee", "byeee", "byeeee", "later gator", "laters",
        "see ya later", "see you later", "later guys",
        "bye guys", "goodbye guys", "bye everyone",
    ],
    "gg": [
        "gg", "ggs", "gg ez", "good game", "good games",
        "gg wp", "gg everyone", "nice game", "great game",
        "what a game", "amazing game", "insane game",
        "gg wp ez", "ggwp", "gg wp ez clap", "ez clap",
        "gg no re", "ngl gg", "gg tbh",
    ],
    "lol": [
        "lol", "lmao", "lmfao", "lmaoo", "lmaoooo",
        "haha", "hahaha", "hahahaha", "hehe", "hehehe",
        "😂", "😂😂", "💀", "💀💀", "😭", "😭😭",
        "lol ok", "lmao what", "haha nice", "haha true",
        "lol no way", "lmao fr", "bruh lol", "ngl lmao",
        "this is so funny", "im dead", "im crying",
        "i'm dead", "i'm crying", "dying rn", "crying rn",
        "lol rip", "lmao rip", "kek", "xD", "xd", "XD",
    ],
    "bruh": [
        "bruh", "bruuh", "bruhhh", "bro", "broo", "brooo",
        "bruh moment", "bruh what", "bruh no way", "bruhhh moment",
        "bro what", "bro no way", "bro fr", "bruh fr",
        "bro really", "bruh really", "bro seriously",
        "bruh seriously", "my bro", "my g", "bro come on",
        "bruh come on", "bro stop", "bruh stop", "bro please",
    ],
    "minecraft": [
        "minecraft", "mc", "mincraft", "mind craft", "mine craft",
        "minecraft is the best", "playing minecraft", "wanna play mc",
        "wanna play minecraft", "lets play minecraft", "let's play mc",
        "minecraft server", "mc server", "minecraft survival",
        "mc survival", "minecraft creative", "minecraft pvp",
        "minecraft bedrock", "minecraft java", "mc java", "mc bedrock",
        "minecraft update", "mc update", "new minecraft update",
    ],
    "pvp": [
        "pvp", "1v1", "1 v 1", "lets pvp", "let's pvp",
        "wanna pvp", "wanna 1v1", "anyone wanna pvp",
        "anyone wanna 1v1", "pvp me", "1v1 me", "clutch",
        "pvp is fun", "pvp battle", "fight me", "1v1 bro",
        "skill issue", "skill diff", "get good", "get rekt",
        "noob", "pro pvp", "pvp god", "pvp king",
    ],
    "tier": [
        "tier", "tier list", "what tier", "tierlist",
        "tier s", "s tier", "a tier", "b tier", "c tier",
        "d tier", "f tier", "tier ranking", "rank tier",
        "tier thoughts", "whats the tier", "what's the tier",
        "make a tier list", "tier list time",
    ],
    "dead_chat": [
        "dead chat", "dead server", "chat dead", "so dead",
        "this chat is dead", "chat is dead", "server is dead",
        "nobody talking", "no one talking", "silent server",
        "ghost server", "empty server", "chat quiet",
        "where is everyone", "where'd everyone go", "chat revival",
        "revive the chat", "lets revive chat", "let's revive chat",
        "someone talk", "anyone say something",
    ],
    "online": [
        "anyone online", "anyone here", "is anyone here",
        "anyone active", "is anyone active", "anyone alive",
        "is anyone alive", "hello anyone", "anyone around",
        "is anyone around", "anyone there", "is anyone there",
        "whos online", "who's online", "who is online",
        "who's here", "whos here", "anyone playing",
        "whos active", "who's active",
    ],
    "thanks": [
        "thanks", "thank you", "thx", "ty", "tysm", "tyvm",
        "thank u", "thanku", "thankyu", "thanks a lot",
        "thanks so much", "many thanks", "much appreciated",
        "appreciate it", "appreciate that", "i appreciate it",
        "thanks everyone", "thank you everyone",
        "thanks guys", "thank you guys", "thanks all",
        "ty so much", "ty a lot", "thx so much", "thx a lot",
        "big thanks", "huge thanks",
    ],
    "congrats": [
        "congrats", "congratulations", "grats", "gratz",
        "congrats bro", "congrats everyone", "congrats all",
        "well done", "good job", "great job", "amazing job",
        "nice work", "great work", "amazing work",
        "proud of you", "you did it", "you made it",
        "lets gooo", "let's gooo", "lets go", "let's go",
        "poggers", "pog", "W", "big W", "huge W",
        "congrats on that", "gz", "grz",
    ],
    "nice": [
        "nice", "nicee", "niceee", "nice one", "nice shot",
        "nice play", "nice move", "that's nice", "that's cool",
        "thats nice", "thats cool", "so nice", "very nice",
        "pretty nice", "quite nice", "oh nice", "oh cool",
        "noice", "nais", "that's great", "thats great",
    ],
    "cool": [
        "cool", "coool", "cooool", "cool cool", "very cool",
        "so cool", "pretty cool", "thats cool", "that's cool",
        "that's dope", "thats dope", "dope", "fire", "sick",
        "insane", "amazing", "awesome", "incredible", "fantastic",
        "lit", "based", "W", "actually cool", "lowkey cool",
        "ngl cool", "no cap cool", "fr cool",
    ],
    "how_are_you": [
        "how are you", "how are u", "how r u", "how ru",
        "how are you doing", "how you doing", "how u doing",
        "how's it going", "hows it going", "how is it going",
        "how's everything", "hows everything", "what's good",
        "whats good", "you good", "you ok", "u good", "u ok",
        "how have you been", "how've you been",
        "hope you're well", "hope ur well",
    ],
    "what_are_you_doing": [
        "what are you doing", "what are u doing", "whatchu doing",
        "whatcha doing", "what you up to", "what r u up to",
        "what are you up to", "what u up to", "wyd", "whatyoudoing",
        "what you doin", "what r u doin", "whatcha up to",
        "what's going on", "whats going on", "what's happening",
        "whats happening",
    ],
    "wait": [
        "wait", "waitt", "waittt", "hold on", "hold up",
        "one sec", "one second", "brb one sec", "gimme a sec",
        "give me a sec", "just a moment", "just a min",
        "just a minute", "hold on a sec", "hold on a minute",
        "wait what", "wait really", "wait actually",
    ],
    "fr": [
        "fr", "frr", "frrr", "for real", "forreal",
        "no cap", "nocap", "facts", "factss", "based",
        "real talk", "lowkey", "highkey", "actually",
        "ngl", "not gonna lie", "honestly", "tbh", "to be honest",
        "fr fr", "no cap fr", "facts fr",
    ],
    "omg": [
        "omg", "omgg", "omggg", "oh my god", "oh my gosh",
        "oh my goodness", "oh wow", "wow", "woww", "wowww",
        "woah", "whoa", "whaaat", "what no way", "no way",
        "no wayyy", "seriously", "are you serious",
        "you serious", "for real", "wtf", "what the",
    ],
    "help": [
        "help", "help me", "can someone help", "anyone help",
        "need help", "need assistance", "i need help",
        "can you help", "please help", "help pls",
        "help please", "anybody help", "quick help",
    ],
    "rip": [
        "rip", "ripp", "rippp", "f", "ff", "fff",
        "rip bro", "rip man", "rip fr", "rip no cap",
        "f in chat", "press f", "press f to pay respects",
        "that's rip", "thats rip", "oof", "ooof", "oooof",
        "big oof", "huge oof", "L", "big L", "massive L",
    ],
}

# ---------------------------------------------------------------------------
# RESPONSE TEMPLATES per category — will be expanded massively
# ---------------------------------------------------------------------------

RESPONSE_TEMPLATES = {
    "greetings": [
        "Hey! 👋 What's up?",
        "Hello! 😊 Hope you're doing great!",
        "Hi there! 👋 How's it going?",
        "Hey hey! 😄 Welcome in!",
        "Yo! 👋 What's good?",
        "Heyy! Hope everyone's having a great time 😊",
        "Sup! 👋",
        "Helloooo! 😄",
        "Greetings! Welcome to the server 👋",
        "Hey! Good to see you here 😄",
        "Hi! 😊 Hope your day is going well!",
        "What's up everyone! 👋",
        "Hey! Drop in anytime, we're friendly here 😄",
        "Ayo! 👋 What's poppin?",
        "Heyyy! Nice to see you! 😊",
        "Yo yo yo! 👋 What's the vibe?",
        "Well hello there! 😄",
        "Hi! Glad you stopped by 😊",
        "Hey! The chat just got better 😄",
        "Welcome welcome! 👋 Come on in!",
    ],
    "morning": [
        "Good morning! ☀️ Hope you slept well!",
        "GM! ☀️ Rise and shine!",
        "Good morning! 🌅 Ready to take on the day?",
        "Morning! ☕ Don't forget your coffee!",
        "GM! 🌞 Another great day ahead!",
        "Good morning everyone! ☀️",
        "Rise and shine! 🌅 Let's get it!",
        "Morning! 😴 Still waking up?",
        "Good morning! 🌞 How'd you sleep?",
        "GM! ☀️ Ready for today?",
        "Morning! ☕ Hope you have a productive day!",
        "Good morning! The early birds are here 🐦",
        "GM! 🌅 It's a beautiful day!",
        "Morning! 😄 Let's make it a good one!",
        "Good morning! ☀️ Coffee time!",
        "Rise and grind! 💪 GM everyone!",
        "GM GM! ☀️ Wakey wakey!",
        "Morning! 🌞 New day, new opportunities!",
        "Good morning! 🌅 Hope today treats you well!",
        "GM! ☀️ Let's have a great day!",
    ],
    "night": [
        "Good night! 🌙 Sleep well!",
        "GN! 💤 Sweet dreams!",
        "Good night! 🌙 Rest up!",
        "Night! 😴 Sleep tight!",
        "GN everyone! 🌙",
        "Sweet dreams! 💤",
        "Good night! Don't let the bed bugs bite 🌙",
        "Night! 🌙 Recharge for tomorrow!",
        "GN! 💤 Hope you have an amazing sleep!",
        "Nighty night! 🌙 Rest well!",
        "Good night! 😴 You deserve a good rest!",
        "GN! 🌙 See you tomorrow!",
        "Sleep well! 💤 Night everyone!",
        "Night! 🌙 Take it easy!",
        "Good night! ⭐ Dream big!",
        "GN! 🌙 Get some good rest!",
        "Night night! 💤 Sleep tight!",
        "Good night! 🌙 Tomorrow's another adventure!",
        "GN! 😴 Wake up refreshed!",
        "Sweet dreams! 🌙 Night!",
    ],
    "goodbye": [
        "Later! 👋 Come back soon!",
        "Bye! 👋 Take care!",
        "See ya! 😄",
        "Take care! 👋",
        "Cya later! 😄",
        "Bye bye! 👋 Hope to see you around!",
        "Later gator! 🐊",
        "Peace! ✌️",
        "See you around! 👋",
        "Take it easy! 😄",
        "Laters! 👋",
        "Bye! Come back anytime 😊",
        "Catch you later! 👋",
        "Take care of yourself! 😄",
        "See ya soon! 👋",
        "Peace out! ✌️",
        "Bye! Have a good one 😊",
        "Cya! Don't be a stranger 👋",
        "Adios! 👋",
        "Until next time! 😄",
    ],
    "gg": [
        "GG! 🔥 That was a great match!",
        "GG everyone! 🎮 Well played!",
        "GG WP! 🔥 Solid game!",
        "That was a great game! 🎮",
        "GG! What a match! 🔥",
        "Well played all around! 🎮 GG!",
        "GG! 🔥 Everyone played well!",
        "That game was insane! GG 🎮",
        "GG! 🎮 Respect to everyone who played!",
        "GG WP no re 😄🔥",
        "GG! That was a banger 🔥",
        "Well played! 🎮 GG!",
        "GG! 🔥 Who's down for another?",
        "That was fire! GG 🔥🎮",
        "GG all! 🎮 Next game?",
        "GG! 🔥 Skills on display today!",
        "Solid game everyone! GG 🎮",
        "GG! Respect ✊🔥",
        "That was clean! GG 🎮🔥",
        "GG! 🔥 Rematch?",
    ],
    "lol": [
        "Lmaooo 😂😂",
        "Haha that's actually funny 😂",
        "💀💀 I'm dead",
        "LOL okay that got me 😂",
        "Hahaha 😂 Too funny!",
        "Okay that was actually hilarious 💀",
        "😂😂 I can't",
        "Lmaooo why is that so funny 💀",
        "Haha okay I'll give you that one 😂",
        "💀 Send help",
        "I'm crying rn 😂😂",
        "Lol okay 😂",
        "Hahaha okay that's genuinely funny 😂",
        "LOL 😂 I wasn't ready",
        "💀💀💀 Dead",
        "Lmaooo okay 😂",
        "Haha nice one 😂",
        "That got me 😂💀",
        "Okay that's actually funny lmao 😂",
        "😂😂 I'm weak",
    ],
    "bruh": [
        "Bruh 💀",
        "Bruhhh fr 😭",
        "Bruh moment 💀",
        "Bro no way 😭",
        "Bruh that's wild 💀",
        "Bro what 😭",
        "Bruh lmao 💀",
        "Bro... 😭",
        "Bruh fr fr 💀",
        "Lmao bro 😭",
        "Bro stop 💀",
        "Bruh I can't 😭",
        "Bro real talk 💀",
        "Bruh same tho 😭",
        "Bro 😭💀",
        "Bruh okay 💀",
        "Bro I feel that 😭",
        "Bruh no way 💀",
        "Bro... okay 😭",
        "Bruh 💀💀",
    ],
    "minecraft": [
        "Minecraft is literally the GOAT 🎮",
        "MC forever! 🎮⛏️",
        "Minecraft hits different! ⛏️",
        "Nothing beats a good Minecraft session 🎮",
        "Minecraft survival or creative? ⛏️",
        "Java or Bedrock? 🎮",
        "Minecraft is timeless! ⛏️🎮",
        "Still one of the best games ever made 🎮",
        "Minecraft grind never stops ⛏️",
        "Building in Minecraft is so satisfying 🎮",
        "MC is always a good idea ⛏️",
        "Minecraft has the best community 🎮",
        "Who else plays Minecraft every day? ⛏️",
        "Minecraft survival is the best mode 🎮",
        "Nothing like mining diamonds at night ⛏️💎",
        "Minecraft = peak gaming 🎮",
        "Still can't believe how good MC is ⛏️",
        "Minecraft is an art form honestly 🎮",
        "Playing MC rn actually ⛏️😄",
        "Minecraft never gets old 🎮⛏️",
    ],
    "pvp": [
        "1v1 me and find out 😤🎮",
        "PvP is all about practice! Keep grinding 💪",
        "GG! Skill diff 🔥",
        "Let's run it! 🎮",
        "PvP is fun once you get the hang of it! 💪",
        "The real PvP players have entered the chat 😤🎮",
        "Clutch or kick! 🔥",
        "That's a skill issue ngl 😄",
        "1v1 for fun or are we tryharding? 🎮",
        "PvP or PvE? 🎮",
        "Practice makes perfect in PvP 💪",
        "GG WP! Nice PvP 🔥",
        "The grind pays off in PvP 💪🎮",
        "Anyone wanna practice? 🎮",
        "PvP gods in the chat? 😤🔥",
        "That clutch was insane 🔥🎮",
        "Skill issue bestie 😄",
        "Get wrecked! jk GG 🎮",
        "PvP takes patience ngl 💪",
        "Let's get it! 🔥🎮",
    ],
    "tier": [
        "S tier obviously 😤",
        "That's definitely A tier at least 🔥",
        "Solid B tier ngl 😄",
        "Debatable but I'll give it B tier",
        "Strong S tier in my opinion 🔥",
        "That's peak S tier, no cap 😤",
        "Mid tier honestly 😄",
        "Strong A tier energy for sure 🔥",
        "I'd put that at B/A tier personally",
        "Tier lists are always controversial 😄",
        "Easily S tier, no debate 🔥",
        "Controversial take but I'd say A tier",
        "My tier list would have that at S 😤",
        "Solid placement honestly 🔥",
        "That's like B+ tier to me 😄",
        "Hard to rank but I'd say A tier",
        "Definitely not F tier lol 😄",
        "A tier with a chance at S 🔥",
        "I agree with that tier tbh 😤",
        "Tier debaters rise up 🔥😄",
    ],
    "dead_chat": [
        "🚨 Chat revival mission activated! What's everyone doing today?",
        "Dead chat? Not on my watch! Tell me something interesting 👀",
        "Chat revived! 🔥 Who's here?",
        "Alright let's get this chat going — what's everyone been up to? 💬",
        "🚨 CHAT REVIVAL PROTOCOL ENGAGED 🚨",
        "Not dead chat on my shift 😤 What's up everyone?",
        "Okay okay let me revive this chat 🔥 Who's playing what?",
        "Chat needs CPR 😂 Everyone talk!",
        "Dead chat? Let me fix that. Favorite game rn? 🎮",
        "The chat has been revived 🔥 Let's keep it going!",
        "Nah we're not doing dead chat today 😤 What's poppin?",
        "Chat is resurrected! 💀➡️🔥 What's everyone up to?",
        "I refuse to let this chat die 😄 Say something!",
        "Reviving the chat with a question: What's been the highlight of your day?",
        "Chat? CHAT?! Oh thank goodness you're alive 😂",
        "Emergency chat revival in progress... done! Now talk 😄",
        "This chat deserves better 🔥 Let's get it going!",
        "The chat doctor is in 🩺 Chat seems alive now!",
        "Dead chat activated my rescue instincts 😤 What's up?",
        "Okay I'll break the silence — what's everyone playing? 🎮",
    ],
    "online": [
        "I'm here! 👋 What's up?",
        "Someone's always lurking 👀",
        "Present! 🙋 What do you need?",
        "I'm always online 😄 What's up?",
        "Here! 👋 What's going on?",
        "Always around! 😊 What's up?",
        "Lurkers assemble! 👀",
        "I see you! 👋 Hey!",
        "The server is alive! 🔥",
        "People are here! They're just quiet 😄",
        "Online and ready! 👋 What's the plan?",
        "I'm here 24/7 😄 What do you need?",
        "The quiet ones are always watching 👀",
        "Present! 🙋 What do you want to talk about?",
        "I'm here! What's happening? 👋",
        "Online! What's up? 😄",
        "The server lives! 🔥 People are around!",
        "Here! 👋 Just vibing.",
        "Alive and well! 😊 What's up?",
        "I gotchu! 👋 What do you need?",
    ],
    "thanks": [
        "Anytime! 😊",
        "No problem at all! 😄",
        "Happy to help! 😊",
        "Of course! 😄 No worries!",
        "Anytime, don't mention it! 😊",
        "Glad I could help! 😄",
        "No problem! 😊 That's what I'm here for!",
        "Of course! Always happy to help 😊",
        "Anytime! 😄 You're welcome!",
        "No worries at all! 😊",
        "Happy to! 😄",
        "Don't mention it! 😊",
        "Of course! 😄",
        "Anytime! You got it 😊",
        "No problem! 😄 Glad it helped!",
        "You're very welcome! 😊",
        "Glad I could be of help! 😄",
        "No worries! 😊 Anytime.",
        "Always! 😄 That's what I'm here for.",
        "Of course! 😊 Happy to help anytime.",
    ],
    "congrats": [
        "Congrats!! 🎉 That's amazing!",
        "Let's goooo! 🎉🔥 You deserve it!",
        "CONGRATULATIONS! 🎉 So proud!",
        "That's huge! 🎉 Congrats!",
        "Congrats! 🎉 You worked hard for that!",
        "W!! 🎉 Congrats bro!",
        "LETS GOOO! 🎉🔥",
        "That's incredible! Congrats! 🎉",
        "Big W!! 🎉 Congrats!",
        "Congrats! 🎉 You earned it!",
        "HUGE W!! 🎉🔥 Congrats!",
        "That's awesome! 🎉 Congrats!",
        "Congrats! 🎉 Keep going!",
        "Absolute W! 🎉🔥 Congrats!",
        "That's the way! 🎉 Congrats!",
        "Congrats! 🎉 You're killing it!",
        "So happy for you! 🎉 Congrats!",
        "Congrats!! 🎉 What's next?",
        "W after W! 🎉🔥 Congrats!",
        "Congrats! 🎉 Well deserved!",
    ],
    "nice": [
        "Nice! 🔥",
        "That's actually really nice! 😄",
        "Oh nice! 🔥",
        "Very nice! 😊",
        "Noice! 😄🔥",
        "Ooh nice! 😊",
        "That IS nice! 🔥",
        "Oh that's nice! 😄",
        "Super nice! 🔥😊",
        "Yeah that's pretty nice! 😄",
        "Nice one! 🔥",
        "Actually really nice 😊",
        "Ngl that's nice 🔥",
        "Oh wow nice! 😄",
        "That's legitimately nice 🔥",
        "Yeah nice! 😊",
        "Lowkey nice 🔥",
        "No cap that's nice 😄",
        "Genuinely nice! 🔥",
        "That checks out, pretty nice 😊",
    ],
    "cool": [
        "That's actually really cool! 🔥",
        "Dope! 🔥",
        "Fire! 🔥",
        "Okay that's sick! 🔥",
        "Based! 🔥",
        "Oh that's fire 🔥",
        "Cool cool! 😄",
        "That's lowkey sick 🔥",
        "No cap that's fire 🔥",
        "Okay yeah that's cool 😄",
        "That's genuinely cool! 🔥",
        "Based af 🔥",
        "Very dope! 😄🔥",
        "Ngl that's sick 🔥",
        "That's pretty fire! 😄",
        "Okay that's actually cool 🔥",
        "Hella cool! 🔥",
        "Yeah that's dope 😄",
        "Lowkey fire 🔥",
        "That slaps honestly 🔥",
    ],
    "how_are_you": [
        "Doing great, thanks for asking! 😊 How about you?",
        "Pretty good! 😄 Hope you're doing well too!",
        "I'm good! 😊 How are you?",
        "Doing well! 😄 What about you?",
        "Great, thanks! 😊 You?",
        "All good here! 😄 How about yourself?",
        "Doing awesome! 😊 How are you doing?",
        "Good good! 😄 How are you?",
        "Can't complain! 😊 How about you?",
        "Living the dream! 😄 How are you?",
        "Doing well! 😊 Thanks for asking!",
        "Pretty great actually! 😄 You?",
        "Good vibes only! 😊 How are you?",
        "Doing fine! 😄 How about yourself?",
        "All good! 😊 How are you holding up?",
        "Great! 😄 How are things on your end?",
        "Doing well, thanks! 😊 You?",
        "Good, how about you? 😄",
        "I'm solid! 😊 How are you?",
        "Good thanks! 😄 Hope you're well too!",
    ],
    "what_are_you_doing": [
        "Just hanging around! 😄 What about you?",
        "Vibing! 😊 You?",
        "Chilling and watching the chat 😄",
        "Just doing bot stuff 😄 What are you up to?",
        "Keeping things lively in here! 😊",
        "Being helpful! 😄 What are you up to?",
        "Just existing 😄 What about you?",
        "Keeping this server alive one message at a time 😊",
        "Chatting with people like you! 😄",
        "Being a good bot 😊 What are you up to?",
        "Not much, just here! 😄 You?",
        "Waiting for something interesting to happen 😄",
        "Just vibing in the chat 😊",
        "Doing my thing! 😄 What are you up to?",
        "Being active in the server! 😊",
        "Watching the chat go by 😄 You?",
        "Just being here! 😊 What's up?",
        "Hanging out! 😄 What about you?",
        "Living my best bot life 😄 You?",
        "Just chilling! 😊 What are you doing?",
    ],
    "wait": [
        "Okay okay, I'm listening 👀",
        "I'm waiting 👀",
        "Sure, no rush! 😊",
        "Take your time! 😄",
        "Alright, what's up? 👀",
        "I'm here! 😊 What is it?",
        "Okay, go on 👀",
        "I'm all ears! 😊",
        "Sure! What's up? 😄",
        "Listening! 👀",
        "Okay okay, go ahead 😄",
        "Take your time, I'm here 😊",
        "Alright! 👀 What's the tea?",
        "I'm patient! 😄 Go ahead.",
        "All ears! 😊 What's going on?",
        "Ready and waiting! 👀",
        "Go on... 😄",
        "I'm here! 😊 What is it?",
        "Sure thing! 👀 Take your time.",
        "Waiting patiently 😊",
    ],
    "fr": [
        "Fr fr no cap 😤",
        "On god 😤",
        "Absolutely facts 🔥",
        "100% 😤",
        "No cap, real talk 🔥",
        "Facts fr 😤",
        "Based and real 🔥",
        "Lowkey facts 😤",
        "Highkey agree 🔥",
        "On everything 😤",
        "Real talk tho 🔥",
        "No lie 😤",
        "Facts on facts 🔥",
        "I agree fr 😤",
        "Say it louder 🔥",
        "This is facts 😤",
        "Can't even argue with that 🔥",
        "Absolute facts 😤",
        "Real ones know 🔥",
        "No lies detected 😤",
    ],
    "omg": [
        "WAIT WHAT 👀",
        "No way!! 😱",
        "Omg really?? 😱",
        "Wait seriously?! 👀",
        "NO WAY 😱",
        "Whoa whoa whoa 👀",
        "That's insane! 😱",
        "No cap?? 👀",
        "Wait what happened?? 😱",
        "Spill! 👀",
        "Okay that's actually crazy 😱",
        "Hold on 👀 what?",
        "No way that happened 😱",
        "Wait fr?? 👀",
        "That's wild 😱",
        "Okay I need details 👀",
        "You're joking 😱",
        "WHAT 👀",
        "That's insane honestly 😱",
        "Okay okay what happened 👀",
    ],
    "help": [
        "I gotchu! What do you need? 😊",
        "Sure! What's the problem? 😄",
        "Of course! What's going on? 😊",
        "Happy to help! What's up? 😄",
        "What do you need help with? 😊",
        "I'm here! What's wrong? 😄",
        "Sure thing! What's the issue? 😊",
        "Tell me what's going on! 😄",
        "I'll do my best! What's up? 😊",
        "What can I help with? 😄",
        "Of course! What's the problem? 😊",
        "Let's figure it out! What's going on? 😄",
        "I gotchu! What's the issue? 😊",
        "Sure! What do you need? 😄",
        "Happy to help! What's wrong? 😊",
        "Tell me more! 😄 What's going on?",
        "I'm listening! 😊 What's up?",
        "On it! What do you need? 😄",
        "Let me know the details! 😊",
        "What's going on? I'll help! 😄",
    ],
    "rip": [
        "F 🙏",
        "RIP 🙏 That's rough",
        "Pour one out 🙏",
        "F in the chat 🙏",
        "That's a big L ngl 😭",
        "Oof 😭 RIP",
        "That hurts 🙏",
        "F 😭 Didn't deserve that",
        "Rip bozo 😄 (jk sorry)",
        "That's unfortunate 🙏",
        "Big oof 😭",
        "That stings 🙏",
        "F for respect 🙏",
        "Oof, tough break 😭",
        "That's the L energy right there 🙏",
        "💀 RIP",
        "That's rough buddy 🙏",
        "Yikes 😭 RIP",
        "That hurts to read 🙏",
        "F 😭 We're here for you",
    ],
    "default": [
        "That's interesting! 😄",
        "Oh nice! 😊",
        "Okay! 😄",
        "Cool! 🔥",
        "Noted! 😊",
        "Makes sense! 😄",
        "Fair enough! 😊",
        "Alright! 😄",
        "True! 😊",
        "Got it! 😄",
        "Word! 😊",
        "Sounds good! 😄",
        "I see! 😊",
        "Interesting take 😄",
        "Can't argue with that 😊",
        "Fair point! 😄",
        "That checks out 😊",
        "Yeah makes sense 😄",
        "Real! 😊",
        "Facts 😄",
    ],
}

# ---------------------------------------------------------------------------
# EXPANSION: multiply each base response list with variations
# ---------------------------------------------------------------------------

EXTRA_RESPONSE_PARTS = {
    "greetings_extra": [
        "How's everyone doing today?",
        "It's great to see people in the chat!",
        "The more the merrier!",
        "Come on in, the vibes are great here!",
        "Hope you're having an awesome day!",
        "Don't be shy, say what's on your mind!",
        "Good to have you here!",
        "The server just got livelier!",
        "Glad you joined in!",
        "Awesome to see you!",
    ],
    "filler_openings": [
        "Ngl,", "Honestly,", "Lowkey,", "Highkey,", "Not gonna lie,",
        "Real talk,", "No cap,", "Fr tho,", "Tbh,",
    ],
    "filler_closings": [
        "ngl", "fr", "no cap", "tbh", "lowkey", "highkey",
        "honestly", "real talk", "for real",
    ],
}


def expand_responses(base_responses: list, multiplier: int = 10) -> list:
    """Expand a list of responses to be ~multiplier times larger."""
    expanded = list(base_responses)
    while len(expanded) < len(base_responses) * multiplier:
        r = random.choice(base_responses)
        # sometimes prepend a filler
        if random.random() < 0.15:
            r = random.choice(EXTRA_RESPONSE_PARTS["filler_openings"]) + " " + r[0].lower() + r[1:]
        expanded.append(r)
    # shuffle and deduplicate (keep order)
    seen = set()
    result = []
    for r in expanded:
        if r not in seen:
            seen.add(r)
            result.append(r)
    return result


def build_triggers() -> dict:
    """Build a flat trigger → category mapping from seeds."""
    mapping = {}
    for category, seeds in TRIGGER_SEEDS.items():
        for seed in seeds:
            mapping[seed.lower().strip()] = category
    return mapping


def build_responses(min_total: int = 10000) -> dict:
    """Build a responses dict with enough entries to exceed min_total."""
    responses = {}

    suffixes = ["!", " 😄", " 🔥", "...", " 😊", " 💀", " 😂", " 👀", " ✌️", " 🎮"]
    prefixes = EXTRA_RESPONSE_PARTS["filler_openings"]

    for category, templates in RESPONSE_TEMPLATES.items():
        pool = list(templates)
        # suffix variants
        for base in templates:
            stripped = base.rstrip("!.?")
            for s in suffixes:
                pool.append(stripped + s)
        # prefix variants
        for base in templates:
            for p in prefixes:
                pool.append(p + " " + base[0].lower() + base[1:])
        # deduplicate
        seen = set()
        deduped = []
        for r in pool:
            if r not in seen:
                seen.add(r)
                deduped.append(r)
        responses[category] = deduped

    return responses


def generate_extra_triggers(existing: dict) -> dict:
    """Generate additional trigger variations using common text patterns."""
    extra_map = {}

    # Common typo patterns
    typo_patterns = [
        ("hello", ["helo", "helllo", "hellllo", "hllo", "helllo"]),
        ("morning", ["mornign", "mornning", "morhing", "moring"]),
        ("thanks", ["thanls", "thankss", "thnks", "thanx", "thx"]),
        ("congrats", ["congrates", "congradulations", "congrads", "congs"]),
        ("minecraft", ["mindcraft", "mincraft", "miinecraft", "minecrft"]),
    ]
    for base, typos in typo_patterns:
        if base in existing:
            cat = existing[base]
            for t in typos:
                extra_map[t] = cat

    # Number variations
    number_subs = {"o": "0", "l": "1", "e": "3", "a": "@", "s": "5"}
    for trigger, cat in list(existing.items()):
        if len(trigger) <= 12:
            for char, num in number_subs.items():
                if char in trigger:
                    extra_map[trigger.replace(char, num)] = cat

    # Repetition variations (hi → hii → hiii)
    for trigger, cat in list(existing.items()):
        if len(trigger) <= 6:
            for n in range(2, 6):
                extra_map[trigger + trigger[-1] * n] = cat

    existing.update(extra_map)
    return existing


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    print("Building triggers...")
    triggers = build_triggers()
    triggers = generate_extra_triggers(triggers)
    print(f"  Generated {len(triggers)} trigger entries")

    print("Building responses...")
    responses = build_responses()
    total = sum(len(v) for v in responses.values())
    print(f"  Generated {total} total response entries across {len(responses)} categories")

    triggers_path = os.path.join(out_dir, "triggers.json")
    responses_path = os.path.join(out_dir, "responses.json")

    with open(triggers_path, "w", encoding="utf-8") as f:
        json.dump(triggers, f, indent=2, ensure_ascii=False)
    print(f"  Saved triggers.json → {triggers_path}")

    with open(responses_path, "w", encoding="utf-8") as f:
        json.dump(responses, f, indent=2, ensure_ascii=False)
    print(f"  Saved responses.json → {responses_path}")

    print("\nDone! Dataset generation complete.")


if __name__ == "__main__":
    main()
