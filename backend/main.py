from flask import Flask
from flask import request
from flask_cors import CORS
from py2neo import Graph, Node, Relationship, NodeMatcher
import nltk
from rake_nltk import Rake
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wn
import requests
import re
app = Flask(__name__)

CORS(app, supports_credentials=True)

graph = Graph("http://localhost:7474", auth=("neo4j", "blcusti"))

r = Rake()
matcher = NodeMatcher(graph)

stopwords = "'-\\,.`~"

snowball_stemmer = SnowballStemmer("english")

def get_raw(s):
    s = s.replace("'", "\\'")
    return s

@app.route('/')
def hello_world():
    return 'Hello World'

# 添加文档
@app.route('/add')
def add_document():
    # 获取标题和文本
    text = request.args.get('text')
    text = text.replace(".", ". ")
    print(text)
    title = request.args.get('title')
    # 创建Document节点
    document_node = Node("Document", title=title, text=text)
    # 分句、创建句段节点，并与文档节点关联
    segments = nltk.sent_tokenize(text)
    for segment in segments:
        # 创建Segment节点
        segment_node = Node("Segment", text=segment)
        text_to_segment = Relationship(document_node, "hasSegments", segment_node)
        graph.create(text_to_segment)
    # 创建Keyword节点
    r.extract_keywords_from_sentences(segments)
    extracted_keywords = r.get_ranked_phrases_with_scores()
    for item in extracted_keywords:
        if item[0] <= 2:
            continue
        keyword_node = Node("Keyword", text=item[1])
        for segment in segments:
            if item[1] in segment:
                segment_node = matcher.match("Segment", text=segment).first()
                segment_to_keyword = Relationship(segment_node, "includeKeywords", keyword_node)
                document_to_keyword = Relationship(document_node, "hasKeywords", keyword_node)
                graph.create(segment_to_keyword)
                graph.create(document_to_keyword)
    title_words = nltk.word_tokenize(title)
    tagged_title = nltk.pos_tag(title_words)
    shortname = title.split(' ')[0]
    for item in tagged_title:
        if list(item)[1] == 'NN':
            shortname = list(item)[0]
            break
    return { 'shortname': shortname }

# 获取文本分句
@app.route('/getsegments')
def get_segment():
	return_dict = {}
	id = 1
	title = request.args.get('title')
	match_relation = graph.run('match (:Document{title:\''+get_raw(title)+'\'})-[:hasSegments]->(s:Segment) return s.text')
	for item in match_relation.data():
		return_dict[id] = item['s.text']
		id = id + 1
	return return_dict

# 获取文档列表
@app.route('/getfilelist')
def get_filelist():
	filelist = {}
	shortname = {}
	flag = 1
	id = 1
	match_document = graph.run('match (d:Document) return d.title')
	for item in match_document.data():
		filelist[id] = item['d.title']
		words = nltk.word_tokenize(filelist[id])
		tagged_words = nltk.pos_tag(words)
		for item in tagged_words:
			if list(item)[1] == 'NN':
				shortname[id] = list(item)[0]
				flag = 0
				break
		if flag:
			shortname[id] = filelist[id].split(' ')[0]
		id = id + 1

	return { 'filelist': filelist, 'shortname': shortname }

# 获取关键词知识网络所需数据
@app.route('/getkeywordgraph')
def get_keyword_graph():
    title = request.args.get('title')
    segment_list = []
    keyword_list = []
    links = {}
    nodes = {}
    text = ""
    link_id = 1
    node_id = 1
    match_document = graph.run('match (d:Document{title:\''+ get_raw(title) +'\'}) return d.text')
    text = match_document.data()
    print()
    match_segments = graph.run('match (:Document{title:\''+ get_raw(title) +'\'})-[:hasSegments]->(s:Segment) return s.text')
    match_keywords = graph.run('match (:Document{title:\''+ get_raw(title) +'\'})-[:hasKeywords]->(k:Keyword) return k.text')
    segment_list = match_segments.data()
    keyword_node_list = match_keywords.data()
    for segment in segment_list:
        segment_text = segment['s.text']
        match_key_word = graph.run("match (:Segment{text:\'"+ get_raw(segment_text) +"\'})-[:includeKeywords]->(k:Keyword) return k.text")
        keyword_list = match_key_word.data()
        temp_dict = { 'id': segment_text, 'group': 2 }
        nodes[node_id] = temp_dict
        node_id = node_id + 1
        for keyword in keyword_list:
            keyword_text = keyword['k.text']
            temp_dict = { 'source': segment_text, 'target': keyword_text, 'value': 5}
            links[link_id] = temp_dict
            link_id = link_id + 1
    for keyword in keyword_node_list:
        keyword_text = keyword['k.text']
        print(keyword_text)
        temp_dict = { 'id': keyword_text, 'group': 1 }
        nodes[node_id] = temp_dict
        node_id = node_id + 1
    return { 'nodes': nodes, 'links': links, 'text': text }

