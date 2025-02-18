from collections.abc import Iterable, Mapping

from IPython.display import HTML, display


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
    options_html = ""
    for option in options:
        explanation_text = explanations.get(option, "")
        options_html += f"""
        <label style="color: {text_color};">
            <input type="radio" name="q{question_id}" value="{option}"
            onclick="checkAnswer(this, '{correct_answer}', '{explanation_text}', 'feedback-{question_id}')"> {option}
        </label><br>
        """

    html_code = f"""
    <style>
        div#multiple-choice-question .output.text_html {{
            background-color: transparent;
        }}
        .mcq-box {{
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 15px;
            width: 400px;
            text-align: left;
            font-size: 18px;
            margin-bottom: 10px;
            background-color: {bg_color};
            border-radius: 10px;
            color: {text_color};
        }}
    </style>

    <div class="mcq-box">
        <p><strong>{question}</strong></p>
        {options_html}
        <p id="feedback-{question_id}" style="font-weight: bold;"></p>
        <p class="mcq-answer-{question_id}" style="display: none; font-weight: bold; color: {answer_color};">
            ✔ Correct Answer: {correct_answer}
        </p>
    </div>

    <script>
    function checkAnswer(element, correct, explanation, feedbackId) {{
        let feedback = document.getElementById(feedbackId);
        if (element.value === correct) {{
            feedback.innerHTML = "✅ Correct!";
            feedback.style.color = "#a8d480";
        }} else {{
            feedback.innerHTML = "❌ Incorrect! " + explanation;
            feedback.style.color = "#EE4B2B";
        }}
    }}
    </script>
    """
    display(HTML(html_code))


def flip_card(
    question_id: str,
    question: str,
    answer: str,
    front_color: str = "#3965a3",
    back_color: str = "#a8d480",
    text_color: str = "white",
    front_font_size: int = 20,
    back_font_size: int = 20,
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
    html_code = f"""
    <style>
        div#flip-card .output.text_html {{
            background-color: transparent;
        }}
        .flip-card-{question_id} {{
            background-color: transparent;
            width: 350px;
            height: 200px;
            perspective: 1000px;
            display: inline-block;
            margin: 10px;
            text-align: center;
            padding: 10px;
        }}
        .flip-card-inner-{question_id} {{
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            transform-origin: center;
        }}
        .flip-card-{question_id}:hover .flip-card-inner-{question_id} {{
            transform: rotateY(180deg);
        }}
        .flip-card-front-{question_id}, .flip-card-back-{question_id} {{
            position: absolute;
            width: 100%;
            height: 100%;
            min-height: 200px;
            backface-visibility: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: {text_color};
            padding: 20px;
            border-radius: 15px;
            box-sizing: border-box;
            overflow: hidden;
            text-align: center;
        }}
        .flip-card-front-{question_id} {{
            background-color: {front_color};
            font-size: {front_font_size}px;
        }}
        .flip-card-back-{question_id} {{
            background-color: {back_color};
            transform: rotateY(180deg);
            font-size: {back_font_size}px;
        }}
    </style>

    <div class="flip-card-{question_id}">
        <div class="flip-card-inner-{question_id}">
            <div class="flip-card-front-{question_id}">
                {question}
            </div>
            <div class="flip-card-back-{question_id}">
                {answer}
            </div>
        </div>
    </div>
    <noscript>
        <p><strong>Q:</strong> {question}</p>
        <p><strong>Answer:</strong> {answer}</p>
    </noscript>
    """
    display(HTML(html_code))
