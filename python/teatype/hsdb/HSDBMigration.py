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
from abc import ABC, abstractmethod

# From package imports
from teatype.io import path
from teatype.logging import hint, log, println

# From-as system imports
from datetime import datetime as dt

# TODO: Migrations always count one up in id dependent on app and model
# TODO: Always create a snapshot of all models before launching index db and if there are changes, create automatic migrations
# TODO: Always create a backup of all raw db entries before every migration (with optional include_non_index_files flag)
class HSDBMigration(ABC):
    __models_snapshot:dict # Holds snapshot data for models that get migrated
    __non_index_files_snapshot:dict|None # Optionally holds snapshot data for non-index files
    _auto_creation_datetime:str|None # ISO-formatted string for auto creation time
    _from_to_string:str # String representation of the migration's origin and destination
    _hsdb_path:str='/var/lib/hsdb' # Default path on linux
    _migration_ancestor:int|None # The previous migration's reference, if any
    _migration_backup_path:str # Path to the backup of the migration
    _migration_descendant:int # The next migration's reference, if any
    _rawfiles_path:str # Path to the rawfiles directory
    _rejectpile_path:str # Path to the rejectpile directory
    app_name:str # Name of the application this migration is associated with
    include_non_index_files:bool # Indicates if non-index files should be part of migration steps
    migration_id:int # Numeric identifier to order migrations
    migration_name:str # Descriptive name for the migration
    was_auto_created:bool # Marks whether the migration was automatically created

    def __init__(self, auto_migrate:bool=True):
        """
        Initializes the migration. If 'auto_migrate' is True, the 'migrate' method is called immediately.
        """
        if auto_migrate:
            self.run() # Proceed with migration if 'auto_migrate' is True
            
        self.overwrite_hsdb_path(self._hsdb_path) # Overwrites the default HSDB path with the default value
        
        # Default ancestor is the previous migration
        self._migration_ancestor = self.migration_id - 1 if self.migration_id != None else None 
        self._migration_descendant = self.migration_id + 1 # Default descendant is the next migration
        self._from_to_string = f'{self._migration_ancestor}->{self._migration_descendant}' # Default migration string

    def auto_create(self):
        """
        Sets '_auto_creation_datetime' to the current time in ISO format
        and marks the migration as automatically created.
        """
        self._auto_creation_datetime = str(dt.now().isoformat())
        self.was_auto_created = True # Acknowledges auto-creation

    def overwrite_hsdb_path(self, hsdb_path:str):
        """
        Allows changing the default HSDB path to a custom path.
        """
        self._hsdb_path = hsdb_path  # Updates the HSDB path with the new value
        
        self._index_path = path.join(hsdb_path, 'index') # Default index path
        self._rawfiles_path = path.join(hsdb_path, 'rawfiles') # Default rawfiles path
        self._rejectpile_path = path.join(hsdb_path, 'rejectpile') # Default rejectpile path
        
        backups_path = path.join(hsdb_path, 'backups')
        migration_backups_path = path.join(backups_path, 'migrations')
        self._migration_backup_path = path.join(migration_backups_path, self._from_to_string)
    
    #########
    # Hooks #
    #########
    
    def run(self):
        self.migrate()
    
    ####################
    # Abstract methods #
    ####################
    
    @abstractmethod
    def migrate(self):
        hint(f'Creating a local backup of the data before the {self._from_to_string} migration in the following path:')
        log('   ' + self._migration_backup_path)
        println()
        
        hint(f'Executing migration {self._from_to_string} for app "{self.app_name}" for data in the following path:')
        log('   ' + self._index_path)
        println()
        raise NotImplementedError('"migrate()" method must be implemented in migration-subclass')