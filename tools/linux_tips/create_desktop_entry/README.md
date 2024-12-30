# Creating a Working `firefox.desktop` File in Ubuntu 20.04

When setting up a custom `.desktop` file for Firefox in Ubuntu 20.04, there are a few pitfalls to watch out for. Here's a step-by-step guide to help you successfully create one.

---

## Key Considerations

1. **No "Allow Launching" Option**: Unlike some earlier versions of Ubuntu, "Allow Launching" is not an option in Ubuntu 20.04.
2. **Full Path for Executable**: The `Exec=` value in the `.desktop` file must contain the full path to the Firefox executable (e.g., `/home/wonko/myapps/firefox/firefox`), unless the executable resides in a directory specified in the `$PATH` variable.
3. **Correct Directory**: The `.desktop` file must be placed in the `~/.local/share/applications/` directory for it to be recognized.

---

## Steps to Create the `firefox.desktop` File

Follow these steps to set up Firefox without installing additional software, all from the command line:

### 1. [Optional] Add a Custom Firefox Icon
- Download a Firefox icon from the web.
- Save it to the `~/.local/share/icons/` directory.
- Name the icon file `firefox`, keeping its original file extension (e.g., `.png`, `.ico`, `.svg`).
- Using the original filename allows your system's themes to apply icon changes dynamically.

---

### 2. Create the `.desktop` File
- Create a file named `firefox.desktop` in the `~/.local/share/applications/` directory:
  ```bash
  touch ~/.local/share/applications/firefox.desktop
  ```
  
- paste the below container [replace the executable file]
    ```
    #!/usr/bin/env xdg-open
    [Desktop Entry]
    Type=Application
    Terminal=false
    Exec=/home/wonko/myapps/firefox/firefox
    Name=Firefox
    Comment=Firefox
    Icon=firefox
    Categories=GNOME;GTK;Network;WebBrowser;
    ```

### 3 Make file executable
  ``` bash
  chmod +x ~/.local/share/applications/firefox.desktop
  ```
