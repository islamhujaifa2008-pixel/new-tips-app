[app]

title = New Tips
package.name = newtips
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf
version = 0.1
requirements = python3,kivy==2.3.0,urllib3,certifi
orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
