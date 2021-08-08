import logging
import tkinter as tk
import serial.tools.list_ports;
import HAMEG_HM1507 as HM

class Gui:

  def __init__(self):
    r = tk.Tk()
    r.title("HAMEG HM1507 Control Panel")
  
    self._port = tk.StringVar(r)
    self._port.set("(N/A)")
    self._h = HM.HAMEG_HM1507()
    self._channels = {
      1: {
        "inv": False,
        "mode_dc": True,
        "div_index": 5
      },
      2: {
        "inv": False,
        "mode_dc": True,
        "div_index": 5
      }
    }
    self._tbases = {
      "A": {
        "single": False,
        "div_index": 5
      },
      "B": {
        "single": False,
        "div_index": 5
      }
    }
    
    f = tk.Frame(r)
    tk.Label(f, text="Port:").pack(side=tk.LEFT)
    self._port_list = tk.OptionMenu(f, self._port, [self._port.get()])
    self._port_list.pack(side=tk.LEFT)
    tk.Button(f, text="Refresh list", command=self._btn_refresh_port_list).pack(side=tk.LEFT)
    tk.Button(f, text="Connect", command=self._btn_connect).pack(side=tk.LEFT)
    tk.Button(f, text="Disconnect", command=self._btn_disconnect).pack(side=tk.LEFT)
    f.pack(side=tk.TOP)
    
    f = tk.Frame(r)
    tk.Button(f, text="AUTOSET", command=self._h.autoset).pack(side=tk.LEFT)
    f.pack(side=tk.LEFT)
    
    f = tk.Frame(r)
    tk.Button(f, text="^\nv", command=lambda: self._btn_channel_down(1)).pack(side=tk.TOP)
    tk.Label(f, text="CHI").pack(side=tk.TOP)
    tk.Button(f, text="v\n^", command=lambda: self._btn_channel_up(1)).pack(side=tk.TOP)
    tk.Button(f, text="INV.", command=lambda: self._btn_channel_inv(1)).pack(side=tk.TOP)
    tk.Button(f, text="DC/AC", command=lambda: self._btn_channel_dcac(1)).pack(side=tk.TOP)
    f.pack(side=tk.LEFT)
    
    f = tk.Frame(r)
    tk.Button(f, text="^\nv", command=lambda: self._btn_channel_down(2)).pack(side=tk.TOP)
    tk.Label(f, text="CHII").pack(side=tk.TOP)
    tk.Button(f, text="v\n^", command=lambda: self._btn_channel_up(2)).pack(side=tk.TOP)
    tk.Button(f, text="INV.", command=lambda: self._btn_channel_inv(2)).pack(side=tk.TOP)
    tk.Button(f, text="DC/AC", command=lambda: self._btn_channel_dcac(2)).pack(side=tk.TOP)
    f.pack(side=tk.LEFT)
    
    f = tk.Frame(r)
    tk.Button(f, text="<>", command=lambda: self._btn_tbase_down("A")).pack(side=tk.LEFT)
    tk.Label(f, text="TB A").pack(side=tk.LEFT)
    tk.Button(f, text="><", command=lambda: self._btn_tbase_up("A")).pack(side=tk.LEFT)
    tk.Button(f, text="SGL", command=lambda: self._btn_tbase_single("A")).pack(side=tk.LEFT)
    f.pack(side=tk.TOP)
    
    f = tk.Frame(r)
    tk.Button(f, text="<>", command=lambda: self._btn_tbase_down("B")).pack(side=tk.LEFT)
    tk.Label(f, text="TB B").pack(side=tk.LEFT)
    tk.Button(f, text="><", command=lambda: self._btn_tbase_up("B")).pack(side=tk.LEFT)
    tk.Button(f, text="SGL", command=lambda: self._btn_tbase_single("B")).pack(side=tk.LEFT)
    f.pack(side=tk.TOP)
    
    self._root = r
    self._btn_refresh_port_list()
    
  def run(self):
    self._root.mainloop()
  
  def _btn_refresh_port_list(self):
    available_ports = [comport.device for comport in serial.tools.list_ports.comports()]
    
    self._port_list['menu'].delete(0, 'end')
    for port in available_ports:
      self._port_list['menu'].add_command(label=port, command=tk._setit(self._port, port))
    
    if self._port.get() not in available_ports:
      self._port.set(available_ports[0])
  
  def _btn_connect(self):
    self._h.connect(self._port.get())
    self._update_channel(1)
    self._update_channel(2)
    self._update_tbase("A")
    self._update_tbase("B")
    
  def _btn_disconnect(self):
    self._h.disconnect()
    
  def _btn_channel_up(self, ch):
    self._channels[ch]["div_index"] = min(self._channels[ch]["div_index"]+1, len(HM.HAMEG_HM1507.V_DIVS)-1)
    self._update_channel(ch)
  
  def _btn_channel_down(self, ch):
    self._channels[ch]["div_index"] = max(self._channels[ch]["div_index"]-1, 0)
    self._update_channel(ch)
  
  def _btn_channel_inv(self, ch):
    self._channels[ch]["inv"] = not self._channels[ch]["inv"]
    self._update_channel(ch)
  
  def _btn_channel_dcac(self, ch):
    self._channels[ch]["mode_dc"] = not self._channels[ch]["mode_dc"]
    self._update_channel(ch)
  
  def _update_channel(self, ch):
    channel = self._channels[ch]
    div = HM.HAMEG_HM1507.V_DIVS[channel["div_index"]]
    self._h.channel(ch, channel["inv"], channel["mode_dc"], div)

  def _btn_tbase_up(self, tb):
    self._tbases[tb]["div_index"] = min(self._tbases[tb]["div_index"]+1, len(HM.HAMEG_HM1507.TIME_DIVS)-1)
    self._update_tbase(tb)
  
  def _btn_tbase_down(self, tb):
    self._tbases[tb]["div_index"] = max(self._tbases[tb]["div_index"]-1, 0)
    self._update_tbase(tb)
  
  def _btn_tbase_single(self, tb):
    self._tbases[tb]["single"] = not self._tbases[tb]["single"]
    self._update_tbase(tb)
  
  def _update_tbase(self, tb):
    tbase = self._tbases[tb]
    div = HM.HAMEG_HM1507.TIME_DIVS[tbase["div_index"]]
    self._h.timeBase(tb, tbase["single"], div)

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.WARNING)

app = Gui()
app.run()
