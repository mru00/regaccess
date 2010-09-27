XML = heater-control-regs.xml
MD  = ~/dev/02versuche/regaccess/
REG = python regaccess-gen.py -i $(MD)
OD  = ~/dev/01atmel/heater-control/firmware

.PHONY: test
test: $(OD)/regaccess.c $(OD)/regaccess.h heatercontrol.py

.PHONY: validate
validate:
	xmlstarlet val regaccess.xsd
	xmlstarlet val --well-formed --err $(XML)
	xmlstarlet val --xsd regaccess.xsd --err $(XML)

$(OD)/regaccess.c: $(OD)/regaccess.h gen_avr_impl.mako $(XML) regaccess-gen.py
	$(REG) $(XML) gen_avr_impl.mako > $@

$(OD)/regaccess.h: gen_avr_header.mako  $(XML) regaccess-gen.py | validate
	$(REG) $(XML) gen_avr_header.mako > $@

heatercontrol.py:  $(XML) gen_python.mako regaccess-gen.py
	$(REG) $(XML) gen_python.mako > $@
	-pychecker -Q $@

test-sizes: test-sizes.c

.PHONY: clean
clean:
	rm heatercontrol.py $(OD)/regaccess.h $(OD)/regaccess.c heatercontrol.pyc *.mako.py *.mako.pyc