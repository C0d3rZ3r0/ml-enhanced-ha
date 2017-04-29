class PredictionModel:

	datasetFile=""
	modelFile=""
	prediction={}
	
	def __init__(self,modelFile):
		self.modelFile=modelFile
		pass
	
	def applyMLAlgorithm(self):
		#TODO:READ datasetFile into a dict
		#TODO:apply machine learning to it
		#TODO:store prediction model in modelFile
		#TODO:store prediction in that prediction dict
		pass
	
	def predictAction(self):
		#TODO:should return a proper JSON built from the prediction dict or the prediction dict
		pass
