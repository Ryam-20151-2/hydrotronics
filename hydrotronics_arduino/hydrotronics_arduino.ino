/////// Copyrighted By Brijesha and Megan ///////

/////// Libraries ///////
#include <dht.h>
#include <Wire.h>
#include <Servo.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

/////// pH Constants ///////
// Sensor Constants 
#define PH_SENSOR_PIN A0
#define PH_OFFSET 0.05
#define PH_NUM_SAMPLES 10

// PID Constants
#define PH_KP 100
#define PH_KI 0.00001
#define PH_KD 0.3

/////// TDS Constants ///////
// Sensor Constants
#define TDS_SENSOR_PIN A1
#define TDS_NUM_SAMPLES 30

// PID Constants
#define MICRO_KP 4.0
#define MICRO_KI 0.06
#define MICRO_KD 0.0
#define BLOOM_KP 4.5
#define BLOOM_KI 0.05
#define BLOOM_KD 0.0
#define GRO_KP 4.5
#define GRO_KI 0.03
#define GRO_KD 0.0

/////// Solenoid Constants ///////
#define SOLENOID_RELAY_PIN A2

/////// Temperature/Humidity Constants ///////
#define TEMP_HUMIDITY_PIN 2

/////// General Constants ///////
#define VREF 5.0
#define TEMPERATURE 25.0
#define MAX_CONTROL_LOOP_TIME (70000U)

/////// ENUMS! ///////
enum nutrient_solution
{
  MICRO,
  BLOOM,
  GRO,
};

enum ph_probe_motion
{
  OUT,
  IN
};

enum solenoid_state
{
  OPEN,
  CLOSE
};

enum state
{
  NOT_SPRAY,
  SPRAY
};

/////// Setup Motor Shields ///////
Adafruit_MotorShield S1 = Adafruit_MotorShield(0x60);
Adafruit_MotorShield S2 = Adafruit_MotorShield(0x61);

/////// Setup Motors Connected to Shields ///////
// Peristaltic Pumps
Adafruit_DCMotor *S1_M1 = S1.getMotor(1);
Adafruit_DCMotor *S1_M2 = S1.getMotor(2);
Adafruit_DCMotor *S1_M3 = S1.getMotor(3);
Adafruit_DCMotor *S1_M4 = S1.getMotor(4);
Adafruit_DCMotor *S2_M1 = S2.getMotor(1);
// PH Probe Servo
Servo ph_servo;
// Lights Stepper/DC...

/////// Nutrient Motors Array ///////
Adafruit_DCMotor* nutrient_motors[3] = {S1_M1, S1_M2, S1_M3};

/////// pH Global Variables ///////
int global_ph_value = 0;

/////// TDS Global Variables ///////
float tds_pid_constants[3][3] = {{MICRO_KP, MICRO_KI, MICRO_KD}, {BLOOM_KP, BLOOM_KI, BLOOM_KD}, {GRO_KP, GRO_KI, GRO_KD}};\
float global_tds_value = 0;

/////// Temperature & Humidity Global Variables ///////
dht DHT;
float global_temp_value = 0;
float global_humidity_value = 0;

/////// Other Global Variables ///////
state current_state = NOT_SPRAY;

void setup() {
  Serial.begin(9600);

  // Set up sensor pins
  pinMode(PH_SENSOR_PIN, INPUT);
  pinMode(TDS_SENSOR_PIN, INPUT);

  // Set up solenoid relay pin
  pinMode(SOLENOID_RELAY_PIN, OUTPUT);

  // Turn On Motor Shields
  S1.begin();
  S2.begin();

  // Attach Servo Control Pin To Arduino PWM Pin
  ph_servo.attach(10);

  // Initialize All Motors To Off
  S1_M1->setSpeed(0);
  S1_M1->run(FORWARD);
  S1_M2->setSpeed(0);
  S1_M2->run(FORWARD);
  S1_M3->setSpeed(0);
  S1_M3->run(FORWARD);
  S1_M4->setSpeed(0);
  S1_M4->run(FORWARD);
  S2_M1->setSpeed(0);
  S2_M1->run(FORWARD);

  current_state = NOT_SPRAY;
}

/////// TDS Functions ///////
void get_tds_value()
{
  unsigned long int tds_avg_value = 0;

  // Read sensor 10 times
  int tds_buffer[10];
  for (int i = 0; i < 10; i++)
  {
    tds_buffer[i] = analogRead(TDS_SENSOR_PIN);
    delay(10);
  }

  // Sort readings to remove outliers
  for (int i = 0; i < 10 - 1; i++)
    {
      for (int j = i+1; j < 10; j++)
      {
        if (tds_buffer[i] > tds_buffer[j])
        {
          int temp;
          temp = tds_buffer[j];
          tds_buffer[i] = tds_buffer[j];
          tds_buffer[j] = temp;
        }
      }
    }

  // Calculate average sensor reading from center samples
  for (int i = 2; i < 8; i ++)
  {
    tds_avg_value += tds_buffer[i];
  }

  tds_avg_value /= 6;
  float tds_voltage = (float)(tds_avg_value * VREF / 1024);

  float comp_coeff = 1.0+0.02*(TEMPERATURE-25.0);
  //temperature compensation
  float comp_voltage=tds_avg_value/comp_coeff;
  
  //convert voltage value to tds value
  float tds_value=(133.42*comp_voltage*comp_voltage*comp_voltage - 255.86*comp_voltage*comp_voltage + 857.39*comp_voltage)*0.5;
  global_tds_value = tds_value;
}

