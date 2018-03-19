from Matrix_Calculator import Matrix

test = Matrix([[1,1,1],[2,3,5],[4,6,8]])
test2 = Matrix([[1,2,3],[1,3,2],[1,4,5]])
iden = Matrix.identity(3)
test[2][2] = 17
test[2] = [5,6,7]
print(Matrix.console_input())