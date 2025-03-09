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

class HSDBValueWrapper:
    """
    Wrapper that stores both the value and the field pointer reference.
    """
    def __init__(self, value, field):
        self._value = value
        # DEPRECATED: This is no longer needed since we are using lazy loading and caching
            # The field metadata (e.g., type, required), no longer keeping reference to the original HSDBField
        self._field = field
        
        self._cached_metadata = None
        self._metadata_loaded = False
        
    def _load_metadata(self):
        """
        Load the metadata (lazy loading).
        """
        if not self._metadata_loaded:
            self._cached_metadata = {
                'cls': self._field.cls,
                'computed': self._field.computed,
                'description': self._field.description,
                'editable': self._field.editable,
                'indexed': self._field.indexed,
                'max_size': self._field.max_size,
                'relation': self._field.relation,
                'required': self._field.required,
                'searchable': self._field.searchable,
                'type': self._field.type,
                'unique': self._field.unique
            }
            self._metadata_loaded = True
        return self._cached_metadata

    @property
    def cls(self):
        metadata = self._load_metadata()
        return metadata['cls']

    @property
    def computed(self):
        metadata = self._load_metadata()
        return metadata['computed']
    
    @property
    def description(self):
        metadata = self._load_metadata()
        return metadata['description']
    
    @property
    def editable(self):
        metadata = self._load_metadata()
        return metadata['editable']
    
    @property
    def indexed(self):
        metadata = self._load_metadata()
        return metadata['indexed']
    
    @property
    def max_size(self):
        metadata = self._load_metadata()
        return metadata['max_size']
    
    @property
    def relation(self):
        metadata = self._load_metadata()
        return metadata['relation']

    @property
    def required(self):
        metadata = self._load_metadata()
        return metadata['required']
    
    @property
    def searchable(self):
        metadata = self._load_metadata()
        return metadata['searchable']

    @property
    def type(self):
        metadata = self._load_metadata()
        return metadata['type']
    
    @property
    def unique(self):
        metadata = self._load_metadata()
        return metadata['unique']

    # DEPRECATED: This method is not needed anymore since lazy loading and caching optimization
        # def __getattr__(self, item):
        #     """
        #     If we access metadata (e.g., `student_A.id.type`), return it from the field.
        #     """
        #     return getattr(self._field, item)

    def __repr__(self):
        return repr(self._value)

    def __str__(self):
        return str(self._value)