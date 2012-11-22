#!/usr/bin/env python

import os
import time

def get_idle_time():
    uid = os.getuid()
    pts = os.listdir("/dev/pts/")

    last_seen = 0
    for pt in pts:
	try:
	    st = os.stat("/dev/pts/" + pt)
	    if st.st_uid == uid:
		# ctime?  mtime?
		last_seen = max(st.st_atime, last_seen)
	except:
	    # PTS closed between listdir and stat?
	    pass

    return time.time() - last_seen

def get_active_pane_title():
    p = os.popen("tmux list-panes -F '#{pane_title} #{pane_active}' -t $(tmux list-windows | grep active | cut -d: -f1) | grep 1$", "r")
    title = p.read()
    p.close()

    return title[:-3]

print get_idle_time(), get_active_pane_title()
