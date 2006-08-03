#!/bin/sh
# $Id$
#
# Template based Nagios notify script.
#
# Author: Elan Ruusamäe <glen@pld-linux.org>
# Date: 2006-08-03
# License: Same as Nagios (GPL v2)
#

templatedir='/etc/nagios/templates'

# Substutute Nagios $VAR$-s (which are exported to environment by Nagios) from template.
template_subst() {
	awk 'BEGIN {
		for (var in ENVIRON) {
			if (substr(var, 1, length("NAGIOS_")) == "NAGIOS_") {
				val = ENVIRON[var];
				var = substr(var, 1 + length("NAGIOS_"));
				gsub(/#/,"\\#",val);
				printf("s#\$%s\$#%s#g\n", var, val);
			}
		}
	}' | sed -f - $tmpl
}

# extract nagios version from status file
export NAGIOS_VERSION=$(awk -F= '/version=/{print $2}' $NAGIOS_STATUSDATAFILE)

tmpl="$templatedir/$1.tmpl"
if [ ! -f "$tmpl" ]; then
	echo >&2 "$0: template '$tmpl' can not be found!"
	exit 1
fi

template_subst "$tmpl"
