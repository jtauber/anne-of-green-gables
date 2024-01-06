#!/usr/bin/env python3

import re

from lxml import etree


def get_text(el):
    s = el.text or ""
    for child in el:
        s += get_text(child)
    s += el.tail or ""
    s = re.sub(r"\s+", " ", s)
    return s


class CiteIndex:

    def output_para(self, kind, text):
        if kind != "h":
            self.para_num += 1

        ref = f"{int(self.chapter_num):02d}.{self.para_num:03d}"
        print(ref, f"{{{kind}}}", text.strip(), sep="\t")


    def go(self, filename):
        self.filename = filename

        with open(filename) as f:
            tree = etree.parse(f)
            root = tree.getroot()

            for child in root:
                if child.tag == "pb":
                    pass

                elif child.tag == "div":
                    if child.attrib.get("type") == "chapter":
                        self.chapter_num = child.attrib.get("n")
                        self.para_num = 0

                        for gchild in child:
                            if gchild.tag == "head":
                                self.output_para("h", get_text(gchild))
                            elif gchild.tag == "p":
                                if gchild.attrib and gchild.attrib.get("class") == "spb":
                                    self.output_para("ps", get_text(gchild))
                                else:
                                    self.output_para("p", get_text(gchild))
                            elif gchild.tag == "pb":
                                pass
                            elif gchild.tag == "quote":
                                assert gchild.attrib == {}
                                assert gchild.text.strip() == ""
                                assert gchild.tail.strip() == ""
                                for ggchild in gchild:
                                    if ggchild.tag == "l":
                                        self.output_para("qt.l", get_text(ggchild))
                                    elif ggchild.tag == "p":
                                        self.output_para("qt.p", get_text(ggchild))
                                    elif ggchild.tag == "closer":
                                        self.output_para("qt.cl", get_text(ggchild))
                                    else:
                                        print(ggchild.tag)
                                        quit()
                            elif gchild.tag == "closer":
                                self.output_para("cl", get_text(gchild))
                            else:
                                assert False, (filename, gchild.sourceline, gchild.tag)
                    
                    else:
                        print(child.attrib.get("type"))
                        quit()

                else:
                    print(child.tag)
                    quit()


cite_index = CiteIndex()
cite_index.go("docs/all.xml")
