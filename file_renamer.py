import os


def rename_files(folder_path, current, prefix=""):
    for filename in os.listdir(folder_path):
        old_name = os.path.join(folder_path, filename)
        new_name = os.path.join(folder_path, f"{prefix}{current:03d}.jpg")
        # os.rename(old_name, new_name)
        print(old_name, new_name)
        current += 1


def custom(folder_path, prefix=""):
    current = 1
    for filename in os.listdir(folder_path):
        old_name = os.path.join(folder_path, filename)
        if filename[0]=='c':
            new_name = os.path.join(folder_path, f"{prefix}{current:03d}.jpg")
            os.rename(old_name, new_name)
            print(old_name, new_name)
            current += 1


if __name__ == "__main__":
    folder_path = r"C:\Users\siqueira\Downloads\forbellone"
    custom(folder_path,'c')
    # rename_files(folder_path, 1,'a')
