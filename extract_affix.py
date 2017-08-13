#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

data = '''
<page>
    <title>elephant</title>
    <ns>0</ns>
    <id>75</id>
    <revision>
      <id>42456378</id>
      <parentid>42372982</parentid>
      <timestamp>2017-03-18T22:34:54Z</timestamp>
      <contributor>
        <ip>85.26.232.157</ip>
      </contributor>
      <comment>t+lez:[[фил]] ([[WT:EDIT|Assisted]])</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{also|Elephant|éléphant|êléphant}}
==English==

===Etymology===
From {{inh|en|enm|elefant}}, {{m|enm|elefaunt}}, from {{etyl|fro|en}} {{m|fro|elefant}}, {{m|fro|elefan}}, {{m|fro|olifant}}, re-latinized in {{
etyl|frm|en}} as {{m|frm|elephant}}, from {{etyl|la|en}} {{m|la|elephantus}}, from {{etyl|grc|en}} {{m|grc|ἐλέφᾱς}} (gen. {{m|grc|ἐλέφαντος}}). 
Believed to be derived from an Afro-Asiatic form such as {{etyl|ber-pro|en}} {{m|ber-pro|*eḷu||elephant}} (compare Tamahaq (Tahaggart) {{m|thv|ê
lu}}, (Ghat) {{m|taq|alu}}) or {{etyl|egy|en}} {{m|egy|𓍋𓃀𓅱𓌟|tr=ȝbw|sc=Egyp}} (''ābu'') ‘elephant; ivory’. More at [[ivory]]. Replaced Middle Eng
lish {{m|enm|olifant}}, which replaced Old English {{m|ang|elpend|t=elephant}}.

===Pronunciation===
* {{IPA|/ˈɛləfənt/|/ˈɛlɪfənt/|lang=en}}
* {{audio|En-us-elephant.ogg|Audio (US)|lang=en}}

===Noun===
{{en-noun}}
[[Image:Elephant near ndutu.jpg|thumb|an elephant]]

# A [[mammal]] of the order ''[[Proboscidea]]'', having a [[trunk]], and two large [[ivory]] [[tusks]] jutting from the upper [[jaw]].
# {{lb|en|figuratively}} Anything [[huge]] and [[ponderous]].
:
==Middle French==

===Noun===
{{frm-noun|m|elephans}}

# {{l|en|elephant}} {{gloss|animal}}

====Descendants====
* French: {{l|fr|éléphant}}

[[Category:frm:Animals]]

</text>
      <sha1>pg3rjzudhjdacuqu1u6gwzrtm84k4qn</sha1>
    </revision>
  </page>

suffix.en:
abolitionize {{suffix|abolition|ize|lang=en}}
abominably {{suffix|abominable|ly|lang=en}}
aboriginality {{suffix|aboriginal|ity|lang=en}}
aboriginally {{suffix|aboriginal|ly|lang=en}}
abortional {{suffix|abortion|al|lang=en}}
abortively {{suffix|abortive|ly|lang=en}}
abortiveness {{suffix|abortive|ness|lang=en}}
abradant {{suffix|abrade|ant|lang=en}}
abrasive {{suffix|abrase|ive|lang=en}}
abrogative {{suffix|abrogate|ive|lang=en}}
abrogator {{suffix|abrogate|or|lang=en}}
abruptly {{suffix|abrupt|ly|lang=en}}
abruptness {{suffix|abrupt|ness|lang=en}}

prefixes:
From {{prefix|grand|child|lang=en}}
From {{prefix|grand|son|lang=en}}
From {{prefix|grand|daughter|lang=en}}
{{prefix|fore|finger|lang=en}}
{{prefix|up|bar|lang=en}}
From {{suffix|half-year|ly|lang=en}}; or {{prefix|half|yearly|lang=en}}.
From {{prefix|up|date|lang=en}}.
{{prefix|en|un|variable}}
{{prefix|up|blow|lang=en}}
{{prefix|un|utterable|lang=en}}
{{prefix|en|un|veracity}}

===Etymology===
From {{prefix|un|known|lang=en}}, past participle of ''[[know]]''. Compare Old English {{m|ang|ungecnawen}}.


Entry Structure:
Page --> Language --> Etymology --> POS 1 --> Definitions
				--> POS 2 --> Definitions

'''

import codecs
import re
defin, etym={}, {} ## definitions and etymological entries

