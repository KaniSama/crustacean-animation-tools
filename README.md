Download latest release [here](https://github.com/KaniSama/crustacean-animation-tools/releases/latest).


# summary
1. [Keyfiller](#keyfiller)
2. [Keychooser](#keychooser)
3. [Keyframe Pies](#keyframe-pies)
4. [Sim setup (CLS)](#cls-sim-setup)

# keyfiller


This add-on adds a function to the dope sheet that inserts keyframes on all channels wherever there's a keyframe on any channel.

Dopesheet > Key > Keyfill

Works on all channels only for selected bones / objects.

![Showcase of the add-on: Keyfill button](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/Keyfiller/Button.png?raw=true)

| Before Keyfill: | After Keyfill: |
| ------ | ------ |
| ![Showcase of the add-on: before](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/Keyfiller/Before.png?raw=true) | ![Showcase of the add-on: after](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/Keyfiller/After.png?raw=true) |




# keychooser


This add-on adds a function to the dope sheet that selects/deselects keyframes on every Nth frame.




# keyframe-pies


This add-on replaces your old Insert Keyframe menu with a pie menu.
>! (Because somebody thought that showing your users the longest list imaginable is a good idea somehow.)

Latches onto the key binding you already have set to "Insert Keyframe". Press it for old menu, hold it for new menu. Shrimple.


| Old menu: | New menu: |
| ------ | ------ |
| ![Showcase of the add-on: old menu](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/KeyframePies/KeyframePiesOldMenu.png?raw=true) | ![Showcase of the add-on: new menu](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/KeyframePies/KeyframePiesNewMenu.png?raw=true) |


Only works in Pose Mode.


## If the add-on stopped working after closing blender:
- Press T in the 3D Viewport window;
- In the toolbox on the left, click "Start add-on" under "Keyframe Pies".
That should bring it back.

![Instructions on restarting the add-on](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/KeyframePies/KeyframePiesDocs.png?raw=true)




# cls-sim-setup


This module inserts an initial keyframe for a selected rig. Make sure you already have the necessary F-curves.

Dopesheet > Key > Setup for simulation

![Showcase of the add-on: Menu](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/CLSSetup/CLSSetupMenu.png?raw=true)

![Showcase of the add-on: Ignore root toggle](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/CLSSetup/CLSSetupMenu2.png?raw=true)

| No "Ignore root": | With "Ignore root": |
| ------ | ------ |
| ![Showcase of the add-on: root](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/CLSSetup/CLSSetupAfterWithRoot.gif?raw=true) | ![Showcase of the add-on: no root](https://github.com/KaniSama/crustacean-animation-tools/blob/main/images/CLSSetup/CLSSetupNoRoot.gif?raw=true) |
