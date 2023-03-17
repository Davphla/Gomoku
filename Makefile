##
## EPITECH PROJECT, 2020
## makefile
## File description:
## Makefile
##

TARGET_NAME	:=	 pbrain-gomoku-ai

TARGET_NAME_WIN	:=	 $(TARGET_NAME).exe

TARGET :=	$(wildcard ./src/*.py) \
		 	$(wildcard ./src/Policies/**/*.py)

PISKVORK := piskvork/piskvork.exe

MAIN := src/main.py

all:	build

build: $(TARGET_NAME)

build-windows: $(TARGET_NAME_WIN)

$(TARGET_NAME): $(TARGET)
	@ln -s $(MAIN) $(TARGET_NAME)
	chmod +x $(TARGET_NAME)
	@echo -e "\033[1;32m[OK]\033[0m" $(TARGET_NAME) "copied"

$(TARGET_NAME_WIN): $(TARGET)
	@which pyinstaller > /dev/null || (echo -e "\033[1;31m[ERROR]\033[0m pyinstaller is not installed" && exit 1)
	@echo "Compiling $(TARGET_NAME_WIN)..."
	@pyinstaller --onefile --name $(TARGET_NAME_WIN) --clean --log-level=ERROR $(TARGET) --paths .
	@cp dist/$(TARGET_NAME_WIN) $(TARGET_NAME_WIN)
	@chmod +x $(TARGET_NAME_WIN)
	@echo -e "\033[1;32m[OK]\033[0m" $(TARGET_NAME_WIN) "compiled"

$(PISKVORK):
	curl https://altushost-swe.dl.sourceforge.net/project/piskvork/piskvork.zip -o piskvork.zip
	unzip piskvork.zip -d piskvork
	rm piskvork.zip

run: build-windows $(PISKVORK)
	@which wine > /dev/null || (echo -e "\033[1;31m[ERROR]\033[0m wine is not installed" && exit 1)
	@echo "Running $(TARGET_NAME_WIN)..."
	wine $(PISKVORK) -p "./piskvork/pbrain-pela.exe" "./$(TARGET_NAME_WIN)"

run-win: build-windows $(PISKVORK)
	@echo "Running $(TARGET_NAME_WIN)..."
	./$(PISKVORK) -p "./piskvork/pbrain-pela.exe" "./$(TARGET_NAME_WIN)"

test: build-windows $(PISKVORK)
	@echo "Running tests..."
	./$(PISKVORK) -p "./$(TARGET_NAME_WIN)" "./$(TARGET_NAME_WIN)"

install: $(PISKVORK)
	@pip3 install -r requirements.txt

clean:
	@rm -rf build dist __pycache__ $(TARGET_NAME_WIN).spec

fclean:
	@rm -f $(TARGET_NAME_WIN) $(TARGET_NAME)

re: fclean all

uninstall: $(PISKVORK)
	@pip3 uninstall -r requirements.txt
	rm -rf piskvork

.PHONY: all run run-win fclean clean re install uninstall build build-windows
