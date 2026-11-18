# Project Requirements

## 1. Project title

Customer Support LLM Fine-Tuning Project

## 2. Problem statement

General-purpose language models can answer customer questions, but they may use the wrong tone, provide inconsistent answers, or invent policy details. This project will customize an open-source instruction-following LLM for customer-support conversations.

The model will learn to produce concise, professional, policy-aware responses from curated examples. Deployment is outside the scope of this stage and will be handled later.

## 3. Intended users

- Customer-support agents who need draft responses
- Customers asking common product and order questions
- AI engineers evaluating domain-specific model customization

## 4. Intended use cases

The model should help with:

- Product and service questions
- Shipping and delivery questions
- Return and refund questions
- Account and order-support questions
- Complaints and emotionally charged messages
- Requests that require escalation to a human agent

## 5. Expected behavior

The assistant should:

- Answer using clear, polite, professional language
- Give direct answers when the required information is available
- Ask for missing information when necessary
- Clearly state uncertainty instead of guessing
- Follow the support policy represented in the training data
- Protect customer privacy
- Escalate cases that require human judgment
- Keep responses concise unless the user needs more explanation

## 6. Out-of-scope behavior

The assistant should not:

- Invent company policies, prices, delivery dates, or guarantees
- Expose personal or confidential customer information
- Make legal, medical, or financial decisions
- Approve exceptions that require human authorization
- Pretend that it completed an action it cannot perform
- Answer unsupported questions as if they were certain

## 7. Initial technical approach

- Start with an open-source instruction-following language model
- Establish a baseline using the original model
- Use supervised fine-tuning (SFT)
- Use LoRA or QLoRA to reduce training requirements
- Keep the final model checkpoint and adapter versioned by experiment
- Evaluate against both the original model and a prompt-only baseline

## 8. Dataset requirements

Training examples should contain a user message and an approved assistant response. Examples should cover normal, difficult, ambiguous, out-of-scope, privacy-sensitive, and escalation scenarios.

Every example must be:

- Correct and relevant
- Free of real personal information
- Consistent with the selected support policy
- Assigned to a useful category
- Valid according to the project dataset schema

The dataset will be split into training, validation, and test sets. Test examples must not be used during training.

## 9. Success criteria

The fine-tuned model will be considered successful when it demonstrates measurable improvement over the baseline on the target support task, including:

- Correctness on common support questions
- Appropriate uncertainty and escalation behavior
- Consistent professional tone
- Reduced hallucination of unsupported policies
- Reliable handling of difficult and out-of-scope questions
- Valid output format for the planned inference interface

Exact numeric thresholds will be finalized after the baseline evaluation and initial dataset review.

## 10. Evaluation requirements

Evaluation will combine:

- Automated task-appropriate metrics
- Human review using a documented rubric
- Side-by-side comparison with the base model
- Failure analysis by error category
- Safety and privacy tests

Evaluation results must be reproducible from a recorded model version, dataset version, and configuration.

## 11. Current scope

Included:

- Requirements definition
- Dataset creation and preparation
- Base-model selection
- Baseline evaluation
- Fine-tuning experiments
- Evaluation and failure analysis
- Final checkpoint and documentation packaging

Deferred:

- Production deployment
- Public API
- User interface
- Authentication and authorization
- Production monitoring and scaling

## 12. Assumption to validate

This project currently assumes a generic online-store customer-support scenario. Before dataset creation, we will define the specific fictional support policy and domain vocabulary so that the examples remain consistent and do not depend on private company data.
