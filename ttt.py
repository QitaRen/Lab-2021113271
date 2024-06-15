import networkx as nx
import matplotlib.pyplot as plt
'''
def visualize_paths(G, paths):
	plt.clf()
	# 创建一个新图，用于保存修改后的图
	red_G = nx.DiGraph()
	blue_G = nx.DiGraph()
	nodes=[]
	for path in paths:
		for node in path:
			if not node in nodes:
				nodes.append(node)
	#print(nodes)
    # 遍历原始图的节点和边，将它们添加到两个新图中
	for node in G.nodes():
		if node in nodes:
			red_G.add_node(node)
		else:
			blue_G.add_node(node)
	
	edges=[]
	for path in paths:
		for i,v in enumerate(path):
			if i>=1:
				edge=(path[i-1],path[i])
				if not edge in edges:
					edges.append(edge)
	#print(edges)
	for edge in G.edges():
		if edge in edges:
			red_G.add_edge(edge[0], edge[1],weight=G.get_edge_data(edge[0],edge[1],default=None).get('weight', None))
		else:
			blue_G.add_edge(edge[0], edge[1],weight=G.get_edge_data(edge[0],edge[1],default=None).get('weight', None))
    
    # 绘制红色图
	pos = nx.spring_layout(red_G)
	nx.draw(red_G, pos, node_color='red', edge_color='red', with_labels=True)
    
    # 绘制蓝色图
	pos = nx.spring_layout(blue_G)
	nx.draw(blue_G, pos, node_color='blue', edge_color='blue', with_labels=True)
    # 保存图表
	plt.savefig('afterPath.png')
    
    # 显示图表（可选）
	#plt.show()
'''
def visualize_paths(G, paths):
	plt.clf()
	# 创建一个新图，用于保存修改后的图
	nodes=[]
	for path in paths:
		for node in path:
			if not node in nodes:
				nodes.append(node)
	edges=[]
	for path in paths:
		for i,v in enumerate(path):
			if i>=1:
				edge=(path[i-1],path[i])
				if not edge in edges:
					edges.append(edge)
	edge_labels = nx.get_edge_attributes(G, 'weight')

	# 绘制有向图
	pos = nx.circular_layout(G)  # 节点布局
	nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1400, font_size=10, font_weight='bold', arrowstyle='->', arrowsize=20)

	# 添加边的权值标签
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')

	# 设置坐标轴比例相同
	plt.axis('equal')

	nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_color='red',node_size=1400)
	nx.draw_networkx_edges(G,pos,edgelist=edges,edge_color='red')
	plt.savefig('afterPath.png')
	
