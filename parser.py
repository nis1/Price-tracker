from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import configparser
import readline

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent':user_agent}
settingsFile = 'settings.ini'

def printMenu():
    print(15 * "-", "MENU", 15 * "-")
    print('1. Display stored parsers')
    print('2. Add a new parser')
    print('3. Delete parser')
    print('4. Execute parser')
    print('5. Quit')
    print (37 * "-")

def menu():
    '''main menu'''
    printMenu()
    while 1:
        while 1:
            try:
                userInput =  int(input("Enter your choice [1-5]: "))
                break
            except:
                print("That's not a valid option! To see the menu type 0")

        if userInput == 0:
            printMenu()
        elif userInput == 1:
            displayParsers()
        elif userInput == 2:
            addParser()
        elif userInput == 3:
            print('Please type the name of the parser that you wish to remove: ')
            rm = input()
            delParser(rm)
        elif userInput == 4:
            parserName = input('Type the name of the parser for execution: ')
            if parserName not in config:
                print('Wrong name. Please try again')
            else:
                fullAddress = config[parserName]['fullAddress']
                whatToParse = config[parserName]['htmlTag']
                exeParser(fullAddress,whatToParse)
        elif userInput == 5:
            break
        else:
            print("That's not a valid option! To see the menu type 0")


def addParser(first_setup=False):
    '''add new parser'''
    parserName = input("Parser's name: ")
    fullAddress = input("Website address: ")
    whatToParse = input('What to parse? ')
    config[parserName] = {}
    config[parserName]['fullAddress'] = fullAddress
    config[parserName]['htmlTag'] = whatToParse

    print('Testing...\n')

    try:
        htmlTags = exeParser(fullAddress,whatToParse)
        print('Successful!\n')
    except:
        print("Couldn't parse" + str(fullAddress) + '\nwith\n' + str(whatToParse))
        print('Abouting...')
        return

    tagNumber = input('Found ' + str(len(htmlTags)) + " tags. Which one of them do you want to track? 1 for the first one, 2 for the second etc... ")
    if tagNumber == '': tagNumber = '0'
    config[parserName]['tagNumber'] = str(tagNumber)
    writeConfig()

def displayParsers():
    '''display all parser modules'''
    sections = config.sections()
    for item in sections:
        print('\033[1;33;40m' + '['+str(item)+']' + '\033[0;37;40m')
        for key in config[item]:
            print(str(key) + ' = ' + config[item][key])
        print()


def delParser(index):
    '''delete parser'''
    config.remove_section(index)
    writeConfig()

def exeParser(fullAddress,whatToParse,htmlTag=0,text=False):
    '''execute parser'''
    try:
        req = Request(fullAddress, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
    except:
        print('\033[1;31;40m' + " HTTP Request fail for: " + str(fullAddress) + '\033[0;37;40m' + '\n')
        return

    #try:
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    someparsing = soup.select(whatToParse)
    if len(someparsing) == 0:
        print('\033[1;31;40m' + 'No data to parse. Check HTML tags\n' '\033[0;37;40m')
        return
    if text==False:
        print('\033[1;32;40m' + str(someparsing[htmlTag]) + '\033[0;37;40m')
    else:
        print('\033[1;32;40m' + str(someparsing[htmlTag].text) + '\033[0;37;40m')

    print('\n')
    return (someparsing)


def writeConfig():
    '''saves the INI config file'''
    try:
        with open(settingsFile, 'w') as newconfigfile:
            config.write(newconfigfile)
    except:
        raise Exception("Couldn't write to config file. Abouting...\n")


config = configparser.ConfigParser()
config.read(settingsFile)

menu()
