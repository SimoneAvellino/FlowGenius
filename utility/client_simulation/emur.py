from __future__ import annotations
from abc import ABC, abstractmethod
import time
import xml.etree.ElementTree as ET
from datetime import datetime
import xmltodict

class EMUR_generator:

    def __init__(self, file_path, file_type, seconds_for_interval=1):
        if file_type == "XML":
            flow_reader = XMLReader(file_path)
        else:
            raise ValueError("Unsupported file type")
        self.flow_reader = flow_reader
        self.seconds_for_interval = seconds_for_interval

    def run(self):
        print("Generating EMUR datar")
        # loop over records in the flow until the end
        while True:
            record = self.flow_reader.next()
            if record is None:
                break
            # process the record
            print(record)
            # sleep for interval
            time.sleep(self.seconds_for_interval)

    def next(self):
        return self.flow_reader.next()


class EMUR_record:
    """
    EMUR data record
    """

    def __init__(self,
                 Identificativo,
                 CodiceIstituto,
                 data_entrata,
                 modalita_arrivo,
                 responsabile_invio,
                 problema_principale,
                 trauma,
                 triage
                 ):
        self.Identificativo = Identificativo
        self.CodiceIstituto = CodiceIstituto
        self.data_entrata = data_entrata
        self.modalita_arrivo = modalita_arrivo
        self.responsabile_invio = responsabile_invio
        self.problema_principale = problema_principale
        self.trauma = trauma
        self.triage = triage


    def __str__(self):
        return f"EMUR record:\n Identificativo: {self.Identificativo}\n  CodiceIstituto: {self.CodiceIstituto}\n  data_entrata: {self.data_entrata}\n  modalita_arrivo: {self.modalita_arrivo}\n  responsabile_invio: {self.responsabile_invio}\n  problema_principale: {self.problema_principale}\n  trauma: {self.trauma}\n  triage: {self.triage}"


class FlowReader(ABC):
    """
    Interface for EMUR data flow reading
    """

    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def flow_type(self) -> str:
        """
        Returns type of flow
        """
        pass

    @abstractmethod
    def next(self) -> EMUR_record | None:
        """
        Returns next record in the EMUR flow
        """
        pass


class XMLReader(FlowReader):
    """
    Reads EMUR data flow from XML file
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        print("rrot", self.root)
        self.current_index = 0

    def flow_type(self) -> str:
        return "XML"

    def next(self) -> dict | None:
        # Check if there are more records to read
        if self.current_index >= len(self.root):
            return None

        # Get the current <item> element
        item = self.root[self.current_index]
        self.current_index += 1

        # Convert the <item> element to a dictionary using xmltodict
        item_dict = xmltodict.parse(ET.tostring(item), process_namespaces=False, strip_whitespace=True)

        # Extract the main dictionary from the root key
        item_dict = item_dict['ns0:item'] if 'ns0:item' in item_dict else item_dict
        # all the keys are in the form of 'ns0:key'
        # so we remove the 'ns0:' part for all the keys in the dictionary also with sub-dictionaries
        item_dict = {key.replace('ns0:', ''): value for key, value in item_dict.items()}
        # FIX


        return item_dict
