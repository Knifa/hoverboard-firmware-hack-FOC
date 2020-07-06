#include "pid.h"
#include "config.h"
#include "defines.h"

PidFeedback pid_feedback;
int32_t pid_output = 0;

float kP = 80.0f;
float kI = 0.0f;
float kD = 3.0f;
float targetAngle = 0.0f;
float dt = ((float) DELAY_IN_MAIN_LOOP / 1000.0f);

double outputSum = 0;
double errorSum = 0;

float lastDterm = 0;
float lastAngle = 0;
float lastError = 0;
float lastOutput = 0;

void pid_init() {

}

void pid_compute(int32_t angle, int32_t gyroAngle) {
  float currentAngle = angle / 100.0f;
  //currentAngle = lastAngle + ((currentAngle - lastAngle) * 0.5f);

  float dAngle = currentAngle - lastAngle;
  //float dAngle = gyroAngle / 10.f;

  float error = targetAngle - currentAngle;
  float dError = error - lastError;

  errorSum = errorSum + error * dt;
  errorSum = CLAMP(errorSum, -100, 100);

  float pTerm = kP * error;
  float iTerm = kI * errorSum;
  float dTerm = kD * dAngle;
  dTerm = lastDterm + ((dTerm - lastDterm) * 0.25f);

  float output = pTerm + iTerm + dTerm;
  //output = lastOutput + ((output - lastOutput) * 1.0f);

  //outputSum += kI * error;
  //outputSum -= kP * dAngle;
  //outputSum = CLAMP(outputSum, -250, 250);
  //float output = outputSum - (kD * dAngle);

  lastAngle = currentAngle;
  lastError = error;
  lastOutput = output;
  lastDterm = dTerm;

  pid_output = output;

  /*pid_feedback.start = (uint16_t) SERIAL_START_FRAME;
  pid_feedback.angle = currentAngle * 100;
  pid_feedback.error = error;
  pid_feedback.pTerm = -kP * dAngle;
  pid_feedback.iTerm = outputSum;
  pid_feedback.dTerm = - (kD * dAngle);
  pid_feedback.output = output;*/

  pid_feedback.start = (uint16_t) SERIAL_START_FRAME;
  pid_feedback.angle = currentAngle * 100;
  pid_feedback.error = error;
  pid_feedback.pTerm = pTerm;
  pid_feedback.iTerm = iTerm;
  pid_feedback.dTerm = dTerm;
  pid_feedback.output = output;
}
