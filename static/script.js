async function submitTask() {

    const task =
        document.getElementById("task").value;

    const level =
        document.getElementById("level").value;

    const input =
        document.getElementById("userInput").value.trim();

    const result =
        document.getElementById("result");

    const loading =
        document.getElementById("loading");

    const button =
        document.getElementById("submitButton");


    // Validate input

    if (!input) {

        result.innerHTML = `
            <div class="error">
                Please enter a question, topic,
                or educational text.
            </div>
        `;

        return;
    }


    // Loading state

    button.disabled = true;

    loading.classList.remove("hidden");

    result.innerHTML =
        "Generating your response...";


    try {

        const response =
            await fetch(`/${task}`, {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    text: input,

                    level: level

                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Request failed"
            );

        }


        displayResult(
            task,
            data.result
        );


    } catch (error) {

        result.innerHTML = `
            <div class="error">
                ${escapeHTML(error.message)}
            </div>
        `;

    } finally {

        button.disabled = false;

        loading.classList.add("hidden");

    }
}


/* ---------------------------
   Display AI Result
---------------------------- */

function displayResult(
    task,
    data
) {

    const result =
        document.getElementById("result");


    // Quiz

    if (
        task === "quiz" &&
        data &&
        data.questions
    ) {

        renderQuiz(
            data.questions
        );

        return;
    }


    // Quiz error

    if (
        task === "quiz" &&
        data &&
        data.error
    ) {

        result.innerHTML = `
            <div class="error">
                ${escapeHTML(data.error)}
            </div>
        `;

        return;
    }


    // Normal text response

    result.innerHTML =
        formatText(data);
}


/* ---------------------------
   Quiz Renderer
---------------------------- */

function renderQuiz(
    questions
) {

    const result =
        document.getElementById("result");


    let html = "";


    questions.forEach(
        (question, index) => {

            html += `
                <div
                    class="quiz-question"
                >

                    <h3>
                        ${index + 1}.
                        ${escapeHTML(
                            question.question
                        )}
                    </h3>

                    <ul
                        class="quiz-options"
                    >
            `;


            question.options.forEach(
                (option, optionIndex) => {

                    const isCorrect =
                        optionIndex ===
                        question.answer;

                    html += `
                        <li
                            class="${
                                isCorrect
                                ? "correct-answer"
                                : ""
                            }"
                        >

                            <strong>
                                ${String.fromCharCode(
                                    65 + optionIndex
                                )}.
                            </strong>

                            ${escapeHTML(
                                option
                            )}

                            ${
                                isCorrect
                                ? " ✓"
                                : ""
                            }

                        </li>
                    `;

                }
            );


            html += `

                    </ul>

                    <div
                        class="quiz-explanation"
                    >

                        <strong>
                            Explanation:
                        </strong>

                        ${escapeHTML(
                            question.explanation
                        )}

                    </div>

                </div>
            `;

        }
    );


    result.innerHTML = html;
}


/* ---------------------------
   Format Text
---------------------------- */

function formatText(
    text
) {

    if (
        text === null ||
        text === undefined
    ) {

        return "No response received.";

    }


    return escapeHTML(
        String(text)
    );
}


/* ---------------------------
   HTML Escape
---------------------------- */

function escapeHTML(
    value
) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}