# My early attempt at making a Matrix object with available matrix operations
# Goals: implement object methods for material in linear algebra class
from fractions import Fraction
from copy import deepcopy

class Matrix:

# Attributes are basic, content is where the rows of the matrix will be stored, each as a list
# an item can be accessed in the format [row][col] with upmost left being [0][0]  
  rows = 0
  cols = 0
  content = []
  
  def __init__(self, parts, standard = True):
    # If the parts are given as a collection of columns, it is not standard and will be fixed
    if standard:
      self.content = deepcopy(parts)
      self.rows = len(parts)
      self.cols = len(parts[0])
    elif not standard:
      temp = []
      for i in range(0,len(parts[0])):
        for o in parts:
          temp.append(o[i])
        self.content.append(temp)
        temp = []
      self.rows = len(parts[0])
      self.cols = len(parts)
  
  def __getitem__(self, key):
      return self.content[key]
  
  def __setitem__(self,key,val):
      self.content[key] = val

  def console_input():
    # Allows a matrix to be input in the console, done by row. An empty row indicates to stop reading.
    accept = ["0","1","2","3","4","5","6","7","8","9"]
    temp = [1]
    content = []
    inp = ""
    s = ""
    r = 0
    while len(temp) >0:
        frac = 0
        temp = []
        r += 1
        inp = input("R" + str(r) + ": ") + " "
        for c in inp:
            if c in accept:
                s += c
            elif c == "/":
                frac = len(s)
                s += c
                
            else:
                try:
                    if frac > 0:
                        temp.append(Fraction(int(s[0:frac]), int(s[frac+1:])))
                        frac = 0
                    else:
                        temp.append(int(s))
                except ValueError:
                    pass
                s = ""
        if len(temp) >0:
            content.append(deepcopy(temp))
        
    return Matrix(content)

  def zerofill(ro, co):
      #constructs a zero matrix with provided dimensions
      zeroVec = []
      zeroMat = []
      for c in range(0,co):
          zeroVec.append(0)
      for r in range(0,ro):
          zeroMat.append(zeroVec[:])
      return Matrix(zeroMat)

  def identity(dim):
      #constructs identity matrix with given dimension
      iden = Matrix.zerofill(dim,dim)
      for k in range(0,dim):
          iden.content[k][k] = 1
      return iden

  def scalarMult(self, scale):
    # For scalar multiplication of matrix
    s_mult = deepcopy(self)
    for i in range(0, s_mult.cols):
      for o in range(0, s_mult.rows):
        s_mult.content[o][i] *= scale
    return s_mult
  
  def multiplication(self, m2):
    # For multiplication of 2 matricies in the order of m1(self) * m2
    if self.cols == m2.rows:
      product = []
      vec = []
      dotprod = 0
      for u in range(0, m2.cols):
        for y in range(0, self.rows):
          for m in range(0, self.cols):
            dotprod += (self.content[u][m] * m2.content[m][y])
          vec.append(dotprod)
          dotprod = 0
        product.append(vec)
        vec = []
      return Matrix(product)
    else:
       print("Not possible")
       return self

  def __mul__(a,b):
      if type(b) == Matrix:
          return a.multiplication(b)
      else:
          return a.scalarMult(b)

  def addition(self, m2):
      if not (self.rows == m2.rows and self.cols == m2.cols):
          print("Not possible")
          return self
      sum = Matrix.zerofill(self.rows,self.cols)
      for r in range(self.rows):
          for c in range(self.cols):
              sum.content[r][c] = self.content[r][c] + m2.content[r][c]
      return sum
 
  def __add__(a,b):
      return a.addition(b)

  def longestStr(self):
      # Returns the integer length of the longest entry (when converted to string)
      mx = 0
      for r in self.content:
          for c in r:
              if len(str(c)) > mx:
                  mx = len(str(c))
      return mx

  def __str__(self):
    # Generates each line as part of a string
    # Keeps a consisten spacing by inserting string into string of spaces, generated based off longest matrix entry
    temp = ""
    ins = "     "
    mx = self.longestStr()
    while (len(ins)-mx) < 3:
        ins += " "
    for i in self.content:
        for o in i:
          temp += str(o) + ins[len(str(o)):]
        temp += "\n"
    return temp
    
  def ref(self, steps = False):
    #returns a row reduced echelon form of given matrix, optional steps printed along way
    ref = deepcopy(self.content)
    hold = []
    wc = 0
    cr = 0
    mult = 0
    while (cr < self.rows and wc < self.cols):
      if steps:
        print("Column ", wc+1, "\n", Matrix(ref), "\n", sep ="")
      while ref[cr][wc] == 0:
        ejct = False
        for i in range(cr+1, self.rows):
          if not ref[i][wc] == 0:
            hold = ref[cr]
            ref[cr] = ref[i]
            ref[i] = hold
            ejct = True
            break
        if ejct:
          if steps:
            print("Row Swap", "\n", Matrix(ref), "\n", sep ="")
          break
        wc += 1
        if wc == self.cols:
          return Matrix(ref)
      for i in range(wc,self.cols):
        ref[cr][i] = Fraction(ref[cr][i], ref[cr][wc])
      for r in range(0,self.rows):
        if r == cr:
          pass
        else:
          mult = ref[r][wc]
          for c in range(wc,self.cols):
            ref[r][c] -= (mult*ref[cr][c])
          if steps:
            print(Matrix(ref), "\n", sep ="")
      cr += 1
      wc += 1
    return Matrix(ref)
  
  def echelon(self, steps = False):
    #returns echelon form of given matrix, optional steps printed
    ref = deepcopy(self.content)
    hold = []
    wc = 0
    cr = 0
    mult = Fraction(0,1)
    while (cr < self.rows and wc < self.cols):
      if steps:
        print("Column ", wc+1, "\n", Matrix(ref), "\n", sep ="")
      while ref[cr][wc] == 0:
        ejct = False
        for i in range(cr+1, self.rows):
          if not ref[i][wc] == 0:
            hold = ref[cr]
            ref[cr] = ref[i]
            ref[i] = hold
            ejct = True
            break
        if ejct:
          if steps:
            print("Row Swap", "\n", Matrix(ref), "\n", sep ="")
          break
        wc += 1
        if wc == self.cols:
          return Matrix(ref)
      for r in range(cr,self.rows):
        if r == cr:
          pass
        else:
          mult = Fraction(ref[r][wc], ref[cr][wc])
          for c in range(wc,self.cols):
            ref[r][c] -= (mult*ref[cr][c])
          if steps:
            print(Matrix(ref), "\n", sep ="")
      cr += 1
      wc += 1
    return Matrix(ref)

  def lu(self):
    # returns Lower matrix of LU decomposition of given matrix
    ref = deepcopy(self.content)
    hold = []
    wc = 0
    cr = 0
    l = []
    vec = []
    mult = Fraction(0,1)
    while (cr < self.rows and wc < self.cols):
      while ref[cr][wc] == 0:
        ejct = False
        for i in range(cr+1, self.rows):
          if not ref[i][wc] == 0:
              print("Not possible")
              return self
        wc += 1
        if wc == self.cols:
          return Matrix(ref)
      mult = Fraction(1,ref[cr][wc])
      for r in range(cr,self.rows):
          vec.append(mult*ref[r][wc])
      while len(vec) < self.rows:
          vec.insert(0,0)
      l.append(vec)
      vec = []
      for r in range(cr,self.rows):
        if r == cr:
          pass
        else:
          mult = Fraction(ref[r][wc], ref[cr][wc])
          for c in range(wc,self.cols):
            ref[r][c] -= (mult*ref[cr][c])
      cr += 1
      wc += 1
    return Matrix(l, standard = False)
  

  def det(self):
      #returns determinant
      if not self.rows == self.cols:
          print("Not possible")
          return self
      if self.rows == 1:
          return self.content[0][0]
      ref = deepcopy(self.content)
      temp = []
      deter = 0
      for c in range(self.cols):
        mult = deepcopy(ref[0][c])
        for r in range(1,self.rows):
            temp.append(deepcopy(ref[r][0:c] + ref[r][c+1:]))
        if c%2 == 0:
            deter += Matrix(temp).det() * mult
        else:
            deter -= Matrix(temp).det() * mult
        temp = []
      return deter
  