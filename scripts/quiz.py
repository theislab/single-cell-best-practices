from collections.abc import Iterable, Mapping
from contextlib import contextmanager

from IPython.display import HTML, display
from jinja2 import Template

# Shared width so flip cards and MCQs line up visually, e.g. when grouped in quiz_tabs().
_CARD_WIDTH_PX = 340

_MULTIPLE_CHOICE_TEMPLATE = Template(
    """
    <style>
        .mcq-box {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 12px;
            width: {{ card_width }}px;
            text-align: left;
            font-size: 15px;
            margin-bottom: 8px;
            background-color: {{ bg_color }};
            border-radius: 8px;
            color: {{ text_color }};
        }
    </style>

    <div class="mcq-box">
        <p><strong>{{ question }}</strong></p>
        {% for option in options %}
        <label style="color: {{ text_color }};">
            <input type="radio" name="q{{ question_id }}" value="{{ option }}"
            data-correct="{{ correct_answer }}" data-explanation="{{ explanations.get(option, '') }}"
            data-feedback-id="feedback-{{ question_id }}"
            onclick="checkAnswer(this)"> {{ option }}
        </label><br>
        {% endfor %}
        <p id="feedback-{{ question_id }}" style="font-weight: bold;"></p>
        <p class="mcq-answer-{{ question_id }}" style="display: none; font-weight: bold; color: {{ answer_color }};">
            ✔ Correct Answer: {{ correct_answer }}
        </p>
    </div>

    <script>
    function checkAnswer(element) {
        let feedback = document.getElementById(element.dataset.feedbackId);
        if (element.value === element.dataset.correct) {
            feedback.innerHTML = "✅ Correct!";
            feedback.style.color = "#a8d480";
        } else {
            feedback.innerHTML = "❌ Incorrect! " + element.dataset.explanation;
            feedback.style.color = "#EE4B2B";
        }
    }
    </script>
    """,
    autoescape=True,
)

_FLIP_CARD_TEMPLATE = Template(
    """
    <style>
        .flip-card-{{ question_id }} {
            background-color: transparent;
            width: {{ card_width }}px;
            height: 170px;
            perspective: 1000px;
            display: inline-block;
            margin: 8px;
            text-align: center;
            padding: 8px;
        }
        .flip-card-inner-{{ question_id }} {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            transform-origin: center;
        }
        .flip-card-{{ question_id }}:hover .flip-card-inner-{{ question_id }} {
            transform: rotateY(180deg);
        }
        .flip-card-front-{{ question_id }}, .flip-card-back-{{ question_id }} {
            position: absolute;
            width: 100%;
            height: 100%;
            min-height: 170px;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: {{ text_color }};
            padding: 14px;
            border-radius: 12px;
            box-sizing: border-box;
            overflow: hidden;
            text-align: center;
        }
        .flip-card-front-{{ question_id }} {
            background-color: {{ front_color }};
            font-size: {{ front_font_size }}px;
        }
        .flip-card-back-{{ question_id }} {
            background-color: {{ back_color }};
            transform: rotateY(180deg);
            font-size: {{ back_font_size }}px;
        }
    </style>

    <div class="flip-card-{{ question_id }}">
        <div class="flip-card-inner-{{ question_id }}">
            <div class="flip-card-front-{{ question_id }}">
                {{ question }}
            </div>
            <div class="flip-card-back-{{ question_id }}">
                {{ answer }}
            </div>
        </div>
    </div>
    <noscript>
        <p><strong>Q:</strong> {{ question }}</p>
        <p><strong>Answer:</strong> {{ answer }}</p>
    </noscript>
    """,
    autoescape=True,
)

_TAB_GROUP_TEMPLATE = Template(
    """
    <style>
        .quiz-tabs-{{ group_id }} {
            width: {{ card_width }}px;
            margin-bottom: 8px;
        }
        .quiz-tab-strip-{{ group_id }} {
            display: flex;
            gap: 4px;
            margin-bottom: 6px;
        }
        .quiz-tab-btn-{{ group_id }} {
            flex: 1;
            border: none;
            border-radius: 6px 6px 0 0;
            padding: 6px 0;
            font-size: 13px;
            font-weight: bold;
            cursor: pointer;
            background-color: #cfd8e3;
            color: #234;
        }
        .quiz-tab-btn-{{ group_id }}.active {
            background-color: #3965a3;
            color: white;
        }
        .quiz-tab-pane-{{ group_id }} {
            display: none;
        }
        .quiz-tab-pane-{{ group_id }}.active {
            display: block;
        }
    </style>
    <div class="quiz-tabs-{{ group_id }}">
        <div class="quiz-tab-strip-{{ group_id }}">
            {% for label in labels %}
            <button class="quiz-tab-btn-{{ group_id }}{% if loop.first %} active{% endif %}"
                data-group-id="{{ group_id }}" data-index="{{ loop.index0 }}"
                onclick="quizTabSwitch(this)">{{ label }}</button>
            {% endfor %}
        </div>
        {% for fragment in fragments %}
        <div class="quiz-tab-pane-{{ group_id }}{% if loop.first %} active{% endif %}">
            {{ fragment | safe }}
        </div>
        {% endfor %}
    </div>
    <script>
    function quizTabSwitch(button) {
        const groupId = button.dataset.groupId;
        const i = Number(button.dataset.index);
        const btns = document.getElementsByClassName("quiz-tab-btn-" + groupId);
        const panes = document.getElementsByClassName("quiz-tab-pane-" + groupId);
        for (let j = 0; j < btns.length; j++) {
            btns[j].classList.toggle("active", j === i);
            panes[j].classList.toggle("active", j === i);
        }
    }
    </script>
    """,
    autoescape=True,
)

