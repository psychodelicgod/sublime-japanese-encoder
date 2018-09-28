import sublime, sublime_plugin, sys
import re
import urllib.request
import json

from .romkan import *
 


baseUrl = "https://jisho.org/api/v1/search/words?keyword=";


sampleKanjiDict = {
	'kan': [{ 'value': '漢', 'meaning': 'chinese'}, {'value': '韓', 'meaning': 'morning, Korea'}], 
	'ji': [{'value': '字', 'meaning': 'character'}]
}


def getKanjiInfo


def isRomaji(char):
	return bool(re.match(r"[a-zA-Z]", char))

def getLastRomajiChunk(str):
	i = 0
	for char in reversed(str):
		if not isRomaji(char):
			return str[len(str)-i:len(str)] 
		i = i + 1
	return str



# class HiraganaCommand(sublime_plugin.TextCommand):
# 	def run(self, args):
# 		view = self.view;
# 		region = sublime.Region(0, view.size())
# 		s = view.substr(region)
# 		view.replace(args, region, romkan.to_hiragana(s))


# class KatakanaCommand(sublime_plugin.TextCommand):
# 	def run(self, args):
# 		view = self.view;
# 		for region in view.sel():
# 			if not region.empty():
# 				s = view.substr(region) 
# 				view.replace(args, region, romkan.to_katakana(romkan.to_roma(s)))



class replaceCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args):
		replacedRegion = sublime.Region(self.view.size()-args['replaceCharsCount'], self.view.size())
		self.view.replace(edit, replacedRegion, args['replacementKanji'])




class convertCommand(sublime_plugin.WindowCommand) :

	availableKanji = []
	replacedString = ""
	view = None
	
	def run(self):
		self.view = self.window.active_view()
		contents = self.view.substr(sublime.Region(0, self.view.size()))
		last4 = contents[len(contents)-4:len(contents)]
		self.replacedString = getLastRomajiChunk(last4)
		if len(self.replacedString) > 0:
			self.availableKanji = sampleKanjiDict[self.replacedString]
			print(self.availableKanji)
			kanjiList = list(map(lambda x: x['value'] + ': ' + x['meaning'], self.availableKanji))
			self.window.show_quick_panel(kanjiList, self.on_done)

	def on_done(self, selectedItemIndex):
		print(self.availableKanji[selectedItemIndex])
		replacementKanji = self.availableKanji[selectedItemIndex]['value']
		self.window.run_command('replace', { 'replaceCharsCount': len(self.replacedString), 'replacementKanji': replacementKanji})



# res = urllib.request.urlopen("https://jisho.org/api/v1/search/words?keyword=kan").read();

# str = res.decode('utf-8')

# j = json.loads(str) 

# print(j['data'][0]['japanese'])
# print(j['data'][0]['senses'])