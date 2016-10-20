all: ${ARGS}.c
	$(call compile)
	$(call profile)
	python3 main.py . anl.txt

compile: ${ARGS}.c
	gcc -Wall -pg ${ARGS}.c -c
	gcc -Wall -pg ${ARGS}.o -o ${ARGS}

profile: ${ARGS}.c
	./${ARGS}
	gprof -b ./${ARGS} ./gmon.out > anl.txt

clean:
	rm -rf *.o anl.txt gmon.out
