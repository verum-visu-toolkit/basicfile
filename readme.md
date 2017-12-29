Install [YAJL 2](https://lloyd.github.io/yajl/) for much faster basicfile parsing.
(todo: find windows installer)

Instructions for Windows:

1. Install [cmake](https://cmake.org/downloads)
2. Install "Visual C++ for Python"
3. Clone [the source of yajl](https://github.com/lloyd/yajl)
4. Follow the instructions in BUILDING.win32 to build + install yajl (be sure to run the cmd prompt as administrator)
5. Copy yajl.dll from the build folder into C:\Windows\SysWOW64 and C:\Windows\System32 (I'm not sure which of these is necessary, but it works for me when it's in both)

todo: make a script that automates as much of this as possible
(e.g. cloning + installing yajl)