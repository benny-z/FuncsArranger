# test.o: test.c test1.c
# 	gcc -finstrument-functions -g -c -o test.o test.c
# 	gcc -finstrument-functions -g -c -o test1.o test1.c

# trace.o: trace.c
# 	gcc -c -o trace.o trace.c

test: test.c
	gcc -Wall -pg -fno-omit-frame-pointer test.c -o test

# test.o: test.c
	# gcc -pg test.c -c

# test: trace.o test.o
# 	gcc test.o trace.o -o test

profile: test
	./test
	# gprof -q -b ./test ./gmon.out > anl.txt
	gprof -b ./test ./gmon.out > anl.txt

graph: profile
	python ~/.local/lib/python2.7/site-packages/gprof2dot.py -n0 -e0 anl.txt | dot -Tpng -o output.png

clean:
	rm -rf test.o trace.o trace test trace.out gmon.out output.png
