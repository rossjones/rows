# coding: utf-8

# Copyright 2014 Álvaro Justen <https://github.com/turicas/rows/>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import datetime
import tempfile
import textwrap
import unittest

import rows


sample_table = textwrap.dedent(u'''
    +----+--------------+------------+
    | id |   username   |  birthday  |
    +----+--------------+------------+
    |  1 |      turicas | 1987-04-29 |
    |  2 | another-user | 2000-01-01 |
    |  3 |       álvaro | 1900-01-01 |
    +----+--------------+------------+
''').strip()

class ExportToTextTestCase(unittest.TestCase):


    def setUp(self):
        self.table = rows.Table(fields=['id', 'username', 'birthday'])
        data = [
                [1, u'turicas', datetime.date(1987, 4, 29)],
                [2, u'another-user', datetime.date(2000, 1, 1)],
                [3, u'álvaro', datetime.date(1900, 1, 1)],
        ]
        for row in data:
            self.table.append(row)


    def test_return_simple_test(self):
        returned = self.table.export_to_text()
        self.assertEqual(returned.strip(), sample_table)
        self.assertEqual(type(returned), unicode)


    def test_column_sizes(self):
        table = rows.Table(fields=['id', 'username', 'big-column-name'])
        data = [
                [1, u'a', datetime.date(1987, 4, 29)],
                [2, u'b', datetime.date(2000, 1, 1)],
                [3, u'c', datetime.date(1900, 1, 1)],
        ]
        for row in data:
            table.append(row)

        expected = textwrap.dedent(u'''
        +----+----------+-----------------+
        | id | username | big-column-name |
        +----+----------+-----------------+
        |  1 |        a |      1987-04-29 |
        |  2 |        b |      2000-01-01 |
        |  3 |        c |      1900-01-01 |
        +----+----------+-----------------+
        ''').strip()
        returned = table.export_to_text()
        self.assertEqual(returned.strip(), expected)


    def test_return_custom_elements(self):
        expected = textwrap.dedent(u'''
            -++++-++++++++++++++-++++++++++++-
            * id *   username   *  birthday  *
            -++++-++++++++++++++-++++++++++++-
            *  1 *      turicas * 1987-04-29 *
            *  2 * another-user * 2000-01-01 *
            *  3 *       álvaro * 1900-01-01 *
            -++++-++++++++++++++-++++++++++++-
        ''').strip()
        returned = self.table.export_to_text(dash='+', plus='-', pipe='*')
        self.assertEqual(returned.strip(), expected)
        self.assertEqual(type(returned), unicode)


    def test_return_custom_encoding(self):
        encoding = 'iso-8859-1'
        returned = self.table.export_to_text(encoding=encoding)
        self.assertEqual(returned.strip(), sample_table.encode(encoding))
        self.assertEqual(type(returned), str)


    def test_filename_simple_test(self):
        tmp = tempfile.NamedTemporaryFile(delete=True)
        with self.assertRaises(ValueError):
            self.table.export_to_text(tmp.name)

        self.table.export_to_text(tmp.name, encoding='utf-8')
        tmp.file.seek(0)
        returned = tmp.file.read()
        tmp.close()

        self.assertEqual(returned.strip(), sample_table.encode('utf-8'))


    def test_fobj_simple_test(self):
        tmp = tempfile.NamedTemporaryFile(delete=True)
        with self.assertRaises(ValueError):
            self.table.export_to_text(tmp.file)

        self.table.export_to_text(tmp.file, encoding='utf-8')
        tmp.file.seek(0)
        returned = tmp.file.read()
        tmp.close()

        self.assertEqual(returned.strip(), sample_table.encode('utf-8'))