// median filtering algorithm
int tds_get_median_num(int arr[], int num_samples){
  int temp_arr[num_samples];
  for (byte i = 0; i<num_samples; i++)
  temp_arr[i] = arr[i];
  int i, j, temp;
  for (j = 0; j < num_samples - 1; j++) {
    for (i = 0; i < num_samples - j - 1; i++) {
      if (temp_arr[i] > temp_arr[i + 1]) {
        temp = temp_arr[i];
        temp_arr[i] = temp_arr[i + 1];
        temp_arr[i + 1] = temp;
      }
    }
  }
  if ((num_samples & 1) > 0){
    temp = temp_arr[(num_samples - 1) / 2];
  }
  else {
    temp = (temp_arr[num_samples / 2] + temp_arr[num_samples / 2 - 1]) / 2;
  }
  return temp;
}

void tds_control_loop(nutrient_solution solution, float tds_target_value)
{
  int tds_buffer[TDS_NUM_SAMPLES];
  int tds_buffer_temp[TDS_NUM_SAMPLES];
  int tds_buffer_index = 0;
  int tds_copy_index = 0;  

  float tds_avg_voltage = 0;
  float tds_value = 0;

  float e_integral = 0;
  float e_prev = 0;
  long prev_T = 0;

  unsigned long start_time = millis();
  unsigned long curr_time = millis();

  while (curr_time < (start_time + MAX_CONTROL_LOOP_TIME))
  {
    static unsigned long tds_sample_time_point = millis();
    if(millis()-tds_sample_time_point > 40U){     //every 40 milliseconds,read the analog value from the ADC
      tds_sample_time_point = millis();
      tds_buffer[tds_buffer_index] = analogRead(TDS_SENSOR_PIN);    //read the analog value and store into the buffer
      tds_buffer_index++;
      if(tds_buffer_index == TDS_NUM_SAMPLES){ 
        tds_buffer_index = 0;
      }
    } 

    static unsigned long tds_calc_time_point = millis();
    if(millis()-tds_calc_time_point > 800U){
      tds_calc_time_point = millis();
      for(tds_copy_index=0; tds_copy_index<TDS_NUM_SAMPLES; tds_copy_index++){
        tds_buffer_temp[tds_copy_index] = tds_buffer[tds_copy_index];
        
        // read the analog value more stable by the median filtering algorithm, and convert to voltage value
        tds_avg_voltage = tds_get_median_num(tds_buffer_temp,TDS_NUM_SAMPLES) * (float)VREF / 1024.0;
        
        //temperature compensation formula: fFinalResult(25^C) = fFinalResult(current)/(1.0+0.02*(fTP-25.0)); 
        float comp_coeff = 1.0+0.02*(TEMPERATURE-25.0);
        //temperature compensation
        float comp_voltage=tds_avg_voltage/comp_coeff;
        
        //convert voltage value to tds value
        tds_value=(133.42*comp_voltage*comp_voltage*comp_voltage - 255.86*comp_voltage*comp_voltage + 857.39*comp_voltage)*0.5;
        global_tds_value = tds_value;
      }
      delay(20);

      // time difference
      long curr_T = micros();
      float delta_T = ((float) (curr_T - prev_T) / 1000000);
      prev_T = curr_T;

      // error
      float e = tds_target_value - tds_value;

      if (e < 5 && e > -5)
      {
        e = 0;
      }

      // derivative
      float de_dt = (e - e_prev) / (delta_T);

      // integral
      e_integral += e * delta_T;

      // control signal
      float u = tds_pid_constants[solution][0]*e + tds_pid_constants[solution][1]*e_integral + tds_pid_constants[solution][2]*de_dt;

      // pump power saturation
      float power = fabs(u);
      if (power > 255)
      {
          power = 255;
      }
      else if (power < 76.5)
      {
          power = 0;
      }

      // select which pump to control
      if (u > 0)
      {
        nutrient_motors[solution]->setSpeed(power);
        nutrient_motors[solution]->run(FORWARD);
      }

      e_prev = e;

      Serial.println(tds_target_value);
      Serial.print(" ");
      Serial.println(global_tds_value);
    }

    curr_time = millis();
  }
}

