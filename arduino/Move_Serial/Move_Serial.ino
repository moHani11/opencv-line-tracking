

void Motor1 (int Speed)
{
    if (Speed == 0)
    {
        digitalWrite (2, 0);
        digitalWrite (4, 0);
        analogWrite (9, 0);
    }
    else if (Speed > 0)
    {
        digitalWrite (2, 1);
        digitalWrite (4, 0);
        analogWrite (9, Speed);
    }
    else if (Speed < 0)
    {
        digitalWrite (2, 0);
        digitalWrite (4, 1);
        analogWrite (9, Speed*-1);
    }
}

void Motor2 (int Speed)
{
    if (Speed == 0)
    {
        digitalWrite (7, 0);
        digitalWrite (8, 0);
        analogWrite (10, 0);
    }
    else if (Speed < 0)
    {
        digitalWrite (7, 1);
        digitalWrite (8, 0);
        analogWrite (10, Speed*-1);
    }
    else if (Speed > 0)
    {
        digitalWrite (7, 0);
        digitalWrite (8, 1);
        analogWrite (10, Speed);
    }
}

void Move (int SpeedLeft, int SpeedRight)
{
    Motor1(SpeedLeft*-1);
    Motor2(SpeedRight*-1);
}

void setup() 
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode (2, OUTPUT);
  pinMode (4, OUTPUT);
  pinMode (9, OUTPUT);

  pinMode (7, OUTPUT);
  pinMode (8, OUTPUT);
  pinMode (10, OUTPUT);
}

void loop() 
{
  int LeftMotor, RightMotor;
  // put your main code here, to run repeatedly:
       
        Serial.println(Serial.read());
      if (Serial.read() == 'M')
      {  
          LeftMotor = Serial.parseInt();
          RightMotor = Serial.parseInt();
          Move (LeftMotor, RightMotor);
      }

      

}
