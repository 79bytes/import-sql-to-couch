import sys

class Verbosity:
	"""Implements rudimentary functionality to provide methods for
	a simple verbosity."""

	def __init__(self, verbose=True):
		"""Initilizes the verbosity-object.

		Parameter:
		bool verbose See also 'SetVerbosity'
		"""

		self.SetVerbosity(verbose)
	# End def

	def SetVerbosity(self, verbose=True):
		"""Sets the verbosity to be en-/disabled.

		Parameter:
		bool verbose True, if verbosity should be enabled, False if not.
		"""

		# Check
		if not isinstance(verbose, bool): raise TypeError

		# Save verbosity-state
		self.__verbosity=verbose
	# End def

	def Enable(self):
		"""Simply enables verbosity.

		Equal to setting verbosity via 'SetVerbosity(True)'.
		"""

		self.__verbosity=True
	# End def

	def Disable(self):
		"""Simply disables verbosity.

		Equal to setting verbosity via 'SetVerbosity(False)'.
		"""

		self.__verbosity=False
	# End def

	def Say(self, *output):
		"""Outputs/Says given parameters to stdout."""
		# Check
		if not self.__verbosity: return

		for op in output:
			print op,
			sys.stdout.flush()
		# End for

		print
		sys.stdout.flush()
	# End def
# End class
