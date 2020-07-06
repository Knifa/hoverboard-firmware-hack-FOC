#ifndef PID_H
#define PID_H

#include <stdint.h>

typedef struct{
  uint16_t    start;
  float     angle;
  float     error;
  float     pTerm;
  float     iTerm;
  float     dTerm;
  float     output;
} PidFeedback;

extern PidFeedback pid_feedback;

extern int32_t pid_output;

void pid_init();
void pid_compute(int32_t angle, int32_t gyroAngle);

#endif
