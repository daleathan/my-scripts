#!/usr/bin/python3
#A Tk frontend for xrandr that can enable/display displays, set the primary display, 
#change the resolution and configure display mirroring or positioning.
#By Charles Bos

from tkinter import *
from tkinter import messagebox
from subprocess import Popen, PIPE

class Display() :
    def __init__(self, name, state, status, resolution, position) :
        '''
        display:    string
        enabled:    bool
        primary:    bool
        resolution: string
        position:   tuple
        '''
        self.display = name
        self.enabled = state
        self.primary = status
        self.resolution = resolution
        self.position = position

    def __str__(self) :
        return "Name: " + self.display + ", Enabled: " + str(self.enabled) + ", Primary: " + str(self.primary) + ", Resolution: " + self.resolution + ", Position: " + str(self.position)

class UI() :
    #Getters
    def getXrandrOutput() :
        out = Popen("xrandr", stdout = PIPE).communicate()
        out = str(out[0]).lstrip("b'").rstrip("'").split("\\n")
        out = [x for x in out if len(x) > 0]
        return out

    def getDisplays(connected) :
        out = UI.getXrandrOutput()
        displays = []
        for x in range(1, len(out)) :
            line = out[x]
            if line[0] == " " : continue
            display = line.split(" ")[0]
            if connected :
                if line.split(" ")[1] != "connected" : continue
            displays.append(display)
        return displays

    def getRelativeDisplays(display) :
        displays = ["None"]
        displays.extend(UI.getDisplays(True))
        displays = [x for x in displays if x != display]
        return displays

    def getPrimary() :
        out = UI.getXrandrOutput()
        for x in range(1, len(out)) :
            line = out[x]
            if line.find("primary") != -1 :
                return line.split(" ")[0]
        return None

    def getAllResolutions(display) :
        out = UI.getXrandrOutput()
        resolutions = []
        started = False
        for x in range(1, len(out)) :
            line = out[x]
            if line.split(" ")[0] == display : 
                started = True
                continue
            if started :
                if line[0] != " " : break
                else : resolutions.append(line.strip().split(" ")[0])
        resolutions += ["Default"]
        return resolutions

    def getCurrentResolution(display, reportOff) :
        out = UI.getXrandrOutput()
        resolutions = UI.getAllResolutions(display)
        for x in range(1, len(out)) :
            line = out[x]
            if line.split(" ")[0] == display :
                for y in resolutions :
                    if line.find(y) != -1 :
                        if y != resolutions[0] : return y
                        else : return "Default"
        if reportOff == True : return None
        else : return "Default"

    def isEnabled(display) :
        if UI.getCurrentResolution(display, True) != None : return True
        else : return False

    #Constructor
    def __init__(self, parent) :
        #Internal functions
        def runConfChange(deadArg) :
            '''
            Copy displayed settings to the associated Display object.
            '''
            display = self.display.get()
            for x in self.displayObjs :
                if x.display == display :
                    x.enabled = self.enabled.get()
                    x.resolution = self.resolution.get()
                    x.position = (self.position.get(), self.relDisp.get())
                    break

        def runPrimaryChange() :
            '''
            Set current display as the primary and ensure that no other
            displays hold the primary flag.
            '''
            display = self.display.get()
            for x in self.displayObjs :
                if x.display == display : x.primary = True
                else : x.primary = False
            self.primButton["state"] = DISABLED

        def runDisplayChange(deadArg) :
            '''
            Update UI elements when a new display is selected from the menu
            '''
            display = self.display.get()
            for x in self.displayObjs :
                if x.display == display :
                    self.enabled.set(x.enabled)
                    if x.primary == True : self.primButton["state"] = DISABLED
                    else : self.primButton["state"] = ACTIVE
                    self.resMenu["menu"].delete(0, "end")
                    for y in UI.getAllResolutions(display) :
                        self.resMenu["menu"].add_command(label = y, command = lambda v = y : updateMenu(v, self.resolution))
                    self.resolution.set(x.resolution)
                    self.relDMenu["menu"].delete(0, "end")
                    for z in UI.getRelativeDisplays(display) :
                        self.relDMenu["menu"].add_command(label = z, command = lambda v = z : updateMenu(v, self.relDisp))
                    self.position.set(x.position[0])
                    self.relDisp.set(x.position[1])
                    break

        def updateMenu(option, var) :
            var.set(option)
            runConfChange(None)

        def runLayoutChange() :
            '''
            When mirroring is enabled, disable the UI elements for screen positioning
            and vice-versa.
            '''
            if self.mirror.get() == False :
                self.posMenu["state"] = ACTIVE
                self.relDMenu["state"] = ACTIVE
            else :
                self.posMenu["state"] = DISABLED
                self.relDMenu["state"] = DISABLED

        def runUpdate() :
            '''
            Call the xrandr command line tool to implement the changes
            '''
            cmd = ["xrandr"]
            for x in self.displayObjs :
                cmd.append("--output")
                cmd.append(x.display)
                if x.enabled == True : cmd.append("--auto")
                else : 
                    cmd.append("--off")
                    continue
                if x.primary == True and UI.getPrimary() != x.display : cmd.append("--primary")
                if x.resolution != "Default" :
                    cmd.append("--mode")
                    cmd.append(x.resolution)
                if self.mirror.get() == False and x.position[1] != "None" :
                    pos = x.position
                    if pos[0] == "Left of" : cmd.append("--left-of")
                    elif pos[0] == "Right of" : cmd.append("--right-of")
                    elif pos[0] == "Above" : cmd.append("--above")
                    else : cmd.append("--below")
                    cmd.append(x.position[1])
            error = Popen(cmd, stderr = PIPE).communicate()
            if str(error[1]) != "b''" :
                messagebox.showerror(title = "Xrandr error", message = str(error[1]).lstrip("b'").rstrip("\\n'"))

        #Set window title
        parent.title("Display Conf Tool")

        #Objects for storing display settings
        self.displayObjs = []
        for x in UI.getDisplays(True) : 
            state = UI.isEnabled(x)
            status = (UI.getPrimary() == x)
            resolution = UI.getCurrentResolution(x, False)
            position = ("Left of", "None")
            self.displayObjs.append(Display(x, state, status, resolution, position))

        #Display selection
        l1 = Label(parent, text = "Configure the output displays.", pady = 5, padx = 40, relief = RAISED).grid(row = 1, column = 1, columnspan = 2, sticky = W, pady = (0, 3))

        #Display chooser
        lf1 = LabelFrame(parent, text = "Select display", padx = 0, pady = 5)
        lf1.grid(row = 2, column = 1, columnspan = 2, sticky = N+S+E+W)
        l2 = Label(lf1, text = "Displays:", pady = 5, padx = 5).grid(row = 1, column = 1, sticky = W)
        self.display = StringVar(parent)
        self.display.set(UI.getDisplays(True)[0])
        displays = UI.getDisplays(True)
        m1 = OptionMenu(lf1, self.display, *displays, command = runDisplayChange).grid(row = 1, column = 2, sticky = W)

        #Display enable/disable
        self.enabled = BooleanVar(parent)
        self.enabled.set(UI.isEnabled(self.display.get()))
        enCb = Checkbutton(lf1, variable = self.enabled, text = "Display enabled", command = lambda : runConfChange(None), pady = 5, padx = 5).grid(row = 2, column = 1, sticky = W)

        #Make primary
        self.primButton = Button(lf1, text = "Make primary", command = runPrimaryChange, padx = 5, pady = 5, bd = 2)
        self.primButton.grid(row = 2, column = 2, sticky = W)
        if UI.getPrimary() == self.display.get() : self.primButton["state"] = DISABLED

        #Resolution
        lf2 = LabelFrame(parent, text = "Set resolution", padx = 0, pady = 5)
        lf2.grid(row = 3, column = 1, columnspan = 2, sticky = N+S+E+W)
        l3 = Label(lf2, text = "Resolution:            ", pady = 5, padx = 5).grid(row = 1, column = 1, sticky = W)
        self.resolution = StringVar(parent)
        resolutions = UI.getAllResolutions(self.display.get())
        self.resolution.set(UI.getCurrentResolution(self.display.get(), False))
        self.resMenu = OptionMenu(lf2, self.resolution, *resolutions, command = runConfChange)
        self.resMenu.grid(row = 1, column = 2, sticky = E)

        #Mirror displays
        lf3 = LabelFrame(parent, text = "Set display layout", padx = 0, pady = 5)
        lf3.grid(row = 4, column = 1, columnspan = 2, sticky = N+S+E+W)
        self.mirror = BooleanVar(parent)
        self.mirror.set(True)
        miCb = Checkbutton(lf3, variable = self.mirror, text = "Mirror displays ", command = runLayoutChange, pady = 5, padx = 5).grid(row = 1, column = 1, sticky = W)

        #Display positioning (non-mirroring mode)
        positions = ["Left of", "Right of", "Above", "Below"]
        self.position = StringVar(parent)
        self.position.set(positions[0])
        self.posMenu = OptionMenu(lf3, self.position, *positions, command = runConfChange)
        self.posMenu.grid(row = 2, column = 1, sticky = W)
        self.posMenu["state"] = DISABLED

        otherDisps = UI.getRelativeDisplays(self.display.get())
        self.relDisp = StringVar(parent)
        self.relDisp.set(otherDisps[0])
        self.relDMenu = OptionMenu(lf3, self.relDisp, *otherDisps, command = runConfChange)
        self.relDMenu.grid(row = 2, column = 2, sticky = E)
        self.relDMenu["state"] = DISABLED

        #Buttons
        b1 = Button(parent, text = "Close", padx = 5, pady = 5, bd = 3, command = parent.destroy).grid(row = 5, column = 1, sticky = W, pady = (3, 0))
        b2 = Button(parent, text = "Update", padx = 5, pady = 5, bd = 3, command = runUpdate).grid(row = 5, column = 2, sticky = E, pady = (3, 0))

top = Tk() 
ui = UI(top)
top.mainloop()