/////// pH Functions ///////
void get_ph_value()
{
  unsigned long int ph_avg_value = 0;

  // Read sensor 10 times
  int ph_buffer[PH_NUM_SAMPLES];
  for (int i = 0; i < PH_NUM_SAMPLES; i++)
  {
    ph_buffer[i] = analogRead(PH_SENSOR_PIN);
    delay(10);
  }

  // Sort readings to remove outliers
  for (int i = 0; i < PH_NUM_SAMPLES - 1; i++)
    {
      for (int j = i+1; j < PH_NUM_SAMPLES; j++)
      {
        if (ph_buffer[i] > ph_buffer[j])
        {
          int temp;
          temp = ph_buffer[j];
          ph_buffer[i] = ph_buffer[j];
          ph_buffer[j] = temp;
        }
      }
    }

  // Calculate average sensor reading from center samples
  for (int i = 2; i < 8; i ++)
  {
    ph_avg_value += ph_buffer[i];
  }

  ph_avg_value /= 6;
  float ph_voltage = (float)(ph_avg_value * VREF / 1024);
  float ph_value = 3.5 * ph_voltage + PH_OFFSET;
  global_ph_value = ph_value;
}

void ph_control_loop(float ph_target_value)
{
  unsigned long int ph_avg_value;
  int ph_buffer[PH_NUM_SAMPLES];

  int ph_value = 0;
  long prev_T = 0;
  float e_Prev = 0;
  float e_Integral = 0;

  unsigned long start_time = millis();
  unsigned long curr_time = millis();

  while (curr_time < (start_time + MAX_CONTROL_LOOP_TIME))
  {
    get_ph_value();
    delay(20);

    // time difference
    long currT = micros();
    float deltaT = ((float) (currT - prev_T) / 1000000);
    prev_T = currT;

    // error
    float e = global_ph_value - ph_target_value;

    if (e < 0.5 && e > -0.5)
    {
      e = 0;
    }

    // derivative
    float de_dt = (e - e_Prev) / (deltaT);

    // integral
    e_Integral += e * deltaT;

    // control signal
    float u = PH_KP*e + PH_KI*e_Integral + PH_KD*de_dt;

    // pump power saturation
    float power = fabs(u);
    if (power > 255)
    {
      power = 255;
    }
    else if (power < 76.5)
    {
      power = 0;
    }

    // select which pump to control
    if (u < 0)
    {
      S2_M1->setSpeed(0);
      S2_M1->run(FORWARD);
      S1_M4->setSpeed(power);
      S1_M4->run(FORWARD);
    }
    else
    {
      S1_M4->setSpeed(0);
      S1_M4->run(FORWARD);
      S2_M1->setSpeed(power);
      S2_M1->run(FORWARD);
    }

    e_Prev = e;

    Serial.print(ph_target_value);
    Serial.print(" ");
    Serial.print(global_ph_value);
    Serial.println();

    curr_time = millis();
  }
}

void move_ph_probe(ph_probe_motion action)
{
  if (action == OUT)
  {
    ph_servo.write(90);
  }
  else
  {
    ph_servo.write(-90);
  }
}

/////// Solenoid Functions ///////
void change_solenoid_state(solenoid_state new_state)
{
  if (new_state == OPEN)
  {
    digitalWrite(SOLENOID_RELAY_PIN, HIGH);
  }
  else
  {
    digitalWrite(SOLENOID_RELAY_PIN, LOW);
  }
}

/////// Temperature/Humidity Functions ///////
float get_temperature_value()
{
  DHT.read22(TEMP_HUMIDITY_PIN);
  return DHT.temperature;
}

float get_humidity_value()
{
  DHT.read22(TEMP_HUMIDITY_PIN);
  return DHT.humidity;
}

/////// Serial Communication Functions ///////
void write_new_entry(String humidity, String temp, String ph, String tds)
{
  Serial.println(humidity+":"+temp+":"+ph+":"+tds);
}

String read_from_serial()
{
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    return data;
  }
}

void loop() 
{
  switch (current_state)
  {
    case NOT_SPRAY:
      unsigned long not_spray_start_time = millis();

      tds_control_loop(MICRO, 660 + 30);
      tds_control_loop(BLOOM, global_tds_value + 20);
      move_ph_probe(IN);
      tds_control_loop(GRO, global_tds_value + 20);
      ph_control_loop(6);
      move_ph_probe(OUT);
      global_temp_value = get_temperature_value();
      global_humidity_value = get_humidity_value();

      //SEND MESSAGE HERE
      write_new_entry(String(global_humidity_value), String(global_temp_value), String(global_ph_value), String(global_tds_value));
      //growth = read_from_serial();
      delay(300000 - (millis() - not_spray_start_time));
      current_state = SPRAY;
      break;
    case SPRAY:
      change_solenoid_state(OPEN);
      delay(10000); // Spraying for 10 seconds
      change_solenoid_state(CLOSE);
      current_state = NOT_SPRAY;
      break;
    default:
      break;
  }
}
