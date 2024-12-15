import os
import shutil
import xml.etree.ElementTree as ET

sdf_mod_list = [
    {
        "model" : "jumping_spider_controls",
        "submodel" : "jumping_spider",
        "component_dicts_list" : [{
            "component" : "plugin",
            "name" : "SuctionPlugin",
            "new_name" : "SuctionPlugin",
            "action" : "modify",
            "prop_dict" : {
                "suction_force":"1",
            }
        }]
    }
]

def dict_to_xml(tag, d):
    """
    Convert a dictionary to XML element recursively.
    """
    if isinstance(d, dict):
        if isinstance(tag,str):
            element = ET.Element(tag)
        else:
            element = tag
        for key, value in d.items():
            if isinstance(value, dict):
                element.append(dict_to_xml(key, value))
            else:
                child = ET.SubElement(element, key)
                child.text = str(value)
        return element
    return ET.Element(tag, text=str(d))

def generate_world_file(original_world_file_dir, original_world_file_name, new_world_file_path):
    src = os.path.join(original_world_file_dir, original_world_file_name)
    dst = new_world_file_path
    shutil.copyfile(src, dst)

    tree = ET.parse(new_world_file_path)
    root = tree.getroot()
    world = root.find("world")

    if "xmlns:experimental" not in root.attrib:
        root.set("xmlns:experimental", "experimental")

    # Locate the specific <include> element by its <uri> child
    
    for mod in sdf_mod_list:  
        model = mod["model"]
        submodel = mod["submodel"]
        for include in world.findall("include"):
            uri = include.find("uri")
            if uri is not None and uri.text == f"model://{model}":
                # Create the new <experimental:params> element
                new_param = ET.Element("experimental:params")
                for component_dict in mod["component_dicts_list"]:
                    component = component_dict["component"]
                    name = component_dict["name"]
                    new_name = component_dict["new_name"]
                    action = component_dict["action"]
                    prop_dict = component_dict["prop_dict"]
                    uri = include.find("uri")
                    new_prop = ET.SubElement(new_param, f"{component}", {
                        "element_id": f"{submodel}::{name}",
                        "name": f"{new_name}",
                        "action": f"{action}"
                    })
                    new_prop = dict_to_xml(new_prop, prop_dict)

                    ET.indent(new_param, '  ')
                    include.append(new_param)
                break 

    tree.write(new_world_file_path, xml_declaration=True, encoding="UTF-8")

