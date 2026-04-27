# Copyright (C) 2024-2026 Burak Günaydin
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

# Third-party imports
from teatype.enum import XTerm

if __name__ == '__main__':
    # Example usage and test cases
    from teatype.logging import *
    println()
    # Output: document-o-c-r-detection
    print(f'{XTerm.RESET}DocumentOCRDetection ' + f'{XTerm.CYAN} -> kebabify                        -> ' + f'{XTerm.GREEN}' + kebabify('DocumentOCRDetection'))
    # Output: document-ocr-detection
    print(f'{XTerm.RESET}DocumentOCRDetection ' + f'{XTerm.CYAN} -> kebabify + preserve_capitals    -> ' + f'{XTerm.GREEN}' + kebabify('DocumentOCRDetection', preserve_capitals=True))
    # Output: camel-case-example
    print(f'{XTerm.RESET}CamelCaseExample     ' + f'{XTerm.CYAN} -> kebabify                        -> ' + f'{XTerm.GREEN}' + kebabify('CamelCaseExample'))
    # Output: pascal-case-example
    print(f'{XTerm.RESET}PascalCaseExample    ' + f'{XTerm.CYAN} -> kebabify                        -> ' + f'{XTerm.GREEN}' + kebabify('PascalCaseExample'))
    # Output: test-string-examples
    print(f'{XTerm.RESET}TestString           ' + f'{XTerm.CYAN} -> kebabify + plural               -> ' + f'{XTerm.GREEN}' + kebabify('TestString', plural=True))
    # Output: sample-name
    print(f'{XTerm.RESET}SampleName           ' + f'{XTerm.CYAN} -> kebabify + remove(ple)          -> ' + f'{XTerm.GREEN}' + kebabify('SampleName', remove='ple'))
    # Output: demo-text
    print(f'{XTerm.RESET}DemoText             ' + f'{XTerm.CYAN} -> kebabify + replace(demo,prod)   -> ' + f'{XTerm.GREEN}' + kebabify('DemoText', replace=('demo', 'prod')))
    # Output: kebab-case-example
    print(f'{XTerm.RESET}kebab-case-example   ' + f'{XTerm.CYAN} -> unkebabify                      -> ' + f'{XTerm.GREEN}' + unkebabify('kebab-case-example'))
    # Output: pascalcaseexample
    print(f'{XTerm.RESET}pascalcaseexample    ' + f'{XTerm.CYAN} -> unkebabify                      -> ' + f'{XTerm.GREEN}' + unkebabify('pascalcaseexample'))
    print(XTerm.RESET)