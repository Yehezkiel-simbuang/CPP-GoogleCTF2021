from z3 import *

solve = z3.Solver()
flag = [BitVec(f"FLAG{i}",8) for i in range(27)]

for i in flag[:-1] :
	solve.add(i >= ord('!'))
	solve.add(i <= ord('~'))

ROM = [z3.BitVecVal(0,8)] * 256

val = [
		187, 85, 171, 197, 185, 157, 201, 105, 187, 55, 217, 
		205, 33, 179, 207, 207, 159, 9, 181, 61, 235, 127, 87,
		161, 235, 135, 103, 35, 23, 37, 209, 27, 8, 100, 100,
		53, 145, 100, 231, 160, 6, 170, 221, 117, 23, 157, 109,
		92, 94, 25, 253, 233, 12, 249, 180, 131, 134, 34, 66,
		30, 87, 161, 40, 98, 250, 123, 27, 186, 30, 180, 179,
		88, 198, 243, 140, 144, 59, 186, 25, 110, 206, 223,
		241, 37, 141, 64, 128, 112, 224, 77, 28 ]

val = [z3.BitVecVal(i, 8) for i in val]

ROM[:90] = val

start = 0b10000000

ROM[start : start + len(flag)] = flag

A,B,C,I,M,N,O,P,Q,R,X,Y,Z = [0] * 13

def solver() :
	global A,B,C,I,M,N,O,P,Q,R,X,Y,Z

	I = 0b00000000
	M = 0b00000000
	N = 0b00000001
	P = 0b00000000
	Q = 0b00000000

	for f in range(27) :
		B = 0b10000000
		B = (B+I) & 0xFF

		A = ROM[B]
		B = ROM[I]

		R = 0b00000001

		X = 0b00000001
		Y = 0b00000000

		while (X != 0b0000000) :
			Z = X
			Z &= B
			Zval = int(str(z3.simplify(Z)))
			if Zval != 0b00000000 :
				Y  = (Y+A) &0xFF

			X = (X+X) & 0xFF
			A = (A+A) & 0xFF

		A = Y

		R ^= 0b11111111
		Z = 0b00000001

		R = (R+Z) & 0xFF
		R = (R+Z) & 0xFF

		if R == 0b00000000 :
			O = M
			O = (O+N) & 0xFF
			M = N
			N = O

			A = (A+M) & 0xFF

			B = 0b00100000
			B = (B+I) & 0xFF

			C = ROM[B]
			A^= C
			P = (P+A) & 0xFF

			B = 0b01000000
			B = (B+I) & 0xFF

			A = ROM[B]
			A^= P
			Q |= A

			A = 0b00000001

			I = (I+A) & 0xFF

			B = 0b11100101 & 0xFF
			B = (B+I) & 0xFF

			if B == 0b00000000 :
				solve.add(Q == 0b00000000)

		else :
			raise ValueError("BUG")


solver()
solve.check()
mod = solve.model()
FLAG = ""
for i in range(27) :
	FLAG += chr(int(str(z3.simplify(mod[flag[i]]))))
print(FLAG)