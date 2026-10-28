A simple Python utility that automatically takes a screenshot whenever the display changes.

Press **F8** to pause or resume automatic capture; press **Ctrl+C** to exit. Beep
notifications use `beepy` and play asynchronously. The global hotkey requires
Accessibility permission on macOS and a supported display server on Linux
(X11; global key hooks may not work under Wayland).