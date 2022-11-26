Driver and crude test programs in MicroPython for XPT2046, ILI9488 480x320 pixel touch displays like https://www.waveshare.com/product/raspberry-pi/boards-kits/raspberry-pi-pico-cat/pico-restouch-lcd-3.5.htm . 
The pico has not enough RAM for framebuffer. This driver writes to the display directly. Unfortunately, display cannot be read due to hardware limitations.
