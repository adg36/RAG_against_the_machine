"""
Custom exceptioins

This module defines all application-specific exceptions used to
represent errors across the different phases.

"""


class RagError(Exception):
    """
    Base exception for all RAG-related errors.

    This is the root exception for the project. All custom exceptions
    inherit from this class to allow unified error handling at the
    application entry point.
    """


class ParseError(RagError):
    """Raised when the input is invalid."""
