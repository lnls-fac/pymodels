# Destination directory
DEST_DIR = /home/fac_files/db/excitation_curves

FILES = *.txt

FULLFILES = $(addprefix $(DEST_DIR)/, $(FILES))

install: $(DEST_DIR) uninstall $(FILES)
	cp $(FILES) $(DEST_DIR)

uninstall:
	-rm -rf $(FULLFILES)

develop: $(DEST_DIR) uninstall $(FILES)
	ln -srf $(FILES) $(DEST_DIR)

$(DEST_DIR):
	mkdir -p $(DEST_DIR)