# 获取文档结点图
@app.route('/getdocgraph')
def get_doc_graph():
    nodes = {}
    temp_dict = {}
    node_id = 0
    shortname = ""
    word_count = 0
    segmentnum = 0
    keywordnum = 0
    match_document = graph.run('match (d:Document) return d.title')
    for doc in match_document:
        doc_title = doc['d.title']
        match_segments = graph.run('match (:Document{title:\''+ get_raw(doc_title) +'\'})-[:hasSegments]->(s:Segment) return s.text')
        match_keyword = graph.run('match (:Document{title:\''+ get_raw(doc_title) +'\'})-[:hasKeywords]->(k:Keyword) return k.text')
        for segment in match_segments:
            segment_text = segment['s.text']
            word_count += len(segment_text.split(' '))
        title_words = nltk.word_tokenize(doc_title)
        tagged_title = nltk.pos_tag(title_words)
        shortname = doc_title.split(' ')[0]
        for item in tagged_title:
            if list(item)[1] == 'NN':
                shortname = list(item)[0]
                break
        for item in match_segments:
            segmentnum += 1
            print(item['s.text'])
        for item in match_keyword:
            keywordnum += 1
        temp_dict = { 'id': shortname, 'group': 1, 'title': doc_title, 'wordcount': word_count, 'segnum': segmentnum, 'wordnum': keywordnum }
        nodes[node_id] = temp_dict
        node_id = node_id + 1
    return { 'nodes': nodes }

# 获取知识网络图
@app.route('/getknowledgenet')
def get_knowledge_net():
    title = request.args.get('title')
    nodes = {}
    links = {}
    keyword_set = set()
    segment_set = set()
    concept_set = set()
    node_id = 0
    link_id = 0
    match_segments = graph.run('match (:Document{title:\''+ get_raw(title) +'\'})-[:hasSegments]->(s:Segment) return s.text')
    for segment in match_segments:
        segment_text = segment['s.text']
        nodes[node_id] = { 'id': segment_text, 'group': 2 }
        node_id = node_id + 1
        match_keywords = graph.run('match (:Segment{text:\''+ get_raw(segment_text) +'\'})-[:includeKeywords]->(k:Keyword) return k.text')
        segment_set = set()
        # 遍历关键词构建知识网络
        for keyword in match_keywords:
            keyword_text = keyword['k.text']
            # 从长关键词中提取名词
            keyword_list = nltk.word_tokenize(keyword_text)
            keyword_tagged_list = nltk.pos_tag(keyword_list)
            for keyword_list_item in keyword_tagged_list:
                if list(keyword_list_item)[1] == 'NN' and list(keyword_list_item)[0] not in segment_set and list(keyword_list_item)[1] not in stopwords:
                    if list(keyword_list_item)[0] not in keyword_set:
                        # 关键词结点只记录一次
                        keyword_set.add(list(keyword_list_item)[0])
                        nodes[node_id] = { 'id': list(keyword_list_item)[0], 'group': 3 }
                        node_id = node_id + 1
                    segment_set.add(list(keyword_list_item)[0])
                    links[link_id] = { 'source': segment_text, 'target': list(keyword_list_item)[0], 'value': 5 }
                    link_id = link_id + 1
    # 通过wordnet寻找上下位关系
    # for keyword in keyword_set:
    #     for item in wn.synsets(keyword, pos=wn.NOUN):
    #         for hypernym in item.hypernyms():
    #             for segment in match_segments:
    #                 segment_text = segment['s.text']
    #                 segment_word_stem_list = [snowball_stemmer.stem(stemmed_word) for stemmed_word in nltk.word_tokenize(segment_text)]
    #                 # print(segment_word_stem_list)
    #                 if hypernym.name().split('.')[0] in segment_word_stem_list:
    #                     print(hypernym)
    # 通过conceptnet获取更多知识
    raw_url = 'http://api.conceptnet.io/c/en/'
    for keyword in keyword_set:
        uri = keyword
        obj = requests.get(raw_url + uri).json()
        preserve = ['default', 'en', 'zh']
        for item in obj['edges']:
            start = end = 'default'
            if 'language' in item['start']:
                start = item['start']['language']
            if 'language' in item['end']:
                end = item['end']['language']
            if start not in preserve or end not in preserve:
                continue
            if item['start']['label'] == keyword and item['rel']['label'] == 'IsA':
                print(item['start']['label'] + ' ' + item['rel']['label'] + ' ' + item['end']['label'])
                if item['end']['label'] not in concept_set and item['end']['label'] not in keyword_set:
                    concept_set.add(item['end']['label'])
                    nodes[node_id] = { 'id': item['end']['label'], 'group': 0 }
                    node_id = node_id + 1
                    links[link_id] = { 'source': keyword, 'target': item['end']['label'], 'value': 3 }
                    link_id = link_id + 1
    return { 'nodes': nodes, 'links': links }

@app.route('/getwordwindow')
def get_word_window():
    window_list = {}
    window_id = 0
    text = ""
    title = request.args.get('title')
    match_document = graph.run('match (d:Document{title:\''+ get_raw(title) +'\'}) return d.text')
    for doc in match_document:
        text = doc['d.text']
    match_keyword = graph.run('match (:Document{title:\''+ get_raw(title) +'\'})-[:hasKeywords]->(k:Keyword) return k.text')
    for keyword in match_keyword:
        keyword_text = keyword['k.text']
        patt = "(.{15})(" + keyword_text + ")(.{15})"
        pattern = re.compile(patt)
        result = pattern.findall(text)
        for item in result:
            window_list[window_id] = { 'former': list(item)[0], 'keyword': list(item)[1], 'latter': list(item)[2] }
            window_id += 1
    return { 'winlist': window_list }
