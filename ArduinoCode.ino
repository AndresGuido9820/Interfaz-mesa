#include <AccelStepper.h>

#define dirPin 2
#define stepPin 3
#define enPin 4

AccelStepper stepper(AccelStepper::FULL4WIRE, stepPin, dirPin);
int amplitudActual = 0;
int velocidadActual = 0;

void setup() {
  Serial.begin(9600);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW); // Habilitar el motor
  stepper.setMaxSpeed(1000); // Velocidad máxima del motor en pasos por segundo
  stepper.setAcceleration(500); // Aceleración del motor en pasos por segundo^2
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int nueva_amplitud = data.substring(0, data.indexOf(',')).toInt();
    int nueva_velocidad = data.substring(data.indexOf(',') + 1).toInt();
    
    // Actualizar la amplitud y velocidad actuales
    amplitudActual = nueva_amplitud;
    velocidadActual = nueva_velocidad;
    
    // Convertir valores de amplitud y velocidad a pasos por segundo
    float pasosPorVuelta = 200; // Cambiar según el tipo de motor paso a paso
    float pasosPorGrado = pasosPorVuelta / 360;
    float pasosPorSegundo = velocidadActual * pasosPorGrado;
    
    // Mover el motor a la nueva amplitud especificada
    stepper.moveTo(amplitudActual);
    while (stepper.distanceToGo() != 0) {
      stepper.run();
      delay(1);
    }

    // Mover el motor a velocidad constante
    stepper.setSpeed(pasosPorSegundo);
    while (true) {
      stepper.runSpeed();
    }

    // Enviar confirmación a Python de que los datos fueron recibidos y procesados correctamente
    Serial.println("Datos recibidos y procesados");
  }
}

