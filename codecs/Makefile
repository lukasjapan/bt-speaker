CC = gcc -O3
CFLAGS =
INSTALL_PREFIX = /usr
HEADER = rtpsbc.h

ifndef PLATFORM
	PLATFORM = armv6
endif

OBJS = rtpsbc.o sbc.o sbc_primitives.o sbc_primitives_$(PLATFORM).o

TARGET = librtpsbc.so

%.o: %.c
	$(CC) $(CFLAGS) -fPIC -c $< -o $@

$(TARGET): $(OBJS)
	$(CC) -shared $(OBJS) -o $(TARGET)

.PHONY: all clean

all: $(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)

install: $(TARGET)
	cp $(TARGET) $(INSTALL_PREFIX)/lib
	cp $(basename $(TARGET)).pc $(INSTALL_PREFIX)/lib/pkgconfig
	cp $(HEADER) $(INSTALL_PREFIX)/include
	ldconfig
