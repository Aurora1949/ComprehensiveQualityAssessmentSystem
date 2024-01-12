from typing import Callable, Any, Iterable
from xml.dom.minicompat import NodeList
from xml.dom.minidom import parse, Element, Node, Document

import lxml
from lxml import etree

from modules.my_module import ConductScorecard


def parse_xml(xml_path: str):
    valid, err = validate_xml_dtd(xml_path, '../config/ComprehensiveFormat-1.0.dtd')
    if not valid:
        print(err)
        raise lxml.etree.DTDValidateError(err)
    dom: Document = parse(xml_path)
    data: Element = dom.documentElement
    projects: NodeList = data.getElementsByTagName('project')
    d: dict = {}
    lst = []
    visit_all_nodes(projects, check_project, d)
    for item in d:
        lst.append({
            'subject': item,
            'add': dict_to_class(d[item]['add']),
            'subtract': dict_to_class(d[item]['subtract'])
        })

    return lst


def validate_xml_dtd(xml_path: str, dtd_path: str) -> tuple[bool, list[str]]:
    # 加载 DTD
    with open(dtd_path) as f:
        dtd = etree.DTD(f)
    # 解析 XML
    xml_doc = etree.parse(xml_path)
    # 验证 XML
    is_valid = dtd.validate(xml_doc)
    return is_valid, dtd.error_log.filter_from_errors()


def check_project(node: Element, d: dict):
    project_name = node.getAttribute('name')
    d[project_name] = {"add": {}, "subtract": {}}
    visit_all_nodes([node], check_add, d[project_name]['add'])
    visit_all_nodes([node], check_subtract, d[project_name]['subtract'])


def check_add(node: Element, d: dict):
    add: NodeList = node.getElementsByTagName('add')
    if is_node_list_empty(add):
        return
    cells: NodeList = add[0].getElementsByTagName('cell')
    visit_all_nodes(cells, save_to_dict, d)


def check_subtract(node: Element, d: dict):
    subtract: NodeList = node.getElementsByTagName('subtract')
    if is_node_list_empty(subtract):
        return
    cells: NodeList = subtract[0].getElementsByTagName('cell')
    visit_all_nodes(cells, save_to_dict, d)


def check_sub_cell(cell: Element):
    if cell.hasAttribute("serialNumber"):
        print("序号:" + cell.getAttribute("serialNumber") + "\t====================")
    if cell.hasChildNodes():
        print("总则:" + cell.getAttribute("content"))
        visit_all_nodes(cell.getElementsByTagName('sub-cell'), check_sub_cell)
    else:
        print("明细:" + cell.getAttribute("content"))
        print("代号:" + cell.getAttribute("codename"))
        print("加分细则:" + cell.getAttribute("standard"))
        print("区域:" + cell.getAttribute("at"))
        print("--------------------------------")


def save_to_dict(cell: Element, d: dict, key=None):
    if cell.hasAttribute("serialNumber"):
        key = cell.getAttribute("serialNumber")
    if cell.hasChildNodes():
        if key is None:
            raise KeyError("key must not to be None.")
        d[key] = {"title": cell.getAttribute("content"), "sub": []}
        visit_all_nodes(cell.getElementsByTagName('sub-cell'), save_to_dict, d[key])
    dic = {}
    update_dict_attr(cell, "content", dic, attr_name_func=lambda x: "title")
    update_dict_attr(cell, "codename", dic)
    update_dict_attr(cell, "standard", dic, value_func=lambda x: [eval(i) for i in x.split(',')])
    update_dict_attr(cell, "at", dic)
    update_dict_attr(cell, "allowNoEvidence", dic, lambda x: "no_evidence", lambda x: True)
    update_dict_attr(cell, "single", dic, value_func=lambda x: True)
    update_dict_attr(cell, "multiple", dic, value_func=lambda x: True)
    update_dict_attr(cell, "perTime", dic, lambda x: "per_time", lambda x: int(x))

    if key:
        d.setdefault(key, {}).update(dic)
    else:
        d["sub"].append(dic)


def update_dict_attr(
        cell: Element,
        attr_name: str,
        d: dict,
        attr_name_func: Callable[[str], str] = lambda x: x,
        value_func: Callable[[str], Any] = lambda x: x
):
    if cell.hasAttribute(attr_name):
        d.update({
            attr_name_func(attr_name): value_func(cell.getAttribute(attr_name))
        })


def visit_all_nodes(nodes: Iterable[Node | Element], func: Callable[[Node | Element, *[Any, ...]], Any], *args):
    for c in nodes:
        func(c, *args)


def is_node_list_empty(nlist: NodeList) -> bool:
    """
    check given node list if it is empty
    :param nlist:
    :return: if node list is empty it returns ``True`` otherwise ``False``
    """
    return nlist.length == 0


def dict_to_class(d: dict) -> list[ConductScorecard]:
    lst = []
    for item in d:
        scorecard_instance = ConductScorecard(serial_number=item, **d[item])
        if sub_list := d[item].get("sub"):
            scorecard_instance.sub = [ConductScorecard(**i) for i in sub_list]
        lst.append(scorecard_instance)
    return lst


if __name__ == '__main__':
    dd = parse_xml('../config/not_valid_xml.xml')
    print()
    # j_data = json.dumps(d, ensure_ascii=False)
    # with open('../files/output.json', 'w+', encoding='utf-8') as f:
    #     f.write(j_data)
    #     f.close()
    # lst = dict_to_class(d)
    # print(lst)
