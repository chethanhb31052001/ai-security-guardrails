
# Applied AI Guardrails for Healthcare IT Helpdesk

A locally deployed AI-powered cybersecurity helpdesk assistant designed for a hospital IT environment. This project combines a local Large Language Model (LLM) with Python-based security guardrails to identify potentially unsafe requests, protect sensitive information, and provide controlled cybersecurity assistance.

## Project Overview

Healthcare organisations handle sensitive patient and staff information. An AI-powered IT helpdesk must therefore consider security, confidentiality, and responsible access to information.

This project demonstrates how a locally running language model can be combined with rule-based security controls to manage potentially risky requests.

The application uses Qwen2.5-1.5B-Instruct in GGUF format through llama-cpp-python. Model inference runs locally, without requiring an external AI API.

## Key Features

- Local LLM deployment using Qwen2.5-1.5B-Instruct.
- Lazy model loading to avoid loading the model when it is not required.
- Input risk detection using regular-expression rules.
- Detection of potentially unauthorised patient record access.
- Credential misuse detection.
- Protection against unauthorised staff directory requests.
- Detection and escalation of selected ransomware and data breach indicators.
- Output validation against predefined unsafe-response patterns.
- Safe fallback responses when unsafe output is detected.
- Timestamped security event logging.
- Automated unit tests for input and output security rules.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12.10 | Application development |
| Qwen2.5-1.5B-Instruct | Local language model |
| GGUF Q4_K_M | Quantised model format |
| llama-cpp-python 0.3.36 | Local model inference |
| Regular Expressions | Rule-based security checks |
| Python unittest | Automated security testing |
| Python datetime | Timestamped event logging |

## Project Structure

```text
ai-security-guardrails/
│
├── models/                 # Local AI model (not uploaded)
│
├── guardrails.py           # Main application and security logic
├── test_model.py           # Standalone model inference test
├── test_guardrails.py      # Automated security unit tests
├── requirements.txt        # Python dependencies
├── .gitignore              # Excluded files and folders
└── README.md               # Project documentation
```

The GGUF model, virtual environment, Python cache files, and local security logs are excluded from version control.

## How It Works

1. The application starts the hospital security helpdesk without immediately loading the local model.
2. A user submits a request through the command-line interface.
3. The input is checked against predefined security rules.
4. The application makes one of three decisions:

   - **Allow:** The request passes the configured input checks and is sent to the LLM.
   - **Block:** The request meets the blocking threshold and is rejected.
   - **Escalate:** The request is flagged for hospital IT Security team review.

5. When an allowed request requires an AI response, the local model is loaded if it has not already been loaded.
6. The generated response is checked against predefined unsafe-output patterns.
7. Unsafe responses matching those patterns are replaced with a safe fallback message.
8. Security decisions are recorded in a local log file with timestamps.

## Security Categories

| Category | Example risk |
|---|---|
| Attack assistance | Requests for malware or credential theft |
| Patient snooping | Unauthorised access to medical records |
| Credential misuse | Sharing passwords or bypassing authentication |
| Sensitive directory | Requests for staff or doctor information |
| Security incident | Ransomware indicators or possible data exposure |

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/ai-security-guardrails.git
cd ai-security-guardrails
```

Replace `YOUR-GITHUB-USERNAME` with your actual GitHub username after publishing the repository.

### 2. Create a Python virtual environment

```bash
python -m venv venv
```

Activate it using PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Note: llama-cpp-python may require a compatible prebuilt wheel or additional native build tools depending on your operating system and Python environment.

### 4. Obtain the local AI model

Download a compatible Qwen2.5-1.5B-Instruct GGUF model in Q4_K_M quantisation.

Create a `models` directory and place the model inside it using this filename:

```text
qwen2.5-1.5b-instruct-q4_k_m.gguf
```

The model file is not included in this repository because of its large size.

Check the model's licence and distribution terms before downloading or redistributing it.

### 5. Run the application

```bash
python guardrails.py
```

The interactive hospital security helpdesk starts. The local model is loaded only when an allowed request requires AI inference.

Type `quit` to exit.

## Model Testing

To test the local model independently of the guardrail application:

```bash
python test_model.py
```

This sends a basic cybersecurity question to the local model.

The local model file must be present in the `models` directory.

## Output Guardrail Testing

Inside the running application, enter:

```text
/test-output
```

This triggers a predefined unsafe-output test string to demonstrate the output validation mechanism.

The application should replace the unsafe test response with the configured safe fallback message.

## Automated Security Tests

The project includes automated unit tests using Python's built-in `unittest` framework.

Run the security tests using:

```bash
python -m unittest -v test_guardrails.py
```

The test suite currently contains nine tests covering:

- Normal requests and safe input handling.
- Malware-related requests.
- Unauthorised patient record access.
- Credential misuse.
- Ransomware incident escalation.
- Sensitive staff directory requests.
- Safe response validation.
- Unsafe keylogger output detection.
- Unsafe subprocess output detection.

### Latest Test Results

| Metric | Result |
|---|---:|
| Total tests | 9 |
| Passed | 9 |
| Failed | 0 |
| Execution time | 0.008 seconds |

All nine automated tests passed in the latest recorded test run.

These tests validate the configured input and output security rules. They do not represent comprehensive security assurance.

## Security Considerations and Limitations

This project is an educational prototype and is not a production-ready healthcare security system.

- Input detection relies on predefined regular-expression patterns and may miss unrecognised or differently phrased threats.
- Output validation uses a limited set of patterns and cannot guarantee detection of every unsafe response.
- The system does not provide comprehensive prompt-injection protection.
- The application does not connect to hospital authentication systems, patient databases, or incident-management systems.
- Escalation is displayed to the user; it does not automatically notify a real security team.
- Logs may contain user-submitted text or generated responses. Never enter real patient information, passwords, or confidential organisational data.

All security decisions should be reviewed by qualified security personnel before real-world deployment.

## Future Improvements

- Improve prompt-injection detection and adversarial input handling.
- Introduce structured security event logging.
- Add role-based access controls.
- Improve output safety evaluation.
- Integrate with a controlled security incident reporting workflow.
- Expand automated testing with additional edge cases and adversarial inputs.

## Project Context

Developed as part of an AI Security academic project, demonstrating local LLM deployment, Python-based security controls, risk classification, automated testing, and responsible AI application design.

## Author

**Chethan Bharatesh**
