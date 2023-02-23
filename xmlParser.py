import re
import xml.etree.ElementTree as ET

class xmlparse:
    def __init__(self, language, instructions):
        self.language = language
        self.instructions = instructions
        
    def parse(xmlString):
        root = ET.parse(xmlString)
        
        