"""
	The main file that runs as the prediction server. It collects
	data from the Raspberry Pi, puts it into a csv file, and
	performs and returns the prediction over this data to the Pi.
	
	All communication is done thru a RESTful WebAPI implemented
	in Flask.
"""

from sklearn.linear_model import LogisticRegression as logit
from sklearn.externals import joblib as joblib
import pandas
import datetime
from learningAgent import LearningAgent as LearningAgent
from predictionModel import PredictionModel as PredictionModel
from flask import Flask as Flask
from flask import jsonify as jsonify

datasetFile="./datasets/dataset1.csv"
b1ModelFile="./models/model1.pkl"
b2ModelFile="./models/model2.pkl"
b3ModelFile="./models/model3.pkl"

b1Model=PredictionModel(b1ModelFile)
b2Model=PredictionModel(b2ModelFile)
b3Model=PredictionModel(b3ModelFile)
agent=LearningAgent(datasetFile)

#stateSet={"ON":1,"OFF":0}
bulbs={"b1":0,"b2":0,"b3":0}
stateSet=("OFF","ON")

hourOfLastPrediction=0
minuteOfLastPrediction=0
DEF_ENTRY_COUNT=10
minEntryCount=10

"""
Some function definitions.
"""
def datasetWrite():
	#hourOfAction=str(datetime.datetime.now().hour)
	#minuteOfAction=str(datetime.datetime.now().minute)
	df=open(datasetFile, 'a+')
	#df.write(hourOfAction+','+minuteOfAction+','+str(bulbs["b1"])+','+str(bulbs["b2"])+','+str(bulbs["b3"])+'\n')
	df.write(str(bulbs["b1"])+','+str(bulbs["b2"])+','+str(bulbs["b3"])+'\n')
	df.close()

def datasetRead():
	df=open(datasetFile, 'r')
	#data=pandas.read_csv(datasetFile)
	#return (data["b1"],data["b2"],data["b3"])
	return pandas.read_csv(datasetFile)
"""
Definitions end.
"""

#initialize Flask
pcServer=Flask(__name__)

@pcServer.route("/")
def startPage():
	return "PC side server is up and running!"

@pcServer.route("/<bulbName>/<newState>")
def changeTo(bulbName,newState):
	global minEntryCount
	
	if bulbName not in bulbs:
		return "Bulb "+bulbName+" does not exist."
	if newState not in stateSet:
		return newState+" is not a valid state."
	else:
		#TODO[done]:write bulbs' current states to dataset file
		bulbs[bulbName]=stateSet.index(newState)
		datasetWrite()
		#decrease minEntryCount till it's zero.
		#if minEntryCount>0:
		#	minEntryCount=minEntryCount-1
		return "Bulb "+bulbName+" is now "+stateSet[bulbs[bulbName]]

@pcServer.route("/writenochange")
def writeNoChange():
	datasetWrite()
	return jsonify(result={"status":200})

@pcServer.route("/generate/<bulbName>")
def generate(bulbName):
	#TODO[Done]:initialize and generate prediction model
	model=logit(C=1)
	data=datasetRead()
	target=None
	features=None
	modelFile=None
	"""	
	global minEntryCount
	
	if(minEntryCount>0):
		return "Generate error: need "+str(minEntryCount)+" more action(s)."
	"""	
	if bulbName=="b1":
		#TODO[Done]:generate and store model1.pkl
		target=data['b1'].values
		features=data[['b2','b3']].values
		modelFile=b1ModelFile
		
	elif bulbName=="b2":
		#TODO[Done]:generate and store model2.pkl
		target=data['b2'].values
		features=data[['b1','b3']].values
		modelFile=b2ModelFile
		
	elif bulbName=="b3":
		#TODO[Done]:generate and store model3.pkl
		target=data['b3'].values
		features=data[['b1','b2']].values
		modelFile=b3ModelFile
		
	else:
		return "Generate error: "+bulbName+" is not a bulb."
	
	model.fit(features,target) #generate model
	joblib.dump(model,modelFile,compress=3) #dump model
	
	return "Model generated and dumped."

@pcServer.route("/predict/<bulbName>")
def predict(bulbName):
	#TODO[Done]:prediction logic
	inputFeatures=None
	modelFile=None
	"""
	hourOfPredictionRequest=datetime.datetime.now().hour
	minuteOfPredictionRequest=datetime.datetime.now().minute
	
	global minEntryCount
	global hourOfLastPrediction
	global minuteOfLastPrediction
	
	if((hourOfPredictionRequest-hourOfLastPrediction)==0):
		if((minuteOfPredictionRequest-minuteOfLastPrediction)<=1):
			minEntryCount=DEF_ENTRY_COUNT #reset # of new entries required
			return "Mis-prediction detected."
	"""
	generate(bulbName)
	if bulbName=="b1":
		#TODO[Done]:load and predict from model1.pkl
		inputFeatures=[[bulbs["b2"],bulbs["b3"]]]
		modelFile=b1ModelFile
		
	elif bulbName=="b2":
		#TODO[Done]:load and predict from model2.pkl
		inputFeatures=[[bulbs["b1"],bulbs["b3"]]]
		modelFile=b2ModelFile
		
	elif bulbName=="b3":
		#TODO[Done]:load and predict from model3.pkl
		inputFeatures=[[bulbs["b1"],bulbs["b2"]]]
		modelFile=b3ModelFile
		
	else:
		return "Unavailable"
	
	model=joblib.load(modelFile)
	newState=stateSet[model.predict(inputFeatures)[0]]
	return newState

if __name__=="__main__":
	pcServer.run(host='0.0.0.0',port=80,debug=True)
