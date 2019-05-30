

# DESCRIPTION:
#######################################################################################################
#
# THIS CODE IS ALMOST IDENTICAL TO "pcaDiffScenV2.py". BEFORE USING THIS CODE, MAKE SURE YOU UNDERSTAND
# THE PREVIOUS VERSION. THE PURPOSE OF THIS CODE IS NOT TO PLOT PCA BUT RATHER TO SEPARATE THE PLOTTED POINTS OF THE PCA CODE FROM V2
# INTO RESPECTIVE QUADRANTS. THE QUADRANTS ARE DEFINED BY THE SIGN OF THE PC1 AND PC2 COMPONENTS. IN OTHER
# WORDS:
#
# IF PC1 IS POSITIVE AND PC2 IS POSITIVE, THEN THE DATA POINT IS IN QUADRANT "A" 
# IF PC1 IS NEGATIVE AND PC2 IS POSITIVE, THEN THE DATA POINT IS IN QUADRANT "B" 
# IF PC1 IS NEGATIVE AND PC2 IS NEGATIVE, THEN THE DATA POINT IS IN QUADRANT "C" 
# IF PC1 IS POSITIVE AND PC2 IS NEGATIVE, THEN THE DATA POINT IS IN QUADRANT "D" 
#
# IF THIS IS STILL CONFUSING, THERE IS A FIGURE IN THE DOC FILE "PCA_Lab_Night.docx" THAT DISPLAYS HOW 
# THESE QUADRANTS LOOK. THE PURPOSE OF THIS CODE IS TO LOOK AT WHICH QUADRANT THE DATA POINT WILL FALL
# INTO, AND COMPARE IT TO THE TIMESTAMP SO THAT YOU CAN SEE IF THERE IS SOME EFFECT AT A SPECIFIC TIME
# THAT CAUSES THE DATA POINT TO MIGRATE TO ANOTHER QUADRANT AND HOW LONG IT RESIDES THERE. THIS CODE IS
# MADE TO BE USED ON ONE SCENARIO AT A TIME. IT WRITES THE QUADRANT RESULTS IN A LOG FILE CALLED "Letters.log"
#
#
# by jordan gonzales
#
#######################################################################################################





# IMPORTS
############################################################################################
import pandas as pd
import numpy as np
#import numpy
#np.set_printoptions(threshold=np.nan)
import random as rd
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt # NOTE: This was tested with matplotlib v. 2.1.0
import fileinput #ADDED
from mpl_toolkits import mplot3d
############################################################################################
 
 
 
 
 
 

# REMOVE BRACKETS FROM magAll LOG FILE, GET FILE NAMES, AND COUNT PACKETS:
############################################################################################

maxPackets = 0

temp = 1

numScen = 1

scen1 = raw_input(str("What is scenario #1?"))

#scen1 = "magBinder_lab_2.log"
#scen2 = "magChair_lab.log"
#scen3 = "magHand_lab.log"
#scen4 = "magNormal_lab.log"
#scen5 = "magSit_lab.log"
#scen6 = "magWalk_lab.log"

#log1 = "magBinder_lab_2.log"
#log2 = "magChair_lab.log"
#log3 = "magHand_lab.log"
#log4 = "magNormal_lab.log"
#log5 = "magSit_lab.log"
#log6 = "magWalk_lab.log"

#if temp <= numScen:
#	scen1 = raw_input(str("What is scenario #" + str(temp) + "? "))
#	temp += 1
	
#if temp <= numScen:
#	scen2 = raw_input(str("What is scenario #" + str(temp) + "? "))
#	temp += 1
	
#if temp <= numScen:
#	scen3 = raw_input(str("What is scenario #" + str(temp) + "? "))
#	temp += 1
	
#if temp <= numScen:
#	scen4 = raw_input(str("What is scenario #" + str(temp) + "? "))
#	temp += 1
	
#if temp <= numScen:
#	scen5 = raw_input(str("What is scenario #" + str(temp) + "? "))
#	temp += 1
	
#if temp <= numScen:
#	scen6 = raw_input(str("What is scenario #" + str(temp) + "? "))
#	temp += 1
	
log1 = scen1 + ".log"
#print(log1)
#log2 = scen2 + ".log"
#print(log2)
#log3 = scen3 + ".log"
#print(log3)
#log4 = scen4 + ".log"
#print(log4)
#log5 = scen5 + ".log"
#print(log5)
#log6 = scen6 + ".log"
#print(log6)




# COMPARING NUMBER OF PACKETS IN EACH SCENARIO TO GET RID OF EXTRA PACKETS:
#################################################################################################################################

#print("\n")

