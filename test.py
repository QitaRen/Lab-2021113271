import hello
import ttt
import networkx as nx
import matplotlib.pyplot as plt

with open('test.txt') as file_object:
	lines=file_object.readlines()
strings=''
for line in lines:
	strings+=line.rstrip()
wordlist=['']
hello.strings2word(strings,wordlist)
G=nx.DiGraph()	

print('功能列表：')
print(' -1、创建有向图并可视化输出')
print(' -2、桥接词查询')
print(' -3、根据桥接词创建新文本')
print(' -4、最短路径查询')
print(' -5、随机游走')
while True:

	choice=input('\n输入数字选择对应功能，输入q退出\n')
	if choice=='q':
		break
	elif choice=='1':
		hello.creatPIC(wordlist,G)
		hello.showDirectedGraph(G)
		print('有向图生成完成，可视化输出保存在 directing_graph.png 中')
	elif choice=='2':
		word1, word2 = input("Enter two words: ").split()
		print(hello.queryBridgeWords(G,word1,word2))
	elif choice=='3':
		inputText=input('请输入待扩展文本：\n')
		#generateNewText(inputText, G)
		print(hello.generateNewText(inputText, G))
	elif choice=='4':
		words = input("Enter one or two words: ")
		wordsshell=['']
		
		hello.strings2word(words,wordsshell)
		if(len(wordsshell)==2):
			word1=wordsshell[0]
			word2=wordsshell[1]
			paths = hello.shortestPATH(G, word1, word2)
			#print(paths)
		
			if paths:
				print('The shortest path from {} to {} is:'.format(word1,word2))
				for path in paths:
					len_weight=path.pop()
					#print(path)
					print(' -'+"{}".format(" -> ".join(path)))
				print('总步长为 '+str(len_weight))
				ttt.visualize_paths(G,paths)
			else:
				print('这两个节点不可达')
		if(len(wordsshell)==1):
			hello.allShortPath(G,wordsshell[0])
		
	elif choice=='5':
		hello.randomWalk(G)
	else:
		print('请输入数字1-5，或字母q')
		
		
		
		
		
	
