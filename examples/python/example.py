#!/usr/bin/python3

'''
    libSVDD: A Library for Support Vector Data Description
    Copyright (C) 2020 Sohail R. Reddy

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
'''

from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import sys

sys.path.append('../../API/')

from libSVDD import *


def generateLabels(vals, flag = True):

	n = vals.shape[0]
	labels = np.zeros(n,  dtype = str)
	
	for i in range(0,n):
	
		if flag:
			labels[i] = '-1'
		elif vals[i,2] <= 80:
			labels[i] = '1'
		elif vals[i,2] >= 230:
			labels[i] = '2'
		elif vals[i,2] >= 170 and vals[i,2] < 230:
			labels[i] = '5'
		elif vals[i,0] >= 800:
			labels[i] = '3'			
		elif vals[i,0] < 800:
			labels[i] = '4'						
		else:
			labels[i] = '6'	
	
	return labels



def grid(x, y, z, resX=100, resY=100, method = 'nearest'):

	xi = np.linspace(min(x), max(x), resX)
	yi = np.linspace(min(y), max(y), resY)
	Z = griddata((x, y), z, (xi[None,:], yi[:,None]), method=method)
	X, Y = np.meshgrid(xi, yi)
	return X, Y, Z


def plotContour(ax, vals,labels, alpha = 1.0):

	labels = labels.astype(np.float)
	levels = np.linspace(min(labels), max(labels), 10, endpoint=True)
	x, y, z = grid(vals[:,0], vals[:,1], labels)
	ax.contourf(x, y, z, cmap = cm.jet, alpha = alpha)
	
	return ax



def example1(objects, labels):

	svm = SVM(libSVDD = '../../src/',
			  objects = objects, labels = labels, 
			  sigma = 120.0, kernel = 1,
			  save = 'example1.dat')
			  
	test = np.loadtxt('testing.dat')
	radius, labels = svm.classify(test)
	return test, labels
	

def example2():

	svm = SVM(libSVDD = '../../src/',init = 'example1.dat')
	test = np.loadtxt('testing.dat')
	radius, labels = svm.classify(test)
	return test, labels


if __name__ == "__main__":


		TrainFig = plt.figure()
		TrainFig.suptitle('Training Data', fontsize=16)
		ax = TrainFig.add_subplot(111)
		train = np.loadtxt('terrain.dat', usecols=(0,1,2))
		labels = generateLabels(train, flag = False)
		ax = plotContour(ax,train,labels, alpha = 1.0)

		#Train using just x and y coordinates
		test, labels = example1(train[:,0:2], labels)
		
	#	test, labels = example2()

		
		TestFig = plt.figure()
		TestFig.suptitle('Testing Data Classified', fontsize=16)
		ax = TestFig.add_subplot(111)
		ax = plotContour(ax,test,labels, alpha = 1.0)

	
		plt.show()



