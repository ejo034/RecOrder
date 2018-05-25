from v2.scripts import QueryRunner
from v2.scripts.RecSys import ItemBased, KnowledgeBased

class RecEngine():
	def __init__(self, typeName):
		self.typeName = typeName


def selectRecommendationEngine(profile, useItemBased, writer):

	engine = None

	userIdList = QueryRunner.getAllUserProfileIds()
	if userIdList is None:
		useItemBased = False


	writer.PrintAndWrite("user list: " + str(userIdList))

	#need to check if the user has enough items in his profile to create a valid recomendation

	if useItemBased is True and profile in userIdList:
		#get content based
		writer.PrintAndWrite("ITEM BASED", False)
		engine = _getItemBasedEngine(writer)

	else:
		#get knowledge based
		writer.PrintAndWrite("KNOWLEDGE BASED", False)
		engine = _getKnowledgeBasedEngine()

	print()
	return engine


def _getItemBasedEngine(writer):
	recommenderEngine = ItemBased.ItemBased(writer)
	return recommenderEngine


def _getKnowledgeBasedEngine():
	recommenderEngine = KnowledgeBased.KnowledgeBased()
	return recommenderEngine
