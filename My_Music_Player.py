import os
import pickle  # pickle is used to save and store the list or dict
from tkinter import *
from tkinter import filedialog  # field dialogbox is used to open the files
from pygame import mixer  # mixer is used to do the operations on the songs
import speech_recognition as sr


#######################################
# r1 = sr.Recognizer()
r2 = sr.Recognizer()
r3 = sr.Recognizer()

#######################################

root = Tk()
root.geometry("600x440+200+100")
root.resizable(False, False)
root.title("Music Mp3 Player")
mixer.init()

playlist = []

###### Initializing Variables ####################


####################  Initializing Functions  ######################

if os.path.exists('songs.pickle'):
    with open('songs.pickle', 'rb') as f:
        playlist = pickle.load(f)
else:
    playlist = []


def retrieve_songs():
    global playlist

    song_list = []
    directory = filedialog.askdirectory()
    for root_, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] == ".mp3":
                path = (root_ + '/' + file).replace('\\', '/')
                song_list.append(path)

    with open('songs.pickle', 'wb') as g:
        pickle.dump(song_list, g)
    playlist = song_list
    track_list['text'] = f'PlayList - {str(len(playlist))} Songs'
    song_list_box.delete(0, END)
    enumerate_songs()


###############  Function To Pause Song  ####################


def pause_song():
    print(" Paused ")
    global paused
    paused = True
    mixer.music.pause()
    root.pause.grid_remove()
    root.resume.grid()


###############  Function To Resume Song  ####################

def resume_song():
    global played, paused
    print(" Resumed ")

    if not played:
        play_song()
    paused = False
    mixer.music.unpause()
    root.resume.grid_remove()
    root.pause.grid()


def prev_song():
    global current

    print("Previous Song")

    if current > 0:
        current -= 1
    else:
        current = 0
    song_list_box.itemconfigure(current + 1, bg='grey')
    play_song()


def play_song(event=None):
    global current, paused, played

    print("Play Song")
    root.pause.grid()

    if event is not None:
        current = song_list_box.curselection()[0]
        for i in range(len(playlist)):
            song_list_box.itemconfigure(i, bg="grey")

    print(playlist[current])
    mixer.music.load(playlist[current])
    song_track['anchor'] = 'w'
    song_track['text'] = os.path.basename(playlist[current])

    paused = False
    played = True

    song_list_box.activate(current)
    song_list_box.itemconfigure(current, bg="skyblue")
    mixer.music.play()


def next_song():
    global current

    print("Next Song")

    if current < len(playlist) - 1:
        current += 1
    else:
        current = 0
    song_list_box.itemconfigure(current - 1, bg='grey')
    play_song()


def change_volume(event=None):
    print("Change Volume")
    current_volume = volume.get()
    mixer.music.set_volume(current_volume / 10)


def speak():
    print("Speak")
    with sr.Microphone() as source:

        print("speak now")
        audio = r3.listen(source)

        if "play" in r2.recognize_google(audio):
            play_song()

        elif "pause" in r2.recognize_google(audio):
            pause_song()

        elif "resume" in r2.recognize_google(audio):
            resume_song()

        elif "back" in r2.recognize_google(audio):
            prev_song()

        elif "next" in r2.recognize_google(audio):
            next_song()

        else:
            print('invalid')


################## Initializing An Images  ##########################


img = PhotoImage(file='music.gif')
next_ = PhotoImage(file='next.gif')
back = PhotoImage(file='previous.gif')
play1 = PhotoImage(file='play.gif')
pause1 = PhotoImage(file='pause.gif')
resume = PhotoImage(file="res.png")
microphone = PhotoImage(file="mic1.png")

resume = resume.subsample(13, 13)
microphone = microphone.subsample(13, 13)

# Creating a Master Frame

master_frame = Frame(root, bg = "skyblue")
master_frame.pack()

################### Creating a Frames #######################

# Creating a Frame for Track 1

track = LabelFrame(master_frame, text='Song Track', font=("times new roman", 15, "bold"), bg="red", fg="white",
                   bd=5, relief=GROOVE)
track.config(width=410, height=300)
track.grid(row=0, column=0, padx=5)

# creating a Frame For Track List

track_list = LabelFrame(master_frame, text=f'PlayList Song', font=("times new roman", 15, "bold"), bg="red",
                        fg="white", bd=5, relief=GROOVE)
track_list.config(width=190, height=400)
track_list.grid(row=0, column=1, rowspan=3, pady=5)

#########################  Track List Widget  #######################

# Scroll bar
scroll_bar = Scrollbar(track_list, orient=VERTICAL)
scroll_bar.grid(row=0, column=2, rowspan=5, sticky="ns")


def enumerate_songs():
    for index, song in enumerate(playlist):
        song_list_box.insert(index, os.path.basename(song))


# Creating A List Box

song_list_box = Listbox(track_list, bg="grey", fg="black", selectmode=SINGLE,
                        yscrollcommand=scroll_bar.set, selectbackground="skyblue")
song_list_box.config(width=25, height=22)
song_list_box.grid(row=0, column=1)

scroll_bar.config(command=song_list_box.yview)
song_list_box.grid(row=0, column=0, rowspan=5)

# whenever someone double click in listbox
song_list_box.bind("<Double-1>", play_song)

# Creating a Frame for control

controls = LabelFrame(master_frame, font=("times new roman", 15, "bold"), bg="brown", fg="white", bd=5,
                      relief=GROOVE)
controls.config(width=410, height=80, padx=10, pady=5)
controls.grid(row=2, column=0)

# Inserting An Image Inside A  Track Frame

canvas = Label(track, image=img)
canvas.grid(row=0, column=0)

song_track = Label(track, font=("times new roman", 16, "bold"), bg="red", fg="white", text="MP3 Player")
song_track.config(width=30, height=1)
song_track.grid(row=1, column=0, padx=10)

#########################  Control Buttons  ########################

# Pause Button

root.pause = Button(controls, image=pause1, command=pause_song, )
root.pause.grid(row=0, column=0)
root.pause.grid_remove()

# Resume Button

root.resume = Button(controls, image=resume, command=resume_song, )
root.resume.grid(row=0, column=0)
root.resume.grid_remove()

# Previous Button

prev = Button(controls, image=back)
prev['command'] = prev_song
prev.grid(row=0, column=1)

# Play Button

play = Button(controls, image=play1, command=play_song)
play.grid(row=0, column=2)

# Forward Button

forward = Button(controls, image=next_)
forward['command'] = next_song
forward.grid(row=0, column=3)

volume = DoubleVar()
slider = Scale(controls, from_=0, to=10, orient=HORIZONTAL, bd=2, relief=GROOVE)
slider['variable'] = volume
slider.set(8)
mixer.music.set_volume(0.8)
slider['command'] = change_volume
slider.grid(row=0, column=4, padx=5)
########################################################################################################
# Voice Button

voice_button = Button(master_frame, image=microphone, border="0", command=speak)
voice_button.grid(row=3, column=1)
voice_button.configure()

#########################################################################################################
# create menus

my_menu = Menu(root)
root.config(menu=my_menu)

# Add song Menu

add_songs_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Music Folder", menu=add_songs_menu)
add_songs_menu.add_command(label="Select Music Folder", command=retrieve_songs)

# Add many songs to playlist
# add_songs_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

############ global variables
current = 0  # our list is empty
paused = True  # initially our song is paused
played = False  # no music is playing yet

root.mainloop()
