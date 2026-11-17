
from llama_cpp import Llama
import re
import datetime

MODEL_PATH = "models/qwen2.5-1.5b-instruct-q4_k_m.gguf"
LOG_FILE = "guardrail_log.txt"

SYSTEM_PROMPT = (
    "You are an internal security helpdesk assistant for a hospital. "
    "Give defensive cybersecurity advice only, for hospital staff. "
    "Never provide attack instructions, malware, or ways to access "
    "systems or patient data without authorisation. "
    "Keep answers short and recommend contacting the IT Security team "
    "when unsure. "
    "Answer in at most 5 short points."
)

# The model is loaded only when an allowed request needs AI inference.
llm = None


def load_model():
    """Load the local language model only when required."""
    global llm

    if llm is None:
        print("Loading local model, please wait...")
        llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,
            verbose=False
        )
        print("Model loaded. Running fully offline.\n")

    return llm


def log_event(outcome, text):
    """Append every decision to a log file with a timestamp."""
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{time_now} | {outcome} | {text}\n")


RISK_RULES = {
    "attack_help": [
        (r"\bsteal\b.{0,40}\bpasswords?\b", 5),
        (r"\b(write|create|make|build)\b.{0,40}\b(keylogger|malware|ransomware)\b", 5),
        (r"\bdisable\b.{0,40}\b(antivirus|firewall)\b", 3),
        (r"\bhack into\b.{0,40}\b(account|system)\b", 5),
    ],

    "patient_snooping": [
        (r"\b(look up|open|check|access|view)\b.{0,40}\b(patient|medical|health)\b.{0,40}\b(without permission|without authorisation|without authorization|secretly|without a legitimate reason)\b", 5),
        (r"\b(celebrity|famous person|neighbour|neighbor|relative|friend|colleague)\b.{0,40}\b(patient record|medical record|health record|patient file)\b", 5),
        (r"\b(give|show|send|reveal|disclose)\b.{0,40}\b(patient details|medical records|patient records|health information)\b", 4),
        (r"\b(extract|download|export|copy)\b.{0,40}\b(patient records|medical records|patient data)\b", 5),
    ],

    "credential_misuse": [
        (r"\b(share|borrow)\b.{0,30}\b(login|password|credentials)\b", 2),
        (r"\bbypass\b.{0,30}\b(login|authentication)\b", 3),
        (r"\b(use|borrow)\b.{0,30}\b(colleague|someone else's)\b.{0,30}\b(badge|card|login)\b", 3),
    ],

    "sensitive_directory": [
        (r"\b(give|show|send|provide|reveal|disclose)\b.{0,60}\b(doctors?|staff|employees?)\b.{0,30}\b(list|directory|contact details)\b", 5),
        (r"\b(give|show|send|provide|reveal|disclose)\b.{0,60}\b(all|complete|entire|full)\b.{0,30}\b(doctors?|staff|employees?)\b", 5),
    ],

    "incident": [
        (r"\b(files?|screens?|systems?)\b.{0,40}\b(locked|encrypted)\b", 4),
        (r"\bransom\s+(note|demand)\b", 4),
        (r"\b(strange|weird|unexpected|suspicious)\b.{0,40}\b(pop-?up|message)\b", 3),
        (r"\b(suspect|suspected|suspecting)\b.{0,40}\bransomware\b", 4),
        (r"\b(possible|suspected|confirmed)?\s*(patient[- ]data|medical[- ]data)\s+(breach|exposure)\b", 4),
    ],
}


def check_input(text):
    """Classify input using predefined risk patterns."""
    total = 0
    reasons = []

    for category, rules in RISK_RULES.items():
        for pattern, score in rules:
            if re.search(pattern, text, re.IGNORECASE):
                total += score

                if category not in reasons:
                    reasons.append(category)

    if "incident" in reasons and "attack_help" not in reasons:
        return "escalate", reasons

    if total >= 5:
        return "block", reasons

    elif total >= 2:
        return "escalate", reasons

    else:
        return "allow", reasons


UNSAFE_OUTPUT = [
    r"\bimport\s+(socket|pynput)\b",
    r"\bos\s*\.\s*system\b",
    r"\bsubprocess\b",
    r"here is (a|the) (keylogger|script|malware)",
]


SAFE_FALLBACK = (
    "This response was withheld by the safety check. "
    "Please contact the hospital IT Security team."
)


def check_output(reply):
    """Check generated output against predefined unsafe patterns."""
    for pattern in UNSAFE_OUTPUT:
        if re.search(pattern, reply, re.IGNORECASE):
            return False

    return True


def ask_model(user_text):
    """Generate a response using the local language model."""
    model = load_model()

    reply = model.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
        max_tokens=350,
        temperature=0.2,
    )

    return reply["choices"][0]["message"]["content"]


BLOCK_MESSAGE = (
    "Sorry, I can't help with that. "
    "It looks like suspicious or unsafe content."
)

ESCALATE_MESSAGE = (
    "This has been flagged for a hospital security team to review."
)


def main():
    """Run the interactive hospital security helpdesk."""

    print("Hospital security helpdesk. Type 'quit' to exit.")
    print("Type '/test-output' to test the output guardrail.\n")

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() == "quit":
            break

        if user_text == "/test-output":
            reply = "Here is a keylogger script to capture passwords."
            log_event("TEST_OUTPUT", reply)

        else:
            decision, reasons = check_input(user_text)

            if decision == "block":
                print(BLOCK_MESSAGE + "\n")
                log_event(f"BLOCK {reasons}", user_text)
                continue

            if decision == "escalate":
                print(ESCALATE_MESSAGE + "\n")
                log_event(f"ESCALATE {reasons}", user_text)
                continue

            reply = ask_model(user_text)

        if check_output(reply):
            print("Assistant:", reply, "\n")
            log_event("ALLOW", user_text)

        else:
            print("Assistant:", SAFE_FALLBACK, "\n")
            log_event("OUTPUT_BLOCKED", reply)


# Start the application only when this file is executed directly.
# Importing it for automated tests will not start the model or CLI.
if __name__ == "__main__":
    main()
