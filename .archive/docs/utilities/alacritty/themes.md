# Alacritty Themes

You can customize the appearance/theme of Alacritty by cloning the [alacrity-theme Github repository](https://github.com/alacritty/alacritty-theme).

## Install themes

- Create a directory `~/.config/alacritty`
- `cd` into the newly created directory and clone the themes repository
  - `cd ~/.config/alacritty`
  - `git clone https://github.com/alacritty/alacritty-theme .`

## Configure Alacritty theme

- Edit your `alacritty.toml` file
  - At the top of the file, add an `import` statement with the path to a theme in the `themes/` directory of the cloned repository
  - Example: `import = ["~/.config/alacritty/themes/atom_one_dark.toml"]`

Visit the [Alacritty Github](https://github.com/alacritty/alacritty-theme#color-schemes) for all themes & previews.
