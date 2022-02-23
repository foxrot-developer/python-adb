from operator import index
import subprocess
import distutils.spawn
import os
import re
import pandas as pd
import csv

ADB_NAME = "adb"
AAPT_NAME = "aapt"

path = './sample'

apks = os.listdir(path)


# Function for checking adb status
def checkADB():

    if(distutils.spawn.find_executable(ADB_NAME) == None):
        return False
    if(distutils.spawn.find_executable(AAPT_NAME) == None):
        return False
    return True


# Function for installing apk
def installAPK(apkPath):

    print("Installing APK...")
    installCommand = [ADB_NAME, "install", apkPath]
    print("APK installed...")
    return subprocess.call(installCommand) == 0

# Generating logcat


def generateLogcat(apkName, package):
    print("Generating logcat for "+apkName+"....")
    os.system(f'adb -d logcat {package} > ./logcat/'+apkName+'.txt')
    print("Logcat generated successfully "+apkName+"....")
    return

# Function for getting apk details


def get_packagename(path, apkName):
    aapt = []
    os.system(f'aapt dump badging {path}> ./logs/'+apkName+'.txt')
    with open('./logs/'+apkName+'.txt', 'rb') as f:
        p1 = "package: name='(.+?)'"
        results1 = re.finditer(pattern=p1, string=f.readline().decode('utf-8'))
        for r in results1:
            packagename = r.group(1)
            aapt.append(packagename)
        p2 = "launchable-activity: name='(.+?)'"
        st = str(f.readlines())
        results2 = re.findall(p2, st)
        activity = results2[0]
        aapt.append(activity)
        print("Reading package done")
        generateLogcat(apkName, aapt[0])
    return aapt


