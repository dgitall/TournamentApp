import json
import csv


# Load the string dictionary from the JSON file
StringRscs = {}
with open('stringfile.json') as json_file:
    StringRscs = json.load(json_file)
    
# Create our global dataset for the entrants. Initialize as empty
#global globalEntrants 
globalEntrants = list()
globalSize = 0

# Function to evaluate the loaded f-strings. This is necessary because you can't include
# dictionary keys if doing it inline due to interference with single and double quotes.
# Taken from: https://stackoverflow.com/questions/47597831/python-fstring-as-function
def fstr(fstring_text, locals, globals=None):
    # Dynamically evaluate the provided fstring_text. Passing in locals and globals allows us
    # to access variables to insert into the f string.
    locals = locals or {}
    globals = globals or {}
    ret_val = eval(f'f"{fstring_text}"', locals, globals)
    return ret_val

def MainApplication():
    global globalEntrants
    global globalSize
    globalEntrants = ProgramStartup()
    globalSize = len(globalEntrants)
    
    ApplicationRun = True
    
    while ApplicationRun:
        
        MenuSelection = MainMenu()
        if MenuSelection == 1:
            NewEntrant()
        elif MenuSelection == 2:
            CancelEntrant()
        elif MenuSelection == 3:
            ViewParticipants()
        elif MenuSelection == 4:
            SaveFile()
        elif MenuSelection == 5:
            ApplicationRun = ExitApp()
            
def ProgramStartup():
    # Do the stuff to get started
    print("\n\n"+StringRscs['StartBanner'])
    # Get how big the data set should be
    size = 0
    InvalidEntry = True
    while InvalidEntry:
        size = input(StringRscs['NumParticipantsPrompt'])
        if size.isnumeric():
            size = int(size)
            if size > 0 and size < 100:
                InvalidEntry = False
    
    # Fill the entrant list with the number of desired empty entrants
    size = int(size)
    Entrants = [None] * size

    print(fstr(StringRscs['InitMessage'], locals()))
    return Entrants
  
## Display the main menu and get a selection from the user      
def MainMenu():
    # Display the menu
    print("\n\n" + StringRscs['MainMenu'])
    # Get User selection
    Selection = 0
    InvalidEntry = True
    while InvalidEntry:
        Selection = input(StringRscs['MenuPrompt'])
        # Validate selection
        if Selection.isnumeric():
            Selection = int(Selection)
            if Selection > 0 and Selection <= 5:
                InvalidEntry = False

    return Selection

## Get a new name and slot from the user and add it to the list
def NewEntrant():
    # Display the menu
    print("\n\n" + StringRscs['SignupBanner'])
    EntrantName = ""
    EntrantSlot = 0
    # Get the entrant name from the user
    InvalidEntry = True
    while InvalidEntry:
        EntrantName = input(StringRscs['SignupNamePrompt'])
        # Validate selection
        if not EntrantName.isnumeric():
            ## Do we care of there is a duplicate name?
            if EntrantName not in globalEntrants:
                InvalidEntry = False
            else:
                print(fstr(StringRscs['SingupNameError'], locals(), globals()))
    # Get the entrant slot from the user
    InvalidSlot = True
    while InvalidSlot:
        InvalidEntry = True
        while InvalidEntry:
            EntrantSlot = input(fstr(StringRscs['SignupSlotPrompt'], locals(), globals()))
            # Validate selection
            if EntrantSlot.isnumeric():
                EntrantSlot = int(EntrantSlot)
                if EntrantSlot > 0 and EntrantSlot <= len(globalEntrants):
                    InvalidEntry = False
        EntrantSlot = int(EntrantSlot)
        # Check to see if there is already an entrant in that slot
        if globalEntrants[EntrantSlot-1] == None:
            InvalidSlot = False
        else:
            print("\n" + fstr(StringRscs['SignupSlotError'], locals()))
            
    globalEntrants[EntrantSlot-1] = EntrantName
    print("\n" + fstr(StringRscs['SignupSuccess'], locals()))
    
    return
    
