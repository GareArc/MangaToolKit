import os
import shutil

def combine_subfolders(root_folder, k, destination_folder):
    subfolders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
    subfolders.sort(key=lambda f: int(''.join(filter(str.isdigit, f)))) # Sort subfolders alphabetically
    # print(subfolders)
    # exit()

    if not subfolders:
        print(f"No subfolders found in '{root_folder}'.")
        return

    num_combined_folders = (len(subfolders) + k - 1) // k  # Calculate the number of combined folders

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for i in range(num_combined_folders):
        combined_folder_name = f"combined_{i+1}"
        combined_folder_path = os.path.join(destination_folder, combined_folder_name)
        os.makedirs(combined_folder_path)

        start_index = i * k
        end_index = (i+1) * k
        selected_subfolders = subfolders[start_index:end_index]

        for subfolder in selected_subfolders:
            subfolder_path = os.path.join(root_folder, subfolder)
            if os.path.exists(subfolder_path):
                prefix = os.path.basename(subfolder)
                for root, dirs, files in os.walk(subfolder_path):
                    for file in files:
                        src_path = os.path.join(root, file)
                        dst_filename = prefix + '_' + file
                        dst_path = os.path.join(combined_folder_path, dst_filename)
                        shutil.copy(src_path, dst_path)
            else:
                print(f"Subfolder '{subfolder_path}' does not exist.")

# Example usage:
root_folder = './imgs/亲爱的我饱含杀意'  # Root folder containing subfolders
k = 10  # Number of subfolders to combine into one folder
destination_folder = 'combined_folders'  # Destination folder where the combined folders will be created

combine_subfolders(root_folder, k, destination_folder)
