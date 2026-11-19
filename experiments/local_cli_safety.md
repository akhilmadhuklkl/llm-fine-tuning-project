# Local CLI safety

The local CLI now fails before returning a result if the safety-output checker detects a direct unsafe action. This keeps the local application path aligned with the CI safety gate.
