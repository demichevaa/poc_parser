import re
import os
from typing import List

import pdfplumber

pdf = pdfplumber.open("./docs/sqlFoundation.pdf")

chapter_5 = slice(154, 184)
chapter_6 = slice(184, 317)
chapter_7 = slice(316, 396)
chapter_11 = slice(542, 753)



chapter_lines: List[str] = []
for page in pdf.pages[chapter_11]:
    chapter_lines.extend(x.get("text") for x in page.extract_text_lines(return_chars=False))
    print(page.extract_text())



def clean_header(lines: List[str]) -> List[str]:
    skip_next = False
    for x in lines:
        if skip_next:
            skip_next = False
            continue

        if x == "ISO/IEC 9075-2:2003 (E)":
            skip_next = True
            continue

        if "©ISO/IEC 2003 – All rights reserved" in x:
            continue

        yield x

def is_topic(x: str) -> bool:
    return bool(re.match(r'^(11(?!\)).*?)(?:\.\d+)*.*', x))


chapter = {}
subtopics = ["Function", "Format", "Syntax Rules", 'Access Rules', 'General Rules', 'Conformance Rules']

chapter_lines = list(clean_header(chapter_lines))
current_topic = "NOT FOUND TOPIC"
current_subtopic = "NOT FOUND SUBTOPIC"

for line in chapter_lines:
    if is_topic(line):
        chapter[line] = {}
        current_topic = line
    elif line in subtopics:
        try:
            current_subtopic = line
            chapter[current_topic][current_subtopic] = []
        except Exception as e:
            print(str(e))
    else:
        try:
            chapter[current_topic][current_subtopic].append(line)
        except Exception as e:
            pass


pdf.close()
main_topic = "NOT FOUND"
for topic, subtopics in chapter.items():
    if not subtopics:
        print(f"Create topic dir {topic}")
        main_topic = topic
        os.makedirs(f"./docs/parsed/{topic}", exist_ok=True)
        continue

    dir = f"./docs/parsed/{main_topic}/{topic}"

    os.makedirs(dir, exist_ok=True)
    for subtopic in subtopics:
        if not subtopics[subtopic] or subtopics[subtopic][0] == "None.":
            continue
        with open(dir + "/" + subtopic, 'w+') as f:
            f.writelines('\n'.join(subtopics[subtopic]))
