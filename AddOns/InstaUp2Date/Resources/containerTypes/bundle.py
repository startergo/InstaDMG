#!/usr/bin/env python

import os

import file

class bundle(file.file):
	'''Class to handle bundles'''
	
	# ---- class methods
	
	@classmethod
	def scoreItemMatch(myClass, itemPath, processInformation, **kwargs):
		
		if os.path.isdir(itemPath) and os.path.exists(os.path.join(itemPath, 'Contents/Info.plist')):
			return myClass.getMatchScore()
		
		return 0