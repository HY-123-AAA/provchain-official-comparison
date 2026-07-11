# PROVCHAIN Official-System Comparison Fixture

This repository is an experiment fixture, not the main PROVCHAIN source repository.

It contains frozen Qwen-generated outputs exported from the local experiment. The original prompts are deliberately excluded. GitHub Actions deterministically packages each selected output and creates a signed SLSA build provenance attestation using `actions/attest`.

The resulting archives, source manifest, GitHub attestation bundle, and verifier logs are imported back into the local PROVCHAIN experiment artifacts. They are used for the official-system comparison with in-toto, gittuf, Cosign/Sigstore, and SLSA verification.
