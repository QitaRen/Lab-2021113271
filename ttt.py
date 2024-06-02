import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
#last version
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
	plt.figure(figsize=(20,20))
	# 绘制有向图
	pos = nx.circular_layout(G)

	# 定义距离阈值
	threshold = 0.01  # 调整这个值来控制节点之间的最小距离

	# 定义扰动幅度
	perturbation_scale = 0.45  # 调整这个值来控制扰动幅度

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
	nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')

	# 设置坐标轴比例相同
	plt.axis('equal')

	nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_color='red',node_size=1400)
	nx.draw_networkx_edges(G,pos,edgelist=edges,edge_color='red')
	plt.savefig('afterPath.png')
	#plt.show()
	
