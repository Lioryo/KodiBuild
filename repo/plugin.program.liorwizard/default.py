# -*- coding: utf-8 -*-
import os, shutil, zipfile, urllib.request
import xbmc, xbmcgui, xbmcvfs

BUILD_URL = "https://lioryo.github.io/KodiBuild/builds/LiorBuild-1.0.zip"
BUILD_NAME = "Lior Build"


def download(url, dest):
    urllib.request.urlretrieve(url, dest)


def main():
    if not xbmcgui.Dialog().yesno("Lior Wizard", "להתקין את " + BUILD_NAME + "?", "הפעולה תחליף את הגדרות Kodi הקיימות."):
        return
    profile = xbmcvfs.translatePath("special://home")
    tmp = xbmcvfs.translatePath("special://temp/LiorBuild.zip")
    xbmcgui.Dialog().notification("Lior Wizard", "מוריד Build...", xbmcgui.NOTIFICATION_INFO, 3000)
    try:
        download(BUILD_URL, tmp)
        xbmcgui.Dialog().notification("Lior Wizard", "מחלץ Build...", xbmcgui.NOTIFICATION_INFO, 3000)
        with zipfile.ZipFile(tmp, 'r') as z:
            z.extractall(profile)
        xbmcgui.Dialog().ok("Lior Wizard", "ההתקנה הסתיימה. סגור ופתח את Kodi מחדש.")
    except Exception as e:
        xbmcgui.Dialog().ok("שגיאה", str(e))

if __name__ == "__main__":
    main()
