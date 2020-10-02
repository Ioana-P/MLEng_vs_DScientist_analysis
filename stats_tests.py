from scipy import stats
import numpy as np
import pandas as pd
from statsmodels.stats.power import TTestIndPower, TTestPower
import seaborn as sns
import matplotlib.pyplot as plt


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


def compare_pval_alpha(p_val, alpha):
    """Return a string status regarding whether the p value is greater than alpha or not
    p_val - the p-value obtained from a t-statistical test;
    alpha - our declared value of alpha for this hypothesis"""
    status = ''
    if p_val >= alpha:
        status = "Fail to reject"
    else:
        status = 'Reject'
    return status


def pool_var(sample1, sample2):
    # Calculates the pooled variances for two samples
    return ((len(sample1)-1)*np.var(sample1) + (len(sample2)-1)*np.var(sample2))/(len(sample1) + len(sample2) - 2)




def welch_t(sample1, sample2):
    """Calculates the t-statistic using Welch's Test; returns a positive float"""
    numerator = np.mean(sample1) - np.mean(sample2)   
    denominator = np.sqrt(np.var(sample1)/len(sample1) + np.var(sample2)/len(sample2))
    return np.abs(numerator/denominator)    

def Cohen_d(expr_sample, ctrl_sample):
    diff = expr_sample.mean() - ctrl_sample.mean()
    pooled_variance = pool_var(expr_sample, ctrl_sample)
    # Calculate Cohen's d statistic
    d = diff / np.sqrt(pooled_variance)
    
    return d

def welch_dof(sample1,sample2):
    """Calculates the degrees of freedom for Welch's T-test"""
    s1 = np.var(sample1)
    s2 = np.var(sample2)
    n1 = len(sample1)
    n2 = len(sample2)
    
    num = (s1/n1 + s2/n2)**2
    denom = (s1/n1)**2/(n1-1) + (s2/n2)**2/(n2-1)
    return num/denom

def p_val(t_stat, df):
    """Calculates the p value by calculating the complement of the cumulative density t-function using our
    degrees of freedom"""
    return 1-stats.t.cdf(t_stat,df)


def plot_dists(sample_list, label_list, colours_list, figsize = (8,8)):
    plt.figure(figsize=figsize)
    x = sns.distplot(sample_list[0],color=colours_list[0], bins=10, label=label_list[0])
    y = sns.distplot(sample_list[1], color=colours_list[1], bins=10, label=label_list[1])
    lines = plt.vlines([np.mean(sample_list[0]),np.mean(sample_list[1])],ymin=0, ymax=0.00005, label='Mean values')
    return x,y,lines,plt.legend()


def visualize_one_side_t(t_stat, dof):
    # initialize a matplotlib "figure"
    fig = plt.figure(figsize=(15,10))
    ax = fig.gca()
    # generate points on the x axis between -4 and 4:
    xs = np.linspace(-1.05*t_stat,1.05*t_stat,200)
    # use stats.t.pdf to get values on the probability density function for the t-distribution
    ys = stats.t.pdf(xs, dof, 0, 1)
    ax.plot(xs, ys, linewidth=3, color='darkblue')

    # Draw one sided boundary for critical-t
    ax.axvline(x=+t_stat, color='red', linestyle='--', lw=3,label='t-statistic')
    ax.legend()
    plt.title(f'Visualizing our t - statistic : {t_stat}')
    plt.show()
    return 

def hypothesis_test(sample1, sample2, 
                        variable,
                        sample1_label, sample2_label,
                        sample1_colour, sample2_colour,
                        alpha = 0.05, figsize=(8,8)):
    """
    This hypothesis test should take in experimental (sample1) and control samples (sample2) and the variable column
    within those dfs which we wish to compare. Panda Dataframes/Series are expected. 
    This function will take num_samples amount of random samples (using np.random.choice) from the data, each of 
    size = sample size, and return a distribution of the sample means. Thus we gain a normal distribution. 
    The function will then calculate Welch's T-test, degrees of freedom, the p-value and determine if the null hypothesis
    can be rejected or not, and if it can, what is the effect size of the experimental sample. 
    sample1 - the experimental sample / post-intervention sample (pd.Dataframe / pd.Series)
    sample2 - the control sample (pd.Dataframe / pd.Series)
    alpha - your chosen alpha value (float)
    variable - which column in both samples is to be compared (string)
    num_samples - how many random samples should be taken from each of the data (int)
    sample_size - how large should each random sample be (int)
    
    returns the status (string)
    """
    
    
    # Get data for tests   data, y_var, n_samples, sample_size
#     test_sample1 = gen_dist_sample_means(sample1, y_var=variable, n_samples=num_samples, sample_size=sample_size)
#     test_sample2 = create_sample_dists(data=sample2, y_var=variable, n_samples=num_samples, sample_size=sample_size)
    
    test_samples = [sample1, sample2]
    test_samples_labels = [sample1_label, sample2_label]
    test_samples_colours = [sample1_colour, sample2_colour]
    
    
    plot_dists(test_samples, test_samples_labels, test_samples_colours, figsize)
    
    
    t_statistic = welch_t(sample1, sample2)
    
    dof = welch_dof(sample1, sample2)
    
    p_value = p_val(t_stat = t_statistic, df = dof)
    
    ###
    # Main chunk of code using t-tests or z-tests, effect size, power, etc
    ###
    power_analysis = TTestIndPower()
    
    # starter code for return statement and printed results
    status = compare_pval_alpha(p_value, alpha)
    assertion = ''
    if status == 'Fail to reject':
        assertion = 'cannot'
    else:
        assertion = "can"
        coh_d = Cohen_d(expr_sample=sample1, ctrl_sample=sample2)
        power = power_analysis.solve_power(effect_size=coh_d, nobs1=len(sample1), alpha=alpha)

    
    
    
    # Here we generate our final statement on whether our null hypothesis can be rejected or not and what 
    # our effect size is, if the H0 is rejected.

    print(f'Based on the p value of {p_value} and our alpha of {alpha} we {status.lower()}  the null hypothesis.'
          f'\n Due to these results, we  {assertion} state that there is a difference between our samples ')

    if assertion == 'can':
        print(f"with an effect size, Cohen's d, of {str(round(coh_d,3))} and power of {power}.")
    else:
        print(".")
    
    plt.savefig(f'fig/hypothesis_test_1_{variable}.jpg')
    print("Returned the following items (in order): status, assertion, cohen's d, t-statistic, degress of freedom")
    return (status, assertion, coh_d, t_statistic, dof)