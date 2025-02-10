# Copyright (C) 2024-2025 Burak Günaydin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# From system imports
from typing import List

# TODO: Migrations always count one up in id dependent on app and model
# TODO: Always create a snapshot of all models before launching index db and if there are changes, create automatic migrations
# TODO: Always create a backup of all raw db entries before every migration (with optional include_files flag)
class HSDBMigration:
    app_name:str
    include_files:bool
    migration_id:int
    models_snapshot:dict
    was_auto_created:bool