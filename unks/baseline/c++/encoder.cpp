#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int encoder(FILE* r_fifo, FILE* w_fifo) {
  #define BLOCK_SIZE 1000
  char buf[BLOCK_SIZE];
  long s;
  s = fread(buf, sizeof(char), BLOCK_SIZE, r_fifo);
  for(;s>0;) {
    fwrite(buf, sizeof(char), s, w_fifo);
    s = fread(buf, sizeof(char), BLOCK_SIZE, r_fifo);
  }
  return 0;
}