# FIRST SCENARIO:
if numScen >= 1:
	scen1Packets = 0
	with open(log1, 'r') as fudge1:
		for line in fudge1:
			if not line.isspace() and line != "[]\n":
				scen1Packets += 1
			
	#print("Number of Packets in Scenario 1: " + str(scen1Packets))

	maxPackets = scen1Packets		# UPDATE NUMBER OF ALLOWED PACKETS


'''
# SECOND SCENARIO:
if numScen >= 2:
	scen2Packets = 0
	with open(log2, 'r') as fudge2:
		for line in fudge2:
			if not line.isspace() and line != "[]\n":
				scen2Packets += 1
			
	#print("Number of Packets in Scenario 2: " + str(scen2Packets))

	if scen2Packets < scen1Packets:	# UPDATE NUMBER OF ALLOWED PACKETS
		maxPackets = scen2Packets
	
	
	
# THIRD SCENARIO:
if numScen >= 3:
	scen3Packets = 0
	with open(log3, 'r') as fudge3:
		for line in fudge3:
			if not line.isspace() and line != "[]\n":
				scen3Packets += 1
			
	#print("Number of Packets in Scenario 3: " + str(scen3Packets))

	if scen3Packets < scen2Packets:	# UPDATE NUMBER OF ALLOWED PACKETS
		maxPackets = scen3Packets
		
		

# FOURTH SCENARIO:
if numScen >= 4:
	scen4Packets = 0
	with open(log4, 'r') as fudge4:
		for line in fudge4:
			if not line.isspace() and line != "[]\n":
				scen4Packets += 1
			
	#print("Number of Packets in Scenario 4: " + str(scen4Packets))

	if scen4Packets < scen3Packets:	# UPDATE NUMBER OF ALLOWED PACKETS
		maxPackets = scen4Packets
		
		
		
# FIFTH SCENARIO:
if numScen >= 5:
	scen5Packets = 0
	with open(log5, 'r') as fudge5:
		for line in fudge5:
			if not line.isspace() and line != "[]\n":
				scen5Packets += 1
			
	#print("Number of Packets in Scenario 5: " + str(scen5Packets))

	if scen5Packets < scen4Packets:	# UPDATE NUMBER OF ALLOWED PACKETS
		maxPackets = scen5Packets
		
		
		
# SIXTH SCENARIO:
if numScen >= 6:
	scen6Packets = 0
	with open(log6, 'r') as fudge6:
		for line in fudge6:
			if not line.isspace() and line != "[]\n":
				scen6Packets += 1
			
	#print("Number of Packets in Scenario 6: " + str(scen6Packets))

	if scen6Packets < scen5Packets:	# UPDATE NUMBER OF ALLOWED PACKETS
		maxPackets = scen6Packets
		
#print("\n")		
print("The Maximum Allowed Number of Packets is: " + str(maxPackets))
'''

#################################################################################################################################






# PUTTING ALL SCENARIOS INTO ONE LOG FILE NOW THAT THEY EACH HAVE THE SAME NUMBER OF PACKETS:
#################################################################################################################################


# THESE COUNTERS KEEP TRACK OF HOW MANY PACKETS FROM WHICH SCENARIO YOU'VE DUMPED INTO THE ALL-INCLUSIVE MAG LOG FILE
scen1Count = 1
'''
scen2Count = 1
scen3Count = 1
scen4Count = 1
scen5Count = 1
scen6Count = 1
'''

# SCEN1 STUFF: 
if numScen >= 1:
	with open(log1) as f1:
		with open('magAll.log', 'w') as f2:
			for line in f1:
				if not line.isspace() and line != "[]\n": 
					if scen1Count <= maxPackets:
						f2.write(line)
						scen1Count += 1



'''
# SCEN2 STUFF: 
if numScen >= 2:
	with open(log2) as f3:
		with open('magAll.log', 'a') as f2:
			for line in f3:
				if not line.isspace():
					if not line.isspace() and line != "[]\n": 
						if scen2Count <= maxPackets:
							f2.write(line)
							scen2Count += 1


	
# SCEN3 STUFF:
if numScen >= 3:				
	with open(log3) as f3:
		with open('magAll.log', 'a') as f2:
			for line in f3:
				if not line.isspace() and line != "[]\n": 
					if scen3Count <= maxPackets:
						f2.write(line)
						scen3Count += 1



# SCEN4 STUFF:		
if numScen >= 4:				
	with open(log4) as f3:
		with open('magAll.log', 'a') as f2:
			for line in f3:
				if not line.isspace() and line != "[]\n": 
					if scen4Count <= maxPackets:
						f2.write(line)
						scen4Count += 1
					
							
					
# SCEN5 STUFF:
if numScen >= 5:						
	with open(log5) as f3:
		with open('magAll.log', 'a') as f2:
			for line in f3:
				if not line.isspace() and line != "[]\n": 
					if scen5Count <= maxPackets:
						f2.write(line)	
						scen5Count += 1	
		
		
		
# SCEN6 STUFF:				
if numScen >= 6:						
	with open(log6) as f3:
		with open('magAll.log', 'a') as f2:
			for line in f3:
				if not line.isspace() and line != "[]\n": 
					if scen6Count <= maxPackets:
						f2.write(line)
						scen6Count += 1

'''


