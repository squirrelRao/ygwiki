#!/bin/bash
cat $1 | sed 's|</td><td>|</td><td>|g' | tr '' '\n' > /tmp/a
cat /tmp/a | sed 's|</TD><TD>|</TD><TD>|g'| tr '' '\n' > $1

cat $1 | sed 's|</div><|</div><|g' | tr '' '\n' > /tmp/a
cat /tmp/a | sed 's|</DIV><|</DIV><|g'| tr '' '\n' > $1



