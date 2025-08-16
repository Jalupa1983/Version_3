[app]

# -------------------------
# App Information
# -------------------------
title = From Darkness We Climb
package.name = clean_time_tracker
package.domain = org.example
source.dir = .
source.main = main.py
version = 0.1
icon.filename = images/fdwc.png
orientation = portrait  # portrait, landscape, or reverse

# -------------------------
# Files to Include
# -------------------------
source.include_exts = py,png,json,txt

# -------------------------
# Python Requirements
# -------------------------
requirements = python3,kivy,plyer,android

# -------------------------
# Permissions
# -------------------------
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# -------------------------
# Android API / NDK Settings
# -------------------------
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# -------------------------
# Architecture
# -------------------------
android.archs = arm64-v8a, armeabi-v7a

# -------------------------
# App Storage & Backup
# -------------------------
android.allow_backup = True
android.private_storage = True  # store data in app-private folder

# -------------------------
# Python-for-Android
# -------------------------
p4a.branch = develop
p4a.bootstrap = sdl2

# -------------------------
# Display & Input
# -------------------------
fullscreen = 0
android.keyboard = True

[buildozer]

# -------------------------
# Logging
# -------------------------
log_level = 2       # 0 = errors, 1 = info, 2 = debug
warn_on_root = 1    # warn if running buildozer as root

# -------------------------
# Output Directory
# -------------------------
# bin_dir = ./bin  # default is fine
