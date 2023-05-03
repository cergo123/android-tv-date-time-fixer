## Android Date & Time Fixer
#### A simple script to fix the NTP server on Android devices (especially TV)

### Description:
Too many Android TV users face a problem where their Android TV time & date reset everytime they power off their TV. This is because the NTP server is not set properly. This script will fix that problem.


### How to use
- Download the executable file from https://github.com/JagarYousef/android-tv-date-time-fixer/releases
- Run it on your device and follow the instructions step by step


### How to build (Ignore this if you are not a developer)
- Clone the repository
- Create a virtual environment
- Install the requirements
- Run `pyinstaller android_time_date_fixer.spec`

### Technical Details
The default Android TV NTP server is mostly `time.android.com`, and like other android links it blocks many countries (e.g. Syria), and also too many other IPs in other countries.
This prevents the device from syncing the time and date, and it resets everytime the device is powered off to the default one, and this in its turn is blocking the WIFI internet connection.

This script will fix this problem by changing the NTP server to `pool.ntp.org` which is a free and open NTP server that is available worldwide.
### Our Facebook Group
[Rojava Programmers Forum](https://www.facebook.com/groups/rpforums)