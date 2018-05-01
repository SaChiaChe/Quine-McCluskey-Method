import sys

while True:
	Variable_number = []
	m = []
	d = []
	Answer = []

	Variable_number_str = sys.stdin.readline()
	if Variable_number_str is '':
		break
	Variable_number = [int(x) for x in Variable_number_str.split()][0]
	m_str = sys.stdin.readline()
	m = sorted([int(x) for x in m_str.split()])
	d_str = sys.stdin.readline()
	d = sorted([int(x) for x in d_str.split()])

	Level = []
	Groups = []

	for GroupId in range(Variable_number+1):
		Groups.append([])

	#Sort to groups depending by how many 1's a term has
	def Sorting_Hat(x):
		x_bin = format(x, 'b').zfill(Variable_number)
		Numof1 = x_bin.count("1")
		return Numof1

	for i in (m + d):
		Groups[Sorting_Hat(i)].append([[i], format(i, 'b').zfill(Variable_number), 0])

	Level.append(Groups)

	#Combine two Implicants to one
	def Combine(x, y):
		x_bin = x[1]
		y_bin = y[1]
		Diff = 0
		for i in range(0, Variable_number):
			if x_bin[i] is not y_bin[i]:
				Diff += 1
				Pos = i
		if Diff is 1:
			New = list(x_bin)
			New[Pos] = '-'
			New = "".join(New)
			x[2] = 1
			y[2] = 1
			return [sorted(x[0] + y[0]), New, 0]
		else:
			return False

	for col in range(0, Variable_number+1):
		Temp1 = []
		for group in range(0, len(Level[col])-1):
			Temp2 = []
			if (len(Level[col][group]) is 0) or (len(Level[col][group]) is 0):
				continue
			for i in Level[col][group]:
				for j in Level[col][group+1]:
					Combined = Combine(i, j)
					if Combined is not False:
						Temp2.append(Combined)
			Temp1.append(Temp2)
		TotalLen = []
		for i in Temp1:
			TotalLen += i
		if len(TotalLen) is 0:
			break
		else:
			Level.append(Temp1)

	#remove the repeated Prime Implicants
	def Remove_Repeat(Group_):
		Temp_ = []
		for i in Group_:
			if Temp_.count(i) is 0:
				Temp_.append(i)
		return Temp_

	for col in range(1, len(Level)):
		Temp = []
		for G in Level[col]:
			Temp.append(Remove_Repeat(G))
		Level[col] = Temp

	# def Print_Level(Level):
	# 	C = 0
	# 	for i in Level:
	# 		print("Column", C, ": ")
	# 		C += 1
	# 		G = 0
	# 		for j in i:
	# 			print("Group", G, ": ")
	# 			for k in j:
	# 				print(k)
	# 			G += 1
	# 		print("")

	# Print_Level(Level)

	#Make "-01-" to "b'c" type
	def Alphalize(x):
		Char_ = []
		for i in range(0, len(x)):
			if x[i] is '1':
				Char_ += [chr(ord('a') + i)]
			elif x[i] is '0':
				Char_ += [chr(ord('a') + i)] + ['\'']
		
		Char = "".join(Char_)
		return [Char]

	PrimeImplicantTable=[]
	for i in reversed(Level):
		for j in i:
			for k in j:
				if k[2] is 0:
					PrimeImplicantTable += [[k[0], Alphalize(k[1]), []]]

	for i in PrimeImplicantTable:
		for j in m:
			if j in i[0]:
				i[2] += ['*']
			else:
				i[2] += ['-']

	CurrentMinterm = list(m)
	Answer = []

	#delete terms in the prime implicant table that cantains only don't care minterms
	def DeleteAllDontCare(PrimeImplicantTable):
		ToBeDeleted = []
		for i in range(0, len(PrimeImplicantTable)):
			if PrimeImplicantTable[i][2].count('*') is 0:
				ToBeDeleted.append(i)
		#print("To be deleted(Don't care)(Row): ", ToBeDeleted)
		for i in reversed(ToBeDeleted):
			del PrimeImplicantTable[i]

	#delete rows included by others
	def DeleteRowsIncludedbyOthers(PrimeImplicantTable):
		ToBeDeleted = []
		for i in range(0, len(PrimeImplicantTable)):
			for j in range(0, len(PrimeImplicantTable)):
				if i is j:
					continue
				if (i in ToBeDeleted) or (j in ToBeDeleted):
					continue
				Success = 1
				for k in range(len(PrimeImplicantTable[i][2])):
					if PrimeImplicantTable[i][2][k] is '*':
						if PrimeImplicantTable[j][2][k] is '-':
							Success = 0
							break
				if Success:
					#print("Checked Row", i, "and", j, ",", i, "should be deleted")
					if i not in ToBeDeleted:
						ToBeDeleted.append(i)
		#print("To be deleted(Rows included): ", ToBeDeleted)
		for i in reversed(sorted(ToBeDeleted)):
			del PrimeImplicantTable[i]

	#delete columns included by others
	def DeleteColsIncludedbyOthers(PrimeImplicantTable, CurrentMinterm):
		ToBeDeleted = []
		for i in range(0, len(CurrentMinterm)):
			for j in range(0, len(CurrentMinterm)):
				if i is j:
					continue
				if (i in ToBeDeleted) or(j in ToBeDeleted):
					continue
				Success = 1
				for k in range(0, len(PrimeImplicantTable)):
					if PrimeImplicantTable[k][2][i] is '*':
						if PrimeImplicantTable[k][2][j] is '-':
							Success = 0
							break
				if Success:
					#print("Checked Col", i, "and", j, ",", j, "should be deleted")
					if j not in ToBeDeleted:
						ToBeDeleted.append(j)
		#print("To be deleted(Columns included): ", ToBeDeleted)
		for i in reversed(sorted(ToBeDeleted)):
			del CurrentMinterm[i]
			for j in PrimeImplicantTable:
				del j[2][i]

	#Find Essential Prime Implicants
	while len(CurrentMinterm) is not 0:
		#print("-----------Start----------")
		# for i in PrimeImplicantTable:
		# 	print(i[0], i[1], i[2])
		DeleteRowsIncludedbyOthers(PrimeImplicantTable)
		DeleteColsIncludedbyOthers(PrimeImplicantTable, CurrentMinterm)
		DeleteAllDontCare(PrimeImplicantTable)
		# for i in PrimeImplicantTable:
		# 	print(i[0], i[1], i[2])
		Essential = []
		for i in range(0, len(CurrentMinterm)):
			AstCount = 0
			CurrentPos = -1
			for j in PrimeImplicantTable:
				CurrentPos += 1
				if j[2][i] is '*':
					AstCount += 1
					AstPos = CurrentPos
				if AstCount > 1:
					break
			if AstCount is 1:
				if AstPos not in Essential:
					Essential += [AstPos]

		if len(Essential) is 0:
			break

		Answer += [PrimeImplicantTable[x][1] for x in Essential]

		# print("Essentials: ", Essential)
		# print("Before: ")
		# print(CurrentMinterm)
		# for i in PrimeImplicantTable:
		# 	print(i[2])

		#delete columns
		for i in Essential:
			DeleteList = PrimeImplicantTable[i][0]
			for j in DeleteList:
				if j in CurrentMinterm:
					Index = CurrentMinterm.index(j)
					del CurrentMinterm[Index]
					for k in PrimeImplicantTable:
						del k[2][Index]
		# print("Delete Col: ")
		# print(CurrentMinterm)
		# for i in PrimeImplicantTable:
		# 	print(i[2])

		#delete rows
		for i in reversed(sorted(Essential)):
			del PrimeImplicantTable[i]
		# print("Delete Row: ")
		# print(CurrentMinterm)
		# for i in PrimeImplicantTable:
		# 	print(i[2])

	#print("Answer Before Petrick's method: ", Answer)

	def Multiplication(ListofTerms):
		ListofTerms_ = list(ListofTerms)
		NewP = ListofTerms_[0]
		del ListofTerms_[0]
		for i in ListofTerms_:
			Temp = []
			for j in NewP:
				for k in i:
					Temp2 = list(j)
					for x in k:
						if x not in Temp2:
							Temp2.append(x)
					Temp.append(Temp2)
			NewP = list(Temp)

		ToBeDeleted = []
		for i in range(0, len(NewP)-1):
			for j in range(i+1, len(NewP)):
				if (i in ToBeDeleted) or (j in ToBeDeleted):
					continue
				Success = 1
				for x in NewP[i]:
					if x not in NewP[j]:
						Success = 0
						break
				if Success:
					if j not in ToBeDeleted:
						ToBeDeleted.append(j)
		for i in reversed(sorted(ToBeDeleted)):
			del NewP[i]

		return NewP

	#Petrick's method
	if len(CurrentMinterm) > 0:
		P = []
		for i in range(0, len(CurrentMinterm)):
			Temp = []
			for j in PrimeImplicantTable:
				if j[2][i] is '*':
					Temp.append(j[1])
			P.append(Temp)
		
		P_Multiplied = Multiplication(P)

		MinID = 0
		for i in range(1, len(P_Multiplied)):
			if len(P_Multiplied[i]) < len(P_Multiplied[MinID]):
				MinID = i
		#print("Minterm:", P_Multiplied[MinID])
		for i in P_Multiplied[MinID]:
			Answer.append([i])
		#print("Answer:", Answer)

	#print the answer (adding the +)
	def PrintAnswer(Answer):
		if len(Answer) is 0:
			return
		print(Answer[0][0], end = "")
		for i in Answer[1:]:
			print(" + ", i[0], end = "")
		print("")

	PrintAnswer(Answer)