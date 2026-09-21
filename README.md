# Computer-Vision-based-3D-Printed-Bionic-Hand
Using Computer Vision and mediapipe tracking to track finger movements and relay them via serial port to a self designed original bionic hand with functioning joints.

I designed and built a bionic hand that receives its inputs through my laptop's webcam. The webcam uses the footage and runs it through mediapipe's hand tracking to track the angles 
of each joint on my finger.
On the hardware front, I used Fusion360 to design articulating fingers with 3 joints each, and hence 3 axis of rotation for the parts. The parts are also designed such that it will not move beyond a certain point to reflect accurately on my actual hand's movements.
The microcontroller I used here is an Arduino Nano, connected to 5 servo motors, one for each finger.
I did however run into some issues, as I was trying to run 5 motors, I realised when all 5 are in play , they demand a lot of current, which throttles the speed and strength of a motor's movements.
Thus, the arm runs on 2 power sources. a phone charger providing unto 3 amps of current at 5 volts, which powers 3 servo motors, and the Arduino's intrinsic power source which is given power through the laptop powers the other 2.
In the future, special dedicated servo drivers and professionally printed PCBs can be used to ensure reliability and minimal throttling.



<img width="300" height="533" alt="image" src="https://github.com/user-attachments/assets/34052431-b61a-45cc-9f30-293a1cfe8205" />
<img width="400" height="533" alt="image" src="https://github.com/user-attachments/assets/a581bdff-40d0-4c27-96ae-2a41408f218f" />


https://github.com/user-attachments/assets/de6bbb05-bb53-4283-bddf-d8cd44d1d4e1
