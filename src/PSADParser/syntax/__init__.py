from syntax.core import SyntaxDescriptionType, SyntaxInfo
import syntax.virt


def get_syntax_description(syntax_info: SyntaxInfo):
    if syntax_info.type == SyntaxDescriptionType.VIRT_DIAGRAMS:
        return syntax.virt.GetSyntaxDesription(syntax_info.diagrams_path)
    if syntax_info.type == SyntaxDescriptionType.RBNF:
        raise Exception("RBNF not supported yet")
    raise Exception("Unsupported syntax description type")
