# -*- coding: latin-1 -*-
import HTU21D
		
def main():
	myHTU21D = HTU21D.HTU21D()
	while(1):
		humidity = myHTU21D.readHoldHumidity()
		temp = myHTU21D.readHoldTemp()
		print "Humidity= " + str(humidity) +" %, température=" + str(temp) + " °C"

if __name__ == '__main__':
    main()
