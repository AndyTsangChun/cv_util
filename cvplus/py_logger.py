import logging

__author__ = "Andy Tsang"
__credits__ = ["Andy Tsang"]
__version__ = "0.0.0"
__maintainer__ = "Andy Tsang"
__email__ = "atc1992andy@gmail.com"

class PyLogger:
	def __init__(self, logger_name=None, log_path=None, log=False, debug=False):
		log_level = logging.CRITICAL
		if log: log_level=logging.INFO
		if debug: log_level=logging.DEBUG

		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(log_level)
		
		# set handler for cmd format
		sh = logging.StreamHandler()
		if logger_name is not None:
			sh_formatter = logging.Formatter('[{}-%(levelname)s] %(message)s'.format(logger_name))
		else:
			sh_formatter = logging.Formatter('[logger-%(levelname)s] %(message)s')
		sh.setFormatter(sh_formatter)
		self.logger.addHandler(sh)

		#set handler to store log
		if log_path is not None:
			fh = logging.FileHandler()
			fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			fh.setFormatter(sh_formatter)
			self.logger.addHandler(fh)

	def debug(self, msg, *args, **kwargs):
		self.logger.debug(msg, *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		self.logger.info(msg, *args, **kwargs)

	def warning(self, msg, *args, **kwargs):
		self.logger.warning(msg, *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		self.logger.error(msg, *args, **kwargs)

	def critical(self, msg, *args, **kwargs):
		self.logger.critical(msg, *args, **kwargs)

	def exception(self, msg, *args, **kwargs):
		"""
		We don't use exception here, cuz its given in the message
		The method allow hiding error msg from terminal for deployment

		Args:
			msg(str): error msg
		"""
		self.logger.debug(msg, *args, **kwargs)