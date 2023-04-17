CC=python

SRC=setup.py
CFLAGS=build_ext --inplace

ARTIFACTS=build/ edit_distance.c  edit_distance.cpython-311-darwin.so

default: all

all: build clean

.PHONY: build
build: $(SRC)
	$(CC) $(SRC) $(CFLAGS)

clean: $(ARTIFACTS)
	@echo "Removing $(ARTIFACTS)"
	@rm -rf $(ARTIFACTS)
