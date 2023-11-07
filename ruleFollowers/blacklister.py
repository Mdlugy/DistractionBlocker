import pyKey
def closeWindow(options):
    pyKey.pressKey("CTRL")
    pyKey.pressKey("W")
    pyKey.releaseKey("CTRL")
    pyKey.releaseKey("W")