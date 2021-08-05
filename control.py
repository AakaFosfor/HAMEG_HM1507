from HAMEG_HM1507 import *

h = HAMEG_HM1507()
# h.timeBase("A", False, "2ms");
# h.channel(1, False, HAMEG_HM1507.CH_DC, "100mV")


from pynput.keyboard import Key, Listener
timeBaseSingle = False
timeBaseDivIndex = 5
channelInv = False
channelDc = True
channelDivIndex = 5
def on_release(key):
  # print('{0} release'.format(key))
  global timeBaseSingle
  global timeBaseDivIndex
  global channelInv
  global channelDc
  global channelDivIndex
  updateTime = False
  updateChannel = False
  try:
    if key.char == "q":
      return False
    if key.char == "c":
      h.connect("COM7")
      updateTime = True
      updateChannel = True
    if key.char == "d":
      h.disconnect();
    if key.char == "a":
      h.autoset();
    if key.char == "s":
      timeBaseSingle = not timeBaseSingle;
      updateTime = True
    if key.char == "o":
      timeBaseDivIndex = min(timeBaseDivIndex+1, len(HAMEG_HM1507.TIME_DIVS)-1)
      updateTime = True
    if key.char == "p":
      timeBaseDivIndex = max(timeBaseDivIndex-1, 0)
      updateTime = True
    if key.char == "i":
      channelInv = not channelInv;
      updateChannel = True
    if key.char == "u":
      channelDc = not channelDc;
      updateChannel = True
    if key.char == "y":
      channelDivIndex = min(channelDivIndex+1, len(HAMEG_HM1507.V_DIVS)-1)
      updateChannel = True
    if key.char == "x":
      channelDivIndex = max(channelDivIndex-1, 0)
      updateChannel = True
  except AttributeError:
    if key == Key.esc:
      return False
  if updateTime:
    h.timeBase("A", timeBaseSingle, HAMEG_HM1507.TIME_DIVS[timeBaseDivIndex])
  if updateChannel:
    h.channel(1, channelInv, channelDc, HAMEG_HM1507.V_DIVS[channelDivIndex])
  
print("q/ESC - end")
print("c - connect")
print("d - disconnect")
print("a - autoset")
print("s - time base single")
print("o - time base +")
print("p - time base -")
print("i - channel inv")
print("u - channel dc/ac")
print("y - channel voltage +")
print("x - channel voltage -")

with Listener(on_release=on_release) as listener:
  listener.join()
