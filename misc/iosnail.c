#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <sys/time.h>
#include <sys/types.h>

#include <sys/ioctl.h>

/*
a playground for producing sequential io and watching it with iostat|vmstat|symstat|...

usage: iosnail <blocksize-in-byte> <count> <min-time-per-write-operation-in-usecs> <use-os-cache> <filename-to-write>

examples:
    ./iosnail 1024 20 500000 0 ./bla.out # tries 20x to write 1024 byte in one write-call every 1/2sec without using cache (=> so duration should be 10s)

    compare the following (watch iostat|vmstat|symstat|... in parallel) 
    ./iosnail $(echo 1024^2|bc) 2 0 0 ./bla
    ./iosnail 2 $(echo 1024^2|bc) 0 0 ./bla

    thanx to unix (everything is a file) we can open complete block-devices like files too:
    ./iosnail $(echo 1024^2|bc) 20 500000 0 /dev/<blockdevice>
  
watch in parallel:

iostat -d <device-your-writing-to> -x 1

# copyright 

    Copyright (C) 2011 Sven Hessenmueller <sven.hessenmueller@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# literature:

- "Basic I/O Monitoring on Linux"|http://www.pythian.com/news/247/basic-io-monitoring-on-linux/
- "Linux Performance Monitoring"|http://www.ufsdump.org/papers/or-linux-performance-2008.pdf
- "Anatomy of a Read and Write Call"|http://www.linuxjournal.com/article/6237?page=0,0
*/

void wait4user(char* msg) {
    /* show msg and wait for user to acknowledge */
    char buf[10];
    printf("%s", msg);
    fflush(stdout);
    fgets(buf,9,stdin); /* wait for user pressing return */
}


/* ------------------------------------------------------------- */

int usecsleep(int usecs) {
    /* sleep intervalls < 1 sec., here microseconds
       eg. usecsleep(500000) => sleep 1/2 sec */

    struct timeval tv;

    tv.tv_sec = 0;
    tv.tv_usec = usecs;
    return select(0,NULL,NULL,NULL, &tv);
}


long int diff_usec(struct timeval tv_a, struct timeval tv_b) {
    /* timediff in usecs */

    /* CHECKME!!! */

    int dsecs = tv_b.tv_sec - tv_a.tv_sec;
    int dusecs = NULL;

    if (dsecs == 0) {
        return tv_b.tv_usec - tv_a.tv_usec;
    }

    if (tv_b.tv_usec >= tv_a.tv_usec) {
        dusecs = dsecs * 1000000 + (tv_b.tv_usec - tv_a.tv_usec);
        return dusecs;
    }

    dsecs = tv_b.tv_sec - tv_a.tv_sec - 1;
    dusecs = dsecs * 1000000 + (1000000 - tv_a.tv_usec + tv_b.tv_usec);

    return dusecs;
}

float diff_sec(struct timeval a, struct timeval b) {
    return (float) diff_usec(a,b) / 1000000;
}

/* ------------------------------------------------------------- */

void do_cycles(int fd, int bpc, int cycles, char *buff) {
    /* write as fast as you can */
    int i;
    for (i=0; i < cycles; i++) {
        //if (write(fd, "Hello World!\n", 13) != 13) {
        if (write(fd, buff, bpc) != bpc) {
            perror("write");
            exit(1);
        }
    }
}

void do_cycles_timed(int fd, int bpc, int cycles, char *buff, int cycleusec) {
    /* if a cycle is faster than cycleusec, wait before doing the next one */

    struct timeval tv_now, tv_then;
    struct timezone tz_now, tz_then;

    int i;
    for (i=0; i < cycles; i++) {
        gettimeofday(&tv_now,&tz_now);

        //if (write(fd, "Hello World!\n", 13) != 13) {
        if (write(fd, buff, bpc) != bpc) {
            perror("write");
            exit(1);
        }

        gettimeofday(&tv_then,&tz_then);

        while(diff_usec(tv_now,tv_then) < cycleusec) { /* wait until cycleusecs are over if necessary */
            gettimeofday(&tv_then,&tz_then);
            sched_yield();
        }
    }

}


int main(int argc, char ** argv) {

    struct timeval tv_now, tv_then;
    struct timezone tz_now, tz_then;

    int fd;
    //char buff[4096];
    //char buff[1048576]; /* 10^2 */
    char * buff;

    
    //int bpc = 1048576; int cycles = 1000; int cycleusec = 1000000, use_os_caching=1; /* user args */
    //int bpc = BUFSIZ; int cycles = 1000; int cycleusec = 1000000, use_os_caching=1; /* user args */

    //int bpc = 1048576; int cycles = 10; int cycleusec = 1000000, use_os_caching = 0; /* user args */
    int bpc = 1; int cycles = 20; int cycleusec = 500000; int use_os_caching = 0; char fname[80] = "./testfile.iosnail"; /* user args */
    //printf("BUFSIZ: %i", BUFSIZ);

    if (argc < 6) {
        printf("iosnail 0.0.2\n");
        printf("usage: iosnail <blocksize> <count> <min-time-per-write-op-in-usecs> <use-os-cache> <filename-to-write>\n");
        exit(1);
    }
    else {
        bpc = atoi(argv[1]);
        cycles = atoi(argv[2]);
        cycleusec = atoi(argv[3]);
        use_os_caching = atoi(argv[4]);
        strcpy(fname,argv[5]);
    }

    printf("bpc: %i, cycles: %i, cycleusec: %i, use_os_caching: %i\n", bpc, cycles,cycleusec,use_os_caching);
    printf("fname: %s\n\n", fname);

    buff = (char *) malloc (bpc); /* allcoate N bytes of memory */

    if (use_os_caching) {
        if((fd = open(fname, O_TRUNC|O_CREAT|O_WRONLY,0644)) < 0) {
            perror("open");
            exit(1);
        }
    }
    else {
        if((fd = open(fname, O_TRUNC|O_CREAT|O_WRONLY|O_SYNC,0644)) < 0) { // NO CACHING!
            perror("open");
            exit(1);
        }
    }

    gettimeofday(&tv_now,&tz_now);

    printf("--start sec: %i usec %i\n", (int) tv_now.tv_sec, (int) tv_now.tv_usec);


    if (!cycleusec) {
        printf("do_cycles... as fast as we can.\n", cycleusec);
        do_cycles(fd,bpc,cycles,buff);
    }
    else {
        printf("do_cycles_timed... 1 cycle >= %iusec\n", cycleusec);
        do_cycles_timed(fd,bpc,cycles,buff,cycleusec);
    }

    //wait4user("please press return to continue\n");
    //usecsleep(500000);

    gettimeofday(&tv_then,&tz_then);

    close(fd);
    free(buff);

    printf("--stop sec: %i usec %i\n", (int) tv_then.tv_sec, (int) tv_then.tv_usec);

    printf("\nbytes written: %i\n", bpc * cycles);
    printf("duration:      ");
    printf("%fs (== %liusec)\n", diff_sec(tv_now,tv_then), diff_usec(tv_now,tv_then));
    printf("MiB/s:         %f\n", ((float) bpc * (float) cycles) / 1024.0 / 1024.0 / diff_sec(tv_now,tv_then));

    return 0;
}

