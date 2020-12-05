import matplotlib
import sklearn
import numpy as np
import csv
import pandas as pd
import argparse
import anytree
from anytree import NodeMixin, RenderTree
count = 0 
final_error = 0
def error(tree):
	if(tree.value == -1):
		global final_error 
		final_error =final_error + tree.error
		return
	else:
		error( tree.rchild)
		error( tree.lchild)
		return

def split(dataset, min_leaf_size, loss_fn):
	#attribute_labels = range(1,len(dataset.columns)+1)
	l=0
	attribute_labels= [None] * len(dataset.columns)
	for column in dataset.columns[0:]:
		attribute_labels[l] = column
		l=l+1
	l=0

	#§print(attribute_labels)
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
	if row >= 2*min_leaf_size:
		#print('sss')
		for i in  range(0,len(dataset.columns)-1):
		# Iterating over the columns of the dataset
			dataset = dataset.sort_values(by=[attribute_labels[i]])			
			# Sorting the dataset based upon the values that are present
			# under the i-th column label
			for j in range(min_leaf_size,row - min_leaf_size+1):
			# Iterating over the row elements - jth row element is
			# considered as the value we are using for splitting
				A = dataset.iloc[:j,:]
				# spliting at the j-th value of the sorted dataset
				B = dataset.iloc[j:,:]
				if loss_fn == 'mean_squared':
					loss_A = A.loc[:,attribute_labels[column-1]].var()
					#finds varience of the last column i.e of the y-values
					loss_B = B.loc[:,attribute_labels[column-1]].var()
					#finds varience of the last column i.e of the y-values
				elif loss_fn == 'absolute':
					loss_A = A.loc[:,attribute_labels[column-1]].mad()
					#print(loss_A)
					#finds mean absolute deviation of the y-values
					loss_B = A.loc[:,attribute_labels[column-1]].mad()
					#finds mean absolute deviation of the y-values
				else:
					print("\nOnly Mean Absolute and Mean Squared Losses areimplemented\n")
 
				var_net = (j*loss_A + (row-j)*loss_B)/row 
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
		value = out_2.iloc[0][attribute_labels[column_no]]
		return(out_1,out_2,attribute_labels[column_no],value)
	else:	
		return(-1,-1,-1,-1)

class MyBaseClass(object):
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
		self.error = 0

def dTree(Data,node,min_leaf_size,loss_fn):
	"""This builds the Descision trees from the given Dataset"""
	(splitData1, splitData2, attribute, value) = split(Data,min_leaf_size,loss_fn)
	global count
	node.name = count;
	if attribute != -1:
		node.attribute = attribute
		node.value = value
		#print(node.value)

		my_1 = MyClass(count, -1, -1,splitData1, None, None, parent=node)
		my_2 = MyClass(count, -1, -1,splitData2, None,None,  parent=node)
		node.rchild = my_2
		node.lchild = my_1
		count = count + 1
		dTree(splitData2,my_2,min_leaf_size,loss_fn)
		count = count + 1
		dTree(splitData1,my_1,min_leaf_size,loss_fn)
	
	return 
def result(node,test):
	if node.value == -1:
		return  node.data.iloc[:,-1].mean()
	if node.value != -1:
		#print(test)
		if test.loc[node.attribute] < node.value:
			return result(node.lchild,test)
		else:
			return result(node.rchild,test)
	return
	
def prune(tree):
	if(tree.rchild.value == -1  ):
		return


	
	#if(parent == None):
	#	return
	print("now")
	lchild_error = tree.lchild.error/len(tree.lchild.data.index)
	rchild_error = tree.rchild.error/len(tree.rchild.data.index)
	tree_error = tree.error/len(tree.data.index)
	if (tree_error<= (lchild_error + rchild_error)):
		tree.lchild = None
		tree.rchild = None
		return
	else:

		prune(tree.lchild)
		prune(tree.rchild)
		return

	#parent_var=parent.data.iloc[:,-1].var()	
	#leaf_var = leaf.data[:,leaf.attribute].var()
	#if(leaf.parent.rchild == None):
	
	#if (parent_error<= (leaf_error + leaf_error2)):
	#	parent.lchild = None
	#	parent.rchild = None
		#if (parent.parent != None):
		#	prune(parent)
		#else:
	  #  return
	#else:
	#	return

