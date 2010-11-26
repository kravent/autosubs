.PHONY: install uninstall
BINDIR	=	/usr/bin/
MAINDIR	=	/opt/autosubs/
LIBDIR	=	$(MAINDIR)lib/

BINSOURCEDIR	=	./bin/
MAINSOURCEDIR	=	./
LIBSOURCEDIR	=	./lib/

BINFILES	=	autosubs autosubs-downloader
MAINFILES	=	autosubs.py autosubsDownloader.py
LIBFILES	=	


install:
	mkdir -p $(MAINDIR)
	mkdir -p $(LIBDIR)
	$(foreach file, $(BINFILES), cp -p $(BINSOURCEDIR)$(file) $(BINDIR);)
	$(foreach file, $(MAINFILES), cp -p $(MAINSOURCEDIR)$(file) $(MAINDIR);)
	$(foreach file, $(LIBFILES), cp -p $(LIBSOURCEDIR)$(file) $(LIBDIR);)
	

uninstall:
	rm -rf $(MAINDIR)
	$(foreach file, $(BINFILES), rm -f $(BINDIR)$(file);)

