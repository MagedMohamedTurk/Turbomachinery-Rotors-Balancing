# -*- coding: utf-8 -*-
"""
Created on Sun Jan 26 21:55:05 2020

@author: MAGED
"""

import click as ck
import numpy as np
import cmath as cm
import cvxpy as cp
from itertools import chain

# =============================================================================
# =============================================================================
# =============================================================================
# # # # Getting the matrix dimensions
# # # # Given: N balance planes (locations for correction masses)
# # # # M vibration readings at
# # # # where M = K X L
# # # # K different conditions of speed and load
# # # # L different location
# =============================================================================
# =============================================================================
# =============================================================================
U=[]
ALPHA=[]
B=[]
A=[]

def get_dim():
    N = ck.prompt("Insert the Number of Balancing Planes available in the Machine", type=int)
    L = ck.prompt("Insert the Number of Vibration Measuring sensors", type=int)
    K = ck.prompt("Insert the Number of Speeds and Loads in concern", type=int)
    M = K*L
    return M,N,K,L
M,N,K,L=get_dim()

if M-N<0:
    print("Number of balancing planes can't be more than the measuring locations.... No solution can be found")
    M,N,K,L=get_dim()

# =============================================================================
# # Create the matrix Am : Zero-rotor data: A1, A2, AM
# =============================================================================
def intial():
    print()
    print("Intial Run Vibrtaion Measurements")
    print("*********************************")
    print()
    A=[]
    for i in range (K):
        print("Enter Intial Vibration Data for speed and load condition #",i+1)
        for row in range(L):
                          print("Insert The Intial vibration value @ measuring plane number",row+1) 
                          while True:
                              try:
                                  aM, aP = [float(x) for x in input("Enter Magnitude and phase (with space between): ").split()]
                                  a=cm.rect(aM,aP*cm.pi/180)
                                  A.append ([a])
                              except :
                                  print("Please Enter Valid Data!")
                              else:
                                  break
    A=np.array (A)
    return A


# =============================================================================
# # slow roll readings
# =============================================================================
def slowroll():
    print()
    print("Slowroll Run Vibrtaion Measurements")
    print("*********************************")
    print()
    Ae=[]
    for row in range(L):
                      print("Insert The Slowroll vibration value @ measuring plane number",row+1) 
                      while True:
                          try:
                              aM, aP = [float(x) for x in input("Enter Magnitude and phase (with space between): ").split()]
                              a=cm.rect(aM,aP*cm.pi/180)
                              Ae.append ([a])
                          except :
                              print("Please Enter Valid Data!")
                          else:
                              break
    Ae=np.array (Ae)
    return Ae




if ck.confirm("Has a Slow Roll Run Been Taken ?"):
    Ae=slowroll()
    A=intial()
else:
    A=intial()
    Ae=np.zeros(A.shape)
A=np.subtract(A,Ae)
Ae=np.zeros(A.shape)




    
    
    

