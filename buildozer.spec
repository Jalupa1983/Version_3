[app]

# -------------------------
# App Information
# -------------------------
title = From Darkness We Climb
package.name = FromDarknessWeClimb
package.domain = org.example
source.dir = .
source.main = main.py
version = 1.0.0
android.version_code = 1
icon.filename = images/fdwc.png

# Supported orientations: landscape, portrait, portrait-reverse, landscape-reverse
orientation = portrait

# -------------------------
# Files to Include
# -------------------------
source.include_exts = py,png,json,txt

# -------------------------
# Python Requirements
# -------------------------
requirements = python3,python-dateutil,kivy,plyer,android

# -------------------------
# Permissions
# -------------------------
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

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
android.archs = arm64-v8a,armeabi-v7a

# -------------------------
# App Storage & Backup
# -------------------------
android.allow_backup = True
android.private_storage = True

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

# -------------------------
# Signing configuration
# -------------------------
android.release_keystore = /home/jason/Documents/Version_3/my-release-key.keystore
android.keystore_password = FromDarknessWeClimb
android.keyalias_name = fdwc-key
android.keyalias_password = FromDarknessWeClimb

[buildozer]

# -------------------------
# Logging
# -------------------------
log_level = 2
warn_on_root = 1

# -------------------------
# Output Directory
# -------------------------
# bin_dir = ./bin
