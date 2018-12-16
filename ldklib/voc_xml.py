import xml.etree.cElementTree as ET
import xml.dom.minidom as MD

def voc_xml_save(im_name, informations,img_shape=(608,608),path_file='./'):
    """
    para:im_name, informations,img_shape=(608,608),path_file='./'
    informations = ((label=>str,rect=>int(4):(xmin,ymin,xmax,ymax)),)
    <object>
		<name>anchor</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>23</xmin>
			<ymin>47</ymin>
			<xmax>103</xmax>
			<ymax>75</ymax>
		</bndbox>
	</object>
    """
    # root = ET.Element("annotation")
    # annotation = root
    annotation = ET.Element("annotation")
    folder = ET.SubElement(annotation, "folder")
    folder.text ='ID'# os.path.dirname(im_name)
    filename = ET.SubElement(annotation, "filename")
    filename.text =im_name+'.jpg'# os.path.basename(im_name).split('.')[0]
    # path = ET.SubElement(annotation, "path")
    # path.text ="../ID/"+im_name+'.jpg'# os.path.abspath(im_name)
    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(img_shape[1])
    ET.SubElement(size, "height").text = str(img_shape[0])
    ET.SubElement(size, "depth").text = "3"
    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = "0"
    for label,box in informations:
        new_xml_object = ET.SubElement(annotation, "object")
        _ = []
        _ = ET.SubElement(new_xml_object, "name")
        _.text = label
        _ = ET.SubElement(new_xml_object, "anchor")
        _.text = "Unspecified"
        _ = ET.SubElement(new_xml_object, "truncated")
        _.text = "0"
        _ = ET.SubElement(new_xml_object, "difficult")
        _.text = "0"
        bndbox = ET.SubElement(new_xml_object, "bndbox")
        xmin = ET.SubElement(bndbox, "xmin")
        ymin = ET.SubElement(bndbox, "ymin")
        xmax = ET.SubElement(bndbox, "xmax")
        ymax = ET.SubElement(bndbox, "ymax")
        xmin.text, ymin.text, xmax.text, ymax.text = map(str, box)
    tree_str = ET.tostring(annotation, 'utf-8')
    reparsed = MD.parseString(tree_str)
    result = reparsed.toprettyxml(encoding="utf-8")
    with open(path_file, 'wb') as f:
        f.write(result)
    return tree_str


def voc_xml_get(filename):
    results=[]
    tree = ET.parse(filename)
    root = tree.getroot()
    for obj_item in root.findall('object'):
        obj_name = obj_item.find('name').text
        for bndbox_item in obj_item.findall('bndbox'):
            xmin = int(bndbox_item.find('xmin').text)
            ymin = int(bndbox_item.find('ymin').text)
            xmax = int(bndbox_item.find('xmax').text)
            ymax = int(bndbox_item.find('ymax').text)
            if xmin>xmax:
                xmin,xmax = xmax,xmin
            if ymin>ymax:
                ymin,ymax = ymax,ymin
            results.append((obj_name,(xmin,ymin,xmax,ymax)))
    return results
