import matplotlib
import matplotlib.pyplot as plt
import torch

BACKEND = "kitty"

if BACKEND == "kitty":
    matplotlib.use("module://matplotlib-backend-kitty")


def plot_from_tensor(tensor: torch.Tensor, crop_range: bool = True) -> None:
    tensor = tensor.detach().permute(1, 2, 0).cpu().numpy()
    if crop_range:
        tensor = (tensor - tensor.min()) / (tensor.max() - tensor.min())
    plt.figure()
    plt.imshow(tensor)
    plt.show()
    plt.close()
