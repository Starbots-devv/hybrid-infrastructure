# Security policy

## Supported versions

Starbots Hybrid Infrastructure is in alpha. Security fixes are made on the latest version on the `main` branch.

## Reporting a vulnerability

Report vulnerabilities privately through GitHub: open this repository's **Security** tab and choose **Report a vulnerability**. Please do not open a public issue for a suspected vulnerability.

Include the affected version and a minimal reproduction that uses synthetic data only. Never include customer inventories, credentials, provider account identifiers, signing keys or production URLs.

## Scope

The CLI is an offline decision aid. Its analyses and the in-memory SQS simulation cannot change real infrastructure, and no result is an approval to do so. `sb-hybrid verify-security` checks the integrity and scope of a security review against a SHA-256 receipt you obtained separately; a hash is not a publisher signature. Missing or stale material stays UNKNOWN or blocked.

The SQS simulator has no AWS SDK, credentials path or real transport. Its signature, journal and replay controls are demonstration mechanisms scoped to one local installation.