# =============================================================================
# # Get the Trial Mass Vibrations Readings B Matrix
# =============================================================================
def get_B():
    
    # =============================================================================
    #         # Create the matrix Un:  Trial mass Magnitudes Ui, U2, . . . ., UN of trial masses in the N balance planes.
    # =============================================================================
            
        print()
        print('======Trail Masses Data======')
        print('******************************')
        U=[]
        
        for i in range(N):
                      print("Insert Trial mass Magnitudes at Balancing Plane",i+1)      
                      while True:
                          try:
                              uM,uP=[float(x) for x in input("Enter Magnitude in (grams)and phase (with space between): ").split()]
                              u=cm.rect(uM,uP*cm.pi/180)
                              U.append ([u])
                          except:
                              print("Please Enter Valid Data!")
                          else:
                              break
        U=np.array (U)
 
    # =============================================================================
    #         # Trial-mass data: Bmn              m = 1, . . . ., M & n = 1, , N
    # =============================================================================
            
        B=[]
        
        
            
        for row in range(N):
                b=[]
                bM=0
                bP=0
                print()
                print("Run #", row+1," with trail mass @ Plane",row+1)
                print("********************************************")
                for i in range (K):
                    print()
                    print("Enter Data for speed and load condition #",i+1)
                    print("******************************************")
                    for col in range (L):
                        print("Insert The vibration value at measuring plane number",col+1,"with the trial mass @ plane",row+1) 
                        while True:
                              try:
                                  bM,bP=[float(x) for x in input("Enter Magnitude and phase (with space between): ").split()]
                                  bmn=cm.rect(bM,bP*cm.pi/180)     # getting the row of the the matrix B
                                  b.append (bmn)
                              except:
                                  print("Please Enter Valid Data!")
                              else:
                                  break   
                    B.append(b)  # filling the rows of the matrix B
        B=np.array (B) 
       
        
        B=np.transpose(B)   # getting each column to be for each trail mass measurements
        B=np.subtract(B,Ae)
                  
    # =============================================================================
    #         # Create the matrices response coefficients Alpha(MN)=(Bmn-Amn)/Un
    # =============================================================================
        
        ALPHA=np.zeros((M,N),dtype=complex)
        
        if ck.confirm("The trail mass was removed each time"):
        
            for i in range (M):
             
                for j in range (N):
                    element=(B[i,j]-A[i])/U[j]
                    ALPHA[i,j]=element.item(0)
                    element=[]
        else:
            for i in range (M):
                    element=(B[i,0]-A[i])/U[0]
                    ALPHA[i,0]=element.item(0)
                    element=[]
            for i in range (M):  
                    for j in range (1,N):
                        element=(B[i,j]-B[i,j-1])/U[j]
                        ALPHA[i,j]=element.item(0)
                        element=[]
        return ALPHA
    
    
# =============================================================================
# # Get direct Influence Coefficient Matrix ALPHA    
# =============================================================================
def ALPHA_MAT():
        # User enter direct Influence Matrix ALPHA: ALPHAmn              m = 1, . . . ., M & n = 1, , N
        
        ALPHA=[]
        
        
            
        for row in range(N):
                b=[]
                bM=0
                bP=0
                print()
                print("Run #", row+1," with trail mass @ Plane",row+1)
                print("********************************************")
                for i in range (K):
                    print()
                    print("Enter Data for speed and load condition #",i+1)
                    print("******************************************")
                    for col in range (L):
                        print("Insert The vibration value at measuring plane number",col+1,"with the trial mass @ plane",row+1) 
                        while True:
                              try:
                                  bM,bP=[float(x) for x in input("Enter Magnitude and phase (with space between): ").split()]
                                  bmn=cm.rect(bM,bP*cm.pi/180)     # getting the row of the the matrix ALPHA
                                  b.append (bmn)
                              except:
                                  print("Please Enter Valid Data!")
                              else:
                                  break   
                ALPHA.append(b)  # filling the rows of the matrix ALPHA
        ALPHA=np.array (ALPHA) 
        
        ALPHA=np.transpose(ALPHA)   # getting each column to be for each trail mass measurements
        return ALPHA
    
# =============================================================================
# # GETTING THE IC MATRIX    
# =============================================================================

    # Load Matrix from csv file 
def loadmat():
    while True:
        try:
            load=ck.prompt("What is the CSV file name?",type=str)          
            ALPHA=np.loadtxt(load+'.csv').view(complex)
            if ALPHA.shape==(M,N):
                print('Matrix loaded..!')
                break
            else:
                print('Matrix dimension mismatch!')
                continue
        except OSError as err:
            print("OS error: {0}".format(err))
            directmat()
            break
    
    return ALPHA  
        
    
    
    
def directmat():
    if ck.confirm("Load Saved Influence Coefficient Matrix"):
    
        ALPHA=loadmat()
    else:
        ALPHA=ALPHA_MAT()            
                                
    return ALPHA        



