CC=python

SRC=setup.py
CFLAGS=build_ext --inplace

ARTIFACTS=build/ edit_distance.c  edit_distance.cpython-311-darwin.so

VALID_TARGETS=build clean help

.PHONY: build
build: $(SRC) help
	$(CC) $(SRC) $(CFLAGS)

.PHONY: clean
clean: $(ARTIFACTS) help
	@echo "Removing $(ARTIFACTS)"
	@rm -rf $(ARTIFACTS)

.PHONY: help
help:
	@echo "Valid targets: $(VALID_TARGETS)"

%:
	@echo "Invalid target. Type 'make help' for valid targets." >&2
	@false
