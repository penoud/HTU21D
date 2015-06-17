import PyBCM2835

class HTU21D:
	COMMAND_START_HOLD_TEMP_CONVERSION = 0xE3
	COMMAND_START_HOLD_HUMIDITY_CONVERSION = 0xE5
	COMMAND_START_NOHOLD_TEMP_CONVERSION = 0xF3
	COMMAND_START_NOHOLD_HUMIDITY_CONVERSION = 0xF5
	COMMAND_WRITE_USER_REG = 0xE6
	COMMAND_READ_USER_REG = 0xE7
	COMMAND_SOFT_RESET = 0xFE


	def __init__(self):
		if not (PyBCM2835.init()):
			raise EnvironmentError("Cannot initialize BCM2835.")
		PyBCM2835.i2c_begin()
		PyBCM2835.i2c_setSlaveAddress(0x40)

		PyBCM2835.delay(100)
	def readHoldHumidity(self):
		PyBCM2835.i2c_write(chr(self.COMMAND_START_HOLD_HUMIDITY_CONVERSION),1)
		PyBCM2835.delay(600)
		data=""+chr(0)+chr(0)+chr(0)
		PyBCM2835.i2c_read(data,3)
		if self.crc8check([ord(data[0]),ord(data[1]),ord(data[2])]):
			#print "received = " + hex(ord(data[0])) + ", " + hex(ord(data[1])) + ", " + hex(ord(data[2]))
			return int(ord(data[0])*256+ord(data[1]))/(2.0**16)*125-6;
		else:
			print "CRC error"
			return 0

	def readHoldTemp(self):
		PyBCM2835.i2c_write(chr(self.COMMAND_START_HOLD_TEMP_CONVERSION),1)
		PyBCM2835.delay(600)
		data=""+chr(0)+chr(0)+chr(0)
		PyBCM2835.i2c_read(data,3)
		if self.crc8check([ord(data[0]),ord(data[1]),ord(data[2])]):
			#print "received = " + hex(ord(data[0])) + ", " + hex(ord(data[1])) + ", " + hex(ord(data[2]))
			return int(ord(data[0])*256+ord(data[1]))/(2.0**16)*175.72-46.85;
		else:
			print "CRC error"
			return 0
	def readNoHoldHumidity(self):
		PyBCM2835.i2c_write(chr(self.COMMAND_START_NOHOLD_HUMIDITY_CONVERSION),1)
		PyBCM2835.delay(600)
		data=""+chr(0)+chr(0)+chr(0)
		PyBCM2835.i2c_read(data,3)
		if self.crc8check([ord(data[0]),ord(data[1]),ord(data[2])]):
			#print "received = " + hex(ord(data[0])) + ", " + hex(ord(data[1])) + ", " + hex(ord(data[2]))
			return int(ord(data[0])*256+ord(data[1]))/(2.0**16)*125-6;
		else:
			print "CRC error"
			return 0
	def readNoHoldTemp(self):
		PyBCM2835.i2c_write(chr(self.COMMAND_START_NOHOLD_TEMP_CONVERSION),1)
		PyBCM2835.delay(600)
		data=""+chr(0)+chr(0)+chr(0)
		PyBCM2835.i2c_read(data,3)
		if self.crc8check([ord(data[0]),ord(data[1]),ord(data[2])]):
			#print "received = " + hex(ord(data[0])) + ", " + hex(ord(data[1])) + ", " + hex(ord(data[2]))
			return int(ord(data[0])*256+ord(data[1]))/(2.0**16)*175.72-46.85;
		else:
			print "CRC error"
			return 0
	def softReset(self):
		PyBCM2835.i2c_write(chr(self.COMMAND_SOFT_RESET),1)
	def crc8check(self, value):
		# from post on forum : https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=76688
		# Ported from Sparkfun Arduino HTU21D Library: https://github.com/sparkfun/HTU21D_Breakout
		remainder = ( ( value[0] << 8 ) + value[1] ) << 8
		remainder |= value[2]

		# POLYNOMIAL = 0x0131 = x^8 + x^5 + x^4 + 1
		# divsor = 0x988000 is the 0x0131 polynomial shifted to farthest left of three bytes
		divsor = 0x988000

		for i in range(0, 16):
			if( remainder & 1 << (23 - i) ):
				remainder ^= divsor
			divsor = divsor >> 1

		if remainder == 0:
			return True
		else:
			return False
