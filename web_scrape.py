import requests
from bs4 import BeautifulSoup
import docx
import os
import configparser
import msvcrt

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

config = configparser.ConfigParser()

def status(status):
    if (str(status)[0] == "2"):
        print(f"Status: {status}")
    elif (str(status)[0] == "4"):
        print(f"Status: {status}")
    else:
        print(f"Status: {status}")

def getSite():
    url = input("URL: ")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        page = requests.get(url, headers=headers)
    except:
        page = requests.get(url)
    status(page.status_code)

    soup = BeautifulSoup(page.content, "html.parser")
    print(f"Title:\n\t{soup.title.text}")
    return soup

def parseSite(soup):
    doc = docx.Document()

    # Get location path
    defaultLoc = input("Use default location? (y/n)").lower()
    if (defaultLoc == "y"):
        config.read('settings.ini')
        location = config["Location"]["defaultPath"]
    else:
        location = filedialog.askdirectory()

    # Compile full file path
    fileName = input("File name: ")
    path = os.path.join(location, f"{fileName}.docx")


    header = soup.find_all("header", class_="entry-header")
    content = soup.find_all("div", class_="entry-content")
    # for items in content:
    #     data = '\n'.join([item.text for item in items.find_all(["h2","p"])])
    #     print(data)

    # Extract main title
    for items in header:
        for item in items.find_all(["h1"]):
            doc.add_heading(item.text, 0)

    # Extract text and headings
    for sections in content:
        for item in sections.find_all(["h2","p", "ul"]):
            if (item.name == "h2"):
                doc.add_heading(item.text)
            elif (item.name == "p"):
                doc.add_paragraph(item.text)
            elif (item.name == "ul"):
                for list in item.find_all(["li"]):
                    doc.add_paragraph(f"- {list.text}")

    doc.save(path)
    print("File saved")

def settings():
    options = "\n 1. Set default folder \n 2. Reset settings \n 3. Back "
    choice = int(input(f"{options}\n > "))

    # Get user input for directory
    if choice == 1:
        config['Location'] = {'defaultPath':f'{filedialog.askdirectory()}'}
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        wait()
    # Set defaultPath to HOME directory
    elif choice == 2:
        config['Location'] = {'defaultPath':f'{os.path.join(os.path.expanduser("~"), "Documents")}'}
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        wait()
    elif choice == 3:
        return
    else:
        print("Invalid option")
        wait()

def wait():
    print("Press Enter...")
    msvcrt.getch()

def menu():
    exit = False
    while not exit:
        os.system('cls')
        options = " 1. Scrape a website \n 2. Settings \n 3. Exit "
        choice = int(input(f"{options}\n > "))

        if choice == 1:
            soup = getSite()
            parseSite(soup)
            wait()
        elif choice == 2:
            settings()
            wait()
        elif choice == 3:
            break
        else:
            print("Invalid option")
            wait()
            

if __name__ == '__main__':
    menu()