import os

import numpy as np
import matplotlib.pyplot as plt
import imageio


# Define the function and its derivative (gradient)
def f(x):
    return x ** 2 / 3


def df(x):
    return 2 * x / 3


# Gradient descent parameters
learning_rate = 0.4
initial_position = 3  # Starting position of the ball

# Create a grid of points for plotting the function
x = np.linspace(-3, 3, 100)
y = f(x)

# Create a list to store the frames
frames = []

frames_folder = 'frames'
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# Perform gradient descent and generate the frames for the GIF
position = initial_position
deltapos = 1
i = -5
while abs(deltapos) > 0.001:
    # Update the position of the ball using gradient descent

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y, label='y = 2 * x / 3')
    ax.scatter(position, f(position), color='red', label='Error Rate')
    ax.set_ylim(-0.1, 3.1)
    ax.set_title(f'Learn rate: {learning_rate} Iteration: {max(1, i - 5)}')
    i += 1
    ax.legend()
    if i > 0:
        deltapos = learning_rate * df(position)
        position -= deltapos

    # Save the current frame
    filename = os.path.join(frames_folder, f'frame_{i}.png')
    plt.savefig(filename)
    plt.close()
    frames.append(imageio.imread(filename))

# Create the GIF
imageio.mimsave(f'gradient_descent_animation_{learning_rate}.gif', frames, fps=15)