def extract_data(data):
	print 'Loading the xml wiktionary dump..'
	try:
		xml = BeautifulSoup(data, 'xml')
	except:
		sys.exit(2)
	print "Done!"

	start, read = False, False
	pages = xml.findAll('page')

	remove_extra_info = True
	print "Starting to process the data..."
	for page in pages:
		title = page.title.text.strip()
		text = page.text
		key = ''
		start, read, read_etym = False, False, False
		for line in text.split('\n'):
			if '==English==' in line:
				start = True
				continue
			elif re.match(r'^==[A-Za-z ]+==$', line): ## NOT ENGLISH
				start, read=False, False
				continue
			elif read_etym:
				if title not in etym:
					etym[title] = []
				etym[title].append(line.strip())
				read_etym = False
			if start and not read:
				if re.findall(r'===Etymology( \d+)?===', line): ## ====Etymology==== or ===Etymology 1====
					read_etym = True

				elif re.findall(r'===(Noun|Verb|Adjective|Adverb)',line): ## POS entry with definitions
					POS_parts = re.search(r'===((Noun|Verb|Adjective|Adverb)( \d+)?)',line).groups()
					POS = POS_parts[1] ## POS
					if POS_parts[2]: ## senses: NOUN 1, Verb 2, etc.
						POS +=' '+POS_parts[2]
					key = ' ||| '.join([title,POS])
					defin[key] = []
					read = True
				continue
			if read:
				if line.startswith('# '): ## Sense Definition
					if remove_extra_info: # remove auxiliary info
						line = re.sub(r'(?:\{\{[^\}]*\}\}|<ref.*?(?:/>|</ref>))','', line)
					if re.findall(r'[A-Za-z]{2,}', line):
						defin[key].append(line)
				elif ((line.startswith('==') or line.startswith('[[')) and len(defin[key])>0): ## read till the definitions section ends
					read = False

def save_to_file(add_base_form,output):
	print "Size of etymological dict:", len(etym)
	writer = codecs.open(output,'w', 'utf-8')
	lexicon={}
	## Now we filter to particular types of morphology. In etym all possible etymological information (compounds, derivations, borrowings) is stored
	bases = []
	for key,value in etym.iteritems():
		for val in value: ##FIX ME TO MULTIPLE VALUES
			match = re.search(r'^(?:From *)?(\{\{(suffix|prefix)\|[a-z-]+\|[a-z-]+\|lang=en\}\})' ,val) # {{prefix|un|vessel|lang=en}}
	       		if match<>None:
				pattern = match.group(1)
				affix = match.group(2)
		        	toks = pattern.split('|')
				if add_base_form:
					bases.append(toks[1] if (affix=='suffix') else toks[2])
		        	lexicon[key] = '+'.join(toks[1:3])+' ||| '+affix
	## BETTER TO MERGE WITH THE UPPER PART
	for key,value in defin.iteritems():
		if len(value)>0:
			title = re.split(r' \|\|\| ', key)[0].strip()
			if title in lexicon.keys():
				writer.write('\n'+key + ' ||| '+ lexicon[title]+' ||| ')
				writer.write(" ".join(value))
			elif title in bases and add_base_form:# [val.split('+')[0] for val in lexicon.values()]:
				writer.write('\n'+key +' ||| None' +' ||| '+ 'BASE' + ' ||| ')
				writer.write(" ".join(value))
			else:
				continue

import sys, getopt

def main(argv):
	infile, outfile ='',''
	base = False
	try:
		opts, args = getopt.getopt(argv,"i:bo:",["input=","base=", "output="])
	except getopt.GetoptError:
		print 'extract_affix.py -i <wiktionary dump> -b <base forms> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--input"):
			infile=arg
		elif opt in ("-b", "--base"):
			base=True
		elif opt in ("-o","--output"):
			outfile=arg

	data=codecs.open(infile,'r','utf-8') #('enwiktionary-20170401-pages-meta-current.xml','r', 'utf-8')
	extract_data(data)
	save_to_file(base, outfile)

if __name__ == "__main__":
	main(sys.argv[1:])


'''
FIX TO ALLOW MULTIPLE ETYMOLOGY CASE:

===Etymology 1===
From {{etyl|la|en}} {{m|la|abscissa}}, feminine of {{m|la|abscissus}}, perfect passive participle of {{m|la|abscindō||cut asunder}}.

====Pronunciation====
* {{a|RP}} {{IPA|/ˈæb.sɪs/|lang=en}}
* {{a|US}} {{IPA|/ˈæb.sɪs/|lang=en}}

====Noun====
{{en-noun|es}}

# {{alternative form of|abscissa|lang=en}}{{defdate|First attested in the late 17&lt;sup&gt;th&lt;/sup&gt; century.}}&lt;ref name=SOED&gt;{{R:SOED5|page=8}}&lt;/ref&gt;

===Etymology 2===
{{back-form|abscission|lang=en}}

====Pronunciation====
* {{a|RP}} {{IPA|/əbˈsɪs/|lang=en}}
* {{a|US}} {{IPA|/æbˈsɪs/|lang=en}}
{{rfap|UK|UK|lang=en}}

====Verb====
{{en-verb|es}}
'''
