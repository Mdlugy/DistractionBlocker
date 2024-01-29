import pyKey
def close_window():
    pyKey.pressKey("CTRL")
    pyKey.pressKey("W")
    pyKey.releaseKey("CTRL")
    pyKey.releaseKey("W")