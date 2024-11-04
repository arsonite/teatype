#!/usr/bin/env python3.11

# Copyright (C) 2024-2025 Burak Günaydin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# From package imports
from teatype.cli import BaseCLI

class Template(BaseCLI):
    def meta(self):
        return {
            'name': '',
            'shorthand': '',
            'help': '',
            'commands': [
                {
                    'name': '',
                    'shorthand': '',
                    'help': '',
                },
            ],
            'arguments': {
                {
                    'name': '',
                    'help': '',
                    'required': True
                }
            },
            'flags': [
                {
                    'short': '',
                    'long': '',
                    'help': '',
                    'help_extension': [
                        '',
                        ''
                    ],
                    'required': False
                },
            ],
        }

    def execute(self):
        raise NotImplementedError('This method must be implemented.')

if __name__ == '__main__':
    Template()