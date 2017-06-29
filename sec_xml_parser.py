#!/usr/bin/env python3

import xml.etree.ElementTree as ET

def main():
    tree = ET.parse('data/sec/litigation_releases_2009.xml')
    root = tree.getroot()
    data = []
    for litigation_release in root:
        data.append([x.text for x in litigation_release])
    print(data)

if __name__ == "__main__":
    main()
