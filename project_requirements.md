# Project Requirements

## 1. Project title

IT Incident Triage and Runbook Assistant

## 2. Problem statement

Engineering teams receive incident reports in inconsistent formats and must quickly determine severity, affected systems, likely causes, and the next diagnostic steps. A general-purpose language model may produce inconsistent triage decisions or suggest unsafe actions.

This project will customize an open-source instruction-following LLM for internal incident triage. The model will transform incident descriptions into structured triage information and recommend safe, documented next steps. It will support engineers, but it will not autonomously execute infrastructure changes.

Deployment is outside the scope of this stage and will be handled later.

## 3. Intended users

- Site reliability engineers
- Platform and DevOps engineers
- Software engineers responding to incidents
- Engineering managers reviewing incident status

## 4. Intended use cases

The model should help with:

- Classifying incident type and severity
- Extracting affected services, symptoms, and timestamps
- Identifying missing information in an incident report
- Recommending the next diagnostic steps
- Selecting a relevant runbook section
- Drafting concise internal incident updates
- Identifying when an incident should be escalated
- Summarizing a resolved incident for later review

## 5. Expected behavior

The assistant should:

- Produce consistent structured triage output
- Separate observed facts from hypotheses
- State uncertainty clearly
- Ask for missing information before making strong recommendations
- Recommend reversible and low-risk diagnostic actions first
- Reference the relevant runbook or procedure when available
- Assign severity using documented criteria
- Escalate incidents that exceed its confidence or authority
- Use concise, professional engineering language

## 6. Out-of-scope behavior

The assistant should not:

- Execute commands or modify infrastructure
- Restart services, delete data, or change production configuration
- Claim that it inspected logs or systems when it did not
- Invent metrics, alerts, dependencies, or runbook steps
- Override an engineer’s incident-severity decision
- Expose secrets, credentials, tokens, or private customer data
- Treat an uncertain hypothesis as a confirmed root cause

## 7. Initial technical approach

- Start with an open-source instruction-following language model
- Establish a baseline using the original model
- Use supervised fine-tuning (SFT)
- Use LoRA or QLoRA to reduce training requirements
- Train on sanitized incident examples and approved runbook responses
- Evaluate against both the original model and a prompt-only baseline
- Keep model checkpoints and adapters versioned by experiment

## 8. Dataset requirements

Training examples should contain an incident report or engineering request and an approved assistant response. Where useful, responses should include structured fields such as:

```json
{
  "severity": "SEV-2",
  "incident_type": "database_latency",
  "affected_services": ["orders-api"],
  "observed_facts": ["p95 latency increased"],
  "hypotheses": ["database connection saturation"],
  "next_steps": ["check connection pool utilization"],
  "escalation_required": true
}
```

Examples should cover normal, difficult, ambiguous, incomplete, and high-severity incidents. They should include cases where the correct behavior is to request more information or escalate.

Every example must be:

- Technically correct and relevant
- Sanitized of credentials, secrets, and private identifiers
- Consistent with the fictional or approved operational policy
- Assigned to a useful incident category
- Valid according to the project dataset schema

The dataset will be split into training, validation, and test sets. Test examples must not be used during training.

## 9. Success criteria

The fine-tuned model will be considered successful when it demonstrates measurable improvement over the baseline on the target incident-triage task, including:

- Accurate severity classification
- Reliable extraction of affected services and observed facts
- Clear separation of facts and hypotheses
- Useful and safe next-step recommendations
- Correct escalation behavior
- Consistent structured output
- Reduced hallucination of infrastructure details

Exact numeric thresholds will be finalized after the baseline evaluation and initial dataset review.

## 10. Evaluation requirements

Evaluation will combine:

- Automated classification and field-extraction metrics
- JSON/schema validity checks
- Human review using a documented rubric
- Side-by-side comparison with the base model
- Failure analysis by error category
- Safety tests for destructive or unauthorized actions

Evaluation results must be reproducible from a recorded model version, dataset version, and configuration.

## 11. Current scope

Included:

- Requirements definition
- Synthetic and sanitized incident-dataset creation
- Dataset preparation and validation
- Base-model selection
- Baseline evaluation
- Fine-tuning experiments
- Evaluation and failure analysis
- Final checkpoint and documentation packaging

Deferred:

- Production deployment
- Connection to live monitoring or ticketing systems
- Automatic command execution
- Public API
- User interface
- Authentication and authorization
- Production monitoring and scaling

## 12. Assumption to validate

This project currently assumes a fictional software platform with documented services, severity criteria, and runbook procedures. Before dataset creation, we will define that fictional platform so examples remain consistent and do not depend on private production data.
