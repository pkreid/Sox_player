#! /user/env/python
import os
import random
from subprocess import Popen
import time

from random import shuffle
from evdev import InputDevice, categorize, ecodes

# Create a class to monitor the keyboard for the right inputs
class Input_handler:
    def get_device(self):
        dev = InputDevice('/dev/input/event3') # the device file of the
                                                # keyboard
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                if "163" in str(event):
                    action = "next"
                    print ">>"
                    return action
                if "164" in str(event):
                    action = "play pause"
                    print "+/> detected"          
                    return action
                if "165" in str(event):
                    action = "prev"
                    print "<<"
                    return action   


class ListGen: #Must be run FIRST
    def create_index(self): 
        for (dirpath, dirs, files) in os.walk('/home/kreid/music'):
            counter = 0 
            tracklist = {}
            for file in files:
                if file.endswith('.flac'):
                    tracklist[counter] = os.path.join(dirpath, file)
                    counter += 1
    
        random.shuffle(tracklist)
        return tracklist

class TrackSelect: 
    def track_lookup(self,song_index,current_track):
        next_song = song_index[current_track]
        return next_song
class Controller():
    def next(self, current_track):
       current_track += 1
       return current_track
    def prev(self, current_track):
       current_track -= 1 
       return current_track
    def kill(self, sox):
        Popen.kill(sox) #KILLS THE CHILD
    
    def play_pause(self, state, sox):
        if state == "pause":
            os.kill(sox.pid, signal.SIGCONT)
            state = "pause"
            return state
        if state == "play":
            os.kill(sox.pid, signal.SIGSTOP)
            state = "pause"
            return state

# SoxPlay: play the song, Background it, get the PID, return current_track
# number
class SoxPlay:
    def play_song(self, song_name):  
        pid = Popen(["play", str(song_name)])
        return pid

def main():
 
    makelist = ListGen()
    list = makelist.create_index() 

#Start Playing
    track_select = TrackSelect()
    current_track = 0 #the index number of the song
    song_name = track_select.track_lookup(list, current_track)
    play = SoxPlay()
    sox = play.play_song(song_name)

    controller = Controller()
#Wait for input
    getbutton = Input_handler()

    while True:
        action = getbutton.get_device()
        if action == "next":
            controller.kill(sox)
            current_track = controller.next(current_track)
            song_name = track_select.track_lookup(list, current_track)
            sox = play.play_song(song_name)
        if action == "prev":
            controller.kill(sox)
            current_track = controller.prev(current_track)
            song_name = track_select.track_lookup(list, current_track)
            sox = play.play_song(song_name)
            

main()