_active_groups: list[list[tuple[str, str]]] = []


def _emit(question_id: str, html_code: str) -> None:
    """Display a rendered quiz widget, or collect it if inside quiz_tabs()."""
    if _active_groups:
        _active_groups[-1].append((question_id, html_code))
    else:
        display(HTML(html_code))


@contextmanager
def quiz_tabs():
    """Group multiple flip_card/multiple_choice_question calls into one tabbed widget.

    Examples:
        >>> with quiz_tabs():
        ...     flip_card("q1", "What is 2+2?", "4")
        ...     multiple_choice_question(
        ...         "q2",
        ...         "What is the capital of France?",
        ...         ["Paris", "London"],
        ...         "Paris",
        ...         {"London": "London is the capital of the UK"},
        ...     )
    """
    group: list[tuple[str, str]] = []
    _active_groups.append(group)
    try:
        yield
    finally:
        _active_groups.pop()
        if group:
            # Derived from the questions' own ids rather than a counter, since
            # quiz cells may be re-executed in separate isolated kernels and a
            # counter would collide across groups on the same page.
            group_id = "grp-" + "-".join(question_id for question_id, _ in group)
            html_code = _TAB_GROUP_TEMPLATE.render(
                group_id=group_id,
                labels=[f"Q{i}" for i in range(1, len(group) + 1)],
                fragments=[html for _, html in group],
                card_width=_CARD_WIDTH_PX,
            )
            display(HTML(html_code))


def multiple_choice_question(
    question_id: str,
    question: str,
    options: Iterable[str],
    correct_answer: str,
    explanations: Mapping[str, str],
    bg_color: str = "#3965a3",
    text_color: str = "white",
    answer_color: str = "red",
) -> None:
    """Interactive multiple choice question component for Jupyter notebooks.

    Args:
        question_id: Unique identifier for the question
        question: The question text to display
        options: Possible answer choices
        correct_answer: The correct option
        explanations: Dict mapping incorrect options to explanation texts
        bg_color: Background color of question box
        text_color: Text color of questions and options
        answer_color: Color of correct answer text

    Examples:
        >>> multiple_choice_question(
            "q1",
            "What is the capital of France?",
            ["Paris", "London", "Berlin", "Madrid"],
            "Paris",
            {
                "London": "London is the capital of the UK",
                "Berlin": "Berlin is the capital of Germany",
                "Madrid": "Madrid is the capital of Spain",
            }
        )
    """
    html_code = _MULTIPLE_CHOICE_TEMPLATE.render(
        question_id=question_id,
        question=question,
        options=options,
        correct_answer=correct_answer,
        explanations=explanations,
        bg_color=bg_color,
        text_color=text_color,
        answer_color=answer_color,
        card_width=_CARD_WIDTH_PX,
    )
    _emit(question_id, html_code)


def flip_card(
    question_id: str,
    question: str,
    answer: str,
    front_color: str = "#3965a3",
    back_color: str = "#a8d480",
    text_color: str = "white",
    front_font_size: int = 17,
    back_font_size: int = 17,
) -> None:
    """Interactive flip card component for Jupyter notebooks.

    Creates a card that reveals the answer when hovered over.

    Args:
        question_id: Unique identifier for the card
        question: Text to show on front of card
        answer: Text to show on back of card
        front_color: Background color of question side
        back_color: Background color of answer side
        text_color: Color of text on both sides
        front_font_size: Font size on question side
        back_font_size: Font size on answer side

    Examples:
        >>> flip_card("q1", "What is 2+2?", "4")
    """
    html_code = _FLIP_CARD_TEMPLATE.render(
        question_id=question_id,
        question=question,
        answer=answer,
        front_color=front_color,
        back_color=back_color,
        text_color=text_color,
        front_font_size=front_font_size,
        back_font_size=back_font_size,
        card_width=_CARD_WIDTH_PX,
    )
    _emit(question_id, html_code)
