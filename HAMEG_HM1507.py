import serial
import time
import logging

class HAMEG_HM1507:
  TIME_DIVS = [
    "50ns",
    "100ns",
    "200ns",
    "500ns",
    "1us",
    "2us",
    "5us",
    "10us",
    "20us",
    "50us",
    "100us",
    "200us",
    "500us",
    "1ms",
    "2ms",
    "5ms",
    "10ms",
    "20ms",
    "50ms",
    "100ms",
    "200ms",
    "500ms",
    "1s",
    "2s",
    "5s",
    "10s",
    "20s",
    "50s",
    "100s"
  ]
  V_DIVS = [
    "1mV",
    "2mV",
    "5mV",
    "10mV",
    "20mV",
    "50mV",
    "100mV",
    "200mV",
    "500mV",
    "1V",
    "2V",
    "5V",
    "10V",
    "20V"
  ]


  def __init__(self):
    self._ser = None
    self._logger = logging.getLogger("HAMEG_HM1507")
    
  def __del__(self):
    self.disconnect()

  def connect(self, port):
    self.disconnect()
    self._logger.info("connecting")
    self._ser = serial.Serial(port=port, baudrate=19200, timeout=1,
                              rtscts=True, stopbits=serial.STOPBITS_TWO,
                              parity=serial.PARITY_NONE)
    self._command(" ")

  def disconnect(self):
    if self._ser is not None:
      self._logger.info("disconnecing")
      self._command("rm0")
      self._ser.close()
      self._ser = None

  def _command(self, command):
    self._logger.debug("sending command: "+command)
    if self._ser is not None:
      for ch in command:
        self._ser.write(ch.encode("utf-8"))
      self._ser.write(b"\r")
      # print(ser.readline())
    else:
      self._logger.warning("Not connected!")
  
  def autoset(self):
    self._command("AUTOSET")
  
  def timeBase(self, base, single, timeDiv):
    if (base is not "A") and (base is not "B"):
      raise IndexError("Only time base A and B exist")
    settings = 0
    if single:
      settings += 32
    if timeDiv not in self.TIME_DIVS:
      raise IndexError("Unknown timeDiv!")
    settings += self.TIME_DIVS.index(timeDiv)
    
    self._command("TB"+str(base)+"="+chr(settings))
  
  def channel(self, channel, inv, modeDc, vDiv):
    if (channel is not 1) and (channel is not 2):
      raise IndexError("Only channel 1 and 2 exist")
    settings = 16
    if inv:
      settings += 32
    if not modeDc:
      settings += 64
    if vDiv not in self.V_DIVS:
      raise IndexError("Unknown vDiv!")
    settings += self.V_DIVS.index(vDiv)
    
    self._command("CH"+str(channel)+"="+chr(settings))
