# -*- coding: utf-8 -*-
import os, sys, json, zipfile, shutil, urllib.request
import xbmc, xbmcgui, xbmcplugin, xbmcvfs
BASE_URL = 'https://lioryo.github.io/KodiBuild/'
BUILDS_JSON = BASE_URL + 'builds.json'
def tr(p):
    return xbmcvfs.translatePath(p) if hasattr(xbmcvfs, 'translatePath') else xbmc.translatePath(p)
def download(url, dest):
    dp = xbmcgui.DialogProgress(); dp.create('Lior Build Wizard', 'מוריד קובץ...')
    def hook(n, bs, total):
        if dp.iscanceled(): raise Exception('בוטל על ידי המשתמש')
        if total > 0: dp.update(min(100, int(n*bs*100/total)), 'מוריד...')
    urllib.request.urlretrieve(url, dest, hook); dp.close()
def backup_current(home):
    b=os.path.join(home,'lior_backup_before_build')
    if os.path.exists(b): shutil.rmtree(b, ignore_errors=True)
    os.makedirs(b, exist_ok=True)
    for name in ['addons','userdata']:
        s=os.path.join(home,name); d=os.path.join(b,name)
        if os.path.exists(s): shutil.copytree(s,d,ignore=shutil.ignore_patterns('Thumbnails','cache','temp','*.log','*.pyc'))
    return b
def install_build():
    try:
        tmp_json=os.path.join(tr('special://temp'),'lior_builds.json'); download(BUILDS_JSON,tmp_json)
        with open(tmp_json,'r',encoding='utf-8') as f: build=json.load(f)['builds'][0]
        if not xbmcgui.Dialog().yesno('Lior Build Wizard','להתקין את %s גרסה %s?'%(build['name'],build['version']),'מומלץ לבצע על Kodi חדש.','יבוצע גיבוי מקומי לפני ההתקנה.'):
            return
        home=tr('special://home'); backup_current(home)
        zpath=os.path.join(tr('special://temp'),'LiorBuild.zip'); download(build['url'],zpath)
        dp=xbmcgui.DialogProgress(); dp.create('Lior Build Wizard','מתקין Build...')
        with zipfile.ZipFile(zpath,'r') as z:
            members=z.infolist(); total=len(members)
            for i,m in enumerate(members):
                if dp.iscanceled(): raise Exception('בוטל על ידי המשתמש')
                target=os.path.abspath(os.path.join(home,m.filename))
                if target.startswith(os.path.abspath(home)): z.extract(m,home)
                if i%20==0: dp.update(int(i*100/max(total,1)),'מעתיק קבצים...')
        dp.close(); xbmcgui.Dialog().ok('Lior Build Wizard','ההתקנה הסתיימה.','סגור ופתח מחדש את Kodi.'); xbmc.executebuiltin('RestartApp')
    except Exception as e:
        xbmc.log('[Lior Wizard] ERROR: %s'%e, xbmc.LOGERROR); xbmcgui.Dialog().ok('שגיאה','ההתקנה נכשלה:',str(e))
def menu():
    li=xbmcgui.ListItem('התקן Lior Build'); xbmcplugin.addDirectoryItem(int(sys.argv[1]), sys.argv[0]+'?action=install', li, False); xbmcplugin.endOfDirectory(int(sys.argv[1]))
if __name__ == '__main__':
    install_build() if 'action=install' in sys.argv[-1] else menu()
