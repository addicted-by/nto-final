#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>

#include "client2server.h"
#include "militime.h"

int tracker(FILE* tracklog) {
	static double hist_dx = 0.;
	client2server* c2s;
	c2s = new client2server;
	char str[500];

	int dx=0;
	int new_dx;
	while(1) {
	  status_type new_status;
	  int new_state,new_position;
	  unsigned char payload[4];
	  long new_ticks;
	    
		new_status=(status_type)c2s->getStatus();
		new_dx=new_status&0x0000000FFF;
		dx=(new_dx<2048)?new_dx:(new_dx%2048)-2048;

		int i;

		fprintf(tracklog,"%d\n",
				(int)dx
				);
		fflush(tracklog);

		hist_dx=dx;
	  if(fabs((double)hist_dx)<500.0)
	  {
		  if(fabs(hist_dx) < 10)
		  {
			  c2s->moveStop();
		  } 
		  else
		  {
		  int speed;
		  speed=4;
		  speed=(speed>100)?100:speed;
			  if(hist_dx>0)
			  {
				  c2s->moveLeft(speed);
			  }
			  else
			  {
				  c2s->moveRight(speed);
			  }
		  }
	  }
	}
	delete (c2s);
	return 0;
}

