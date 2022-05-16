#!/bin/bash

#starting utility applications at boot time
lxsession &
eval $(gnome-keyring-daemon --start)
export SSH_AUTH_SOCK
export CALIBRE_USE_SYSTEM_THEME=1
nm-applet &
# pamac-tray &
numlockx on &
blueman-applet &
unclutter &
xfce4-power-manager &
picom --config $HOME/.config/picom/picom-blur.conf &
#/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
dunst &
emacs --daemon &
run volumeicon &
~/.fehbg &
