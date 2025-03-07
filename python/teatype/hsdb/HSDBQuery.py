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

class HSDBQuery:
    def __init__(self, model_class):
        # model_class is used later to help interpret attribute types and relations
        self.model_class = model_class
        self.conditions = []  # list of (attribute_path, operator, value)
        self.sort_key = None
        self.current_attribute = None

    def __repr__(self):
        return f"<HSDBQuery conditions={self.conditions} sort_by={self.sort_key}>"

    def _add_condition(self, op, value):
        if self.current_attribute is None:
            raise ValueError("No attribute specified. Call where() first.")
        # Each condition is stored with its attribute path, operator, and value.
        self.conditions.append((self.current_attribute, op, value))
        self.current_attribute = None

    def all(self):
        # Calling all resets any previous conditions
        self.conditions = []
        return self

    def sort_by(self, attribute_name):
        self.sort_key = attribute_name
        return self

    def filter_by(self, attribute_name):
        # Alias for where()
        return self.where(attribute_name)

    def where(self, attribute_name):
        # Set current attribute that the following operator verb will apply to
        self.current_attribute = attribute_name
        return self

    def equals(self, value):
        self._add_condition('==', value)
        return self

    def less_than(self, value):
        self._add_condition('<', value)
        return self

    def greater_than(self, value):
        self._add_condition('>', value)
        return self