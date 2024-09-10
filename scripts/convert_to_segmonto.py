import lxml.etree as ET
import glob
import sys
import json
import tqdm 

alto = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}
alto_ns_cr = '{http://www.loc.gov/standards/alto/ns-v4#}'


def main():
    with open("typologie.json") as input_file:
        json_mapping = json.load(input_file)

    for file in tqdm.tqdm(glob.glob(f"../*/*/*.xml")):
        if "segmonto" in file:
            continue
        as_tree = ET.parse(file)
        all_tags = as_tree.xpath("//alto:Tags/alto:OtherTag", namespaces=alto)
        all_labels = as_tree.xpath("//alto:Tags/alto:OtherTag/@LABEL", namespaces=alto)
        all_ids = as_tree.xpath("//alto:Tags/alto:OtherTag/@ID", namespaces=alto)
        all_labels_and_tags = list(zip(all_tags, all_labels, all_ids))
        try:
            tags_element = as_tree.xpath("//alto:Tags", namespaces=alto)[0]
        except IndexError:
            print(file)
            continue
        default_tag = ET.Element(alto_ns_cr + "OtherTag")
        default_tag.set("LABEL", "DefaultLine")
        default_tag.set("ID", "LT0")
        tags_element.insert(0, default_tag)
        for element, label, ident in all_labels_and_tags:
            replacement = json_mapping[ident[0]][label]
            if replacement == "None":
                element.getparent().remove(element)
            else:
                element.set("LABEL", replacement)

        # On s'occupe des lignes sans typologie
        all_lines = as_tree.xpath("//alto:TextLine[not(@TAGREFS)]", namespaces=alto)
        for line in all_lines:
            line.set("TAGREFS", "LT0")
            
        
        # On supprime les blocs sans ligne
        all_widow_blocks = as_tree.xpath("//alto:TextBlock[not(alto:TextLine)]", namespaces=alto)
        for text_block in all_widow_blocks:
            text_block.getparent().remove(text_block)

        with open(file.replace(".xml", ".segmonto.xml"), "w") as output_xml:
            output_xml.write(ET.tostring(as_tree, pretty_print=True, encoding="utf-8").decode())


if __name__ == '__main__':
    main()

