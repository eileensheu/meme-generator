"""Provide quote_engine specific exceptions."""

class InvalidFileFormat(Exception):
	"""An exception for invalid file format."""
	pass

class InvalidFilePath(Exception):
	"""An exception for invalid file path."""
	pass

class UnsupportedFileType(Exception):
	"""An exception for unsupported file type."""
	pass