# Get the name and slot for an entrant to remove from the list
def CancelEntrant():
    # Display the menu
    print("\n\n" + StringRscs['CancelBanner'])
    EntrantName = ""
    EntrantSlot = 0
    # Get the entrant name from the user
    InvalidEntry = True
    InvalidMatch = True
    while InvalidMatch:
        while InvalidEntry:
            EntrantName = input(StringRscs['CancelNamePrompt'])
            # Validate selection
            if not EntrantName.isnumeric():
                InvalidEntry = False
        # Get the entrant slot from the user
        InvalidEntry = True
        while InvalidEntry:
            EntrantSlot = input(fstr(StringRscs['CancelSlotPrompt'], locals(), globals()))
            # Validate selection
            if EntrantSlot.isnumeric():
                EntrantSlot = int(EntrantSlot)
                if EntrantSlot > 0 and EntrantSlot <= len(globalEntrants):
                    InvalidEntry = False
        EntrantSlot = int(EntrantSlot)
        # Check to see if the entrant name in the slot matches
        if globalEntrants[EntrantSlot-1] == EntrantName:
            InvalidMatch = False
        else:
            print("\n" + fstr(StringRscs['CancelError'], locals()))

    globalEntrants[EntrantSlot-1] = None 
    print("\n" + fstr(StringRscs['CancelSuccess'], locals()))
    return
    
# Print out a list of the current entries
# User enters the main entry they are interested in and print 5 before and 5 after
def ViewParticipants():
    # Display the banner
    print("\n\n" + StringRscs['ViewBanner'])
    ViewSlot = 0
    # Get the central slot to view from the user
    InvalidEntry = True
    while InvalidEntry:
        ViewSlot = input(fstr(StringRscs['ViewPrompt'], locals(), globals()))
        # Validate selection
        if ViewSlot.isnumeric():
            ViewSlot = int(ViewSlot)
            if ViewSlot > 0 and ViewSlot <= len(globalEntrants):
                InvalidEntry = False
                
    ViewSlot = int(ViewSlot)
    ViewStart = ViewSlot - 5
    if ViewStart <= 0: ViewStart = 0
    ViewEnd = ViewSlot + 5
    if ViewEnd > globalSize: ViewEnd = globalSize
    
    print("\n" + fstr(StringRscs['ViewHeader'], locals()))
    for i in range(ViewStart, ViewEnd):
        if globalEntrants[i] == None:
            Name = "[empty]"
        else:
            Name = globalEntrants[i]
        print(f"{i+1}: {Name}")

    return

# Check that the user wants to to save the file and then do it
def SaveFile():
    # Display the banner
    print("\n\n" + StringRscs['SaveBanner'])
    Choice = 'n'
    InvalidEntry = True
    while InvalidEntry:
        Choice = input(StringRscs['SavePrompt'])
        # Validate selection
        if not Choice.isnumeric():
            if Choice == 'y' or Choice == 'n':
                InvalidEntry = False  
    
    # User said yes to save the file
    if Choice == 'y':
        success = False
        success = Save()
        if not success:
            print(StringRscs['SaveError'])
        
    return

# Save the data to a file
def Save():
    success = True
    
    try:
        with open('save.csv', 'w', newline='') as csvfile:
            fileWriter = csv.writer(csvfile, delimiter=',')
            for i, name in enumerate(globalEntrants):    
                if name == None:  
                    row = [i+1, '[empty]']
                else: 
                    row = [i+1, name]
                fileWriter.writerow(row)    
    except:
        # We could handle a few different type of errors here like the file is open elsewhere
        # But not for this application
        success = False
        
    return success

# Check with the user and exit if they really want to
def ExitApp():
    # Display the banner
    print("\n\n" + StringRscs['ExitBanner'])
    ContinueApp = False
    Choice = 'n'
    InvalidEntry = True
    while InvalidEntry:
        Choice = input(StringRscs['ExitPrompt'])
        # Validate selection
        if not Choice.isnumeric():
            if Choice == 'y' or Choice == 'n':
                InvalidEntry = False

    # User said yes to quit
    if Choice == 'y':
        print(StringRscs['ExitGoodbye'])
    else:
        ContinueApp = True
    
    return ContinueApp

# Main Body
MainApplication()
