import click
import sys
import numpy as np
from PIL import Image
import requests
import urllib.request
import os
import urwid


@click.group()
def main():
    pass

@main.command()
@click.argument('username')
def getuser(username):
    response = requests.get('https://api.github.com/users/' + username)
    if response:
        userImage = displayUserData(response)
        urwid.set_encoding('UTF-8')
        profilePic = urwid.Text(userImage)
        left = urwid.Filler(profilePic, 'middle')
        printLoop = urwid.MainLoop(left, screen=urwid.raw_display.Screen())
    #    printLoop.run()

        os.remove("tmp.jpg")
    else:
        click.echo('Failure')


def getAnsiColorCode(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)

def getColor(r,g,b):
    return "\x1b[48;5;{}m \x1b[0m".format(int(getAnsiColorCode(r,g,b)))

def displayUserImage(img_path):
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        exit("File retrieval Failure")
    h = 25
    w = 35

    text = ""

    img = img.resize((w,h), Image.ANTIALIAS)
    img_arr = np.asarray(img)
    h,w,c = img_arr.shape
    for x in range(h):
        text += '\n'
        for y in range(w):
            pix = img_arr[x][y]
            text += getColor(pix[0], pix[1], pix[2])
    print(text)
    return text
    
    

def displayUserData(response):
    userData = response.json()
    urllib.request.urlretrieve(userData['avatar_url'], 'tmp.jpg')
    return displayUserImage('tmp.jpg')

if __name__ == '__main__':
    main()