def result2 (node,test):

	actual = test.iloc[-1].mean()
	predic_mean = node.data.iloc[:,-1].mean()
	node.error = node.error + abs(actual - predic_mean )
	if node.value == -1:
		#print(node.name)
		#print(len(node.data.index
		return

	if node.value != -1:
		#print(test)
		if test.loc[node.attribute] < node.value:
			#predic_mean = node.data.iloc[:,-1].mean()
			result2(node.lchild,test)
			return
		else:
		#predic_mean = node.data.iloc[:,-1].mean()
			result2(node.rchild,test)
		return
	return
	




def main():
	parser = argparse.ArgumentParser(
			description = 'Parses the arguments	given to the file through CLI')
	parser.add_argument('--train_data', 
			help="path to the train data file")
	parser.add_argument('--test_data', 
			help="path to the test data file")
	parser.add_argument('--min_leaf_size', 
			help="specifies the minimum leaf size with which the tree is to be built")
	parser.add_argument('--absolute', 
	help="specifies the loss function as MAD(Mean Absolute Deviation)", action = 'store_true')
	parser.add_argument('--mean_squared', 
			help="specifies the loss function as MSD(Mean Squared Deviation)", 
			action = 'store_true')
	args = parser.parse_args()
	trainFile = args.train_data
	print(trainFile)
	testFile = args.test_data
	print(testFile)
	min_leaf_size = args.min_leaf_size
	print(min_leaf_size)
	if args.absolute:
		loss_fn = 'absolute'
	elif args.mean_squared:
		loss_fn = 'mean_squared'
	else:
		print("\nLoss Function not specified")
		raise SystemExit



	data = pd.read_csv(trainFile)
	#print(data)
	test = pd.read_csv(testFile)
	test_row = len(test.index)
	results= pd.DataFrame(np.zeros((test_row, 1)))
	print(loss_fn)
	my0 = MyClass('root', -1, -1,data,None,None)

	dTree (data,my0,int(float(min_leaf_size)),loss_fn)
	l=0
	for  i in range(1,len(data.index)+1):
		result2(my0,data.iloc[l])
		l=l+1

	#for pre, _, node in RenderTree(my0):
	#	treestr = u"%s%s" % (pre, node.name)
	#	print(treestr.ljust(8), node.error/len(node.data.index))#,node.data.iloc[:,-1].var(),len(node.data.index))
	#for pre, _, node in RenderTree(my0):
	#	treestr = u"%s%s" % (pre, node.name) 
	#	print(node.data)
	my99=my0
	#print('this')
	#print(my99.attribute)
	l=0
	for  i in range(1,len(data.index)+1):
		result2(my0,data.iloc[l])
		l=l+1
	#prune(my0)
	#for pre, _, node in RenderTree(my0):
	#	treestr = u"%s%s" % (pre, node.name)
	#	print(treestr.ljust(8), node.error, node.value,node.data.iloc[:,-1].var(),len(node.data.index))
	#print(my0.value)
	random =0
	l=0
	df = pd.DataFrame(columns=[ 'output'])
	# df is the final result matrix
	for  i in range(1,len(test.index)+1):
		df.loc[i] = [result(my0,test.iloc[l])]
		#print(result(my0,test.iloc[l]))
		l=l+1

	#print(df)
	df.to_csv('output.csv')#
	error(my0)
	global final_error
	global count
	#print(final_error/len(data.index))
	#print(count)



if __name__ == '__main__':
	main()
