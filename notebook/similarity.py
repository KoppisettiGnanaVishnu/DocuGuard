'''import math

A=[1,0]
B=[1,0]

dot_product=A[0]*B[0] + A[1]*B[1]

magnitude_A=math.sqrt(A[0]**2 + A[1]**2)
magnitude_B=math.sqrt(B[0]**2 + B[1]**2)

similarity=dot_product/(magnitude_A*magnitude_B)

print(similarity)'''

import math

def cosine_similarity(A,B):
    dot_product=A[0]*B[0] + A[1]*B[1]
    
    magnitude_A=math.sqrt(A[0]**2 + A[1]**2)
    magnitude_B=math.sqrt(B[0]**2 + B[1]**2)
    
    similarity=dot_product/(magnitude_A*magnitude_B)
    
    return similarity

A=[-1,0]
B=[1,0]

similarity=cosine_similarity(A,B)
print(similarity)