if ck.confirm ('Insert Direct Influence Coeffecient Matrix?'):
               
    ALPHA=directmat() 

else:       
    ALPHA=get_B()



# =============================================================================
# PRINTING MATRIX
# =============================================================================
        
def printmat(Z):
    ZZ=list(chain.from_iterable(Z))
    P=[cm.polar(x) for x in ZZ]
    
    a=([str(np.round(x[0],2)) for x in P])
    b=([str(np.round(x[1]*180/3.14,0)) for x in P])
    Pp=[]
    PP=[]
    k=Z.shape[0]
    for i in range(k):
        for j in range(Z.shape[1]):
            Pp.append(''.join(map(str,[a[i+j*k],'@',b[i+j*k]])))
        PP.append(Pp)
        Pp=[]
    print()  
    print('--------------------------------')
    print('Influence Coeffecienct  Matrix')
    print('--------------------------------')  
    print()
    for xs in PP:
        
        print("    ".join(map(str, xs)))
    print()
    
    return    




printmat(ALPHA)


# =============================================================================
# CHECKING THE IC MATRIX
# =============================================================================
        

# CHECKING SYMMETRICITY

if M==N:
    check=np.allclose(ALPHA,ALPHA.T,0.2,1e-06)
    
    if check != True:
        print('Warning !! Influence Matrix is assymetrical!!')


# CHECKING ILL-CONDITIONED PLANES   
Q,R = np.linalg.qr(ALPHA)
dep=[]
Rdia=abs(np.diag(R))
for i in range (R.shape[0]):
    if abs(Rdia[i]/max(Rdia))<0.2:
        dep.append(i)
        print ('Warning ! Plane#',i+1,'is ill-Conditioned!!')
if dep!=[]:
    if ck.confirm('Do you wish to eliminate the ill-conditioned plane?'):
        ALPHA=np.delete(ALPHA,dep,1)
        N=N-len(dep)
    printmat(ALPHA)


# =============================================================================
# # SAVE IC MATRIX
# =============================================================================

def savemat():
    while ck.confirm("Do You wish to save the Influence Coefficient Matrix"):
        try:
               name=ck.prompt("What is the project name", type=str)
               np.savetxt(name+'.csv',  ALPHA.copy().view(float).reshape(M,N*2))
               print('Matrix Saved...!')
               break
        except IOError:
            print(" Error Saving......!!")
            print()
            continue

savemat()



# ==============================================================
# # Calculate the ERROR    
# =============================================================================
def error(x):
     E=max(abs(np.add(np.matmul(ALPHA,x.value),A)))
     return E


# =============================================================================
# # Printing the data
# =============================================================================
def PHASE(x):
    PHASE=cm.phase (x)*180/cm.pi
    if PHASE<0:
            PHASE= PHASE+360
    return PHASE
if ck.confirm("Calculate with ALL trial mass kept on shaft?"):
    def prnt(W):
        
        for i in range (N):
            print("Correction at plane #",i+1,"=  ", "%5.2f" %abs((W.value+U).item(i)),"grams and in an angle of", "%4.1f" %(PHASE((W.value+U).item(i))),"degrees") 
else:
    def prnt(W):
        for i in range (N):
            print("Correction at plane #",i+1,"=  ", "%5.2f" %abs(W.value.item(i)),"grams and in an angle of", "%4.1f" %(PHASE(W.value.item(i))),"degrees") 
            
            
            
