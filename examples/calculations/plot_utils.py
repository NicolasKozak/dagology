from scipy.optimize import curve_fit
from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)  
    
plot_markers = ['o', '*', '^', 'v', 's', '+', 'x', 'D', 'p', '8']

########################
# Plotting graphs
########################
    
def plot_power_law_fit(n_range, y, errors=None, power=None, title="", x_label="Number of nodes N", y_label="Path weight", legend=True, figsize=(8,6)):
    plt.figure(figsize=figsize)
    # Define the power law function
    if power is not None:
        power_law = lambda x, a: a + power*np.log(x)
    else:
        power_law = lambda x, a, power: a + power*np.log(x)

    # Fit the power law function to the data
    n_range = n_range.astype('float64')
    params, pcov = curve_fit(power_law, n_range, np.log(y))
    a_fit = np.exp(params[0])

    if power is None:
        power = params[1]
        print(f'Fitted power: {params[1]: .4f} +-{np.sqrt(np.diag(pcov))[1]: .4f}')

    # Plot the original data and the fitted power law
    plt.scatter(n_range, y, marker='.')
    if errors is not None:
        plt.errorbar(n_range, y, yerr=errors, fmt='none', capsize=5)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(n_range, a_fit*pow(n_range, power), label=r'Power law fit: $L=%.2f \cdot N^{%.2f}$' % (a_fit, power), color='red')
    if legend:
        plt.legend()
    # Set log-log scale
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    
def plot_histogram(x, density=False, bins=50, title="", x_label="", y_label="", add_vertical_lines=True, beta_fit=False, figsize=(8, 6)):
    if not y_label:
        y_label = "Density" if density else "Frequency"
    
    plt.figure(figsize=figsize)
    plt.hist(x, density=density, bins=bins, edgecolor='black')

    if add_vertical_lines:
        # Add dashed vertical lines at ±45 degrees
        plt.axvline(np.radians(45), color='r', linestyle='--', label=r'Angle $= \pm \pi/4$')
        plt.axvline(-np.radians(45), color='r', linestyle='--')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if beta_fit:
        # Fit beta distribution to the given data
        params = beta.fit(x)

        # Print the parameters of the fitted beta distribution
        print("Fitted Beta Distribution Parameters:")
        print(f"alpha = {params[0]: .4f}")
        print(f"beta = {params[1]: .4f}")
        print(f"loc = {params[2]: .4f}")
        print(f"scale = {params[3]: .4f}")

        # Plot the fitted beta distribution
        eps = 0.01
        x_lin = np.linspace(np.min(x) + eps, np.max(x) - eps, num=100)
        beta_fit = beta.pdf(x_lin, *params)
        plt.plot(x_lin, beta_fit,  color='orange', label=r'Beta distribution fit: $\alpha = %.3f$, $\beta = %.3f$' % (params[0], params[1]))
        plt.legend()
    plt.show()


def propagate_relative_error(f, a, b, a_std, b_std):
    """Computes the standard deviation of f by adding relative uncertainties of a and b."""
    return np.abs(f) * np.sqrt((a_std / a)**2 + (b_std / b)**2)