from typing import Optional, Union


class BaseContent:
    s_content = ''
    score_standard = ''

    def __init__(self, content: str, standard: str):
        self.s_content = content
        self.score_standard = standard

    def get_content(self):
        return self.s_content

    def get_score_standard(self):
        return self.score_standard


class Content(BaseContent):
    m_content = ''

    def __int__(self, m_content: str, content: str, standard: str):
        self.m_content = content
        super().__init__(m_content, standard)

    def get_content(self):
        return self.m_content


class ConductScorecard:
    serial_number: Optional[str]
    title: str
    codename: Optional[str]
    standard: Optional[list[Union[int, float]]]
    at: Optional[str]
    sub: Optional[list["ConductScorecard"]]
    no_evidence: bool
    single: bool
    multiple: bool
    per_time: Optional[int]

    def __init__(self,
                 title: str,
                 serial_number: Optional[str] = None,
                 codename: Optional[str] = None,
                 standard: Optional[list[Union[int, float]]] = None,
                 at: Optional[str] = None,
                 sub: Optional[list['ConductScorecard']] = None,
                 no_evidence: bool = False,
                 single: bool = False,
                 multiple: bool = False,
                 per_time: Optional[int] = None
                 ):
        self.serial_number = serial_number
        self.title = title
        self.codename = codename
        self.standard = standard
        self.at = at
        self.sub = sub
        self.no_evidence = no_evidence
        self.single = single
        self.multiple = multiple
        self.per_time = per_time

    def __str__(self):
        return f"ConductScorecard(serial_number={self.serial_number}, title={self.title}, codename={self.codename}, " \
               f"standard={self.standard}, at={self.at}, sub={self.sub}, no_evidence={self.no_evidence}, " \
               f"single={self.single}, multiple={self.multiple}, per_time={self.per_time})"
