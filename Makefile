all: lint
	@:

lint:
	./lint.sh

clean:
	@:

install: lint
	cp bin/* ~/.local/bin/
