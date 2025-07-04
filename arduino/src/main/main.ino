#include <Arduino.h>
#include <RotaryEncoder.h>

//PIN DEFINITIONS
//ENCODER A
#define ENC_A_1 19
#define ENC_A_2 18
#define ENC_A_SW 39
//ENCODER B
#define ENC_B_1 21
#define ENC_B_2 20
#define ENC_B_SW 38
//FADERS
#define FADER_1 11
#define FADER_2 12
#define FADER_3 13
#define FADER_4 14
#define FADER_5 15
//MATRIX TOP
#define MTXA_IN1 52
#define MTXA_IN2 50
#define MTXA_IN3 48
#define MTXA_IN4 46
#define MTXA_IN5 44
#define MTXA_OUT1 42
#define MTXA_OUT2 40
//MATRIX BOT
#define MTXB_IN1 53
#define MTXB_IN2 51
#define MTXB_IN3 49
#define MTXB_IN4 47
#define MTXB_IN5 45
#define MTXB_OUT1 43
#define MTXB_OUT2 41

RotaryEncoder *EncoderA = nullptr;
RotaryEncoder *EncoderB = nullptr;

bool _EncoderASwitch = true;
bool _EncoderBSwitch = true;

int _EncoderADirection = 0;
int _EncoderBDirection = 0;

int FADERPINS[5] = {FADER_1, FADER_2, FADER_3, FADER_4, FADER_5};
int _Faders[5] = {0, 0, 0, 0, 0};

int MTXAINS[5] = {MTXA_IN1, MTXA_IN2, MTXA_IN3, MTXA_IN4, MTXA_IN5};
int _MTXA[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int MTXBINS[5] = {MTXB_IN1, MTXB_IN2, MTXB_IN3, MTXB_IN4, MTXB_IN5};
int _MTXB[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int e = 0;

void EncACheckPosition() {
  EncoderA->tick();
}

void EncBCheckPosition() {
  EncoderB->tick();
}

void setup() {
  Serial.begin(1000000);

  EncoderA = new RotaryEncoder(ENC_A_1, ENC_A_2, RotaryEncoder::LatchMode::TWO03);
  attachInterrupt(digitalPinToInterrupt(ENC_A_1), EncACheckPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC_A_2), EncACheckPosition, CHANGE);
  EncoderB = new RotaryEncoder(ENC_B_1, ENC_B_2, RotaryEncoder::LatchMode::TWO03);
  attachInterrupt(digitalPinToInterrupt(ENC_B_1), EncBCheckPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(ENC_B_2), EncBCheckPosition, CHANGE);

  pinMode(ENC_A_SW, INPUT_PULLUP);
  pinMode(ENC_B_SW, INPUT_PULLUP);

  pinMode(MTXA_IN1, INPUT_PULLUP);
  pinMode(MTXA_IN2, INPUT_PULLUP);
  pinMode(MTXA_IN3, INPUT_PULLUP);
  pinMode(MTXA_IN4, INPUT_PULLUP);
  pinMode(MTXA_IN5, INPUT_PULLUP);
  pinMode(MTXA_OUT1, OUTPUT);
  pinMode(MTXA_OUT2, OUTPUT);

  pinMode(MTXB_IN1, INPUT_PULLUP);
  pinMode(MTXB_IN2, INPUT_PULLUP);
  pinMode(MTXB_IN3, INPUT_PULLUP);
  pinMode(MTXB_IN4, INPUT_PULLUP);
  pinMode(MTXB_IN5, INPUT_PULLUP);
  pinMode(MTXB_OUT1, OUTPUT);
  pinMode(MTXB_OUT2, OUTPUT);
}

void loop() {
  CheckEncoderASwitch();
  CheckEncoderBSwitch();
  CheckFaders(1); //deadzone=0
  CheckMtxA();
  CheckMtxB();
  CheckEncoderA();
  CheckEncoderB();
  // Serial.println((int)(EncoderA->getDirection()));
  // Output();
}

void CheckEncoderA() {
  int x = (int)(EncoderA->getDirection());
  if (x>0) {
    Serial.println("E_A_1");
  }
  else if (x<0) {
    Serial.println("E_A_0");
  }
}

void CheckEncoderB() {
  int x = (int)(EncoderB->getDirection());
  if (x>0) {
    Serial.println("E_B_1");
  }
  else if (x<0) {
    Serial.println("E_B_0");
  }
}

void CheckEncoderASwitch() {
  bool x = digitalRead(ENC_A_SW);
  if (x != _EncoderASwitch) {
    _EncoderASwitch = x;
    Serial.print("S_20_");
    Serial.println(!x);
  }
}

void CheckEncoderBSwitch() {
  bool x = digitalRead(ENC_B_SW);
  if (x != _EncoderBSwitch) {
    _EncoderBSwitch = x;
    Serial.print("S_21_");
    Serial.println(!x);
  }
}

void CheckFaders(int deadzone) {
  for (int i=0; i<=4; i++) {
    int f = map(analogRead(FADERPINS[i]),0, 1023, 0, 255);
    if (f == 254) {
      f = 255;
    } else if (f == 1) {
      f = 0;
    }
    if (f > _Faders[i]+deadzone || f < _Faders[i]-deadzone) {
      _Faders[i] = f;
      Serial.print("F_");
      Serial.print(i);
      Serial.print("_");
      Serial.println(_Faders[i]);
    }
  }
}

void CheckMtxA() {
  pinMode(MTXA_OUT1, OUTPUT);
  pinMode(MTXA_OUT2, INPUT);
  digitalWrite(MTXA_OUT1, 0);
  for (int i=0; i<=4; i++) {
    bool x = digitalRead(MTXAINS[i]);
    if (x != _MTXA[i]) {
      _MTXA[i] = x;
      Serial.print("S_");
      Serial.print(i);
      Serial.print("_");
      Serial.println(_MTXA[i]);
    }
  }
  pinMode(MTXA_OUT2, OUTPUT);
  pinMode(MTXA_OUT1, INPUT);
  digitalWrite(MTXA_OUT2, 0);
  for (int i=5; i<=9; i++) {
    bool x = digitalRead(MTXAINS[i-5]);
    if (x != _MTXA[i]) {
      _MTXA[i] = x;
      Serial.print("S_");
      Serial.print(i);
      Serial.print("_");
      Serial.println(_MTXA[i]);
    }
  }
}

void CheckMtxB() {
  pinMode(MTXB_OUT1, OUTPUT);
  pinMode(MTXB_OUT2, INPUT);
  digitalWrite(MTXB_OUT1, 0);
  for (int i=0; i<=4; i++) {
    bool x = !digitalRead(MTXBINS[i]);
    if (x != _MTXB[i]) {
      _MTXB[i] = x;
      Serial.print("S_");
      Serial.print(i+10);
      Serial.print("_");
      Serial.println(_MTXB[i]);
    }
  }
  pinMode(MTXB_OUT2, OUTPUT);
  pinMode(MTXB_OUT1, INPUT);
  digitalWrite(MTXB_OUT2, 0);
  for (int i=5; i<=9; i++) {
    bool x = !digitalRead(MTXBINS[i-5]);
    if (x != _MTXB[i]) {
      _MTXB[i] = x;
      Serial.print("S_");
      Serial.print(i+10);
      Serial.print("_");
      Serial.println(_MTXB[i]);
    }
  }
}