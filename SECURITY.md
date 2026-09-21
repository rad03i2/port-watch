# Security Policy

## Scope
Port Watch opens outbound TCP connections to hosts and ports explicitly supplied by the operator. It does not authenticate, exploit, fingerprint, or send application-layer payloads.

## Safe use
Use this tool only on systems you own or are authorized to test. The CLI limits a single port specification to 256 distinct ports by default to discourage accidental broad scans. Avoid aggressive intervals against remote infrastructure.

## Privacy
Port Watch has no telemetry, analytics, cloud backend, credential storage, or API keys. JSON output may contain hostnames/IP addresses; treat logs according to your environment's privacy requirements.

## Reporting
Please report security concerns privately through GitHub's supported security reporting channel when available. Do not include credentials, private keys, or sensitive production data in public issues.

Maintainer: Radwan Abdulhadi Ahmed (@rad03i2)
