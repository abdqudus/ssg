import os, shutil
import sys
from generate import generate_pages_recursive
def main():
    basepath = sys.argv[0] or '/'

    def clear_directory_contents(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)  # Remove files or symbolic links
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path) 

    def cpy_files(src,dest):
        if(os.path.exists(dest)):
            clear_directory_contents(dest)
        cpy_list = os.listdir(src)
        for path_segment in cpy_list:
            new_src = os.path.join(src,path_segment)
            # check if object to copy is a file or folder
            isFile = os.path.isfile(new_src)
            if isFile:
                shutil.copy(new_src,dest)
            else:
                new_dest = os.path.join(dest,path_segment)
                os.mkdir(new_dest,0o777)
                cpy_files(new_src, new_dest)

                
    current_path = os.getcwd()
    static = os.path.join(current_path,"static")
    docs = os.path.join(current_path,'docs')

    template_path = os.path.join(current_path,'template.html')
    dest_path = os.path.join(current_path,"docs")
    from_path = os.path.join(current_path,'content')

    cpy_files(static,docs)
    generate_pages_recursive(from_path, template_path,dest_path,basepath)

    
main()

