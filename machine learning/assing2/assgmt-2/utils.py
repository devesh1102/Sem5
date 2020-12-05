import numpy as np
 

def square_hinge_loss(targets, outputs):
  # Write thee square hinge loss here
  return 1.0

def logistic_loss(targets, outputs):
  # Write thee logistic loss loss here
  return 1.0

def perceptron_loss(targets, outputs):
  # Write thee perceptron loss here
  return 1.0

def L2_regulariser(weights):
    regulariser = 0
    for x in weights:
        regulariser = regulariser + [x]*[x]
    # Write the L2 loss here
    return regulariser

def L4_regulariser(weights):
    regulariser = 0
    for x in weights:
        regulariser =regulariser + [x]**4
    # Write the L4 loss here
    return regulariser

def square_hinge_grad(weights,inputs, targets, outputs):
    grad_array = []
    #inputs.insert(0, 1)
    f = 1
    for i in (weights):
        dummy = 0 
        x = 1
        for j in (outputs):
            if j*targets[x] < 1:
                temp = -2 * ( 1 - targets[x]*j)*input[x][f]* targets[x]
                dummy  = temp + dummy
                x=x+1 
        grad_array.append(dummy)
        f=f+1

  # Write thee square hinge loss gradient here

    return grad_array

def logistic_grad(weights,inputs, targets, outputs):
  # Write thee logistic loss loss gradient here
    grad_array = []
    inputs.insert(0, 1)
    f=1
    for i in (weights):
        dummy = 0 
        x = 1
        for j in (outputs):
            temp = -1 * targets[x]* input[x][f] /(1+ exp(-1*targets[x]*j))
            dummy  = temp + dummy
            x=x+1 
        grad_array.append(dummy)
        f= f + 1

  # Write thee square hinge loss gradient here

    return grad_array
    return 1.00

def perceptron_grad(weights,inputs, targets, outputs):
  # Write thee perceptron loss gradient here
  return np.random.random(11)

def L2_grad(weights):
    # Write the L2 loss gradient here
    return 0.00

def L4_grad(weights):
    # Write the L4 loss gradient here
    return 0.00

loss_functions = {"square_hinge_loss" : square_hinge_loss, 
                  "logistic_loss" : logistic_loss,
                  "perceptron_loss" : perceptron_loss}

loss_grad_functions = {"square_hinge_loss" : square_hinge_grad, 
                       "logistic_loss" : logistic_grad,
                       "perceptron_loss" : perceptron_grad}

regularizer_functions = {"L2": L2_regulariser,
                         "L4": L4_regulariser}

regularizer_grad_functions = {"L2" : L2_grad,
                              "L4" : L4_grad}
