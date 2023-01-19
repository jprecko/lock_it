## Kod för keypad som loggar via MQTT.

### Vad har du gjort?
Ett smart kodlås baserat på mikrocontrollern ESP32 och med Arduino framework.
En fyrsiffrig kod ska slås in för att öppna en dörr.
Varje gång man trycker på en knapp, så blir det ett litet pipljud från en buzzer.
Om man skriver fel kod, låter buzzern med ett error-ljud också.

ESP32 kontaktar en MQTT server via wifi och loggar varje lyckat eller misslyckat försök.

### Varför har du / ni gjort som ni gjort
Vi har valt kodlås istället för IR fjärrkontroll (för att slå in koden) för att det är säkrare.
Vi har valt MQTT som protokoll för att det är branchstandard och har mycket låg overhead.

### Hur funkar det du gjort tekniskt?
En keypad och en buzzer (som piper) är kopplade till ESP32.
En wifi anslutning skapas.
En koppling till en MQTT server skapas också, med användare och lösenord.
Det skapas en array med storlek 4, och koden jämför de 4 siffror som användaren matar in med ett hårdkodat lösen som finns i koden.
Via MQTT loggas det varje gång en användare matat in 4 siffror (lyckat eller misslyckat loggas separat).
Efter att 4 siffror matats in (lyckat eller misslyckat) så återställs array:en till 0.

### Vilken hårdvara och IOT-miljö har används och varför?
För denna del av projektet har vi använt oss av mikrokontrollern ESP32 med ett breakout till breadboard.
Därför den var relativt billig, kompatibel med Arduino framework och hade både wifi och bluetooth inbyggt.

### Vad hade du gjort framåt om du haft mer tid?
Då hade vi velat skapa en riktig MQTT server på en edge device med Ubuntu och plottat lyckade och misslyckade försök på en webbsida.

![esp32-lock](https://user-images.githubusercontent.com/7149573/213385744-56d6e3db-6da7-4db9-b37e-e6129fb47b0c.png)
