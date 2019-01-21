#!/usr/bin/python

import getopt
import sys
import os
import easywebdav as ew
# import urllib.parse

def main(argv):
    username = ''
    password = ''
    inputfiles = ''
    outputfiles = ''
    usage = 'main.py -u <username> -p <password> -i <input> -o <output>'
    try:
        opts, args = getopt.getopt(argv, "h:u:p:i:o:", ["user=", "password=", "input=", "output="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-u", "--users"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-i", "--input"):
            inputfiles = arg
        elif opt in ("-o", "--output"):
            outputfiles = arg
    return username, password, inputfiles, outputfiles


def list_local_objects(location):
    files = []
    try:
        if os.path.isfile(location):
            files.append(location)
        elif os.path.isdir(location):
            for root, dirnames, filenames in os.walk(location):
                for f in filenames:
                    files.append(os.path.join(root, f))
    except FileNotFoundError:
        print("Input directory or file was not found: ", location)
        sys.exit(2)
    return [f.replace('\\','/') for f in files]


def webdav_connect(u, pw):
    try:
        webdav = ew.connect(
            host=u + '.stackstorage.com',
            path='remote.php/webdav',
            username=u,
            password=pw,
            protocol='https',
            port=443,
            verify_ssl=True
        )
        webdav.exists('')
        return webdav
    except Exception as e:
        print('Webdav connection could not be created!')
        print(u + '.stackstorage.com', 'remote.php/webdav', u, pw, 'https', 443, True)
        print(e)
        sys.exit(2)


def files_to_dirs(files):
    return list(set(['/'.join(str(f).split('/')[:-1]) for f in files]))


if __name__ == "__main__":
    username, password, inputfiles, outputfiles = main(sys.argv[1:])
    try:
        # Collect files that exist in webdav location
        wd = webdav_connect(username, password)
        # remote_files = [urllib.parse.unquote(obj.name.strip('/')) for obj in wd.ls(outputfiles)]

        # Collect Local Files to upload
        local_files = list_local_objects(inputfiles)

        # Create dirs based on local
        # Strip root from local files
        print("\n------------------------\nCreating new directories\n------------------------\n")
        dirs = [d.replace(inputfiles, '').strip('/') for d in files_to_dirs(local_files)]
        no_of_new_dirs = 0
        for d in dirs:
            new_dir = outputfiles + "/" + d
            print("Creating directory: " + new_dir)
            if not wd.exists(new_dir):
                wd.mkdirs(new_dir)
                no_of_new_dirs += 1

        # Uploading to destination files
        print("Start uploading")
        files = [(f, f.replace(inputfiles, '').strip('/')) for f in local_files]
        no_of_files = 0
        no_of_mbs = 0
        no_of_fails = 0
        for f in files:
            u_file = f[0]
            u_file_size = os.stat(u_file).st_size / 10 ** 6
            d_file = outputfiles + "/" + f[1]
            print("Uploading file: " + u_file + ", Destination file: " + d_file + ", Filesize: " + str(round(u_file_size)) + "MB")
            try:
                wd.upload(u_file, d_file)
            except Exception as e:
                print("Failed: " + u_file)
                no_of_fails += 1
                continue
            no_of_files += 1
            no_of_mbs += u_file_size

        # Final report
        print("\n------------------\nUpload completed!!\n------------------\n")
        print("Number of directories created: " + str(no_of_new_dirs))
        print("Number of files uploaded: " + str(no_of_files))
        print("Number of files failed: " + str(no_of_fails))
        print("MB's uploaded: " + str(round(no_of_mbs)))
    except Exception as e:
        print("Something went wrong, oops!")
        print(e)
        sys.exit(2)
    print("Program executed succesfully")
    sys.exit(0)