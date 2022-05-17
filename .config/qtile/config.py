# -*- coding: utf-8 -*-
import os
import socket
import subprocess
from typing import List  # noqa: F401from typing import List  # noqa: F401

from libqtile import bar, hook, layout, qtile, widget, pangocffi
from libqtile.command import lazy
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen, ScratchPad, DropDown
from libqtile.log_utils import logger
from libqtile.lazy import lazy

mod = "mod4"  # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"  # My terminal of choice
myBrowser = "google-chrome-stable"  # My browser of choice
myFileBrowser = "dolphin"  # My file browser of choice

keys = [
    ### The essentials
    Key([mod], "Return", lazy.spawn(myTerm + " -e fish"), desc="Launches My Terminal"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.spawn("rofi -show drun -theme applications -show-icons -monitor -1"),
        desc="Run Launcher",
    ),
    Key([mod], "b", lazy.spawn(myBrowser), desc="Browser"),
    Key([mod], "t", lazy.spawn(myFileBrowser), desc="File Browser"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle through layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill active window"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    # Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        ["control", "shift"],
        "e",
        lazy.spawn("emacsclient -c -a emacs"),
        desc="Doom Emacs",
    ),
    # Multimedia Keys
    Key(
        [],
        "XF86AudioPlay",
        lazy.spawn("playerctl -p cider play-pause"),
        desc="Play/Pause Audio",
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        desc="Toggle Audio Mute",
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
        desc="Raise Volume",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
        desc="Lower Volume",
    ),
    Key([], "XF86Calculator", lazy.spawn("galculator"), desc="Open Calculator"),
    ### Switch focus to specific monitor (out of two)
    Key([mod], "w", lazy.to_screen(0), desc="Keyboard focus to monitor 1"),
    Key([mod], "e", lazy.to_screen(1), desc="Keyboard focus to monitor 2"),
    ### Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to prev monitor"),
    ### Treetab controls
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.move_left(),
        desc="Move up a section in treetab",
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.move_right(),
        desc="Move down a section in treetab",
    ),
    ### Window controls
    Key([mod], "j", lazy.layout.down(), desc="Move focus down in current stack pane"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up in current stack pane"),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        lazy.layout.section_down(),
        desc="Move windows down in current stack",
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        lazy.layout.section_up(),
        desc="Move windows up in current stack",
    ),
    Key(
        [mod],
        "h",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc="Shrink window (MonadTall), decrease number in master pane (Tile)",
    ),
    Key(
        [mod],
        "l",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc="Expand window (MonadTall), increase number in master pane (Tile)",
    ),
    Key([mod], "n", lazy.layout.normalize(), desc="normalize window size ratios"),
    Key(
        [mod],
        "m",
        lazy.layout.maximize(),
        desc="toggle window between minimum and maximum sizes",
    ),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    ### Stack controls
    Key(
        [mod, "shift"],
        "Tab",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc="Switch which side main pane occupies (XmonadTall)",
    ),
    Key(
        [mod],
        "space",
        lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack",
    ),
    Key(
        [mod, "shift"],
        "space",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Emacs programs launched using the key chord CTRL+e followed by 'key'
    KeyChord(
        ["control"],
        "e",
        [
            Key([], "e", lazy.spawn("emacsclient -c -a 'emacs'"), desc="Launch Emacs"),
            Key(
                [],
                "b",
                lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'"),
                desc="Launch ibuffer inside Emacs",
            ),
            Key(
                [],
                "d",
                lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"),
                desc="Launch dired inside Emacs",
            ),
            Key(
                [],
                "i",
                lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'"),
                desc="Launch erc inside Emacs",
            ),
            Key(
                [],
                "m",
                lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"),
                desc="Launch mu4e inside Emacs",
            ),
            Key(
                [],
                "n",
                lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'"),
                desc="Launch elfeed inside Emacs",
            ),
            Key(
                [],
                "s",
                lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'"),
                desc="Launch the eshell inside Emacs",
            ),
            Key(
                [],
                "v",
                lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"),
                desc="Launch vterm inside Emacs",
            ),
        ],
    ),
    # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
    KeyChord(
        [mod],
        "p",
        [
            Key(
                [],
                "p",
                lazy.spawn("sh -c '~/.local/bin/rofi_powermenu'"),
                desc="A logout menu",
            ),
            Key(
                [],
                "l",
                lazy.spawn("sh -c '~/.local/bin/lock-screen'"),
                desc="Lock the screen",
            ),
            Key(
                [],
                "d",
                lazy.spawn("sh -c '~/.local/bin/rofi_dock'"),
                desc="A dock menu",
            ),
            Key(
                [],
                "r",
                lazy.spawn("rofi -show run -theme generic -monitor -1"),
                desc="Rofi run menu",
            ),
        ],
    ),
]

