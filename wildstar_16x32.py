from pyftdi.ftdi import Ftdi
from pyftdi.spi import SpiController
import sys, ftd2xx as ftd

import usb.backend.libusb1

backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\\Users\\Administrator\\Downloads\\libusb-1.0.24\\libusb-1.0.dll")
# https://libusb.info/
dev = usb.core.find(backend=backend, find_all=True)

class controller_16x32:

    def __init__(self):

        # d = ftd.open(0)

        # Instantiate a SPI controller

        ctrl = SpiController()

        # Configure the first interface (IF/1) of the FTDI device as a SPI master

        # ftdi://ftdi:232h/1

        ctrl.configure('ftdi://ftdi: 232h/1')

        # Get a port to a SPI slave w/ /CS on A*BUS3 and SPI mode 0

        self.spi = ctrl.get_port(cs=0, freq=1E5, mode=0)

        # Request the JEDEC ID from the SPI slave

        jedec_id = self.spi.exchange([0x9f], 3)

        print(f'Opening USB to SPI connection')

    def __del__(self):

        print(f'Closing USB-SPI connection')

    def spi_write(self, bf, reg, data):

        cmd_code = bytearray(B"\x28")

        ic_addr = bf.to_bytes(1, 'big')

        reg_addr = reg.to_bytes(1, 'big')

        reg_data = data.to_bytes(2, 'big')

        write_buf = cmd_code + ic_addr + reg_addr + reg_data

        self.spi.write(write_buf, True, True)

    def spi_read(self, bf, reg):

        cmd_code = bytearray(B"\x00")

        ic_addr = bf.to_bytes(1, 'big')

        reg_addr = reg.to_bytes(1, 'big')

        dummy_bytes = bytearray(B"\x00\x00")

        read_buf = cmd_code + ic_addr + reg_addr + dummy_bytes

        read_value = self.spi.exchange(read_buf, 5, True, True)

        return read_value

    def setup(self):

        RF_BIAS_NUM = [0x20, 0x28, 0x30, 0x38, 0x40, 0x48, 0x50, 0x58]

        CTRL_CFG_REG = 0x00

        PTAT_BIAS_CFG_REG = 0x01

        LNAREF1_REG = 0x69

        LNAREF2_REG = 0x6A

        LNAREF3_REG = 0x6B

        LNAREF4_REG = 0x6C

        i = 0

        while i < 4:

            j = 0

            self.spi_write(i, PTAT_BIAS_CFG_REG, 0x0C8A)

            self.spi_write(i, CTRL_CFG_REG, 0x0000)

            self.spi_write(i, LNAREF1_REG, 0x0010)

            self.spi_write(i, LNAREF2_REG, 0x0070)

            self.spi_write(i, LNAREF3_REG, 0x0010)

            self.spi_write(i, LNAREF4_REG, 0x0010)

            while j < 8:
                self.spi_write(i, RF_CH_NUM[j], 0x03F8)

                self.spi_write(i, RF_BIAS_NUM[j], 0x6EDB)

                j += 1

            i += 1


if __name__ == "__main__":

    RF_CH_NUM = [0x22, 0x2A, 0x32, 0x3A, 0x42, 0x4a, 0x52, 0x5a]

    RF_BIAS_NUM = [0x20, 0x28, 0x30, 0x38, 0x40, 0x48, 0x50, 0x58]

    a = controller_16x32()

    # Ping each beamformer

    a.spi_write(0, 2, 0xabcd)

    rdbk = a.spi_read(0, 2)

    if (rdbk == 0xabcd):
        print(f'BF Addr 0 is responsive')
    else:
        print(f'BF Addr 0 is unresponsive')
        print(rdbk)

    a.spi_write(1, 2, 0xabcd)

    rdbk = a.spi_read(0, 2)

    if (rdbk == 0xabcd):
        print(f'BF Addr 1 is responsive')
    else:
        print(f'BF Addr 1 is unresponsive')
        #print(f'  readback:  0x{rdbk:02x}:')

    a.spi_write(2, 2, 0xabcd)

    rdbk = a.spi_read(0, 2)

    if (rdbk == 0xabcd):
        print(f'BF Addr 2 is responsive')
    else:
        print(f'BF Addr 2 is unresponsive')
        #print(f'  readback:  0x{rdbk:02x}:')

    a.spi_write(3, 2, 0xabcd)

    rdbk = a.spi_read(0, 2)

    if (rdbk == 0xabcd):
        print(f'BF Addr 3 is responsive')
    else:
        print(f'BF Addr 3 is unresponsive')
        #print(f'  readback:  0x{rdbk:02x}:')

    a.setup()

    # Programm antenna in order of robotic arm scan

    a.spi_write(1, RF_CH_NUM[4], 0x03F8)

    a.spi_write(3, RF_CH_NUM[3], 0x03F8)

    a.spi_write(3, RF_CH_NUM[2], 0x03F8)

    a.spi_write(1, RF_CH_NUM[5], 0x03F8)

    a.spi_write(1, RF_CH_NUM[6], 0x03F8)

    a.spi_write(3, RF_CH_NUM[1], 0x03F8)

    a.spi_write(3, RF_CH_NUM[0], 0x03F8)

    a.spi_write(1, RF_CH_NUM[7], 0x03F8)

    a.spi_write(1, RF_CH_NUM[0], 0x03F8)

    a.spi_write(3, RF_CH_NUM[7], 0x03F8)

    a.spi_write(3, RF_CH_NUM[6], 0x03F8)

    a.spi_write(1, RF_CH_NUM[1], 0x03F8)

    a.spi_write(1, RF_CH_NUM[2], 0x03F8)

    a.spi_write(3, RF_CH_NUM[5], 0x03F8)

    a.spi_write(3, RF_CH_NUM[4], 0x03F8)

    a.spi_write(1, RF_CH_NUM[3], 0x03F8)

    a.spi_write(0, RF_CH_NUM[4], 0x03F8)

    a.spi_write(2, RF_CH_NUM[3], 0x03F8)

    a.spi_write(2, RF_CH_NUM[2], 0x03F8)

    a.spi_write(0, RF_CH_NUM[5], 0x03F8)

    a.spi_write(0, RF_CH_NUM[6], 0x03F8)

    a.spi_write(2, RF_CH_NUM[1], 0x03F8)

    a.spi_write(2, RF_CH_NUM[0], 0x03F8)

    a.spi_write(0, RF_CH_NUM[7], 0x03F8)

    a.spi_write(0, RF_CH_NUM[0], 0x03F8)

    a.spi_write(2, RF_CH_NUM[7], 0x03F8)

    a.spi_write(2, RF_CH_NUM[6], 0x03F8)

    a.spi_write(0, RF_CH_NUM[1], 0x03F8)

    a.spi_write(0, RF_CH_NUM[2], 0x03F8)

    a.spi_write(2, RF_CH_NUM[5], 0x03F8)

    a.spi_write(2, RF_CH_NUM[4], 0x03F8)

    a.spi_write(0, RF_CH_NUM[3], 0x03F8)

