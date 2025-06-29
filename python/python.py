import tkinter as tk
from tkinter import *
import fnmatch
import os
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter.ttk import Progressbar
#from pydub import audiosegment
import wave
import eyed3

canvas = tk.Tk()
canvas.title('Music Player')
canvas.geometry("600x600")
#canvas.resizable(False,False)
canvas.config(bg='light green') 

image_icon = PhotoImage(file='icon.png')
canvas.iconphoto(False, image_icon)

rootpath="C:\\Users\YOJASHRI\Music"
pattern ="*.mp3"

mixer.init()

current_position = 0
Pause = False
selected_folder_path = 0


prev_img = tk.PhotoImage(file='prev_img.png')
stop_img = tk.PhotoImage(file='stop_img.png')
play_img = tk.PhotoImage(file='play_img.png')
pause_img = tk.PhotoImage(file='pause_img.png')
next_img = tk.PhotoImage(file='next_img.png')

def select():
    global selected_folder_path
    song_name = listBox.get('anchor')
    song_path = os.path.join(rootpath, song_name)

    label.config(text = listBox.get('anchor'))
    mixer.music.load(song_path)
    mixer.music.play()

    audio = MP3(song_path)
    song_length = audio.info.length

    update_progress_bar()


def stop():
    mixer.music.stop()
    listBox.select_clear('active')

def play_next():
    next_song = listBox.curselection()
    next_song = next_song[0] + 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)

    mixer.music.load(rootpath + '\\' + next_song_name)
    mixer.music.play()

    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)

def play_prev():
    next_song = listBox.curselection()
    next_song = next_song[0] - 1
    next_song_name = listBox.get(next_song)
    label.config(text = next_song_name)

    mixer.music.load(rootpath + '\\' + next_song_name)
    mixer.music.play()

    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)

def pause_song():
    if pauseButton['text'] == 'pause':
        mixer.music.pause()
        pauseButton['text'] = 'play'
    else:
        mixer.music.unpause()
        pauseButton['text'] = 'pause'


def update_progress_bar():
    current_pos = mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
    if song_length > 0:
        progress = (current_pos / song_length) * 100
        pbar['value'] = progress

    if mixer.music.get_busy():
        canvas.after(1000, update_progress_bar)
    else:
        pbar['value'] = 0 




listBox = tk.Listbox(canvas, fg='aqua',bg='cornflowerblue',width = 100, font= ('ds-digital',20))
listBox.pack(padx=15,pady=15)

label = tk.Label(canvas,text='', bg = 'light green', fg = 'red', font = ('ds-digital',20))
label.pack(pady=15)

top = tk.Frame(canvas, bg ='light green')
top.pack(padx=15, pady=15, anchor= 'center')

prevButton = tk.Button(canvas,text='Prev', image= prev_img, bg ='light green', borderwidth= 0, command=play_prev)
prevButton.pack(pady=15 , in_ = top, side= 'left')

stopButton = tk.Button(canvas,text='Stop' , image= stop_img, bg ='light green', borderwidth= 0, command= stop)
stopButton.pack(pady=15 , in_ = top, side= 'left')

playButton = tk.Button(canvas,text='Play' , image= play_img, bg ='light green', borderwidth= 0, command = select)
playButton.pack(pady=15 , in_ = top, side= 'left')

pauseButton = tk.Button(canvas,text='Pause' , image= pause_img, bg ='light green', borderwidth= 0, command= pause_song)
pauseButton.pack(pady=15 , in_ = top, side= 'left')

nextButton = tk.Button(canvas,text='Next' , image= next_img, bg ='light green', borderwidth= 0 , command= play_next)
nextButton.pack(pady=15 , in_ = top, side= 'left')

pbar = Progressbar(canvas, length = 300 , mode = 'determinate')
pbar.pack(padx = 0, pady = 10)


def adjust_volume(val):
    volume = float(val) / 100  # Convert to a range between 0.0 and 1.0
    mixer.music.set_volume(volume)

volume_slider = tk.Scale(canvas, from_=0, to=100, orient='horizontal', command=adjust_volume)
volume_slider.set(100)  # Set initial volume to max
volume_slider.pack(padx=25, pady=10)


for root,dirs,files in os.walk(rootpath):
    for filename in fnmatch.filter(files,pattern):
        listBox.insert('end',filename)

canvas.mainloop()