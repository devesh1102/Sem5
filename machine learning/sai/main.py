import matplotlib
import sklearn
import numpy as np
import csv
import pandas as pd
import anytree
from anytree import NodeMixin, RenderTree

def split(dataset, min_leaf_size, loss_fn):
	attribute_labels = range(1,len(dataset.columns+1)
	#'row' is the number of rows in the matrix
	row = len(dataset.index)
	#'column' is the number of columns in the matrix
	column = len(dataset.columns)
	column_no = 0
	l = 0
	min_var = 9999 # initializing it to a large value
	row_no = 0
	min_col_var =9999# # initializing it to a large value
	row_found = 0
	 = None
	loss = None
	if row >= 2*min_leaf_size:
		for i in  range(0,len(dataset.columns)-1):
		# Iterating over the columns of the dataset
			dataset = dataset.sort_values(by=[attribute_labels[i])
			# Sorting the dataset based upon the values that are present
			# under the i-th column label
			for j in range(min_leaf_size,row - min_leaf_size+1):
			# Iterating over the row elements - jth row element is
			# considered as the value we are using for splitting
				A = dataset.iloc[:j,:]
				# spliting at the j-th value of the sorted dataset
				B = dataset.iloc[j:,:]
				if loss_fn == 'mean_squared':
					loss_A = A.loc[:,attribute_names[column-1]].var()
					#finds varience of the last column i.e of the y-values
					loss_B = B.loc[:,attribute_names[column-1]].var()
					#finds varience of the last column i.e of the y-values
				elif loss_fn == 'absolute':
					loss_A = A.loc[:,attribute_names[column-1]].mad()
					#finds mean absolute deviation of the y-values
					loss_A = A.loc[:,attribute_names[column-1]].mad()
					#finds mean absolute deviation of the y-values
				else:
					print("\nOnly Mean Absolute and Mean Squared Losses are
							implemented\n")

				var_net = (j*var_A + (row-j)*var_B)/row 
				#weighted mean of the two variences
				if var_net < min_col_var:
					min_col_var = var_net
					row_found = j 
					#storing the value of row for which min varience 
					#occurs for ith attribute
					A_dum = A
					B_dum = B
        

			if min_col_var < min_var: 
				min_var = min_col_var
				row_no = row_found
				column_no = l
				out_1 = A_dum
				out_2 = B_dum
			l=l+1
			min_col_var =9999
		#print(out_1)
		#print(out_2) 
		value = out_2.iloc[0][attributes[column_no]]
		return(out_1,out_2,attributes[column_no],value)
	else:	
		return(None,None,-1,None)

MyBaseClass(object):
	foo = 4
class MyClass(MyBaseClass, NodeMixin):  # Add Node feature
	def __init__(self, name, attribute, value,data, rchild,lchild,parent=None):
		super(MyClass, self).__init__()
		self.name = name
		self.attribute = attribute
		self.value = value
		self.data = data
		self.rchild = None
		self.lchild = None
		self.parent = parent

def dTree(Data,node,count):
	"""This builds the Descision trees from the given Dataset"""
	(splitData1, splitData2, attribute, value) = split(Data)
	count = count + 1
	node.name = count;
	if attribute != -1:
		node.attribute = attribute
		node.value = value
		my_1 = MyClass(count+1, -1, -1,splitData1, None, None, parent=node)
		my_2 = MyClass(count+2, -1, -1,splitData2, None,None, parent=node)
		node.rchild = my_2
		node.lchild = my_1

		dTree(splitData2,my_2,count)
		count = count + 1
		dTree(splitData1,my_1,count)
	
	return 
def result(node,test):
	if node.value == -1:
		#print(node.name)
		#print(len(node.data.index))
		return  node.data.iloc[:,-1].mean()

	if node.value != -1:
		#print(test)
		if test.loc[node.attribute] < node.value:
			return result(node.lchild,test)
		else:
			return result(node.rchild,test)
	return
	
def prune(leaf):
	parent = leaf.parent
	parent_var = parent.data[:,parent.attribute].var()
	leaf_var = leaf.data[:,leaf.attribute].var()
	brother_leaf = leaf.parent.lchild
	if brother_leaf == leaf:
		brother_leaf = leaf.parent.rchild
	leaf_var2 = brother_leaf.data[:,brother_leaf.attribute].var()
	w1 = len(leaf.data.rows)
	w2 = len(brother_leaf.data.rows)
	if (parent_var < (w1*leaf_var + w2*leaf_var2)/(w1+w2)):
		parent.lchild = None
		parent.rchild = None
		prune(parent)
	else:
		return

def pruneTree(head):
	"""Prunes the tree using the condition - """
	current_node = head
	while(True):
		if (current_node.lchild != None):
			pruneTree(current_node.lchild)
		if (current_node.rchild != None):
			pruneTree(current_node.rchild)
		if (current_node.lchild == None && current_node.rchild == None):
			prune(current_node)
		return

def main():
	data = pd.read_csv('/Users/deveshkumar/Downloads/ml_assing/data/second/second/train (2).csv')
	#print(data)
	test = pd.read_csv('/Users/deveshkumar/Downloads/ml_assing/data/second/second/test.csv')
	test_row = len(test.index)
	count =0 
	results= pd.DataFrame(np.zeros((test_row, 1)))

	my0 = MyClass('root', -1, -1,data,None,None)
	dTree (data,my0,count)
	for pre, _, node in RenderTree(my0):
		treestr = u"%s%s" % (pre, node.name)
		print(treestr.ljust(8), node.attribute, node.value,node.data.iloc[:,-1].mean())
	#for pre, _, node in RenderTree(my0):
	#	treestr = u"%s%s" % (pre, node.name)
	#	print(node.data)
	l = 0;
	#print(my0.value)
	random =0
	df = pd.DataFrame(columns=[ 'output'])
	# df is the final result matrix
	for  i in range(1,len(test.index)+1):
		df.loc[i] = [result(my0,test.iloc[l])]
		print(result(my0,test.iloc[l]))
		l=l+1

	print(df)
	df.to_csv('out2.csv')#


if __name__ == '__main__':
	main()