with open('magAll.log') as f:
	totalPacketCount = sum(1 for _ in f)

with open('magAll.log', 'r') as magAll:
	text = magAll.read()
	text = text.replace("[", "")
	text = text.replace("]", "")
	text = text.replace("'", "")
	

with open('magAllClean.log', 'w') as magAll:
	magAll.write(text)

time = []
buff = []

i = 0

file2 = open("magAllClean.log", "r")
for line in file2:
    if i % 2 == 0:
        time.append(line)
    else:
        buff.append(line)
    i += 1
file2.close()

file1 = open("time.log", "w")

for i in time:
    file1.write(i)

file1.close()

file2 = open("buff.log", "w")

for i in buff:
    file2.write(i)

file2.close()

	
bookmark = totalPacketCount // numScen
#print("Bookmark: ", bookmark)
	
data = np.genfromtxt('buff.log', delimiter = ',');
print(data)
#################################################################################################################################







# PERFORM PCA CALCULATIONS ON THE DATA:
###################################################################
# First center and scale the data
scaled_data = preprocessing.scale(data)
#print("Scaled Data: ")	<---------------# UNCOMMENT LATER
#print(scaled_data) 	<---------------# UNCOMMENT LATER

pca = PCA() # create a PCA object
pca.fit(scaled_data) # do the math
pca_data = pca.fit_transform(scaled_data) 
#print("PCA Data: ", pca_data)   #<------# UNCOMMENT LATER

per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)
#print(per_var)		<-------------------# UNCOMMENT LATER
labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
#print(labels)		#<-------------------# UNCOMMENT LATER
###################################################################


# FRISCO'S ADDITIONS:
########################################################
# NOTE: AVERAGE TIME BETWEEN PACKETS IS 0.07 SECONDS, 
# SO IF IT HAS BEEN MUCH LONGER THAN THAT, SUCH AS 10*0.07 = 0.7 SECONDS
# SINCE A PACKET FALLS INTO THE SAME CATEGORY, THEN SOMETHING HAPPENED DURING 
# THAT TIME FRAME TO MAKE THE PACKETS HAVE SUBSTANTIALLY DIFFERENT PC VALUES. 

file1 = open("time.log", "r")
file2 = open("PC1_2_neg.log", "w")
file3 = open("PC1_2_pos.log", "w")
file4 = open("PC1_pos_PC2_neg.log", "w")
file5 = open("PC1_neg_PC2_pos.log", "w")

file8 = open("Letters.log", "w") # ADDED

i = 0

file8.write('A = Neg-Neg, B = Pos-Pos, C = Pos-Neg, D = Neg-Pos\n\n')
for x in file1:
	if pca_data[i][0] > 0 and pca_data[i][1] > 0:	# QUADRANT A
		#file2.write(x)
		file8.write("A\t\t" + str(x))
	elif pca_data[i][0] < 0 and pca_data[i][1] > 0:	# QUADRANT B
		#file3.write(x)
		file8.write("B\t\t" + str(x))
	elif pca_data[i][0] < 0 and pca_data[i][1] < 0:	# QUADRANT C
		#file4.write(x)
		file8.write("C\t\t" + str(x))
	else:
		#file5.write(x)
		file8.write("D\t\t" + str(x)) # QUADRANT D
	i += 1
		
file1.close()
file2.close()
file3.close()
file4.close()
file5.close()

file6 = open("PC1_2_neg.log", "r")
file7 = open("negChange.log", "w")
#file8 = open("Letters.log", "w") # ADDED
last = 0.0
flagBox = 0
for x in file6:
	x = x.strip("\n")
	new = x
	x = float(x)
	last = float(last)
	change = float(x) - float(last)
	
	if change >= 1:	#<--------------------- ARBITRARY. TRY CHANGING TO DIFFERENT MULTIPLES OF 0.07
		change = round(change, 2)
		last = round(last, 2)
		if flagBox == 0:
			file7.write('\t\t\t' + "Timestamp when the packets left the negative-negative quadrant: " + '\t' + "How long it was out of the negative-negative quadrant: \n")
			flagBox = 1
		file7.write('\t\t\t\t\t\t\t' + str(last)  + '\t\t\t\t\t\t\t\t\t\t\t\t\t\t' + str(change))
		file7.write(str(change))
		file7.write("\n")
	last = x
	
