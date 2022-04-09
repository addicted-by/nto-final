#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BLOCK_SIZE 1000

int decoder(FILE* r_fifo, FILE* w_fifo, FILE* tracklog)
{
  char buf[BLOCK_SIZE*2];
  long s;

  s = fread(buf, sizeof(char), BLOCK_SIZE*2, r_fifo);
  for(;s>0;) {
    if (s > 1) fwrite(buf, sizeof(char), s, w_fifo);
    s = fread(buf, sizeof(char), BLOCK_SIZE*2, r_fifo);     
  }
  return 0;
}
