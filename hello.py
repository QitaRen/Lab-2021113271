import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import random
import numpy as np
#最小值函数
def min(a,b):
	return a if a<b else b
	
#输入有向图G，初始词word1，目的词word2，返回值为最短路径列表，如不可达，则返回空列表
def shortestPATH(G, word1, word2):
	paths=[[word1,0]]
	shortest_len=0
	while True:
		for path in paths:
			if path[-2]==word2:
				if shortest_len==0:
					shortest_len=path[-1]
				else:
					shortest_len=min(shortest_len,path[-1])
		if shortest_len:
			#print(shortest_len)
			paths_emp=[]
			for i,path in enumerate(paths):
				
				if path[-2]==word2 and path[-1]==shortest_len:
					paths_emp.append(path)
					#print(paths)
			return paths_emp
		paths_copy=[]
		for path in paths:
			if list(G.successors(path[-2])):
				weight=path.pop(-1)
				for next_node in list(G.successors(path[-1])):
					weight_temp=weight+G.get_edge_data(path[-1],next_node,default=None).get('weight', None)
					paths_copy.append(path+[next_node]+[weight_temp])
		if not paths_copy:
			return paths_copy
		else:
			paths=paths_copy
		#print(paths)
				
def allShortPath(G,word1):
	for word2 in G.nodes():
		if word2 != word1:
			paths=shortestPATH(G, word1, word2)
			if not paths:
				code='there is no path form '+'"'+word1+'"'+' to '+'"'+word2+'"\n'
				print(code)
			else:
				print('the shorest path from {} to {} is:'.format(word1,word2))
				for path in paths:
					len_weight=path.pop()
					print(' -'+"{}".format(" -> ".join(path)))
				print('总步长为： {}\n'.format(str(len_weight)))
							
				
#将输入字符串切片			
def strings2word(strings,wordlist):
	i=0
	temp=0
	for letter in strings:
		if letter.isalpha():
			if temp==1:
				wordlist.append('')
			wordlist[i]+=letter.lower()
			temp=0
		elif temp==0:
			i+=1
			#wordlist.append('')
			temp=1
			
#根据字符串列表构建有向图		
def creatPIC(wordlist,G):
	dic=Counter(wordlist)
	for v in dic:
		G.add_node(v)
	edgeslist=[]
	for i,v in enumerate(wordlist):
		if i>=1:
			edge=wordlist[i-1]+' '+v
			edgeslist.append(edge)
	#print(edgeslist)
	edge_num=Counter(edgeslist)
	#print(edge_num)
	#print(edge_num)
	for k,v in edge_num.items():
		edge_div_list=['']
		
		strings2word(k,edge_div_list)
		#print(k)
		
		G.add_edge(edge_div_list[0],edge_div_list[1],weight=v)
		
		
#打印有向图G，打印结果保存在directing_graph.png中
def showDirectedGraph(G):
	plt.clf()
	edge_labels = nx.get_edge_attributes(G, 'weight')
	plt.figure(figsize=(20,20))
	# 绘制有向图
	pos = nx.circular_layout(G)

	# 定义距离阈值
	threshold = 0.01  # 调整这个值来控制节点之间的最小距离

	# 定义扰动幅度
	perturbation_scale = 0.55  # 调整这个值来控制扰动幅度

	# 检查节点之间的距离，并给它们添加扰动
	moved = True
	while moved:
		moved = False
		for i in pos:
			for j in pos:
				if i != j:
					# 计算两点之间的距离
					distance = np.linalg.norm(np.array(pos[i]) - np.array(pos[j]))
					if distance < threshold:
						# 如果距离小于阈值，给节点 j 添加扰动
						pos[j] += np.random.normal(0, perturbation_scale, size=len(pos[i]))
						moved = True
	nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1400, font_size=10, font_weight='bold', arrowstyle='->', arrowsize=20)

	# 添加边的权值标签
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

	# 设置坐标轴比例相同
	plt.axis('equal')
	#plt.show()
	# 显示图形
	plt.savefig("directing_graph.png")
	#plt.show()

