[app]



# (str) Title of your application
title = SumUp

# (str) Package name
package.name = SumUp

# (str) Package domain (needed for android/ios packaging)
package.domain = sumup_game

# (str) Source code where the main.py live
source.dir = ./
#source.dir = /home/yjy/Desktop/test/

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,numpy

# (list) Supported orientations
# Valid options are: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait
# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 31

# (int) Android SDK version to use
#android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
android.wakelock = False

# (list) Android application meta-data to set (key=value format)
android.meta_data = android.debug=true


# (list) The Android archs to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
#android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
#android.allow_backup = True
