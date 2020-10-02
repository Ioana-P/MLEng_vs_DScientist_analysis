from scipy import stats
import numpy as np
import pandas as pd


def normality_test(distribution, alpha : float, printout=True):
    """Wrapper function for testing whether the distribution of values
    is a normal distribution.
    Params:
    distribution - (np array / list) our distribution of values
    alpha - (float) if our p-value is above apha then we cannot reject the null hypothesis
    Returns:
    statistic - (float) s^2 + k^2, returned by scipy.stats.shapiro
    p-value - (float) probability of observing the distribution given that
    the null hypothesis is true, returned by scipy.stats.shapiro. 
    The null hypothesis in question is that the numbers come from a normal distribution"""
    
    stat, p_val = stats.shapiro(distribution)
    if printout:
        if p_val < alpha:
            print("p-value is ", p_val)
            print("The null hypothesis can be rejected")
        else:
            print("p-value is ", p_val)
            print("The null hypothesis cannot be rejected")
        
    return stats, p_val

def subsample_to_normal(distribution, alpha : float, n_samples : int , n_max_iter : int, random_state=12345):
    """Function that samples from a distribution until it passes a 
    normality test (normality_test)
    Params:
    distribution - (np array / list) our distribution of values
    alpha - (float) if our p-value is above apha then we cannot reject the null hypothesis
    n_samples - (int) how many data points we'd like to have in our final distribution
    n_max_iter - (int) maximum number of times we'll attempt to subsample from before giving up
    Returns:
    normal_distribution_subsample - np array of value following a normal distribution    
    """
    
    if type(distribution)==list:
        distribution = np.array(distribution)
    for i in range(n_max_iter):
        new_dist = np.random.choice(distribution, n_samples, False)
        k, p_val = normality_test(new_dist, alpha, False)
        if p_val > alpha:
            print("p-value for this distribution is ", p_val)
            return new_dist
        
    print("Iterations timed out; could not generate a suitably normal distribution")
    return


def gen_dist_sample_means(distribution, n_samples : int, sample_size : int):
    """Function that samples from a distribution and creates a distribution of sample 
     means. Based on Central Limit theorem this should give us a normal distribution. 
    Params:
    distribution - (np array / list) our distribution of values
    n_samples - (int) how many data points we'd like to have in our final distribution
    sample_size - (int) how large is each sample that we average over
    Returns:
    normal_distribution_subsample - np array of value following a normal distribution    
    """
    new_dist = []
    for i in range(n_samples):
        sample = np.random.choice(distribution, sample_size)
        sample_mean = np.mean(sample)
        new_dist.append(sample_mean)
    return np.array(new_dist)