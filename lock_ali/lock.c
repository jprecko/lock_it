#include <Keypad.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);

Servo myservo;  // create servo object to control a servo

int pos = 0;

#define Password_length 5 //längd av lössenordet + null karaktär
char Data[Password_length]; // Karakär för att hålla lössenordet 
char Master[Password_length] = "1234"; // själva Lössenordet 
byte date_count = 0; // räknare för Karaktär som är 0 från början
char key; // den håller karaktär som matas in från keypad

const uint8_t ROWS = 4;
const uint8_t COLS = 4;
char keys[ROWS][COLS] = {
  { '1', '2', '3', 'A' },
  { '4', '5', '6', 'B' },
  { '7', '8', '9', 'C' },
  { '*', '0', '#', 'D' }
};

uint8_t colPins[COLS] = { 5, 4, 3, 2 }; // Pins connected to C1, C2, C3, C4
uint8_t rowPins[ROWS] = { 9, 8, 7, 6 }; // Pins connected to R1, R2, R3, R4

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

void setup() {
  Serial.begin(9600);
  myservo.attach(12);
  lcd.init();
  lcd.backlight();

}

void loop() {
  lcd.setCursor(0, 0);
  lcd.print(" Enter PassWord");
  static char keyIn[4]; // Save the input characters in array size 4
  static byte keyInNum = 0; // How many key press?
  char key = keypad.getKey();

  if(key)
  {
    Data[date_count] = key;
    lcd.setCursor(date_count, 1);
    lcd.print(Data[date_count]);
    Serial.println(Data[date_count]);
    date_count++;
  }
  if (date_count == Password_length -1)
  {
    if (!strcmp(Data, Master)) // här jämförs (Data som matas in  ) och (Master som är riktiga lössenordet)
    {
      myservo.write(pos);             // tell servo to go to position in variable 'pos'
      lcd.print("  Corect");
      delay(2000);
      myservo.write(90); 
    }
    else
    {
      lcd.print("  Incorect");
      delay(1000);
    }
    lcd.clear();
    while (date_count !=0)
    {
      Data[date_count--] = 0;
    }
    return;
  }
}
