# Git LFS (Git Large File Storage)
As you know, Git is a version control system (i.e tracks file verisions). Most files people work with while using Git are smaller, such as the majority of files in this repository. However, sometimes you'll need to work with large files (think many megabytes or gigabytes). In such a case, you'll need to use Git LFS ("Large File Storage"). If you're in the model group for this project, you may notice that the `.gz` files in `/model/data` are only like 133 bytes of text data instead of the expected data. If so, you'll need to use **git-lfs** to pull the large files. If not, you already have Git LFS installed and it pulled the full file size the first time and subsequently you're good to go.

### Example Large File Not Downloaded
```
version https://git-lfs.github.com/spec/v1
oid sha256:a950e0536a3f9c60021b7a9dd4cd2cc717d6dc90ab24c7a5645769df190af7ce
size 29403751
```

# Pulling Large Files with Git LFS
Once you have Git LFS installed:
1. `git lfs fetch`
2. `git lfs pull`
3. Check the large files and ensure they downloaded correctly

# Linux Installation (DNF)
1. `dnf install git-fls`

# Mac and Windows
Checkout this website: https://git-lfs.com/