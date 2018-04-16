# my-scripts
Feel free to help yourself to anything you like here. Mail me if you have any
queries - my email address is on my profile page.

Please note that I have not tested any of these scripts outside of Arch Linux -
indeed, some of these scripts will work only in Arch Linux (though those should
just be the ones that use pacman).

If anyone has any suggestions for improvements (or even pull requests!) then
they will be gratefully recieved. What follows is a short description of each
script and a note on any dependencies it has.

* **aur-cache.py** - I'm not a fan of AUR helpers like yaourt - I prefer to
download the tarballs and install them manually. But what to do about the 
compiled package, the build directory and the AUR tarball? This script 
automates that cleanup. Say you downloaded foo.tar.gz from the AUR to 
~/Downloads and built foo-1.0-1.pkg.tar.xz. This script will copy the 
.pkg.tar.xz file to a cache directory (I use ~/.aurcache but that's completely 
arbitrary). It will then delete the ~/Downloads/foo directory and 
~/Downloads/foo.tar.gz. And it will do that for any build directory it finds in
~/Downloads. The ~/Downloads and ~/.aurcache directories are written into the 
program but you can supply different directories as arguments or you can just 
edit the script. - Depends: python
* **aur-ccache.py** - This clears out any packages in your AUR cache directory -
mine is ~/.aurcache - other than the ones currently installed. A bit like
running pacman -Sc basically. Depends: python, pacman
* **aurcheck.py** - This will check the AUR for any updates to your packages. 
If you have wget installed it will also offer to download the updated tarballs.
This doesn't use any APIs for interacting with the AUR - just web scraping. 
This is probably the script I use most. It works well for me though I'm not 
sure how fast it would be if you had a lot of AUR packages installed - I have 
only a few. - Depends: python, python-requests, python-beautifulsoup4, pacman,
wget (optional)
* **bin2text.py** - A silly little script that I wrote just for fun really. 
Does what it says on the tin. - Depends: python
* **display-conf-tool.py** - This is a general pupose Tk gui frontend to
xrandr. It can enable/disable displays, configure display resolutions, display
mirroring and display positioning. It started out as a reimplementation of
display-selector.sh in Tk because zenity is slow and working fast is more
important to me than looking good! But later I re-wrote it to make it work in
all contexts (i.e. no hardcoded display names) and to add more features. - 
Depends: python, tk, xorg-xrandr
* **display-selector.sh** - A zenity dialogue for calling xrandr. This allows me
to switch between my laptop screen and the HDMI port. Note that the display
names are hardcoded and the functionality is very limited. This can only
enable or disable displays. You should use display-conf-tool.py instead
which is faster, detects displays instead of relying on hardcoded names
and has many more xrandr settings exposed. - Depends: bash, zenity, xorg-xrandr
* **end-session.py** - A python Tk dialogue that can call systemctl 
{reboot,poweroff,suspend...}. Not particularly useful to me now. I can't 
remember why I wrote this one. - Depends: python, tk, systemd
* **fat_copy.sh** - This is quite useful actually. It can copy directories and 
files, replacing any characters in filenames or directory names
that are illegal for the FAT filesystem with underscores. It should be noted 
that this doesn't actually 'copy' directories strictly speaking. 
It only copies files - directories are created in the new location using mkdir.
This is because copying directories can only be done recursively which means
the entire directory tree would be copied over to the FAT filesystem without
the necessary changes to the names of any of the files or subdirectories in
the tree. - Depends: bash, coreutils
* **fvwm-recent-files.py** - This script parses the recently-used.xbel file
which is written to by GTK+ applications, determines the 10 most
recently used files, which applications are the correct ones for opening
those files and then outputs the results in FVWM menu format, essentially
giving you a dynamic 'recently used' menu similar to the one found in MATE's
Places menu. It has support for icons and filename truncation, the latter of
which is configurable. You can also choose the maximum number of entries in
the menu. - Depends: python, python-urllib3
* **gkgetsecret.py** - So recently I got interested in storing my passwords
in an encrypted fashion using GNOME Keyring. But for applications that don't
talk to GNOME Keyring I needed an easy way of getting the passwords out. This
python script can talk to GNOME Keyring using libsecret and get the password
or attribute value for a given description or a set of attribute-value pairs.
It's only very simple but seems to work well for me. - Depends: python,
python-gobject, libsecret
* **gnome-screensaver-idlelock.sh** - I wrote this one when I was still using
GNOME Screensaver 3.6 with Xfce. And I was doing that because XScreenSaver's
DPMS timeouts conflict with xfce-power-manager's timeouts. It uses xprintidle
to get the idle time and then locks the screen when the timeout is reached
as long as Xfce's presentation mode is not engaged. Xautolock does this sort of
thing much better though so just use that. Personally, I don't use this or 
xautolock. Instead, I ditched the pointless power manager and just went back to
the excellent XScreenSaver. - Depends: bash, xprintidle, gnome-screensaver, 
xfconf
* **mcityconf.py** - This is another python Tk program. It can read and write to
a few of Metacity's DConf keys - namely, the ones controlling themes and fonts.
This was written back when I was still using Compiz 0.9 with Xfce - the
gtk-window-decorator reads from Metacity's settings so I was actually using it
to change the Compiz theme. I no longer use this (or Compiz for that matter)
but I think it still works fine. - Depends: python, tk, metacity, glib2
(for gsettings)
* **mp3-range.sh** - This is one of two scripts I wrote that analyse an mp3 
collection by date. Basically, you supply two arbitrary dates - 1980 and
1989 for instance - and it will tell you how many tracks you have that have a
date tag in that range. - Depends: bash, id3lib (for id3info)
* **mp3-renamer.py** - This is one of my genuinely useful scripts. Supply it 
with a directory of mp3 files and it will scan their tags and rename them all
according to a standard format: "Track number" "Track name.mp3". It's recursive
so it can handle subdirectories just fine. Any tracks that lack tag
information will not be renamed but instead the script will report the names
of the files that it could not rename. - Depends: python, python-mutagen
* **mp3compress.sh** - Oh yes, this was when I wanted all of my mp3's on my 
phone which is rather lacking in memory. I got it into my head that I could 
batch compress all my tracks to 192 kbps. And that's exactly what this script 
does (it allows you to choose other bitrates as well). And the script works.
The tracks sounded awful though and I haven't used this again. Instead, 
I've come to terms with the limited memory of my phone and just have
my most recent tracks on it. No, I won't get a new phone. Not until the old
one has broken! ;) - Depends: bash, lame
* **music-years.py** - The second one of my scripts for analysing music 
collections by date. This one can report quite a lot, including the mean year of
release, the top 10 years for tagged tracks and the number of tracks per decade
amongst other things. I still run this one every now and then. It tells me I'm a
bit of an 80s person ;) - Depends: python, python-mutagen
* **obiconadder.py** - This one I wrote for some random person in the Arch Linux
forums. He had a weird corner case where he had an OpenBox menu that he'd
written by hand and he wanted all the menu entries to have icons but he
didn't want to locate all the icons manually and add them to his menu file one
by one. He couldn't use an automatic menu generator for OpenBox because that
would overwrite the menu file he had already written. So I wrote this script
for him that reads an OpenBox menu file, locates the icon for each menu entry
and then edits the menu file in place, adding the icon paths in the correct
places. I've never had a use for it myself, what with me not being an OpenBox
user, but I think he was rather pleased with it. - Depends: python
* **pkgdate.py** - So this is another pacman based script. Put simply, it lists
packages in order of the last time they were installed. It's quite useful in 
that it allows one to check which packages they have installed recently without
having to check the pacman log, which might well be filled with other output.
There might be a builtin pacman function for this but if there is, I have never
come across it. - Depends: python, pacman
* **safehibernate.sh** - A script that uses vmstat to check that the amount
of used memory doesn't exceed the amount of free swap before hibernating.
If it does, then it displays an xmessage dialogue that states this instead of
attempting to hibernate. - Depends: bash, procps-ng (for vmstat), systemd, 
xorg-xmessage
* **setgtktheme.py** - This is by far my most popular script for people who 
visit here, or at least that's what GitHub's visit tracker tells me. It's a 
python Tk dialog for setting the GTK theme, fonts etc. I originally wrote it for
someone in the Arch Linux forums who wanted a program that could allow him
to set the GTK2 and GTK3 themes independently. LXAppearance, the only other
similar tool that I know of, forces you to have the same theme for GTK 2 and 3.
The other upside of this script is that it will not overwrite the GTK settings
files. Anything in there will be left in place and only the things that the
script needs to touch will it touch. This is unlike LXAppearance which will
completely overwrite anything in the settings files. Even though this was
written for somebody else, I still use it myself to this day. - Depends:
python, tk
* **suffolklibraries.py** - This was just a little experiment on my part, it was
not intended to be useful (and if you don't live in Suffolk, England then it
can't possibly be of use anyway). But what it does is it provides a CLI for
the Suffolk Libaries website. You can use it to log in and show books that
you have out on loan and when they are due to be returned. It uses a headless
browser called phantomjs and a browser automation framework called selenium.
At the time, I was very taken with browser automation. I still find it 
interesting now though I haven't yet found a use for it in my day to day 
workflow. Maybe one of these days... - Depends: python, python-selenium, 
python-beautifulsoup4, phantomjs
* **text2bin.py** - opposite of bin2text.py - Depends: python
* **tkscrot.py** - this is a dead simple python Tk frontend to scrot. It's
intended to imitate the look and feel of GNOME Screenshot. I got rid of
GNOME Screenshot itself partly because it uses the GNOME header bars and partly
because of the application size. For me, GNOME Screenshot takes up 10x as much
space as this script and scrot combined. MATE Screenshot is even worse as it's
not distributed separately but as part of MATE Utils which includes a whole
bunch of applications I neither want nor need. - Depends: python, tk, scrot
* **volume-change.sh** - a script I wrote to change the volume when using
PulseAudio. It has three actions, volume increase, decrease and (un)mute which
can be each be bound to the XF86Audio keys. - Depends: bash, pulseaudio, 
alsa-utils
* **xfpm-idle-toggle.sh** - Another script that dates from my Xfce days. I 
wanted to be able toggle Xfce's presentation mode using a keyboard shortcut and
I wanted a notification showing that the mode had been turned on/off. I no 
longer use Xfce or its power manager so this is no longer useful to me. - 
Depends: bash, xfconf, libnotify (for notify-send)