# =============================================================================
# =============================================================================
# # #### SPLITTING
# =============================================================================
# =============================================================================
def Split(W):

    print()
    print()
    print("***********************")
    print("SPLITTING CONSTRAINTS")
    print("***********************")  
    print()
    # =============================================================================
    #     ## Nh   ...........get Available holes for spiltting
    # =============================================================================
    def get_H_angles():
        Nh= ck.prompt("How many Candidate holes available for splitting?",type=int)
        while Nh<1 : 
            print('At least on hole should be available')
            Nh= ck.prompt("How many Candidate holes available for splitting?",type=int)
            continue
   
        H_angles=[]
        for i in range (Nh):
            h_angle= ck.prompt("Enter the angle of hole available for for splittling",type=float)
            while h_angle<0 or h_angle>360 : 
                print('Enter angle between 0-360')
                Nh= ck.prompt("Enter the angle of hole available for for splittling",type=float)
                continue
            
            H_angles.append(h_angle) 
          
        H_angles=np.array(H_angles)
        return H_angles,Nh
            
    # =============================================================================
    #     ## Nw   ...........get Available weight for balancing
    # =============================================================================
    def get_W_tpes():
        Nw= ck.prompt("How many weights types  available for splitting?",type=int)
        while Nw<1 : 
            print('At least on weight type should be available')
            Nw= ck.prompt("How many weights types  available for splitting?",type=int)
            continue
        W_types=[]   # List of the available holes angles
        for i in range (Nw):
            w_type= ck.prompt('Enter weight type available for splitting',type=float)
            while w_type<0 : 
                print('Enter valid weight type in grams')
                w_type= ck.prompt('Enter weight type available for splitting',type=float)
                continue
            W_types.append(w_type)
        W_types=np.array(W_types)
        return W_types,Nw 
    
    # =============================================================================
    #         # MATRIX OF WEIGHTS AT EVERY LOCATION
    # =============================================================================
    H_angles,Nh=get_H_angles()
    W_types,Nw =get_W_tpes()
    W_MAT=[]
    for i in range (Nw):
        Vc_row=[]
        for j in range(Nh):
            Vc_element=cm.rect(W_types[i],H_angles[j]*cm.pi/180 )
            Vc_row.append(Vc_element)
        W_MAT.append(Vc_row)
    Vc_row=[]
    W_MAT=np.array(W_MAT)
    # =============================================================================
    #     # Define the objecive function
    # =============================================================================
 
    
    S = cp.Variable((Nw,Nh), boolean=True)
    
    
    
    Real=cp.norm((cp.sum(cp.multiply(np.real(W_MAT),S))-np.real(W)))
    Imag=cp.norm((cp.sum(cp.multiply(np.imag(W_MAT),S))-np.imag(W)))

    
    Residules=cp.norm(cp.hstack([Real, Imag]), 2)
    obj_split= cp.Minimize(Residules)

    # =============================================================================
    #     # Set thelver  CONSTRAINTS
    # =============================================================================
    Nh_max= ck.prompt('Enter maximum number of weights per hole',type=int)
    Const1=[cp.sum(S,axis=0)<=Nh_max]
    # =============================================================================
    #     # Solve the poblem
    # =============================================================================
    Prob_S=cp.Problem(obj_split,Const1)
    Prob_S.solve(solver=cp.ECOS_BB)
    S=np.array(np.round(S.value))
    # =============================================================================
    #     # PRINTING RESULTS
    # =============================================================================
    print('PLANE #',N)
    print('----------------')
    for i in range (Nw):
        for j in range(Nh):
                if S[i,j]>0 :
                    print (W_types[i],'grams @',H_angles[j],'degrees')
                else:
                    print('')
    
    print ('Error in Splitting the weight vector',round(Prob_S.value,2))
    return S



# =============================================================================
# # Call for split function
# =============================================================================
def Call_Split(W):
    while ck.confirm('Do you Wish to split?'):
        split_plane=ck.prompt('Which Plane to split weight',type=int)
        while split_plane<1 or split_plane>N:
            print('please enter a number between 1-',N)
            split_plane=ck.prompt('Which Plane to split weight',type=int)
            continue
        Split(W[split_plane-1].value)
        
        
        
        
# =============================================================================
# =============================================================================
# # #USING CVXPY LEAST SQUARES TO SOLVE THE PROBLEM
# =============================================================================
# =============================================================================
                
