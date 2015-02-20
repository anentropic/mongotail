#  Mongotail, Log all MongoDB queries in a "tail"able way.
#  Copyright (C) 2015 Mariano Ruiz (<http://mrdev.com.ar>).
#
#  Author: Mariano Ruiz <mrsarm@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import sys
from bson import json_util


def print_obj(obj):
    ts_time = obj['ts']
    operation = obj['op']
    doc = obj['ns'].split(".")[-1]
    if operation in ('query', 'insert', 'remove', 'update'):
        if 'query' in obj:
            query = json_util.dumps(obj['query'])
        else:
            query = ""
        if operation == 'update':
            if 'updateobj' in obj:
                query += ' -> ' + json_util.dumps(obj['updateobj'])
                query += '. %s updated.' % obj['nMatched']
        elif operation == 'insert':
            if query != "":
                query += ". "
            query += '%s inserted.' % obj['ninserted']
        elif operation == 'remove':
            query += '. %s deleted.' % obj['ndeleted']
    elif operation == "command":
        query = json_util.dumps(obj['command']['query'])
        if 'count' in obj["command"]:
            doc = obj["command"]["count"]
            operation = "count"
        else:
            raise RuntimeError('Unknow command "%s"\nDump: %s' % (operation, json_util.dumps(obj)))
    else:
        raise RuntimeError('Unknow command "%s"\nDump: %s' % (operation, json_util.dumps(obj)))

    #print json_util.dumps(obj)
    sys.stdout.write("%s %s [%s] : %s\n" % (ts_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                                            operation.upper().ljust(6), doc, query))
    sys.stdout.flush()  # Allows pipe the output during the execution with others tools like 'grep'