def generateCSV(columns, data):
    print(columns)
    with open('Output.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)
        print("Csv created ........")


features = []


def findExistance(apk):

    permission_dict = {
        'package_name': apk,
        'SEND_SMS': 0,
        'READ_PHONE_STATE': 0,
        'GET_ACCOUNTS': 0,
        'RECEIVE_SMS': 0,
        'READ_SMS': 0,
        'USE_CREDENTIALS': 0,
        'MANAGE_ACCOUNTS': 0,
        'WRITE_SMS': 0,
        'READ_SYNC_SETTINGS': 0,
        'AUTHENTICATE_ACCOUNTS': 0,
        'WRITE_HISTORY_BOOKMARKS': 0,
        'INSTALL_PACKAGES': 0,
        'CAMERA': 0,
        'WRITE_SYNC_SETTINGS': 0,
        'READ_HISTORY_BOOKMARKS': 0,
        'INTERNET': 0,
        'RECORD_AUDIO': 0,
        'NFC': 0,
        'ACCESS_LOCATION_EXTRA_COMMANDS': 0,
        'WRITE_APN_SETTINGS': 0,
        'BIND_REMOTEVIEWS': 0,
        'READ_PROFILE': 0,
        'MODIFY_AUDIO_SETTINGS': 0,
        'READ_SYNC_STATS': 0,
        'BROADCAST_STICKY': 0,
        'WAKE_LOCK': 0,
        'RECEIVE_BOOT_COMPLETED': 0,
        'RESTART_PACKAGES': 0,
        'BLUETOOTH': 0,
        'READ_CALENDAR': 0,
        'READ_CALL_LOG': 0,
        'SUBSCRIBED_FEEDS_WRITE': 0,
        'READ_EXTERNAL_STORAGE': 0,
        'ACCESS_NETWORK_STATE': 0,
        'SUBSCRIBED_FEEDS_READ': 0,
        'CHANGE_WIFI_MULTICAST_STATE': 0,
        'WRITE_CALENDAR': 0,
        'MASTER_CLEAR': 0,
        'UPDATE_DEVICE_STATS': 0,
        'WRITE_CALL_LOG': 0,
        'DELETE_PACKAGES': 0,
        'GET_TASKS': 0,
        'GLOBAL_SEARCH': 0,
        'DELETE_CACHE_FILES': 0,
        'WRITE_USER_DICTIONARY': 0,
        'REORDER_TASKS': 0,
        'WRITE_PROFILE': 0,
        'SET_WALLPAPER': 0,
        'BIND_INPUT_METHOD': 0,
        'READ_SOCIAL_STREAM': 0,
        'READ_USER_DICTIONARY': 0,
        'PROCESS_OUTGOING_CALLS': 0,
        'CALL_PRIVILEGED': 0,
        'BIND_WALLPAPER': 0,
        'RECEIVE_WAP_PUSH': 0,
        'DUMP': 0,
        'BATTERY_STATS': 0,
        'ACCESS_COARSE_LOCATION': 0,
        'SET_TIME': 0,
        'WRITE_SOCIAL_STREAM': 0,
        'WRITE_SETTINGS': 0,
        'REBOOT': 0,
        'BLUETOOTH_ADMIN': 0,
        'BIND_DEVICE_ADMIN': 0,
        'WRITE_GSERVICES': 0,
        'KILL_BACKGROUND_PROCESSES': 0,
        'SET_ALARM': 0,
        'ACCOUNT_MANAGER': 0,
        'STATUS_BAR': 0,
        'PERSISTENT_ACTIVITY': 0,
        'CHANGE_NETWORK_STATE': 0,
        'RECEIVE_MMS': 0,
        'SET_TIME_ZONE': 0,
        'CONTROL_LOCATION_UPDATES': 0,
        'BROADCAST_WAP_PUSH': 0,
        'BIND_ACCESSIBILITY_SERVICE': 0,
        'ADD_VOICEMAIL': 0,
        'CALL_PHONE': 0,
        'BIND_APPWIDGET': 0,
        'FLASHLIGHT': 0,
        'READ_LOGS': 0,
        'SET_PROCESS_LIMIT': 0,
        'MOUNT_UNMOUNT_FILESYSTEMS': 0,
        'BIND_TEXT_SERVICE': 0,
        'INSTALL_LOCATION_PROVIDER': 0,
        'SYSTEM_ALERT_WINDOW': 0,
        'MOUNT_FORMAT_FILESYSTEMS': 0,
        'CHANGE_CONFIGURATION': 0,
        'CLEAR_APP_USER_DATA': 0,
        'CHANGE_WIFI_STATE': 0,
        'READ_FRAME_BUFFER': 0,
        'ACCESS_SURFACE_FLINGER': 0,
        'BROADCAST_SMS': 0,
        'EXPAND_STATUS_BAR': 0,
        'INTERNAL_SYSTEM_WINDOW': 0,
        'SET_ACTIVITY_WATCHER': 0,
        'WRITE_CONTACTS': 0,
        'BIND_VPN_SERVICE': 0,
        'DISABLE_KEYGUARD': 0,
        'ACCESS_MOCK_LOCATION': 0,
        'GET_PACKAGE_SIZE': 0,
        'MODIFY_PHONE_STATE': 0,
        'CHANGE_COMPONENT_ENABLED_STATE': 0,
        'CLEAR_APP_CACHE': 0,
        'SET_ORIENTATION': 0,
        'READ_CONTACTS': 0,
        'DEVICE_POWER': 0,
        'HARDWARE_TEST': 0,
        'ACCESS_WIFI_STATE': 0,
        'WRITE_EXTERNAL_STORAGE': 0,
        'ACCESS_FINE_LOCATION': 0,
        'SET_WALLPAPER_HINTS': 0,
        'SET_PREFERRED_APPLICATIONS': 0,
        'WRITE_SECURE_SETTINGS': 0}

    logFile = open('./logs/'+apk+'.txt', 'r')
    lines = logFile.readlines()
    for key in permission_dict:
        for line in lines:
            if(key in line):
                permission_dict[key] = 1

    features.append(permission_dict)
    return list(permission_dict.keys())


def findExistanceSignature(apk):

    permission_dict = {
        'transact': 0,
        'onServiceConnected': 0,
        'bindService': 0,
        'attachInterface': 0,
        'ServiceConnection': 0,
        'android.os.Binder': 0,
        'java.lang.Class.getCanonicalName': 0,
        'java.lang.Class.getMethods': 0,
        'java.lang.Class.cast': 0,
        'java.net.URLDecoder': 0,
        'android.content.pm.Signature': 0,
        'android.telephony.SmsManager': 0,
        'getBinder': 0,
        'ClassLoader': 0,
        'android.content.Context.registerReceiver': 0,
        'java.lang.Class.getField': 0,
        'android.content.Context.unregisterReceiver': 0,
        'java.lang.Class.getDeclaredField': 0,
        'getCallingUid': 0,
        'javax.crypto.spec.SecretKeySpec': 0,
        'android.intent.action.BOOT_COMPLETED': 0,
        'android.content.pm.PackageInfo': 0,
        'KeySpec': 0,
        'TelephonyManager.getLine1Number': 0,
        'DexClassLoader': 0,
        'HttpGet.init': 0,
        'SecretKey': 0,
        'java.lang.Class.getMethod': 0,
        'System.loadLibrary': 0,
        'android.intent.action.SEND': 0,
        'javax.crypto.Cipher': 0,
        'android.telephony.gsm.SmsManager': 0,
        'TelephonyManager.getSubscriberId,': 0,
        'Runtime.getRuntime': 0,
        'java.lang.Object.getClass': 0,
        'java.lang.Class.forName': 0,
        'android.intent.action.PACKAGE_REPLACED': 0,
        'Binder': 0,
        'android.intent.action.SEND_MULTIPLE': 0,
        'IBinder': 0,
        'android.os.IBinder': 0,
        'createSubprocess': 0,
        'URLClassLoader': 0,
        'abortBroadcast': 0,
        'android.intent.action.TIME_SET': 0,
        'TelephonyManager.getDeviceId': 0,
        'getCallingPid': 0,
        'android.intent.action.PACKAGE_REMOVED': 0,
        'android.intent.action.TIMEZONE_CHANGED': 0,
        'java.lang.Class.getPackage': 0,
        'java.lang.Class.getDeclaredClasses': 0,
        'android.intent.action.ACTION_POWER_DISCONNECTED': 0,
        'android.intent.action.PACKAGE_ADDED': 0,
        'PathClassLoader': 0,
        'TelephonyManager.getSimSerialNumber': 0,
        'Runtime.load': 0,
        'TelephonyManager.getCallState': 0,
        'TelephonyManager.getSimCountryIso': 0,
        'sendMultipartTextMessage': 0,
        'PackageInstaller': 0,
        'sendDataMessage': 0,
        'HttpPost.init': 0,
        'java.lang.Class.getClasses': 0,
        'TelephonyManager.isNetworkRoaming': 0,
        'android.intent.action.PACKAGE_DATA_CLEARED': 0,
        'HttpUriRequest': 0,
        'android.intent.action.PACKAGE_CHANGED': 0,
        'android.intent.action.NEW_OUTGOING_CALL': 0,
        'divideMessage': 0,
        'Runtime.exec,': 0,
        'android.intent.action.SENDTO': 0,
        'TelephonyManager.getNetworkOperator': 0,
        'MessengerService': 0,
        'IRemoteService': 0,
        'SET_ALARM': 0,
        'ACCOUNT_MANAGER': 0,
        'android.intent.action.CALL': 0,
        'TelephonyManager.getSimOperator': 0,
        'onBind': 0,
        'Process.start': 0,
        'android.intent.action.SCREEN_ON': 0,
        'Context.bindService': 0,
        'android.intent.action.BATTERY_OKAY': 0,
        'ProcessBuilder': 0,
        'java.lang.Class.getResource': 0,
        'defineClass': 0,
        'android.intent.action.PACKAGE_RESTARTED': 0,
        'android.intent.action.CALL_BUTTON': 0,
        'android.intent.action.CALL_BUTTON': 0,
        'android.intent.action.CALL_BUTTON': 0,
        'findClass': 0,
        'intent.action.RUN': 0,
        'android.intent.action.SET_WALLPAPER': 0,
        'Runtime.loadLibrary': 0,
        'android.intent.action.BATTERY_LOW': 0,
        'android.intent.action.ACTION_POWER_CONNECTED': 0,
    }

    logFile = open('./logcat/'+apk+'.txt', 'r')
    lines = logFile.read()
    for key in permission_dict:
        if(key in lines):
            permission_dict[key] = lines.count(key)

    features.append(permission_dict)
    return list(permission_dict.keys())


print(checkADB())

global permissionsColumns, signatureColumns

for apk in apks:
    installAPK('./sample/'+apk)
    result = get_packagename('./sample/'+apk, apk)
    print(result[0])
    permissionsColumns = findExistance(apk)
    signatureColumns = findExistanceSignature(apk)

temp = []
temp = permissionsColumns + signatureColumns

print(temp)

generateCSV(temp, features)
