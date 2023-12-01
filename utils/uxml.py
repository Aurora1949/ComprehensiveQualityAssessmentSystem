import json
from typing import Callable, Any, Optional
from xml.dom.minicompat import NodeList
from xml.dom.minidom import parse, Element, Node, Document

from modules.my_module import ConductScorecard


def parse_xml(xml_path: str):
    dom: Document = parse(xml_path)
    data: Element = dom.documentElement
    projects: NodeList = data.getElementsByTagName('project')
    d: dict = {}
    lst = []
    for project in projects:
        p_list = NodeList()
        p_list.append(project)
        project_name = project.getAttribute('name')
        d[project_name] = {"add": {}, "subtract": {}}
        visit_all_nodes(p_list, check_add, d[project_name]['add'])
        visit_all_nodes(p_list, check_subtract, d[project_name]['subtract'])
    for item in d:
        lst.append({
            'subject': item,
            'add': dict_to_class(d[item]['add']),
            'subtract': dict_to_class(d[item]['subtract'])
        })
    return lst


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
        if cell.hasAttribute("single"):  # 仅限单选
            d[key].update({"single": True})
        visit_all_nodes(cell.getElementsByTagName('sub-cell'), save_to_dict, d[key])
    else:
        dic = {
            "title": cell.getAttribute("content"),
            "codename": cell.getAttribute("codename"),
            "standard": [eval(i) for i in cell.getAttribute("standard").split(',')],
            "at": cell.getAttribute("at")
        }

        if cell.hasAttribute("allowNoEvidence"):  # 允许无证明
            dic.update({"no_evidence": True})
        if cell.hasAttribute("single"):  # 仅限单选
            dic.update({"single": True})
        if cell.hasAttribute("multiple"):
            dic.update({"multiple": True})  # 允许多项
        if cell.hasAttribute("accumulative"):
            dic.update({"accumulative": True})  # 加减分按次

        if key:
            d[key] = dic
        else:
            d["sub"].append(dic)


def visit_all_nodes(nodes: NodeList, func: Callable[[Node | Element, *[Any, ...]], Any], *args):
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
    d = parse_xml('../config/xlsx_format_xml.xml')
    print()
    # j_data = json.dumps(d, ensure_ascii=False)
    # with open('../files/output.json', 'w+', encoding='utf-8') as f:
    #     f.write(j_data)
    #     f.close()
    # lst = dict_to_class(d)
    # print(lst)
