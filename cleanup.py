#! /Library/Frameworks/Python.framework/Versions/3.11/bin/python3
import os
import subprocess
import shutil

PROJECT_DIR = "/home/andre/repos/github.com/sample-md-proj"

OUTPUT_DIR = f"{PROJECT_DIR}/docs"
RES_DIR = f"{PROJECT_DIR}/images"
SINGLE_FILE = f"{OUTPUT_DIR}/single_file.md"

bash_cmd_docx = f"pandoc --from=markdown --to=docx {
    SINGLE_FILE} -o single_file.docx"
bash_cmd_pdf = f"pandoc --from=markdown --to=pdf {
    SINGLE_FILE} -o single_file.pdf"
bash_cmd_html = f"pandoc -s --css=images/pandoc.css --from=markdown --to=html {
    SINGLE_FILE} -o single_file.html"


class HeaderStruct(object):
    def __init__(self):
        self.h1 = 0
        self.h2 = 0
        self.h3 = 0
        self.h4 = 0
        self.h5 = 0
        self.h6 = 0
        self.fig = 0

    def add_notation(self, text):
        new_text = ""
        if (text.startswith("# ")):
            self.h1 += 1
            self.h2 = 0
            self.h3 = 0
            self.h4 = 0
            self.h5 = 0
            self.h6 = 0
            self.fig = 0
            new_text = "\n# " + str(self.h1) + ". " + text[2:]
        elif (text.startswith("## ")):
            self.h2 += 1
            self.h3 = 0
            self.h4 = 0
            self.h5 = 0
            self.h6 = 0
            new_text = "## " + str(self.h1) + "." + \
                str(self.h2) + ". " + text[3:]
        elif (text.startswith("### ")):
            self.h3 += 1
            self.h4 = 0
            self.h5 = 0
            self.h6 = 0
            new_text = "### " + str(self.h1) + "." + \
                str(self.h2) + "." + \
                str(self.h3) + ". " + text[4:]
        elif (text.startswith("#### ")):
            self.h4 += 1
            self.h5 = 0
            self.h6 = 0
            new_text = "#### " + str(self.h1) + "." + \
                str(self.h2) + "." + \
                str(self.h3) + "." + \
                str(self.h4) + ". " + text[5:]
        elif (text.startswith("##### ")):
            self.h5 += 1
            self.h6 = 0
            new_text = "##### " + str(self.h1) + "." + \
                str(self.h2) + "." + \
                str(self.h3) + "." + \
                str(self.h4) + "." + \
                str(self.h5) + ". " + text[6:]
        elif (text.startswith("###### ")):
            self.h6 += 1
            new_text = "###### " + str(self.h1) + "." + \
                str(self.h2) + "." + \
                str(self.h3) + "." + \
                str(self.h4) + "." + \
                str(self.h5) + "." + \
                str(self.h6) + ". " + text[7:]

        return new_text

    def label_figure(self, text):
        self.fig += 1
        new_text = "!["
        new_text += "Figure "

        if self.h1 != 0:
            new_text += str(self.h1) + "."
        if self.h2 != 0:
            new_text += str(self.h2) + "."
        if self.h3 != 0:
            new_text += str(self.h3) + "."
        if self.h4 != 0:
            new_text += str(self.h4) + "."
        if self.h5 != 0:
            new_text += str(self.h5) + "."
        if self.h6 != 0:
            new_text += str(self.h6) + "."

        new_text += "f" + str(self.fig) + ": "

        ind = text.find("[")
        new_text += text[ind + 1:]

        return new_text


def print_single_file(file_name):
    process = subprocess.Popen(
        bash_cmd_docx.split(), stdout=subprocess.PIPE, cwd=OUTPUT_DIR)
    process = subprocess.Popen(
        bash_cmd_pdf.split(), stdout=subprocess.PIPE, cwd=OUTPUT_DIR)
    process = subprocess.Popen(
        bash_cmd_html.split(), stdout=subprocess.PIPE, cwd=OUTPUT_DIR)


def get_all_files(path):
    dir_list = os.listdir(path)

    dir_list.sort()
    return dir_list


def get_md_files(path):
    dir_list = get_all_files(path)
    new_list = []

    for file in dir_list:
        if file.endswith('.md'):
            new_list.append(file)

    new_list.sort()
    return new_list


def reset_output_file(output_file):
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            os.remove(output_file[:-3]+".docx")
            os.remove(output_file[:-3]+".pdf")
        except OSError:
            print("Failed to remove file.")
    else:
        print("The file does not exist.")

    file_list = get_all_files(RES_DIR)
    for file in file_list:
        shutil.copy(RES_DIR+"/"+file, OUTPUT_DIR+"/images")


def write_all_files(output_file, file_list):
    hstruct = HeaderStruct()

    for file in file_list:
        write_single_file(output_file, file, hstruct)


def write_single_file(output_file, input_file, hstruct):
    if os.path.exists(output_file):
        out = open(output_file, "a")

        with open(input_file, "r") as inp:
            for line in inp:
                if line.startswith("#"):
                    out.write(hstruct.add_notation(line).rstrip() + "\n")
                elif line.startswith("!["):
                    out.write(hstruct.label_figure(line).rstrip() + "\n")
                else:
                    out.write(line.rstrip() + "\n")

        out.close()
    else:
        out = open(output_file, "w")

        with open(input_file, "r") as inp:
            for line in inp:
                if line.startswith("#"):
                    out.write(hstruct.add_notation(line).rstrip() + "\n")
                else:
                    out.write(line.rstrip() + "\n")

        out.close()


def main():
    file_list = get_md_files(PROJECT_DIR)
    reset_output_file(SINGLE_FILE)

    write_all_files(SINGLE_FILE,  file_list)

    print_single_file(SINGLE_FILE)


if __name__ == '__main__':
    main()
