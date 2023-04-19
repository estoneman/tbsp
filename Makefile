CC=python

SRCDIR=py

ARTIFACTS=$(addprefix $(SRCDIR)/, edit_distance.c \
		    edit_distance.cpython-311-darwin.so)

VALID_TARGETS=build clean help

default: all

all: build clean

.PHONY: build
build: $(SRC)
	$(CC) setup.py

.PHONY: clean
clean:
	@echo "Removing $(ARTIFACTS)"
	@rm -rf $(ARTIFACTS)

help:
	@echo "Valid targets: $(VALID_TARGETS)"

