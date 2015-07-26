#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "test1.h"

void baz()
{
	printf("baz\n");
}

void bar()
{
	printf("bar\n");
	baz();
	baz();
}


void foo()
{
	printf("foo\n");
	bar();
}

int main()
{
	// int x = 100; 
	// int y = 26;
	// if ((x|y) < 0) {
	// 	printf("got here\n");
	// }
	// int direction = 1;
	// char direction_name = direction["abcd"];
	// printf("\n%c\n", direction_name);

	// register short *to = (short*) malloc(4 * sizeof(short));
	// register short *from = (short*) malloc(4 * sizeof(short));
	// from[0] = 1;
	// from[1] = 2;
	// from[2] = 3;
	// from[3] = 4;

	// register count;
	// register n = (count + 3) / 4;
	// switch (count % 4) {
	// case 0: do { *to = *from++;
	// case 7:      *to = *from++;
	// case 6:      *to = *from++;
	// case 5:      *to = *from++;
	// case 4:      *to = *from++;
	// case 3:      *to = *from++;
	// case 2:      *to = *from++;
	// case 1:      *to = *from++;
	//         } while (--n > 0);
	// }

	int a = 3;
	int b = 7;
	a^=b^=a^=b;
	printf("%d", a);
	return 0;
}