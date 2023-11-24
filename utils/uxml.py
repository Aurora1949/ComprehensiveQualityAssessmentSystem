from typing import Callable, Any
from xml.dom.minicompat import NodeList
from xml.dom.minidom import parse, Element, Node, Document


def parse_xml(xml_path: str):
    dom: Document = parse(xml_path)
    data: Element = dom.documentElement
    projects: NodeList = data.getElementsByTagName('project')
    visit_all_nodes(projects, check_add)
    visit_all_nodes(projects, check_subtract)


def check_add(node: Element):
    add: NodeList = node.getElementsByTagName('add')
    if is_node_list_empty(add):
        return
    cells: NodeList = add[0].getElementsByTagName('cell')
    visit_all_nodes(cells, check_sub_cell)


def check_subtract(node: Element):
    subtract: NodeList = node.getElementsByTagName('subtract')
    if is_node_list_empty(subtract):
        return
    cells: NodeList = subtract[0].getElementByTagName('subtract')
    visit_all_nodes(cells, check_sub_cell)


def check_sub_cell(cell: Element):
    if cell.hasChildNodes():
        print(cell.getAttribute("content"))
        visit_all_nodes(cell.getElementsByTagName('sub-cell'), check_sub_cell)
    else:
        print(cell.getAttribute("content") + "at" + cell.getAttribute("at"))


def visit_all_nodes(nodes: NodeList, func: Callable[[Node | Element], Any]):
    for c in nodes:
        func(c)


def is_node_list_empty(nlist: NodeList) -> bool:
    """
    check given node list if it is empty
    :param nlist:
    :return: if node list is empty it returns ``True`` otherwise ``False``
    """
    return nlist.length == 0


if __name__ == '__main__':
    parse_xml('../config/xlsx_format_xml.xml')
