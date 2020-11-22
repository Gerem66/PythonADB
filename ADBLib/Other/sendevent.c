// Compile arm : arm-linux-gnueabi-gcc -static -march=armv7-a sendevent.c -o sendevent-arm64

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/ioctl.h>
//#include <linux/input.h> // this does not compile
#include <unistd.h>
#include <errno.h>

// from <linux/input.h>
typedef uint32_t        __u32;
typedef uint16_t        __u16;
typedef __signed__ int  __s32;
struct input_event {
    struct timeval time;
    __u16 type;
    __u16 code;
    __u32 value;
};
#define MICROSEC 1000000
#define EVIOCGVERSION _IOR('E', 0x01, int) /* get driver version */
// end <linux/input.h>

int GetValNumber(char *line) {
    char c;
    int nb = 0;
    int inVal = 0;
    while (c = *line++) {
        if (c == ' ') {
            if (inVal)
                inVal = 0;
        } else if (c != '\n') {
            if (!inVal) {
                inVal = 1;
                nb++;
            }
        }
    }
    return nb;
}

int main(int argc, char *argv[])
{
    int i;
    int fd;
    int ret;
    int version;
    struct input_event event;

    if(argc != 3) {
        fprintf(stderr, "use: %s input_device input_events\n", argv[0]);
        return 1;
    }

    fd = open(argv[1], O_RDWR);
    if(fd < 0) {
        fprintf(stderr, "could not open %s, %s\n", argv[optind], strerror(errno));
        return 1;
    }
    if (ioctl(fd, EVIOCGVERSION, &version)) {
        fprintf(stderr, "could not get driver version for %s, %s\n", argv[optind], strerror(errno));
        return 1;
    }

    FILE * fd_in = fopen(argv[2], "r");
    if (fd_in == NULL) {
        fprintf(stderr, "could not open input file: %s\n", argv[2]);
        return 1;
    }

    char line[128];
    float sleep_time;
    char type[32];
    char code[32];
    char value[32];

    while (fgets(line, sizeof(line), fd_in) != NULL) {
        int n = GetValNumber(line);
        if (n == 1) {
            sscanf(line, "%f", &sleep_time);
            usleep(sleep_time * MICROSEC);
        } else if (n == 3) {
            sscanf(line, "%s %s %s", type, code, value);

            // write the event to the appropriate input device
            memset(&event, 0, sizeof(event));
            event.type = (int) strtol(type, NULL, 16);
            event.code = (int) strtol(code, NULL, 16);
            event.value = (uint32_t) strtoll(value, NULL, 16);
            ret = write(fd, &event, sizeof(event));
            if (ret < sizeof(event)) {
                fprintf(stderr, "write event failed, %s\n", strerror(errno));
                return -1;
            }

            // Clear temporary buffers
            memset(line, 0, sizeof(line));
            memset(type, 0, sizeof(type));
            memset(code, 0, sizeof(code));
            memset(value, 0, sizeof(value));
        }
    }

    fclose(fd_in);
    close(fd);

    return 0;
}
