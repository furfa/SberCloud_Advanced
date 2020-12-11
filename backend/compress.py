import os
import sys
import subprocess

root = sys.path[0]
im_path = os.path.join(root, "static", "images")

for i in os.listdir(im_path):
    path = os.path.join(im_path, i)

    if path.endswith(".jpg"):
        subprocess.Popen(["jpegtran", "-copy", "none",
                          "-optimize", "-progressive", "-outfile", path, path])

    if path.endswith(".png"):
        subprocess.Popen(["optipng", "-o7", "-strip",
                          "all", "-out", path, path])

print(path)
