#Let's import the required modules
from sys import exit
from time import sleep
from random import randint
#DHTrivia is used to hold all of the trivia questions
#asked periodically of the user
import DHTrivia
#The DHImage_pools module is used
#to hold all of the ASCII art present throughout the game
import DHImage_pools

# This section actually calls the classes and their functions
# It also keeps an eye on the player's health.
# If health ever == 0, then the death class is run and the game
# is over. Too bad, so sad.
#*************************SYSTEM********************
class the_brain:
    def play(self, game_map, next_scene, life, money, weapon):
        #Every function in each of the classes returns values for life, money and
        #weapons. In this way, the game is continually updated
        #To health lost/gained, weapons changed, money earned
        output = game_map.get(next_scene)
        output, health, snogs, weapon = output.scene_contents(life, money, weapon)
        if health > 0 or next_scene == 'overview':
#keep printing the player's health, money and weapon in use
            print(f'''
Health: {health}
Snogs: {snogs}
Weapon: {weapon}
            ''')
            return(output, health, snogs, weapon)
        #if the user's health ever == 0, player is dead
        else:
            return('death')

#*************************START********************
#This class will only run if the user dies
class death:
    def scene_contents(self, life, money, weapon):
        print("You are...\nDEAD")
        exit(0)

#Here is the start of the game
#Introducing the user to currency, life etc
class overview:
    def scene_contents(self, life, money, weapon):
        print(DHImage_pools.knight)
        life = 100
        money = 0
        weapon = 'mallet'
        #Here's what's up
        print(f'''
You are a noble warrior from afar come to vanquish
an evil dragon that has been terrorizing the local
villagers. As you were traveling to the village you
stopped for a nap and cows stole all of your armor
and weapons. In return the cows left you with a
wooden mallet. In order to vanquish the dragon you
must earn snogs to purchase more armor and and a
better weapon.

Health: {life}
Snogs: {money}
Weapon: {weapon}
        ''')
        #wait for the user to continue
        input('>')
        return('start', health, money, weapon)

#Do you want to go to the beach or the woods?
class start_scene:
    def scene_contents(self, life, money, weapon):
        sleep(1)
        print('''
You find yourself on a beach. One path continues along
the shore and the other path goes into the woods.
Do you:
        ''')
        print("s) Follow the shore")
        print("w) Go into the woods")
        choice = input('>')
        if choice == 's':
            return('shore start', life, money, weapon)
        elif choice == 'w':
            return('woods start', life, money, weapon)
        else:
            print(f"I do not understand what {choice} means")
            return('start', life, money, weapon)


#Here are the classes for the shore
#*************************SHORE********************
class shore_start:
    def scene_contents(self, life, money, weapon):
        print("You walk along the beach until you meet a fisherman.")
        sleep(2)
        print(DHImage_pools.fisherman)
        input('>')
        print('''
Fisherman: Hello there. I could use some help.
Do you want to work for me?
	''')
        #throughout the game, most of the yes or no questions
        #also have a third option m (for maverick). This third
        #option allows the user to break the rules. Sometimes
        #The maverick is beneficial... sometimes it is
        #detrimental. Depends on the case.
        choice = input('(y/n/m)\n>')
        if choice == 'y':
            return('fisherman y', life, money, weapon)
        elif choice == 'n':
            return('cow', life, money, weapon)
        elif choice == 'm':
            return('fisherman m', life, money, weapon)
        else:
            print(f'I do not know what {choice} means')
            return('shore start', life, money, weapon)



    #Either go to fisher man y or fisher man m
    #if no, go to cow

#Do you want to go fishing?
class fisher_man_y:
    def scene_contents(self, life, money, weapon):
        print('''
Fisherman: Wonderful!
The dragon stole all of my fish stores.
We need to go out in my boat to catch
some fish for my family.''')
        input('>')
        #the scenario variable is a random integer that is used
        #to select one of 3 possible scenarios
        scenario = randint(0, 2)
        if scenario == 0:
            print('''
You spend all day fishing but don't catch anything.
Fisherman: Thank you for your help. Too bad we didn't
catch anything this time.
		''')
            input('>')
            return('cow', life, money, weapon)
        elif scenario == 1:
            print(DHImage_pools.fish)
            print('''
You cast your nets in a promising location.
After some time you pull up the nets to find
a bountiful catch of nark-gills, a great
delicacy in the area.
Fisherman: This is wonderful! Here are 20 snogs
for your help. (Snogs + 20)
            ''')
            money += 20
            input('>')
            return('cow', life, money, weapon)
        elif scenario == 2:
            print('''
The fisherman says that turtles can be found
in the swamp, so you go and cast the nets in
the nearby marsh. As you pull up the nets you
find yourself face to face with a baby alligator.
You were bitten by an alligator (Health - 20)
            ''')
            life -= 20
            input('>')
            return('cow', life, money, weapon)