file6.close()
file7.close()
		

 

 
'''
# PLOTS PCA GRAPH:
###########################################################################
pca_df = pd.DataFrame(pca_data, columns = labels)
#print(pca_df)	#<-------------------# UNCOMMENT LATER
#print(pd.DataFrame.to_string(pca_df))		###### NOT SURE ABOUT THIS ONE
#pd.set_option('display.max_rows', len(x))
#print(x)
#pd.reset_option('display.max_rows')

ax = plt.axes(projection='3d') 
plt.title('Blue = ' + scen1 + ',  Red = ' + scen2 + ',  Green = ' + scen3 + ',  Purple = ' + scen4 + ',  Orange = ' + scen5 + ',  Yellow = ' + scen6, fontsize=15)
plt.xlabel('PC1 - {0}%'.format(per_var[0]))
plt.ylabel('PC2 - {0}%'.format(per_var[1]))
ax.set_zlabel('PC3 - {0}%'.format(per_var[2]))

#bookmarkCount = 1

# PLOTS FIRST SCENARIO
#if numScen >= bookmarkCount:
#	for i in range((bookmarkCount-1) * bookmark, bookmark):
#		plt.scatter(pca_df.loc[i].PC1, pca_df.loc[i].PC2, color='blue') #NORMAL
#		bookmarkCount += 1
	
# PLOTS SECOND SCENARIO
#if numScen >= bookmarkCount:
#	for j in range(bookmark, bookmarkCount*bookmark):
#		plt.scatter(pca_df.loc[j].PC1, pca_df.loc[j].PC2, color='red') #ACTIVE
#	bookmarkCount += 1
	
# PLOTS THIRD SCENARIO
#if numScen >= bookmarkCount:
#	for k in range((bookmarkCount-1) * bookmark,  bookmarkCount * bookmark):
#		plt.scatter(pca_df.loc[k].PC1, pca_df.loc[k].PC2, color='green') #ACTIVE
#	bookmarkCount += 1
	
# PLOTS FOURTH SCENARIO	
#if numScen >= bookmarkCount:
#	for x in range((bookmarkCount-1) * bookmark,  bookmarkCount * bookmark):
#		plt.scatter(pca_df.loc[x].PC1, pca_df.loc[x].PC2, color='purple') #ACTIVE
#	bookmarkCount += 1
		
# PLOTS FIFTH SCENARIO
#if numScen >= bookmarkCount:
#	for y in range((bookmarkCount-1) * bookmark,  bookmarkCount * bookmark):
#		plt.scatter(pca_df.loc[y].PC1, pca_df.loc[y].PC2, color='orange') #ACTIVE
#	bookmarkCount += 1


# COLORCODE:
###########################################################################

if numScen >= 1:
	for i in range(0, bookmark):
		ax.scatter3D(pca_df.loc[i].PC1, pca_df.loc[i].PC2, pca_df.loc[i].PC3, color='blue',alpha=0.0) 
		
if numScen >= 2:
	for i in range(bookmark, 2*bookmark):
		ax.scatter3D(pca_df.loc[i].PC1, pca_df.loc[i].PC2, pca_df.loc[i].PC3, color='red',alpha=0.0) 

if numScen >= 3:
	for i in range(2*bookmark, 3*bookmark):
		ax.scatter3D(pca_df.loc[i].PC1, pca_df.loc[i].PC2, pca_df.loc[i].PC3, color='green',alpha=0.0) 
		
if numScen >= 4:
	for i in range(3*bookmark, 4*bookmark):
		ax.scatter3D(pca_df.loc[i].PC1, pca_df.loc[i].PC2, pca_df.loc[i].PC3, color='purple',alpha=0.0) 
		
if numScen >= 5:
	for i in range(4*bookmark, 5*bookmark):
		ax.scatter3D(pca_df.loc[i].PC1, pca_df.loc[i].PC2, pca_df.loc[i].PC3, color='orange',alpha=0.0) 
		
if numScen >= 6:
	for i in range(5*bookmark, 6*bookmark):
		ax.scatter3D(pca_df.loc[i].PC1, pca_df.loc[i].PC2, pca_df.loc[i].PC3, color='yellow',alpha=0.2) 
		
np.savetxt(r'dataFrame.txt', pca_df.values, fmt='%.10f')
	

plt.show()
###########################################################################






# PCA FOR PHASE:
#############################################################################################

#if phaseOrNo == "y":

loading_scores = pd.Series(pca.components_[0])
## now sort the loading scores based on their magnitude
sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)
 
#top_10 = sorted_loading_scores[0:10].index.values
#print('Loading scores: ')                    commented out for testing
#print(sorted_loading_scores)
	














#############################################################################################
'''
