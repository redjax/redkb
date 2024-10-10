# Alacritty on Windows

## alacritty.toml config file

Configuration file: `%APPDATA%\alacritty\alacritty.toml`

```toml
## Configuration docs: https://github.com/alacritty/alacritty/blob/master/extra/man/alacritty.5.scd

## Reload config on changes
live_config_reload = true
## NOTE: env vars like %APPDATA% or ${env:APPDATA} do NOT work here
working_directory = "c:\\"

## Import themes.
#  NOTE: You must clone the git repository or download the themes/ directory,
#  and put it at the location in the import statement.
#  https://github.com/alacritty/alacritty-theme
import = ["~/.config/alacritty/themes/atom_one_dark.toml"]

[env]
TERM = "alacritty"

[window]
## Set CWD as window title
dynamic_title = true
## Ignored when dynamic_title = true
title = "Alacritty"

## Fullscreen, Maximized, Windowed, SimpleFullscreen
startup_mode = "Windowed"

## How transparent the window is; 0.0 to 1.0
opacity = 0.95

## Add additional padding evenly around terminal content
dynamic_padding = true
padding.x = 4
padding.y = 0

## Full, None, Transparent, Buttonless
decorations = "Full"
## Dark, Light
decorations_theme_variant = "Dark"

## Default terminal width
dimensions.columns = 100
## Default terminal height
dimensions.lines = 25

## On-screen dimensions for window placement on open
position.x = 300
position.y = 150

[scrolling]
history = 1000
multiplier = 3

[font]
size = 15.0

offset.x = 0
offset.y = 0

glyph_offset.x = 0
glyph_offset.y = 0

[colors]
draw_bold_text_with_bright_colors = true

[bell]
## "Ease", "EaseOut", "EaseOutSine", "EaseOutQuad",
#  "EaseOutCubic", "EaseOutQuart", "EaseOutQuint",
#  "EaseOutExpo", "EaseOutCirc", "Linear"
animation = "EaseOutExpo"
color     = "#C0C5CE"
## Command to run when bell is rung
command   = "None"
## Time in milliseconds. 0=disabled
duration  = 0

[selection]
save_to_clipboard = true 
semantic_escape_chars = ",│`|:\"' ()[]{}<>\t"

[cursor]
## Time in milliseconds between blinks, default 750
blink_interval = 650
## Time in seconds for cursor to "hold" its blink, default 5
blink_timeout = 5
## Thickness of cursor relative to cell width. 0.0 to 1.0, default 0.15
thickness = 0.25
## Render cursor as a hollow box when window loses focus
unfocused_hollow = true
## Block, Beam, Underline
style.shape = "Block"
## Never, Off, On, Always
style.blinking = "On"

vi_mode_style.shape = "Block"
vi_mode_style.blinking = "Never"

[shell]
## Windows Powershell 1.0
program = "powershell"
# args = []

## Windows PowerShell Core (7)
# program = "C:\\Program Files\\PowerShell\\7\\pwsh.exe"
# args = []

[[keyboard.bindings]]
action = "Paste"
key    = "V"
mods   = "Control|Shift"

[[keyboard.bindings]]
action = "Copy"
key    = "C"
mods   = "Control|Shift"

[[keyboard.bindings]]
action = "ScrollPageUp"
key    = "PageUp"
mods   = "Shift"

[[keyboard.bindings]]
action = "ScrollPageDown"
key    = "PageDown"
mods   = "Shift"

[[keyboard.bindings]]
action = "ScrollToTop"
key    = "Home"
mods   = "Shift"

[[keyboard.bindings]]
action = "ScrollToBottom"
key    = "End"
mods   = "Shift"

[[keyboard.bindings]]
key = "Return"
mods = "Control|Shift"
action = "SpawnNewInstance"

[[keyboard.bindings]]
action = "IncreaseFontSize"
key = "Equals"
mods = "Control"

[[keyboard.bindings]]
action = "DecreaseFontSize"
key = "Minus"
mods = "Control"

[[keyboard.bindings]]
action = "ClearLogNotice"
key = "L"
mods = "Control"

[[keyboard.bindings]]
chars = "\f"
key = "L"
mods = "Control"

[mouse]
hide_when_typing = true

[[mouse.bindings]]
action = "PasteSelection"
mouse = "Middle"

[debug]
highlight_damage   = false
log_level          = "Warn"
persistent_logging = false
print_events       = false
render_timer       = false

[[hints.enabled]]
regex = "[^ ]+\\.rs:\\d+:\\d+"
command = { program = "code", args = [ "--goto" ] }
mouse = { enabled = true }

```
