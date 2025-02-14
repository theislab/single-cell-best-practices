from IPython.display import HTML, display


def multiple_choice_question(
    question_id,
    question,
    options,
    correct_answer,
    explanations,
    bg_color="#3965a3",
    text_color="white",
    answer_color="red",
):
    options_html = ""
    for option in options:
        explanation_text = explanations.get(
            option, ""
        )  # Get explanation if the answer is incorrect
        options_html += f"""
        <label style="color: {text_color};">
            <input type="radio" name="q{question_id}" value="{option}"
            onclick="checkAnswer(this, '{correct_answer}', '{explanation_text}', 'feedback-{question_id}')"> {option}
        </label><br>
        """

    html_code = f"""
    <style>
        /* to remove the background color in dark mode */
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

        <!-- Correct Answer (Hidden in HTML, Always Visible in PDF) -->
        <p class="mcq-answer-{question_id}" style="display: none; font-weight: bold; color: {answer_color};">
            ✔ Correct Answer: {correct_answer}
        </p>
    </div>

    <script>
    function checkAnswer(element, correct, explanation, feedbackId) {{
        let feedback = document.getElementById(feedbackId);
        if (element.value === correct) {{
            feedback.innerHTML = "✅ Correct!";
            feedback.style.color = "green";
        }} else {{
            feedback.innerHTML = "❌ Incorrect! " + explanation;
            feedback.style.color = "red";
        }}
    }}
    </script>
    """
    display(HTML(html_code))
