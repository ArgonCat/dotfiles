from typing import List  # noqa: F401

from libqtile import bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

##################################################################################
#  Themes  
##################################################################################

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"]] # backbround for inactive screens


##################################################################################
#  Keys
##################################################################################

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.\
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    #Launch applications
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "t", lazy.spawn("brave"), desc="Launch Brave"),
    Key([mod], "y", lazy.spawn("ytmdesktop"), desc="Launch Youtube Music"),
    Key([mod], "d", lazy.spawn("discord"), desc="Launch Discord"),
    Key([mod], "a", lazy.spawn("anki"), desc="Launch Anki"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Dmenu hotkey
    Key([mod], "r", lazy.run_extension(extension.DmenuRun(
        dmenu_prompt=">",
        dmenu_font="mononoki Nerd Font Mono",
        background=colors[0][0],
        foreground=colors[7][0],
        selected_background=colors[4][0],
        selected_foreground=colors[2][0],
        dmenu_height=30,  # Only supported by some dmenu forks
    ))),
    Key([mod], "p", lazy.spawn("passmenu -nb "+colors[0][0]+" -nf "+colors[7][0]+" -sb "+colors[4][0]+" -sf "+colors[2][0]+" -fn \"mononoki Nerd Font Mono\" -h 30 -p £"), desc="Run Passmenu"),

    #Switch screens
    Key([mod], "v", lazy.to_screen(0)),
    Key([mod], "b", lazy.to_screen(1)),
]

#Define groups with keybinds 1-9
group_names = 'WWW DEV SYS CHAT MUS VIS ETC'.split()
groups = [Group(name, layout='monadtall') for name in group_names]
for i, name in enumerate(group_names):
    indx = str(i + 1)
    keys += [
        Key([mod], indx, lazy.group[name].toscreen()),
        Key([mod, 'shift'], indx, lazy.window.togroup(name))]

##################################################################################
#  Layouts
##################################################################################
layout_theme = {"border_width": 1,
                "margin": 0,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.RatioTile(**layout_theme),
]

##################################################################################
#  Screens
##################################################################################

widget_defaults = dict(
    font='mononoki Nerd Font Mono',
    fontsize=15,
    padding=2,
    background=colors[0]
)

extension_defaults = widget_defaults.copy()

def initwidgetslist():
    widgetslist = [widget.GroupBox(
               active = colors[2],
               inactive = colors[7],
               rounded = False,
               highlight_color = colors[1],
               highlight_method = "line",
               this_current_screen_border = colors[6],
               this_screen_border = colors [4],
               other_current_screen_border = colors[6],
               other_screen_border = colors[4],
               foreground = colors[2],
               background = colors[0],
        ),
        widget.Spacer(length=bar.STRETCH),
        widget.Systray(),
        widget.Sep(),
        widget.Battery(format='{percent:2.0%}' ),
        widget.Sep(),
        widget.CheckUpdates(
                 update_interval = 1800,
                 distro = "Arch_checkupdates",
                 display_format = "{updates} Updates",
                 foreground = colors[2],
                 mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                 background = colors[5]
                 ),
        widget.Sep(),
        widget.Clock(format='%d/%m|%H:%M:%S'),
        widget.Sep(),
        widget.CurrentLayout(),
        widget.Sep(),]
    return widgetslist 

screens = [
    Screen(
        top=bar.Bar(initwidgetslist(), opacity=0.9, size=30),
    ),
    Screen(
        top=bar.Bar(initwidgetslist(), opacity=0.9, size=30),
    ),
]

##################################################################################
#  Floating
##################################################################################

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

##################################################################################
#  Background Config
##################################################################################

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
