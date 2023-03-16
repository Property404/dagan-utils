all: lint
	@:

lint:
	./lint.sh

clean:
	@:

install:
	cp bin/* ~/.local/bin/
