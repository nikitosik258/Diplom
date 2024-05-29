from yargy import Parser, rule
from yargy.pipelines import morph_pipeline, caseless_pipeline
from yargy.interpretation import fact

Problem = fact('Problem', ['target', 'add_word', 'second_word'])
TARGET = morph_pipeline([
    "цель", "способ", "изобретение", "модель", "задача",
    "использование", "технический", "проблема", "необходимость"
])
ADD_WORD = caseless_pipeline([
    "предлагаемого", "настоящего", "данного", "решаемая",
    "описываемого", "приведенного"
])
SECOND_WORD = morph_pipeline([
    "изобретение", "предназначено", "позволяет", "решения",
    "способа", "способствует", "достигается", "обеспечивает",
    "относится", "результат", "решает", "направлено", "использовано",
    "модели", "демонстрирует", "гарантирует"
])

problem_rule = rule(
    TARGET.interpretation(Problem.target),
    ADD_WORD.interpretation(Problem.add_word).optional(),
    SECOND_WORD.interpretation(Problem.second_word)
)
parser = Parser(problem_rule)

def check_if_problem(sentence):
    matches = list(parser.findall(sentence))
    return bool(matches)
