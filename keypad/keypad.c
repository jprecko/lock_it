#include <Keypad.h>
#include <WiFi.h>
#include "ThingSpeak.h"

const char* ssid = "NetworkName";
const char* password = "NetworkPassword";
unsigned long thingSpeakChannel = X;
const char* APIKey = "XXXXXXXXXXXXXXXX";

WiFiClient client;

// symbols on the buttons of the keypad
char keys[4][4] = {
 {'1', '2', '3', 'A'},
 {'4', '5', '6', 'B'},
 {'7', '8', '9', 'C'},
 {'*', '0', '#', 'D'}
};
byte rowPins[4] = {14, 27, 26, 25}; // connect to the row pinouts of the keypad
byte colPins[4] = {13, 21, 22, 23}; // connect to the column pinouts of the keypad
// initialize an instance of class Keypad
Keypad myKeypad = Keypad(makeKeymap(keys), rowPins, colPins, 4, 4);

int buzzerPin = 18;
char passWord[] = {"1234"};

void setup() {
    pinMode(buzzerPin, OUTPUT);
    Serial.begin(115200);
    delay(500);

    WiFi.mode(WIFI_STA); // Wifi mode station, optional
    WiFi.begin(ssid, password);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
    ThingSpeak.begin(client);  // Initialize ThingSpeak
    static int numberSucces = 0;
    static int numberFailed = 0;
}

void loop() {
 static char keyIn[4]; // Save the input characters in array size 4
 static byte keyInNum = 0; // How many key press?
 char keyPressed = myKeypad.getKey(); // Get the character input
 if (keyPressed) {
    digitalWrite(buzzerPin, HIGH);
    delay(100);
    digitalWrite(buzzerPin, LOW);

    keyIn[keyInNum++] = keyPressed;

    if (keyInNum == 4) 
    {
        bool isRight = true; // Save password is correct or not
        for (int i = 0; i < 4; i++) 
        {
            if (keyIn[i] != passWord[i])
            {
                isRight = false;
                break;
            }
        }
    if (isRight) 
    {
        Serial.println("Password correct!");
        numberSucces++;
        int x = ThingSpeak.writeField
                (myChannelNumber, 1, numberSucces, APIKey);
        if(x == 200)
        {
            Serial.println("Channel update successful.");
        }
        else
        {
            Serial.println("Problem updating channel. 
                            HTTP error code " + String(x));
        }

    }
    else 
    {
        digitalWrite(buzzerPin, HIGH);// Make a wrong password prompt tone
        delay(1000);
        digitalWrite(buzzerPin, LOW);
        Serial.println("Password NOT correct!");
        numberFailed++;
        int x = ThingSpeak.writeField
                (myChannelNumber, , numberFailed, APIKey);
        if(x == 200)
        {
            Serial.println("Channel update successful.");
        }
        else
        {
            Serial.println("Problem updating channel. 
                            HTTP error code " + String(x));
        }
    }
    keyInNum = 0; // Reset the number of the input characters to 0
    }
  }
}
