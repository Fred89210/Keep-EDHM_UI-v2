# Keep EDHM_UI v2

You want to keep [EDHM_UI](https://github.com/BlueMystical/EDHM_UI) v2 while waiting for [EDHM_UI](https://github.com/BlueMystical/EDHM_UI) v3 to become more stable but you still want to use the latest version of [EDHM](https://github.com/psychicEgg/EDHM/tree/main/Odyssey), this script is for you.

This script automatically replaces certain files in EDHM_UI v2 so that it installs and runs with the latest version of EDHM.

Additionally, this script replaces the EDHM_UI update mechanism, so EDHM_UI v2 will no longer prompt you to install the update to v3. If you later wish to upgrade to v3, download the installer from the [EDHM_UI Github](https://github.com/BlueMystical/EDHM_UI).

With this change, if a script update becomes available, EDHM_UI will prompt you to update with the usual popup. Accept the update, and you're done.

I will release updates at the same time as I release new versions of [EDHM](https://github.com/psychicEgg/EDHM/tree/main/Odyssey), as long as I feel v2 is still useful.

Updates made using this script will:
- Add the latest version of EDHM
- Add/modify/remove EDHM options *(as needed)*
- Add new ships to the EDHM_UI Shipyard

These updates will not fix user interface issues or make changes other than EDHM options, as the EDHM_UI application will remain at version 2.2.67.

---

- **Close the game**.
- Install [EDHM_UI v2.2.67](https://github.com/BlueMystical/EDHM_UI/releases/tag/v2.2.67) *(if it hasn't already)*
- Run the [latest version of the script](https://github.com/Fred89210/Keep-EDHM_UI-v2/releases)

If all goes as expected, the script will start [EDHM_UI](https://github.com/BlueMystical/EDHM_UI) when it finishes, and EDHM_UI will install the new version of [EDHM](https://github.com/psychicEgg/EDHM/tree/main/Odyssey).

This script has been designed and tested only on Windows 10/11.

---

NOTE:

Since translations have been left out of the original project for a very long time, languages other than English show poor results.

For simplicity, I'm only maintaining English, so **I recommend using the app in English**.

---

### <ins>Troubleshooting</ins>

If you used EDHM_UI v3, you may encounter the following error message in EDHM_UI v2:

NOTE:

From December 2025, the update script includes a mechanism to automatically move the EDHM_UI v3 history files, so this error should no longer occur. These files will be placed in the `save_v3_history` subfolder of the `History` folder.

```String was not recognized as a valid DateTime. at System.DateTime.ParseExact(String s, String format, IFormatProvider provider) at EDHM_UI_mk2.MainForm.History_LoadElements(Int32 ItemsToLoad) in G:\@Proyectos\EDHM_UI\source\EDHM_UI_mk2\MainForm.cs:line 3151``` 

This is caused by the presence of EDHM_UI v3 history files. These files do not use the same format as EDHM_UI v2, which prevents v2 from reading them.

To solve the problem, simply go to the folder `%USERPROFILE%\EDHM_UI\ODYSS\History` and delete the files with a name like `20251006T090148520Z` *(or even delete all the contents of this folder if you do not need to keep your history)*.

---

I've been developing EDHM since 2023 but I'm not a developer, I'm just trying to do my best so please bear with me.

More information about [EDHM here](https://github.com/psychicEgg/EDHM/tree/main/Odyssey).
