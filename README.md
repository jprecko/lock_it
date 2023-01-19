# lock_it

## Intro
Projektet är indelat i ett antal mindre delprojekt, där de olika delarna tillsammans skapar ett låssystem. Två av projekten är inriktade på hur en fysisk knappsats kan integreras med olika komponenter ett lås kan behöva så som en indikator i form av ljus, ljud och en mindre LCD. Dessa funktionaliteter är skrivna med hjälp av Arduinos framework. Ett av de två projekten innehåller även funktionalitet för att koppla upp sig mot en MQTT-server. Huvudprojektet innehåller även ett tredje delprojekt med syfte att logga, och läsa ström från en Pico W som sedan sickas till en MQTT-server för vidare processering. Det finns även funktionalitet för att ta emot information via MQTT med en platshållarfunktion som slår på och av en lampa för demosyfte.

Ett vidare mål med projektet är att sammanfoga all funktionalitet för att i slutändan få ett fungerande smart lås.