W=cp.Variable((N,1),complex=True)
objective=cp.Minimize(cp.sum_squares(ALPHA*W+A))
prob=cp.Problem(objective)
prob.solve()
print("Residule Squares")
print("-----------------")
print("Maximum Residual Error =","%.2f" %error(W))
prnt(W)
print ("Expected residual Array")
print(np.round(abs(np.add(np.matmul(ALPHA,W.value),A)),2))

Call_Split(W)        
    
# =============================================================================
# =============================================================================
# # # SOLVING USING MIN-MAX 
# =============================================================================
# =============================================================================

print("")
print("")
print("MIN-MAX")
print("-----------------") 
 
W2=cp.Variable((N,1),complex=True)    
objective2=cp.Minimize(cp.norm((ALPHA*W2+A),"inf"))
prob2=cp.Problem(objective2)
prob2.solve()
print("Maximum Residual Error =","%.2f" %error(W2))  
prnt(W2)
print ("Expected residual Array")
print(np.round(abs(np.add(np.matmul(ALPHA,W2.value),A)),2))
    
Call_Split(W2)   
# =============================================================================
# =============================================================================
# # # CONSTRAINTS MIN MAX
# =============================================================================
# =============================================================================
print()
print()
print("*******************")
print("CONSTRAINTS")
print("*******************")
if ck.confirm("Do you wish to put a limit for weights at each plane?"):
    wc=[]
    for i in range(N):
        
        while True:
            try:
                print("Enter MAX weight at plane#",i+1)
                wc.append(float(input()))
            except :
                print("Please Enter Valid Data!")
            else:
                break 
    const=[]
    const +=   [cp.norm(W2[i])<=wc[i]for i in range (N) ]
    prob3=cp.Problem(objective2,const)
    prob3.solve()
    print("Maximum Residual Error =","%.2f" %error(W2))  
    prnt(W2)
    print ("Expected residual Array")
    print(np.round(abs(np.add(np.matmul(ALPHA,W2.value),A)),2))

Call_Split(W2)   

