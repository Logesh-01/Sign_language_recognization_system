#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

const int flexPins[] = {A0, A1, A2, A3, A4};

const int flexResistance = 25000;
const int flexBendResistance =125000;
const int bendAngleRange =90;


void setup() {
  Serial.begin(9600);

  Wire.begin();
  mpu.initialize();

  // Verify connection
  if (mpu.testConnection()) {
    Serial.println("MPU6050 connection successful");
  } else {
    Serial.println("MPU6050 connection failed");
  }
}

void loop() {
  int flexValues[5];
  for (int i = 0; i < 5; i++)
  {
    flexValues[i] = analogRead(flexPins[i]);
  }

  float flexResistances[5];
  float bendDegrees[5];

  for (int i = 0; i < 5; i++)
  {
    flexResistances[i] = flexResistance * (1023.0/flexValues[i] - 1.0);
    bendDegrees[i] = map(flexResistances[i], flexResistance, flexBendResistance, 0, bendAngleRange);
    bendDegrees[i] = constrain(bendDegrees[i], 0, bendAngleRange);
  }

  
  Serial.print("Flex Values: ");
   for (int i = 0; i < 5; i++)
   {
    Serial.print(flexValues[i]);
    Serial.print("\n ");
   }

   Serial.print("Resistances: ");
   for (int i = 0; i < 5; i++)
   {
    Serial.print(flexResistances[i]);
    Serial.print("\n ");
   }

   Serial.print("Bend Degrees: ");
   for (int i = 0; i < 5; i++)
   {
    Serial.print(bendDegrees[i]);
    Serial.print("\n ");
   }
  
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  // Print values
  Serial.print("Accel: ");
  Serial.print(ax); Serial.print("\n ");
  Serial.print(ay); Serial.print(", ");
  Serial.print(az); Serial.print(" , ");

  Serial.print("Gyro: ");
  Serial.print(gx); Serial.print("\n ");
  Serial.print(gy); Serial.print(", ");
  Serial.println(gz);

  delay(20000);
}