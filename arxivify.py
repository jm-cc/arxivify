import sys
import re
import os
import shutil

tex_to_be_processed=[]
tex_already_processed=[]
graphics_to_be_copied=[]
#If you have special files to be copied, just uncomment and modify this line 
graphics_to_be_copied=["ecrc.sty","elsevier-logo-3p.pdf","SDlogo-3p.pdf","elsarticle.cls","elsarticle-num.bst"] 

def usage():
    print("axivify.py <master_file>")
    print("Should be launched from <master_file> directory.")

def parse_file(filename):
    res=''
    with open(filename,'r') as f:
        for line in f:
            #Remove comments
            if line[0]=="%":
                continue
            if "%" in line and "\%" not in line:
                line=line.split("%")[0]+"\n"
            #Detect input/include
            pattern="\\\(input|include)\{(?P<file>.+)\}"
            match=re.search(pattern,line)
            if match:
                potential_file=match.group("file")
                if potential_file not in tex_already_processed+tex_to_be_processed:
                    tex_to_be_processed.append(potential_file)
            #Detect graphics
            pattern="\\\includegraphics(\[.+\])?\{(?P<file>.+)\}"
            match=re.search(pattern,line)
            if match:
                graphics_to_be_copied.append(match.group("file"))
            res+=line
    return res

def main(master_file):
    dest_directory="./arxivify"
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    if master_file.endswith(".tex"):
        master_file=master_file[:-4]
    tex_to_be_processed.append(master_file)

    while True:
        if not tex_to_be_processed:
            break
        file=tex_to_be_processed.pop()
        if not(file.endswith(".tex")):
            file+=".tex"
        tex_already_processed.append(file)
        new_text=parse_file(file)
        #Write modified file
        (dirname,filename)=os.path.split(file)
        dest=os.path.join(dest_directory,dirname)
        if not os.path.exists(dest):
            os.makedirs(dest)        
        fp=open(os.path.join(dest,file),'w')
        #Force PDFLatex
        if file==master_file+".tex":
            fp.write("\\pdfoutput=1\n")
        fp.write(new_text)
        fp.close()

    for g in graphics_to_be_copied:
        (dirname,filename)=os.path.split(g)
        dest=os.path.join(dest_directory,dirname)
        if not os.path.exists(dest):
            os.makedirs(dest)
        shutil.copy2(g,dest)

    #Add "<master_file>.bbl"
    if os.path.isfile(master_file+".bbl"):
        shutil.copy2(master_file+".bbl",dest_directory)

if __name__ == '__main__':
    if (len(sys.argv)!=2):
        usage()
    main(sys.argv[1])