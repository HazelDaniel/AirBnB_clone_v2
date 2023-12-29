#!/usr/bin/bash
# this bash script fixes the sql dump issue pertaining to foreign key constraint failure

echo "working..."
dump_path="$(dirname ${BASH_SOURCE[0]})/7-dump.sql"
if cat "$dump_path" | grep -Piq "password\('hbnb_dev_pwd'\)"; then
	echo "" 1> /dev/null;
else
	sed -i "s/'hbnb_dev_pwd'/PASSWORD('hbnb_dev_pwd')/g" "$dump_path"
fi
sed -i "s/) ENGINE=InnoDB.*/) ENGINE=InnoDB;/g" "$dump_path"