groups = [
    Group("", layout="monadtall"),
    Group("", layout="monadtall"),
    Group("", layout="monadtall"),
    Group("", layout="monadtall"),
    Group("", layout="monadtall"),
    Group("", layout="monadtall"),
    Group("", layout="floating"),
    ScratchPad("SPD", dropdowns = [
        DropDown("cider",
                 "cider",
                 opacity=1,
                 y = 0.1,
                 x = 0.25,
                 height=0.5,
                 width=0.5,
                 on_focus_lost_hide=False,
                 warp_pointer=True,
                 ),
        DropDown("terminal",
                 myTerm,
                 opacity = 1,
                 y = 0.1,
                 x = 0.25,
                 height = 0.5,
                 width = 0.5,
                 on_focus_lost_hide=True,
                 warp_pointer=True,
                 ),
    ]),
]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder

keys.extend([
    Key([mod, "shift"], "m", lazy.group["SPD"].dropdown_toggle("cider")),
    Key([mod], "a", lazy.group["SPD"].dropdown_toggle("terminal")),
])

dgroups_key_binder = simple_key_binder("mod4")

colors = [
    ["#D9E0EE", "#D9E0EE"],  # 0foreground
    ["#161320", "#161320"],  # 1background
    ["#3b4252", "#3b4252"],  # 2background lighter
    ["#F28FAD", "#F28FAD"],  # 3red
    ["#ABE9B3", "#ABE9B3"],  # 4green
    ["#FAE3B0", "#FAE3B0"],  # 5yellow
    ["#96CDFB", "#96CDFB"],  # 6blue
    ["#DDB6F2", "#DDB6F2"],  # 7magenta
    ["#89DCEB", "#89DCEB"],  # 8cyan
    ["#C3BAC6", "#C3BAC6"],  # 9white
    ["#6E6C7E", "#6E6C7E"],  # 10grey
    ["#F8BD96", "#F8BD96"],  # 11orange
    ["#96CDFB", "#96CDFB"],  # 12super cyan
    ["#5e81ac", "#5e81ac"],  # 13super blue
    ["#242831", "#242831"],  # 14super dark background
    ["#01203E", "#01203E"],  # 15 Oxford Blue
    ["#011A33", "#011A33"],  # 16
    ["#011327", "#011327"],  # 17
    ["#000D1B", "#000D1B"],  # 18
    ["#000816", "#000816"],  # 19
    ["#000610", "#000610"],  # 20
    ["#10141D", "#10141D"],  # 21
    ["#1D2027", "#1D2027"],  # 22
    ["#26292F", "#26292F"],  # 23
    ["#2C2F37", "#2C2F37"],  # 24
]

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors[7],
    "border_normal": colors[2],
}
layouts = [
    # layout.MonadWide(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Stack(stacks=2, **layout_theme),
    # layout.Columns(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
        font="Ubuntu",
        fontsize=10,
        sections=["FIRST", "SECOND", "THIRD", "FOURTH"],
        section_fontsize=10,
        border_width=2,
        bg_color=colors[2],
        active_bg=colors[7],
        active_fg=colors[14],
        inactive_bg=colors[13],
        inactive_fg=colors[1],
        padding_left=0,
        padding_x=0,
        padding_y=5,
        section_top=10,
        section_bottom=20,
        level_shift=8,
        vspace=3,
        panel_width=200,
    ),
    layout.Floating(**layout_theme),
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(font="Noto Sans", fontsize=14, padding=2)
extension_defaults = widget_defaults.copy()

group_box_settings = {
    "font": "JetBrainsMono Nerd Font",
    "fontsize": 20,
    "padding": 10,
    "active": colors[0],
    "inactive": colors[10],
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors[3],
    "block_highlight_text_color": colors[4],
    "highlight_method": "block",
    "this_current_screen_border": colors[13],
    "this_screen_border": colors[2],
    "other_current_screen_border": colors[16],
    "other_screen_border": colors[2],
    "foreground": colors[0],
    "background": colors[16],
    "urgent_border": colors[3],
}

text_size = 18
icon_size = 14

custom_play_states = {"paused": "", "playing": "", "stopped": " "}


def get_player_text():
    try:
        status = (
            subprocess.check_output(
                [
                    "/usr/bin/playerctl",
                    "-p",
                    "cider",
                    "metadata",
                    "-f",
                    "{{artist}}|{{album}}|{{title}}|{{lc(status)}}",
                ]
            )
            .decode("utf-8")
            .strip()
        )
    except:
        return custom_play_states["stopped"]
    status_info = status.split("|")
    player_text = f"{status_info[2]}  {custom_play_states[status_info[3]]}  {status_info[0]} [{status_info[1]}]"
    return pangocffi.markup_escape_text(player_text)


