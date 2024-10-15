# Here is a guide for installing the scikit-learn surprise library. You should only need this guide if you are trying to run `build_colab_model.py`

To get the `scikit-surprise` library working, you will need a C++ compiler, you can first try and run 
```
pip install scikit-surprise
```
If this works, great! If not, keep reading this guide.

## For Windows

**Install Visual Studio Build Tools:** Download and install Microsoft Visual C++ Build Tools from the following link: [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

## For macOS

**Install Xcode Command Line Tools:** macOS comes with an integrated compiler via Xcode Command Line Tools. To install them, run:

```
xcode-select --install
```

**Verify the Compiler:** Once the installation is complete, check that the compiler is available:
```
gcc --version
```

## For Linux

**Install Build Essentials:** On Ubuntu or Debian, install the **build-essential** package, which includes the necessary C++ compiler:
```
sudo apt-get update
sudo apt-get install build-essential
```

**Verify the Compiler:** After installation, verify that g++ is installed:
```
g++ --version
```

# Install Surprise

Now that you have the necessary tools installed, you can install the **Surprise** library.

```
pip install scikit-surprise
```

You can now attempt to run `build_colab_model.py`, and hopefully `scikit-learn surprise` will be working.