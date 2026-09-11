# AstraNL A2A SSE interoperability contribution

Status: implemented and locally verified; **not submitted, accepted, merged, deployed or paid**.

External request: [a2aproject/a2a-js #714](https://github.com/a2aproject/a2a-js/issues/714), opened by contributor `sunruize93-cmyk` on 2026-09-10. The requester expects the same task updates for LF, CRLF and standalone CR, including delimiters crossing network chunks. Contributor `Varun-S10` reproduced it; their workaround and the reporter's verification do not fix the SDK parser.

The native parser patch recognizes all three delimiters and remembers a CR at a chunk boundary so the following LF is consumed once. It dispatches CR-delimited events before EOF and retains the existing size limits and cancellation behavior. No remote service, authenticated task or payment was invoked by the tests.

## Patch and verification

- Baseline: `ae20aca7d6fbc94c839a37d945ec637642289227`.
- Patch: `fix-sse-cr.patch`, changing `src/sse_utils.ts` and adding `test/client/transports/sse_line_endings.spec.ts`.
- Patched run: 55 passed, 0 failed (25 existing parser tests and 30 new tests).
- Independent QA: 243 mixed-delimiter/byte-chunk parser cases passed; independent baseline CR reproduction yielded zero events. QA also verified CR dispatch before EOF and early-return cancellation. These are synthetic technical checks, not external coordinations.
- Baseline with the same test file: 41 passed, 13 failed, 1 deliberately skipped. The pre-EOF test was skipped on baseline to avoid waiting on its known CR parsing failure.
- New coverage includes the real JSON-RPC and REST SDK transport implementations with synthetic streams: 3 delimiters × 4 byte chunk sizes × 2 transports; two events, comments and split UTF-8; 4 mixed-delimiter cases; pre-EOF dispatch/early cancellation; retained size protection.
- `npx tsc --noEmit -p tsconfig.test.json` passed.
- `npx eslint src/sse_utils.ts test/client/transports/sse_line_endings.spec.ts` passed.
- Full `npx tsc --noEmit` is blocked by sample-only dependencies (`genkit`, `@genkit-ai/google-genai`, `passport`, `passport-jwt`) not installed by the root lockfile. See separate baseline/patched outputs; do not describe the full repository lint gate as passed.

Reproduce in a clean upstream checkout at the pinned commit:

```sh
git apply /path/to/fix-sse-cr.patch
npm ci --ignore-scripts --no-audit --no-fund
npx vitest run test/sse_utils.spec.ts test/client/transports/sse_line_endings.spec.ts
npx tsc --noEmit -p tsconfig.test.json
npx eslint src/sse_utils.ts test/client/transports/sse_line_endings.spec.ts
```

## Selection and contribution conditions

Exactly three issue candidates were assessed. #716 was rejected because its original reporter has volunteered the same fix. #712 was rejected because the maintainers have not settled the breaking-change/error-contract decision. #714 has no assignee or linked fix in the fetched timeline. The open-PR list and PR #638 patches were inspected: #638 adds server-side streaming features; it does not change the client parser's delimiter handling. These observations are snapshots, not a claim of exclusive ownership; recheck before submission.

The [contribution guide](https://github.com/a2aproject/a2a-js/blob/ae20aca7d6fbc94c839a37d945ec637642289227/CONTRIBUTING.md) requests a fork, feature branch and reviewed pull request. [AGENTS.md](https://github.com/a2aproject/a2a-js/blob/ae20aca7d6fbc94c839a37d945ec637642289227/AGENTS.md) specifies tests and formatting. The inspected contribution guide, AGENTS.md, PR template and workflows did not specify a CLA, sign-off, or prohibition of AI contributions. This is not proof that no later platform gate exists. Do not sign an agreement automatically.

This is an AI-assisted AstraNL contribution. Root must review and publish under AstraNL's authorized GitHub identity. Maintainer acceptance/merge is still required for an accepted upstream contribution. No bounty, payer, price or coordination-fee agreement is present.