def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth=0,
            background=colors[14],
            padding=15,
            size_percent=40,
        ),
        widget.Image(
            background=colors[14],
            foreground=colors[0],
            filename="/usr/share/pixmaps/archlinux-logo.svg",
            margin=3,
        ),
        widget.TextBox(
            background=colors[16],
            foreground=colors[14],
            text=" ",
            font="JetBrainsMono Nerd Font",
            fontsize=24,
            padding=0,
        ),
        widget.GroupBox(**group_box_settings),
        widget.TextBox(
            background=colors[17],
            foreground=colors[16],
            text=" ",
            font="JetBrainsMono Nerd Font",
            fontsize=24,
            padding=0,
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[8],
            background=colors[17],
            padding=-2,
            scale=0.55,
        ),
        widget.TextBox(
            background=colors[18],
            foreground=colors[17],
            text=" ",
            font="JetBrainsMono Nerd Font",
            fontsize=24,
            padding=0,
        ),
        widget.TaskList(
            highlight_method="border",  # or block
            icon_size=None,
            max_title_width=200,
            padding_x=5,
            padding_y=3,
            margin_x=5,
            margin_y=5,
            fontsize=14,
            border=colors[1],
            foreground=colors[0],
            background=colors[18],
            txt_floating="🗗 ",
            txt_minimized="_ ",
            markup_focused='<span underline="low">{}</span>',
        ),
        widget.Spacer(background=colors[18]),
        widget.GenPollText(
            **widget_defaults,
            func=get_player_text,
            update_interval=1,
            background=colors[18],
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn("playerctl -p cider play-pause"),
                "Button2": lambda: qtile.cmd_spawn("playerctl -p cider previous"),
                "Button3": lambda: qtile.cmd_spawn("playerctl -p cider next"),
            },
        ),
        # widget.Mpris2(
        #     **widget_defaults,
        #     name="cider",
        #     objname="org.mpris.MediaPlayer2.cider",
        #     display_metadata=["xesam:title", "xesam:album", "xesam:artist"],
        #     # stop_pause_text="Not Playing",
        #     scroll_text=None,
        #     scroll_interval=None,
        #     background=colors[18],
        # ),
        widget.TextBox(
            background=colors[18],
            foreground=colors[16],
            text=" ",
            font="JetBrainsMono Nerd Font",
            fontsize=24,
            padding=0,
        ),
        widget.TextBox(
            background=colors[16],
            foreground=colors[13],
            text="",
            font="Font Awesome 5 Free Solid",
            fontsize=icon_size,
        ),
        widget.CPU(
            background=colors[16],
            foreground=colors[0],
            update_interval=1,
            format="{load_percent: 03.0f} %",
            fontsize=text_size,
        ),
        widget.Sep(
            background=colors[16],
            linewidth=0,
            padding=10,
            size_percent=50,
        ),
        widget.TextBox(
            text="",
            font="Font Awesome 5 Free Solid",
            background=colors[16],
            foreground=colors[13],
            fontsize=icon_size,
        ),
        widget.Memory(
            background=colors[16],
            foreground=colors[0],
            format="{MemPercent: 03.0f} %",
            fontsize=text_size,
        ),
        widget.TextBox(
            background=colors[16],
            foreground=colors[15],
            text=" ",
            font="JetBrainsMono Nerd Font",
            fontsize=24,
            padding=0,
        ),
        widget.Wttr(
            background=colors[15],
            foreground=colors[0],
            location={"Cape Town": "Cape Town"},
            fontsize=text_size,
            format="%c %t (%w)",
            mouse_callbacks={
                "Button1": lazy.spawn(
                    "sh -c 'alacritty --class weather -o window.dimensions.columns=80 -o window.dimensions.lines=47 -e ~/.local/bin/get-weather'"
                ),
            },
        ),
        widget.TextBox(
            background=colors[15],
            foreground=colors[14],
            text=" ",
            font="JetBrainsMono Nerd Font",
            fontsize=24,
            padding=0,
        ),
        widget.TextBox(
            background=colors[14],
            foreground=colors[4],
            text=" ",
            font="Font Awesome 5 Free Solid",
            fontsize=14,
        ),
        widget.Clock(
            background=colors[14],
            foreground=colors[0],
            format="%a %d %b %H:%M",
            fontsize=text_size,
        ),
        widget.Systray(background=colors[14], icon_size=20, padding=4),
        widget.Sep(
            background=colors[14],
            linewidth=0,
            padding=10,
            size_percent=50,
        ),
    ]
    return widgets_list


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[9:10]
    del widgets_screen2[-2]
    return widgets_screen2


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen1(),
                size=32,
                opacity=0.65,
                background="000000",
                margin=[5, 5, 0, 5],
            )
        ),
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen2(),
                size=32,
                opacity=0.65,
                background="000000",
                margin=[5, 5, 0, 5],
            )
        ),
    ]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()


def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


# @hook.subscribe.client_new
# def set_floating(window):
#     if (
#         window.window.get_wm_transient_for()
#         or window.window.get_wm_type() in floating_types
#     ):
#         window.floating = True


# floating_types = ["notification", "toolbar", "splash", "dialog"]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        # default_float_rules include: utility, notification, toolbar, splash, dialog,
        # file_progress, confirm, download and error.
        *layout.Floating.default_float_rules,
        Match(title="Confirmation"),  # tastyworks exit box
        Match(wm_class="pinentry-gtk-2"),  # GPG key password entry
        Match(wm_class="Cider"),
        Match(wm_class="weather"),
        Match(wm_class="blueman-manager"),
    ],
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    try:
        subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])
    except Exception as e:
        logger.exception(str(e))


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
