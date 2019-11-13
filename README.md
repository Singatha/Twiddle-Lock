# Twiddle Lock

- A project for creating an electronic form of the classic "dial combination safe" combinational lock mechanism which is implemented using the raspberry pi. The Raspberry-based application listens to a button that indicates you are about to put in a dialed code, and this dialed code is be sensed by an ADC connected to a POT that is attached to the knob that represents the ‘twiddle knob’. The application needs to read in sampled values from the ADC connected to the twiddle knob and determines if the sample value values match the sequence. If they match the LED blinks green else it blinks red.

- clone or download the repo
- Hardware parts:
  - Raspberry Pi Model 3B
  - MCP3008 SPI
  - 10K Potentiometer
  - 1x Green LED
  - 1x Red LED
  - 2x Pushbuttons
- setup the raspberry pi circuit using the *twiddlesafe.jpg*
- run the practical6.py 
  - **_python practical6.py_**
