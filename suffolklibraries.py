#!/usr/bin/python
#Console client for the Suffolk Libraries website
#Uses Python Selenium and PhantomJS
#By Charles Bos

from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import datetime
import os

def showHelp() :
    print('''Suffolk Libraries console commands\n-----\n
login          Login in to your Suffolk Libraries account. 
               If stored credentials are found, the process will be automatic.\n
logout         Logout of your Suffolk Libraries account.\n
show loans     Show all loans on your account.\n
show urgent    Show all loans due in the next seven days.\n
exit           Close the program.\n
help           Show this dialog.''')

def home() :
    browser.get("https://suffolk.spydus.co.uk/cgi-bin/spydus.exe/MSGTRN/OPAC/LOGINB")

def getCredentials() :
    creds = []
    if os.path.exists(credFile) :
        file = open(credFile, "r")
        contents = file.read()
        contents = contents.split("\n")
        contents = [x for x in contents if x != '']
        for x in contents :
            y = x.split(" = ")
            creds.append(y[1].strip())
        file.close()
        return creds
    else :
        username = input("Please enter your library card number: ")
        password = input("Please enter your pin number: ")
        store = input("Would you like to remember these credentials? [y/n] ")
        if store == "y" :
            file = open(credFile, "w")
            file.write("id = " + username + "\npin = " + password)
            file.close()
        creds.append(username), creds.append(password)
        return creds

def login(browser, creds) :
    username = browser.find_element_by_id("BRWLID")
    password = browser.find_element_by_id("BRWLPWD")
    loginButton = browser.find_element_by_class_name("inputSubmit")
    username.send_keys(creds[0])
    password.send_keys(creds[1])
    loginButton.click()
    #Check that login succeeded
    htmlString = str(BeautifulSoup(browser.page_source, "html.parser"))
    if htmlString.find("Invalid ID or PIN, please try again.") != -1 :
        print("\nInvalid login. Stored credentials will now be removed. Please try again.")
        try :
            os.remove(credFile)
        except IOError :
            pass
        return False
    else : return True

def logout(browser) :
    logoutButton = browser.find_element_by_link_text("Logout")
    logoutButton.click()
    
def getLoans(browser) :
    try :
        currentLoans = browser.find_element_by_link_text("Current loans")
        currentLoans.click()
    except selenium.common.exceptions.NoSuchElementException :
        pass

    htmlString = str(BeautifulSoup(browser.page_source, "html.parser"))
    loanList = []
    titleStart = htmlString.find('''NAVLVL=SET">''')
    titleEnd = htmlString.find("</a>", titleStart)
    dateStart = htmlString.find('''<td align="center">''', titleEnd)
    dateEnd = htmlString.find("<br/>", dateStart)
    while 0 <= titleStart <= len(htmlString) :
        title = htmlString[titleStart + 12:titleEnd]
        date = htmlString[dateStart + 19:dateEnd]
        loanList.append((title, date))
        titleStart = htmlString.find('''NAVLVL=SET">''', titleEnd)
        titleEnd = htmlString.find("</a>", titleStart)
        dateStart = htmlString.find('''<td align="center">''', titleEnd)
        dateEnd = htmlString.find("<br/>", dateStart)

    return loanList

def showLoans(loans, urgency) :
    if urgency == False :
        if loans != [] :
            print("All loans\n-----\nTitle" + (" " * 45) + "Due: ")
            for x in loans : print("{:50s}".format(x[0]) + x[1])
        else : print("No loans")
    else :
        urgent = []
        for x in loans :
            y = x[1]
            y = datetime.datetime.strptime(y, "%d %b %Y").date()
            margin = datetime.timedelta(days = 7)
            if datetime.date.today() <= y <= datetime.date.today() + margin : urgent.append(x)
        if urgent == [] : print("No urgent loans")
        else :
            print("\nUrgent loans\n-----\nTitle" + (" " * 45) + "Due: ")
            for x in urgent : print("{:50s}".format(x[0]) + x[1])

def runCommand(command) :
    global loginStatus
    if command == "help" : showHelp()
    if command == "login" :
        if not loginStatus :
            home()
            creds = getCredentials()
            loginStatus = login(browser, creds)
        else : print("You are already logged in.")
    if command == "logout" :
        if loginStatus == False : print("You are not logged in.")
        else :
            logout(browser)
            loginStatus = False
    if command == "show loans" :
        if loginStatus == False : print("You are not logged in.")
        else :
            loans = getLoans(browser)
            showLoans(loans, False)
    if command == "show urgent" :
        if loginStatus == False : print("You are not logged in.")
        else :
            loans = getLoans(browser)
            showLoans(loans, True)

if __name__ == "__main__" :
    #Vars
    homeDir = os.path.expanduser("~")
    credFile = homeDir + "/.suffolklibraries"
    commands = ["help", "login", "logout", "show loans", "show urgent", "exit"]
    browser = webdriver.PhantomJS()
    global loginStatus
    loginStatus = False

    #Start console
    print("Welcome to the Suffolk Libraries console! Enter 'help' to show commands.\n")
    command = True
    while command != "exit" :
        command = input("[Suffolk Libraries]: ")
        if command not in commands : print("Command not found.")
        else : runCommand(command)

    #Cleanup
    try :
        os.remove("ghostdriver.log")
    except IOError :
        pass