class fisher_man_m:
    def scene_contents(self, life, money, weapon):
        print(f'''
My what a rebel you are.
You take your {weapon} and start attacking
the fisherman. Although initially surprised
the fisherman proceeds to pull out his knife
and chase you into the woods. (Health -= 15)
        ''')
        life -= 15
        return('woods start', life, money, weapon)

class cow:
    def scene_contents(self, life, money, weapon):
        print("You continue walking along the shore until you meet a cow.")
        sleep(2)
        print(DHImage_pools.cow)
        print('''
Cow: Hello there.
Do you want to answer a trivia question?\n''')

        choice = input("y/n/m\n>")
        if choice == 'y':
            return('cow y', life, money, weapon)
        elif choice == 'n':
            return('dark forest', life, money, weapon)
        elif choice == 'm':
            return('cow m', life, money, weapon)
        else:
            print(f"I do not know what {choice} means")
            return('cow', life, money, weapon)


class cow_y:
    def scene_contents(self, life, money, weapon):
        number = randint(0, len(DHTrivia.cow_questions)-1)
        #When asking the question, it is popped from the list
        #to remove the possiblity of asking the same question
        #twice
        answer = DHTrivia.cow_answers.pop(number)
        question = DHTrivia.cow_questions.pop(number)
        print(question)
        choice = input(">")

        #if the user gets the question wrong, they get kicked
        #and lose 5 health
        if choice != answer:
            print(f'''
Cow: Wow... That was wrong. The right answer is {answer}
The cow roundhouse kicks you in the stomach. Health - 5
''')
            life -=5
            sleep(2)
            return('dark forest', life, money, weapon)
        #if the user gets the question correct, the cow
        #gives them a sword... better than that mallet
        else:
            print('''
Cow: Nicely done! You clearly know your cow trivia.
Here is an iron sword for your knowledge.''')
            weapon = 'sword'
            sleep(2)
            return('dark forest', life, money, weapon)


#if the user wants to be a rebel, they can use their
#weapon to attack the cow... because.... Well. I'm not
#sure why...
class cow_m:
    def scene_contents(self, life, money, weapon):
        print(f'''
You use your {weapon} and attack the cow.
Turns out the cow was a master in kung-fu (health -10)
Eventually you overcome and eat burgers for dinner (health + 15)
''')
        life +=5
        return('dark forest', life, money, weapon)

#once the cow has been dealt with, the user heads
#into a dark forest
class dark_forest:
    def scene_contents(self, life, money, weapon):
        print('''
After your encounter with the cow you find a
path that heads into a dark forest. Against
your better judgement, you go into the woods.
As you walk deeper and deeper into the forest,
the light fades more and more. Eventually night
falls. You stumble around the woods until you
realise that you are completely lost. Eventaully
your see a speck of light in the distance.
Overjoyed you rush towards it and find a cute
german hut. Do you knock on the door?
''')
        choice = input('y/n/m\n>')
        if choice == 'y':
            return('dark forest y', life, money, weapon)

        elif choice == 'n':
            return('field of cows', life, money, weapon)
#as you can see here... sometimes the maverick
#option can be quite absurd
        elif choice == 'm':
            print('''
You see a fire in the yard in front of the house.
You pick out a partially burning piece of wood
and throw it through the window of the peaceful
hut. Screams issue from the house and a man bursts
out of the house with a shotgun and a pack of
hunting dogs. Seeing you he fires at you (health -15)
and the dogs start chasing you. You run all night
until you find yourself in a feild full of cows.
            ''')
            life -= 15
            return('field of cows', life, money, weapon)
        else:
            print(f"I do not know what {choice} means")
            return('dark forest', life, money, weapon)


class dark_forest_y:
    def scene_contents(self, life, money, weapon):
        print('''
You knock on the front door. Footsteps.
The door opens and a man wearing lederhosen
opens the door.
Man: Hello zere, do vu vant to eat zome of
zis vierner Schitzel?''')
        choice = input("y/n/m\n>")
        if choice == 'y':
            return('schneiders house y', life, money, weapon)
        if choice == 'n':
            return('field of cows', life, money, weapon)
        if choice == 'm':
            return('schneiders house m', life, money, weapon)

