import matplotlib.pyplot as plt
import os

def save_custom_plot(data, column, title, filename, output_dir='.'):
    """
    Saves a histogram plot.
    Default output_dir is '.' (current folder) to avoid path errors.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data[column].dropna(), bins=30, edgecolor='black')
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.grid(True)
    
    # Create folder if it doesn't exist
    if output_dir != '.':
        os.makedirs(output_dir, exist_ok=True)
        
    # Save the file
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()