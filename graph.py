import matplotlib.pyplot as plt

# read all content from the file "Train_DETR.txt"
contents = ""
with open("Train_DETR.txt", "r") as f:
    contents = f.read()
    f.close()

# APs and ARs
APs = [[] for _ in range(6)]
ARs = [[] for _ in range(6)]

# (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ]
# (AP) @[ IoU=0.50      | area=   all | maxDets=100 ]
# (AP) @[ IoU=0.75      | area=   all | maxDets=100 ]
# (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ]
# (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ]
# (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ]
# (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ]
# (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ]
# (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ]
# (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ]
# (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ]
# (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ]
AP_labels = ["AP\n(IoU=0.50:0.95, area=all, maxDets=100)",
                "AP\n(IoU=0.50, area=all, maxDets=100)",
                "AP\n(IoU=0.75, area=all, maxDets=100)",
                "AP\n(IoU=0.50:0.95, area=small, maxDets=100)",
                "AP\n(IoU=0.50:0.95, area=medium, maxDets=100)",
                "AP\n(IoU=0.50:0.95, area=large, maxDets=100)"]
AR_labels = ["AR\n(IoU=0.50:0.95, area=all, maxDets=1)",
                "AR\n(IoU=0.50:0.95, area=all, maxDets=10)",
                "AR\n(IoU=0.50:0.95, area=all, maxDets=100)",
                "AR\n(IoU=0.50:0.95, area=small, maxDets=100)",
                "AR\n(IoU=0.50:0.95, area=medium, maxDets=100)",
                "AR\n(IoU=0.50:0.95, area=large, maxDets=100)"]

# split the content by "\nEpoch"
contents = contents.split("\nEpoch")
for i, content in enumerate(contents):
    _content = content.split("\n")
    print(_content)
    print(f"Epoch {i}:")
    content = [float(str.split(" = ")[-1]) for str in content.split("\n")[-13:-1]]
    for j in range(6):
        APs[j].append(content[j])
        ARs[j].append(content[j + 6])

# print(APs)
# print(ARs)
for i in range(6):
    print(f"{AP_labels[i]}: {APs[i]}")
    print(f"{AR_labels[i]}: {ARs[i]}")

n_rows = 2
n_cols = 3

# Create 2 figures, one for APs and one for ARs
figAP, axsAP = plt.subplots(n_rows, n_cols, figsize=(10*n_cols, 20))
figAR, axsAR = plt.subplots(n_rows, n_cols, figsize=(10*n_cols, 20))

# n_rows = 1

# Adjust vertical spacing
figAP.subplots_adjust(hspace = 0.2)
figAR.subplots_adjust(hspace = 0.2)

# Setup subplots
for i in range(n_rows):
    for j in range(n_cols):
        axsAP[i, j].grid(True)
        axsAR[i, j].grid(True)
        axsAP[i, j].set_title(AP_labels[i * n_cols + j])
        axsAR[i, j].set_title(AR_labels[i * n_cols + j])
        axsAP[i, j].set_ylim([0, 1])
        axsAR[i, j].set_ylim([0, 1])

        x_ticks = [i for i in range(len(APs[0]))][::20]
        axsAP[i, j].set_xticks(x_ticks)
        axsAR[i, j].set_xticks(x_ticks)

        y_ticks = [0.1 * i for i in range(11)]
        axsAP[i, j].set_yticks(y_ticks)
        axsAR[i, j].set_yticks(y_ticks)

# Plot APs
for i in range(n_rows):
    for j in range(n_cols):
        axsAP[i, j].plot(APs[i * n_cols + j])
        # draw 2 horizontal lines at APs[i * n_cols + j][0] and APs[i * n_cols + j][-1]
        axsAP[i, j].axhline(y=APs[i * n_cols + j][0], color='r', linestyle='--')
        axsAP[i, j].axhline(y=APs[i * n_cols + j][-1], color='r', linestyle='--')

# Plot ARs
for i in range(n_rows):
    for j in range(n_cols):
        axsAR[i, j].plot(ARs[i * n_cols + j])
        # draw 2 horizontal lines at ARs[i * n_cols + j][0] and ARs[i * n_cols + j][-1]
        axsAR[i, j].axhline(y=ARs[i * n_cols + j][0], color='r', linestyle='--')
        axsAR[i, j].axhline(y=ARs[i * n_cols + j][-1], color='r', linestyle='--')

# Save figures
figAP.savefig("APs.png")
figAR.savefig("ARs.png")