# =============================================================================
# =============================================================================
# # # CONSTRAINTS LMI DEFINE NON-CRITICIAL PLANES MAX VIBRATION
# =============================================================================
# =============================================================================
print()
print()
print("*******************")
print("NON CRITICAL PLANES")
print("*******************")
def LMI():

    Lcr= ck.prompt("How many Critical planes in the problem?",type=int)
    while Lcr>L or Lcr<1: 
        print('Enter a number between 1-',L)
        Lcr= ck.prompt("How many Critical planes in the problem?",type=int)
        continue

    List_cr=[]
    List_Ncr=[]
    
    
    
    
    
    def get_List(Critical_Plane,K,L):
        for i in range (K):
            List_cr.append(Critical_Plane+L*i)            
        return   List_cr

    

    for i in range (Lcr):
        Critical_Plane= ck.prompt("Insert the Critical Plane index", type=int)
        while Critical_Plane>L or Critical_Plane<1:
            print('Enter a number between 1-',L)
            Critical_Plane= ck.prompt("Insert the Critical Plane index", type=int)
            
        List_cr=get_List(Critical_Plane,K,L)
    List=[x+1 for x in range (M)]
    List_Ncr=[x for x in List if x not in List_cr]
            
            
    # =============================================================================
    #     #Construct The critical and non critical Matricies
    # =============================================================================
        
    
    # Acr RETURNS ERROR WHEN L=1!!!!

    ALPHAcr=[]
    Acr=[]
    ALPHAncr=[]
    Ancr=[]
    for i in range (len(List_cr)):
        ALPHAcr.append(ALPHA[List_cr[i]-1])
        Acr.append(A[List_cr[i]-1])
    for i in range(len(List_Ncr)):
        ALPHAncr.append(ALPHA[List_Ncr[i]-1])
        Ancr.append(A[List_Ncr[i]-1])
    ALPHAcr=np.array(ALPHAcr)
    Acr=np.array(Acr)
    ALPHAncr=np.array(ALPHAncr)
    Ancr=np.array(Ancr)
    
    
    
    
    
    Vm= ck.prompt("Insert the maximum vibration for NON-critical sensors",type=float)
    
    #SOLVING USING LMI 
    wc=[]
    for i in range(N):
        
        while True:
            try:
                print("Enter MAX weight at plane#",i+1)
                wc.append(float(input()))
            except :
                print("Please Enter Valid Data!")
            else:
                break 

    W4R=(cp.Variable((N,1)))
    W4I= (cp.Variable((N,1)))
    
    
    
    
    
    
        
    RRfcr=cp.diag(np.real(Acr)+np.real(ALPHAcr)@W4R-np.imag(ALPHAcr)@W4I)
    IRfcr=cp.diag(np.imag(Acr)+np.imag(ALPHAcr)@W4R+np.real(ALPHAcr)@W4I)

    RRfNcr=cp.diag(np.real(Ancr)+np.real(ALPHAncr)@W4R-np.imag(ALPHAncr)@W4I)
    IRfNcr=cp.diag(np.imag(Ancr)+np.imag(ALPHAncr)@W4R+np.real(ALPHAncr)@W4I)
    
    
    Vc=cp.Variable()
   
    
    
    zcr=np.zeros((RRfcr.shape[0],RRfcr.shape[1]))
    Icr=np.eye(RRfcr.shape[0])
    zncr=np.zeros((RRfNcr.shape[0],RRfNcr.shape[1]))
    Incr=np.eye(RRfNcr.shape[0])
    
    
    
    objective4=cp.Minimize(Vc)
    
    LMI1 =cp.bmat( [   
                            [Vc*Icr,        RRfcr,    zcr,        -IRfcr],
                            [RRfcr,          Icr,      IRfcr,          zcr],    
                            [zcr,            IRfcr,    Vc*Icr,        RRfcr],
                            [-IRfcr,         zcr,       RRfcr,          Icr]      
                                                                                ]) 
    LMI2 =cp.bmat( [   
                        [Vm**2*Incr,        RRfNcr,    zncr,        -IRfNcr],
                        [RRfNcr,          Incr,      IRfNcr,          zncr],
                        [zncr,            IRfNcr,    Vm**2*Incr,        RRfNcr],
                        [-IRfNcr,         zncr,       RRfNcr,          Incr]      
                                                                            ])
    const_LMI_w=[]
    
    for i in range(N):
        LMI3 =cp.bmat( [   
                            [wc[i]**2,        W4R[i],    0,        -W4I[i]],
                            [W4R[i],          1,      W4I[i],          0],
                            [0,       W4I[i],    wc[i]**2,        W4R[i]],
                            [-W4I[i],         0,       W4R[i],          1]      
                                                                                      ])
        const_LMI_w.append(LMI3>>0)
    const_LMI_w.append( LMI1  >>0)
    const_LMI_w.append( LMI2 >>0)
    
       
                 
    prob4=cp.Problem(objective4,const_LMI_w)
    prob4.solve(solver=cp.CVXOPT, kktsolver=cp.ROBUST_KKTSOLVER)
    return W4R,W4I
  
if ck.confirm("Do you wish to put a maximum vibration limits for non critical Vibration Sensors?"):
    
    while True:
        try:
            W4R,W4I=LMI() 
            W4 = W4R+W4I*1j
            print("")
            print("")
            print("LMI Influence Coefficient Method ")
            print("-----------------") 
            print("Maximum Residual Error =",error(W4))  
            prnt(W4)
            print ("Expected residual Array")
            print(np.round(abs(np.add(np.matmul(ALPHA,W4.value),A)),2))
            if ck.confirm('Try Again'):
                continue
            else:
                break
        except ValueError:
            print('Error in solution')
            print('')
            if ck.confirm('Try Again'):
                continue
            else:
                break
            continue

                    
Call_Split(W)   
