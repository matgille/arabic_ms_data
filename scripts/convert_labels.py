import lxml.etree as ET
import glob
import sys


alto = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}

def main():
    all_labels = []
    for file in glob.glob(f"*/*/*.xml"):
        as_tree = ET.parse(file)
        mapping = {"0": "test"}
        labels = as_tree.xpath("//alto:Tags/alto:OtherTag/@LABEL", namespaces=alto)
        ids = as_tree.xpath("//alto:Tags/alto:OtherTag/@ID", namespaces=alto)
        as_tuples = list(zip(labels, ids))
        all_labels.extend(as_tuples)
        
    all_labels = list(set(all_labels))
    blocks_as_dict = {}
    lines_as_dict = {}
    for label, id in all_labels:
        if id[0] == "B":
            try:
                blocks_as_dict[label].append(id)
            except KeyError:
                blocks_as_dict[label] = [id]
        elif id[0] == "L":
            try:
                lines_as_dict[label].append(id)
            except KeyError:
                lines_as_dict[label] = [id]
        else:
            print(id)
            
    print(lines_as_dict)
    print(blocks_as_dict)

if __name__ == '__main__':
    main()
