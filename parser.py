class MibParser(object):
    """
    Parse the SNMP MIB data to readable JSON format
    """

__snmp_name_map__ = {
"type": "SNMPv2-MIB::snmpTrapOID.0",
"ap_id": "SNMPv2-SMI::enterprises.14179.2.2.1.1.3.0",
"ap_mac": "SNMPv2-SMI::enterprises.14179.2.6.2.35.0",
"client_mac": "SNMPv2-SMI::enterprises.14179.2.6.2.34.0",
"client_ip": "SNMPv2-SMI::enterprises.14179.2.6.2.43.0"
}

def __init__(self):
    pass

def parse(self, line):
    #print line
    raw_dict={}
    parsed_dict = {}
    sections_t = map(lambda s: s.strip(), line.split('|', 1))
    parsed_dict['time'] = sections_t[0]
    sections = map(lambda s: s.strip(), sections_t[1].split('\t'))
    for sec in sections:
        parts = map(lambda s: s.strip(), sec.split('='))
        if len(parts) == 2:
            raw_dict[parts[0]] = parts[1]
        elif len(parts) == 1:
            raw_dict[parts[0]] = ""
        else:
            print "ERROR: number of parts (divided by =) for section is wrong:"
            print sec
            return
    #print json.dumps(raw_dict, indent=4, separators=(',',':'))
    type_raw = raw_dict[self.self.__snmp_name_map__["type"]]
    t = type_raw.split('.')[-1]
    if t == "53":
        type_parsed = '1'
    if t == "1":
        type_parsed = '0'
    parsed_dict["type"] = type_parsed

    ap_id_raw = raw_dict[self.__snmp_name_map__["ap_id"]]
    ap_id_parsed = ap_id_raw.split(':')[1].strip().strip('\"')
    parsed_dict["ap_id"] = ap_id_parsed

    ap_mac_raw = raw_dict[self.__snmp_name_map__["ap_mac"]]
    ap_mac_parsed = ap_mac_raw.split(':')[1].strip()
    parsed_dict["ap_mac"] = ap_mac_parsed

    client_mac_raw = raw_dict[self.__snmp_name_map__["client_mac"]]
    client_mac_parsed = client_mac_raw.split(':')[1].strip()
    parsed_dict["client_mac"] = client_mac_parsed

    client_ip_raw = raw_dict[self.__snmp_name_map__["client_ip"]]
    client_ip_parsed = client_ip_raw.split(':')[1].strip()
    parsed_dict["client_ip"] = client_ip_parsed

    #print raw_dict
    #rint json.dumps(parsed_dict, indent=4, separators=(',',':'))
    #print parsed_dict
    return parsed_dict