#let's eat dinner at schneider's.
#What a lovely place
class schneiders_house_y:
    def scene_contents(self, life, money, weapon):
        print('''
The man introduces himself as Schneider
and brings you inside to share his
Weirner Schnitzel with you. (Health +=5).''')
        input('>')
#oh look. Schneider is willing to help you out
#by gifting a weapon to you. How nice
        print('''
He then goes on to tell you about how
terrible the dragon is and when you
mention that you have come to defeat
the dragon he is overjoyyed and offers:
1) Axe: (25 damage)
2) Mace: (30)
3) Bow and Arrow: (35 damage)
which do you choose?''')
        choice = input('1/2/3\n>')
        if choice == '1':
            print('''Schneider:
Ah ja! Zis axe has peen in zee family
for generazions. May it zerffe vu vell
in your guest to defeat zee drakon.
''')
            weapon = 'axe'
            return("field of cows", life, money, weapon)
        elif choice == '2':
            print('''Schneider:
Ah! Zee mace is ein most boverful
veabon for zee most boverful varrior.
I haffe nein doupt zat it vill aid vu
in your hunt to defeat zee drakon
''')
            weapon = 'mace'
            return("field of cows", life, money, weapon)
#hmmm... the bow is not very good in a fire...
#doesn't the dragon breath fire?
        elif choice == '3':
            print('''
Excellent choice! Zee pow und arrow is
a fery uzeful veabon. Effen zough it
does not do so vell in fire, it is
boverful enough to defeat almost any
enemy
''')
            weapon = 'bow and arrow'
            return("field of cows", life, money, weapon)
        else:
            print(f"I do not know what {choice} means")
            return('schneiders house y', life, money, weapon)

class schneiders_house_m:
    def scene_contents(self, life, money, weapon):
#So yea... if you are a maverick the house no longer belongs to
#schneider... it is instead the house of a great Wizard
        print(f'''
You decide to break the rule yet again.
Using your {weapon} you start attacking
the man and his weirner schnitzel.
Unfortunately for you, the man is a great
wizard and casts a spell making you pass out.
He then teleports you to a field of cows. (Health -20)
''')
        life -=20
        return("field of cows", life, money, weapon)

#well... here is where I need to keep coding.
#guess I should get working on that
class field_of_cows:
    def scene_contents(self, life, money, weapon):
        exit(0)

#*************************WOODS********************
class woods_start:
    def scene_contents(self, life, money, weapon):
        print("THE WOODS")
        exit(0)



#this system class holds a dictionary that acts like the game map
# in each of the ^^ functions, it returns the left part, and then
#the brain class calls the actual part.
class system:

    scenes = {
        'death': death(),
        'overview': overview(),
        'start': start_scene(),
        #**********The shore**********
        'shore start': shore_start(),
        'fisherman y': fisher_man_y(),
        'fisherman m': fisher_man_m(),
        'cow': cow(),
        'cow y': cow_y(),
        'cow m': cow_m(),
        'dark forest': dark_forest(),
        'dark forest y': dark_forest_y(),
        "schneiders house y": schneiders_house_y(),
        "shcneiders house m": schneiders_house_m(),
        "field of cows": field_of_cows(),

        #**********The woods**********
        "woods start": woods_start()

    }
    #These are the weapon's and their assigned damage values
    #I think I will be using these at the end of the game
    #while the user fights the dragon
    weapons = {
    #'weapon': damage
    'mallet': 5,
    'axe': 25,
    'sword': 20,
    'mace': 30,
    'bow and arrow': 50
    }



#*************************RUNNING THE GAME********************
#These are our instances
g_constants = system()
g_smarts = the_brain()

#path is a list of the actions that the user took
path = []

#These is the variable setup at the beginning of the game
g_scene = 'overview'
health = 100
snogs = 0
weapon = 'mallet'
damage  = g_constants.weapons.get('mallet')

#until the game scene = end, this loop continues
#to call the brain class with updated values
while g_scene != 'end':
    g_scene, health, snogs, weapon = g_smarts.play(g_constants.scenes, g_scene, health, snogs, weapon)
    #the path is used as the user history making a record
    #of where the user has been
    path.append(g_scene)
    print(path)
    print(f"g_scene = {g_scene}")