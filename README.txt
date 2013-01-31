pa_systray - minimal systray app to monitor pulseaudio server
=============================================================

pa_systray monitors, whether pulseaudio is currently running or not.
you can start/stop the server via by clicking on the icon (or via the context
menu).

OBJECTIVE
=========
my preferred audio-API is JACK (the low-latency "pro"-audio framework on linux).
this works great for all kinds of audio-software (ardour, Pure Data,
Supercollider,...) but doesn't really work with many desktop-applications,
including my favourite browser.
otoh, virtually all "standard" desktop-applications support pulseaudio these days.
in order to keep my audio-system as low-latency as possible AND at the same time
be able to easily use audio-output of my desktop-applications, i have decided to
run pulseaudio on top of jack (that is: pulseaudio is an ordinary jack client),
as described 
[here](https://wiki.archlinux.org/index.php/PulseAudio/Examples#Pulseaudio_through_JACK_the_old_way).
i also like to be able to get rid of pulseaudio whenever i feel that i want to
go "pro" completely.
`pa_systray` allows me to turn off pulseaudio whenever i feel like it.

`pasuspender` is not very appealing to me, as it makes working with my favourite
sound programs the exception, rather than the default (also, i have to decide to
suspend pa for the entire run-cycle of my sound programs, which can be days)


USAGE
=====
simply run
$ ./pa_systray

image paths are currently hardcoded to 'images/' but you can change that in the source code

DEPENDENCIES
============
pa_systray depends is written in python and uses Qt.
you need "PySide" (Qt-bindings for python) in order to run it.
pa_systray uses the `pulseaudio` cmdline tool to start/stop/check the
pulseaudio server.

on debian, you can simply do:
# aptitude install python-pyside.qtcore python-pyside.qtgui
# aptitude install pulseaudio

LICENSE
=======
pa_systray is heavily based on the pyside systray example
http://qt.gitorious.org/pyside/pyside-examples/blobs/e5d379f38bf03406056e8b14af95ae36a0a1de08/examples/desktop/systray/systray.py

Copyright © 2012 IOhannes m zmölnig <zmoelnig@umlaeute.mur.at>.
      forum::für::umläute

pa_systray is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

pa_systray is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program; if not, see <http://www.gnu.org/licenses/>.

the images are taken from the pulseaudio website, and are:
    Copyright © Pierre Ossman <ossman@cendio.se> for Cendio AB
and licensed under the terms of the GNU General Public License 2.0
