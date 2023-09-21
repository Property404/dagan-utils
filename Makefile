INSTALL_DIR=~/.local/bin/

all: lint
	@:

lint:
	./lint.sh

test:
	./test.sh

clean:
	@:

install:
	mkdir -p ${INSTALL_DIR}
	cp bin/* ${INSTALL_DIR}
