import numpy as np

# Is @apositiveint a square number?
def is_square(apositiveint):
    x = apositiveint // 2
    seen = set([x])
    while x * x != apositiveint:
        x = (x + (apositiveint // x)) // 2
        if x in seen:
            return False
        seen.add(x)
    return True

# Do a linear fit, returning the square of the gradient and the sum of the residuals
def do_fit (lx, ly):
    A = np.vstack([lx, np.ones(len(lx))]).T
    out = np.linalg.lstsq (A, ly, rcond=None)
    m, c = out[0]
    gradsq = (m*m)
    resid = 0.0
    if out[1].size > 0:
        resid = out[1][0]
    return gradsq, resid

# What does this want to do? Return, for a given timestep (or for every timestep), the average verticalness of the lines of best fit to groups of centres.
def domcentres_analyse (dc, isvert=True):

    sos_gradients = []
    summed_residuals = []
    numt = np.shape(dc)[0]
    N = int(np.shape(dc)[1])
    # is N a square number?
    if is_square(N) == False:
        print ('domcentres_analyse current coded only for square arrays of domains (could be fixed)')
        return sos_gradients, summed_residuals
    n = int(np.sqrt(N))

    tt = 0 # timepoint
    while tt < numt:
        # sum of the square of the gradient for all 5 in a column
        sos_gradient = 0.0
        # The sum of the residuals for 5 linear fits
        sum_resid = 0.0
        if isvert:
            for i in range(0,N,n):
                # Note: Swap around x and y, so that truly vertical lines will come out with m=0 (approx)
                ly = dc[tt,i:n+i,0] # x
                lx = dc[tt,i:n+i,1] # y
                gradsq, resid = do_fit (lx, ly)
                sos_gradient = sos_gradient + gradsq
                sum_resid = sum_resid + resid
        else:
            for i in range(0,n):
                # For n=5; if i=0, indices: 0,5,10,15,20
                #          if i=1, indices: 1,6,11,16,21 etc.
                lx = dc[tt,i:N-n+1+i:n,0] # x
                ly = dc[tt,i:N-n+1+i:n,1] # y
                gradsq, resid = do_fit (lx, ly)
                #print ('gradsq: {0}, resid: {1}'.format(gradsq, resid))
                sos_gradient = sos_gradient + gradsq
                sum_resid = sum_resid + resid

        print ('Sum of squared gradients: {0}, sum of residuals: {1}'.format (sos_gradient, sum_resid))
        # For this time-point, append the sum of the squared gradients
        # - closer to 0 means closer to a perfect, rectangular grid
        sos_gradients.append (sos_gradient)
        # For this time-point, append the sum of the
        # residuals. Smaller means better aligned centroids.
        summed_residuals.append (sum_resid)

        tt = tt + 1

    return sos_gradients, summed_residuals
