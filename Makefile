CORE_FILES=argcount colorstrip countdown dec2hex fhas fsize fswap hex2dec peval untilfail
INSTALL_DIR=~/.local/bin/

all: lint
	@:

lint:
	./lint.sh

test:
	./test.py

clean:
	@:

# Install just the core files
mininstall:
	mkdir -p ${INSTALL_DIR}
	$(foreach script,${CORE_FILES},cp ./bin/${script} ${INSTALL_DIR};)

install:
	mkdir -p ${INSTALL_DIR}
	cp bin/* ${INSTALL_DIR}
