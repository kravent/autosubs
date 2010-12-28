.PHONY: install uninstall
BINDIR	=	/usr/bin/
MAINDIR	=	/opt/autosubs/

BINSOURCEDIR	=	./bin/
MAINSOURCEDIR	=	./src/

BINFILES	=	autosubs autosubs-downloader autosubs-translate autosubs-encode


install:
	mkdir -p $(MAINDIR)
	$(foreach file, $(BINFILES), cp -p $(BINSOURCEDIR)$(file) $(BINDIR);)
	cp -R -p $(MAINSOURCEDIR)* $(MAINDIR)
	

uninstall:
	rm -rf $(MAINDIR)
	$(foreach file, $(BINFILES), rm -f $(BINDIR)$(file);)

