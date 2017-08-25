import sublime, sublime_plugin, sys

import romkan.common as romkan




sampleKanjiDict = {
	'kan': ['漢', '韓'], 
	'ji': ['字']
}




class HiraganaCommand(sublime_plugin.TextCommand):
	def run(self, args):
		view = self.view;
		region = sublime.Region(0, view.size())
		s = view.substr(region)
		view.replace(args, region, romkan.to_hiragana(s))


class KatakanaCommand(sublime_plugin.TextCommand):
	def run(self, args):
		view = self.view;
		for region in view.sel():
			if not region.empty():
				s = view.substr(region)
				view.replace(args, region, romkan.to_katakana(romkan.to_roma(s)))


class KanjiCommand(sublime_plugin.TextCommand):
	def run(self, args):
		view = self.view;
		for region in view.sel():
			if not region.empty():
				s = view.substr(region)
				view.replace(args, region, sampleKanjiDict['kan'][0])


      
class PromptkanjiCommand(sublime_plugin.WindowCommand):


	def run(self):
		view = self.window.active_view()
		region = view.sel()[0];
		s = view.substr(region)
		availableKanji = sampleKanjiDict[s]
		self.window.show_quick_panel(availableKanji, self.on_done)

	def on_done(self, selectedItemIndex):
		view = self.window.active_view()
		region = view.sel()[0]
		s = view.substr(region)
		availableKanji = sampleKanjiDict[s]
		kanji = availableKanji[selectedItemIndex]
		self.window.run_command('kanji')