#桥介词查询函数1，应用于main
def queryBridgeWords(G,word1,word2):
# 检查单词是否在图中
	word1=word1.lower()
	word2=word2.lower()
	if word1 not in G and word2 in G:
		return "No " + '"'+word1+'"'+ " in the graph!"
	elif word1 in G and word2 not in G:
		return "No " + '"'+word2+'"'+ " in the graph!"
	elif word1 not in G and word2 not in G:
		return "No " +'"'+ word1 +'"'+ " and " +'"'+ word2 +'"'+ " in the graph!"

	bridge_words = []

# 遍历所有节点，检查是否存在桥接词
	for node in G.nodes():
		if word1 in G.predecessors(node) and word2 in G.successors(node):
			bridge_words.append(node)

# 输出结果
	if not bridge_words:
		return "No bridge words from " +'"'+ word1 +'"'+ " to " +'"'+ word2 +'"'+ "!"
	elif len(bridge_words) == 1:
		return "The bridge word from " +'"'+ word1 +'"'+ " to " +'"'+ word2 +'"'+ " is: " + bridge_words[0] + "."
	else:
		return "The bridge words from " +'"'+ word1 +'"'+ " to " +'"'+ word2 +'"'+ " are: " + ", ".join(bridge_words[:-1]) + ", and " + bridge_words[-1] + "."

#桥介词函数2，其返回值为桥介词而非查询结果语句       
def queryBridgeWords_s(G,word1,word2):
    # 检查单词是否在图中
    word1=word1.lower()
    word2=word2.lower()
    if word1 not in G and word2 in G:
        return 0
    elif word1 in G and word2 not in G:
        return 0
    elif word1 not in G and word2 not in G:
        return 0
    
    bridge_words = []
    
    # 遍历所有节点，检查是否存在桥接词
    for node in G.nodes():
        if word1 in G.predecessors(node) and word2 in G.successors(node):
            bridge_words.append(node)
    
    # 输出结果
    if not bridge_words:
        return 0
    elif len(bridge_words) == 1:
        return bridge_words[0]
    else:
        return bridge_words[random.randint(0,len(bridge_words)-1)]	




#根据桥介词生成新文本，返回值为生成的新文本
def generateNewText(inputText, G):
    # 预处理输入文本
    words=['']
    strings2word(inputText,words)
    processed_words = [word.strip(".,!?()[]{}:;\"'<>") for word in words]
    #print(processed_words)
    
    # 遍历单词列表，查询桥接词
    new_words = []
    for i in range(len(processed_words) - 1):
        word1 = processed_words[i]
        word2 = processed_words[i + 1]
        
        # 查询桥接词
        bridge_words = queryBridgeWords_s(G, word1, word2)
        
        # 插入桥接词
        if bridge_words:
            new_words.append(word1)
            new_words.append(bridge_words)
        else:
            new_words.append(word1)
    
    # 添加最后一个单词
    new_words.append(processed_words[-1])
    #print(new_words)
    # 生成新文本
    new_text = ' '.join(new_words)
    return new_text

def randomWalk(G):

	START=1
	while START:
		current_node = random.choice(list(G.nodes()))
		passed_node = [current_node]
		passed_edge = []
		while True:
			nextnode=list(G.successors(current_node))
			if not nextnode:
				break
			next_node=random.choice(nextnode)
			next_edge=(current_node,next_node)
			if next_edge in passed_edge:
				passed_node.append(next_node)
				break
			else:
				passed_node.append(next_node)
				passed_edge.append(next_edge)
			current_node=next_node
		write_to_file(passed_node)
		yesno = input('是否继续?是[Y]否[任意输入]\n')
		if yesno == 'Y':
			print('继续\n')
		else:
			print('中止\n')
			START = 0
def write_to_file(passed_node):
	file_path="randomWalkoutput.txt"
	with open(file_path,'a') as file:
		for node in passed_node:
			file.write(node+' ')
		file.write('\n')
