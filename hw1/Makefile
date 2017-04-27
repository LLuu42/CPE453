DEP = lwp.c lwp.h
LWP = liblwp.a 

all:	$(LWP)

$(LWP):	lwp.o	
	ar r $@ lwp.o	
	ranlib $@

lwp.o:	lwp.c lwp.h
	gcc -m32 -Wall -pedantic -c -o lwp.o lwp.c

clean :
	rm *.o *.a
	 
