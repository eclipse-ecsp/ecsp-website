import xml.etree.ElementTree as ET
import os


def parse_components(xml_file):
    print("Parsing components")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    comps = []
    namespace = "{" + root.tag.split("}")[0][1:] + "}"
    print(namespace)
    components = root.findall(f".//{namespace}component")

    for component in components:
        name = component.find(f".//{namespace}name")

        try:
            version = component.find(f".//{namespace}version").text
        except:
            version = ""

        try:
            license = component.find(f".//{namespace}license")
            licenseid = license.find(f".//{namespace}id").text
        except:
            licenseid = ""

        try:
            project_url = ""
            # get reference value for type vcs from externalReferences from components.xml file
            externalReferences = component.findall(f".//{namespace}externalReferences/{namespace}reference")
            for reference in externalReferences:
                if reference.get('type') == 'vcs':
                    project_url = reference.find(f".//{namespace}url").text
                    break
        except:
            project_url = ""

        comps.append({
            'name': name.text,
            'version': version,
            'license': licenseid,
            'project': project_url
        })
    return comps


def format_output(component_array):
    string = ''
    for comp in component_array:
        string += comp.get('name') + '(' + comp.get('version') + ')' + '<br/>'
        string += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'License' + ': ' + comp.get('license') + '<br/>'
        string += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + 'Project' + ': ' + comp.get('project') + '<br/>'
        string += ' <br/><br/>'
    return string


files = [f for f in os.listdir('.')]
print(files)
# Change this to the path of your XML file
xml_file = "./bom.xml"

component_array = parse_components(xml_file)
output = format_output(component_array)

# Define the placeholder to be replaced
placeholder = "{{third_party_content}}"

# Read the contents of the file
with open("./NOTICE.template", "r") as file:
    content = file.read()

# Replace the placeholder with the components string
modified_content = content.replace(placeholder, output)

# Write the modified content back to the file
with open("NOTICE.md", "w+") as file:
    file.write(modified_content)

print("Notice generated successfully!")
