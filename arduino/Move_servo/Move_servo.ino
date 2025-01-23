 

#include <SoftwareSerial.h>
  

#include <Servo.h>

Servo servos[4]; // Array to store the servo objects

int leftSpeed = 0;  // Last received left speed
int rightSpeed =0; // Last received right speed
String inputString = "",input; // To store incoming serial data
void setup() {
  
  Serial.begin(9600); // Start Serial communication at 9600 baud rate
  servos[0].attach(6); // Left backward servo
  servos[1].attach(7); // Left forward servo
  servos[2].attach(8); // Right forward servo
  servos[3].attach(9);
  LED();// Right backward servo

}

void loop() {
  // Check for incoming data

 
  while (Serial.available() > 0) {


    char inChar = Serial.read();
    if (inChar == '\n') {  // Check if the newline character (end of input) is received
      processInput(inputString); // Process the complete input
      inputString = ""; // Clear input for the next command
    } else {
      inputString += inChar; // Append the character to the input
    }
  }

        move(leftSpeed, rightSpeed);



  // Short delay for stability
  delay(20);
}   

// Function to parse and set speeds
void processInput(String input) {
  int spaceIndex = input.indexOf(' ');
  if (spaceIndex > 0) {
    // Separate left and right speeds from input string
    leftSpeed = input.substring(0, spaceIndex).toInt();
    rightSpeed = input.substring(spaceIndex + 1).toInt();

    // Ensure values are within -100 to 100 range
    leftSpeed = constrain(leftSpeed, -100, 100);
    rightSpeed = constrain(rightSpeed, -100, 100);
  }
}

// Function to control speed and direction of the servos
void move(int leftSpeed, int rightSpeed) {
  // Map speed to servo angles for continuous servos
  int leftServoAngle = map(leftSpeed, -100, 100, 180, 0);  // Inverted for left side
  int rightServoAngle = map(rightSpeed, -100, 100, 0, 180); // Normal for right side

  int leftServoAngle_back = map(leftSpeed, -100, 100, 160, 20);  
  int rightServoAngle_back = map(rightSpeed, -100, 100, 20, 160); 

  // Set servo positions based on mapped angles
  servos[0].write(leftServoAngle); // Left backward servo
  servos[1].write(leftServoAngle); // Left forward servo
  servos[2].write(rightServoAngle); // Right forward servo
  servos[3].write(rightServoAngle); // Right backward servo
}
