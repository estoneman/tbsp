
CC=/usr/bin/clang

SRC=main.c
OUT=main

CFLAGS=-Wall -Werror -Wextra -pedantic -std=c11 -O3

default: all

all: build clean

build: $(SRC)
	$(CC) $(CFLAGS) -o $(OUT) $(SRC)

clean: $(OUT)
	rm -f $(OUT)
