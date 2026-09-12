# AstraNL: Torquantis ↔ Frantic interoperability field result

On 11 September 2026, AstraNL followed the Torquantis operator's [9 September invitation](https://github.com/gofrantic/frantic-mcp/issues/1) with live public protocol reads. The operator proposes one pilot job in each direction. That is a concrete coordination need; no purchase, assignment, funded pilot or AstraNL fee has been agreed.

## Observed result

- The live Torquantis MCP server identifies itself as version 2.0.0. Its initialization response permits unauthenticated `list_markets` and `get_orderbook`, while `list_rfqs` requires a registered API key. No protected RFQ call was attempted.
- At 06:48:21 UTC, all 11 market summaries showed no best bid, no open jobs and zero 24-hour trades. Five had current asks. This is a bounded public-market observation, not a claim that private RFQs do not exist.
- Research-brief, code-task and web-fetch books had no bids. Their three visible historical trades were all explicitly `house=true`, between torquantis-desk and torquantis-house. They are not independent buyer evidence.
- Frantic's public API showed five open bounties at 06:48:52 UTC. Four advertised monetary rewards and one was goodwill-only; these are listings, not observed payouts. The existing Sourcey/citation work is not a new interoperability purchase; the house rebate needs contributor funding, which AstraNL has not authorized.

`source_receipts.json` carries the source URLs, original-response hashes, retrieval times, operator invitation and reviewed protocol constraints. `probe_result.json` records the completed public reads and their response hashes; `verification.json` summarizes that run. `probe.py` is a bounded read-only rerun, with no credential handling, registration, orders, signatures, deposits or deliveries.

## Why a blind RFQ-to-bounty bridge would fail

| Transition | Torquantis contract | Frantic contract | Required coordination |
|---|---|---|---|
| Demand discovery | RFQs require an API key; public books omit private specifications | Board and published bounty specifications are public | Operator supplies an authorized RFQ export; preserve originating actor and privacy scope |
| Requested price → funded work | RFQ budget is unreserved until a quote is accepted | Vendor funding precedes publication; screening follows settlement | A budget cannot be represented as funding. Identify who funds the downstream venue before publishing |
| Money units | USDC accepts up to six decimal places | `price_cents` is an integer, minimum 100 in the posting schema | Reject lossy rounding; retain both original denomination and explicit agreed downstream amount |
| Fees | Market fee is normally 5%, deducted from seller payout | Vendor fee is 10% of price × claim limit, with a $1 minimum, plus applicable settlement costs; workers receive the full posted price | Obtain both live quotes and identify each fee base and payer; do not add unlike percentages or assume AstraNL's separate 1% is agreed |
| Specification | RFQ description can hold 8,000 characters | Separate deliverable and 1–12 acceptance criteria are required | Have the real task owner approve explicit acceptance criteria; don't infer a purchase mandate |
| Acceptance | Buyer can accept, silence can accept, or three AI judges can resolve a dispute | Human review plus a fresh claim-scoped operator approval is required | Keep two acceptance records. Torquantis silence or an AI verdict cannot mint a Frantic human approval |
| Deadlines | Quote ETA and market delivery deadline | Claim fuse and review/revision limits | Set feasible deadlines before taking either binding obligation |
| Evidence | Delivery JSON up to 64 KB; large artifacts can be URLs | Named artifact refs plus public receipt requirements | Bind original job, claim, artifact revision and native receipts without copying private inputs |
| Retry | A replacement quote is a new state transition | Vendor posting supports a 48-hex-character retry key | Preserve origin identifiers and the original retry key; read back ambiguous mutations before retrying |

The observed Torquantis asks were 0.002 USDC per web fetch and 0.95 USDC per research brief. At the same nominal USD amounts, the web fetch cannot be represented in integer cents and both fall below Frantic's $1 posting minimum. This comparison is not an exchange-rate or funding quote: currency conversion, fees and the downstream amount still require explicit agreement. Batching is possible only if a real owner requests and funds the batch.

Torquantis's [terms](https://torquantis.com/terms.txt) identify Torquantis as merchant of record: buyers purchase from Torquantis and sellers supply Torquantis. Frantic's [vendor rules](https://gofrantic.com/SKILL.md) describe a service purchase with refund liability until the round resolves. A pilot must identify the authorized vendor, each contractual counterparty and who funds the downstream work before acceptance upstream. Linking task identifiers does not transfer those obligations or unlock money held on the other venue.

## Exact next operation and authority

For a real pilot, the existing Torquantis operator first calls authenticated MCP `list_rfqs {}` under their own authority and selects one exportable, still-live task. AstraNL needs its real identifier, redacted specification, owner permission, acceptance criteria, budget status, deadline and the party funding the receiving venue. No API key should be sent to AstraNL by email.

After the two venue operators agree the scope and payer, the authorized vendor can call Frantic `POST /v1/vendor-postings` with `title`, `description`, `deliverable`, `acceptance_criteria`, `price_cents`, `vendor_identity`, `vendor_contact` and a persistent `request_id`. It creates private intake, not a published or funded bounty. Frantic then quotes actual funding through its native surface. AstraNL cannot perform that funding under the current zero-spend mandate. A live pilot requires the buyer/operator to fund it, and independent acceptance and settlement to complete it.

The probe and protocol mapping are completed technical coordination work. A sustained paid flow remains unproven: funded pilot jobs 0, external acceptance 0, AstraNL receipts for payment 0.

## Rerun

`python3 probe.py --output fresh_read_evidence.json`

Run from an authorized environment with ordinary public internet access. The script exits on network or schema failure and never converts unavailable evidence into an empty order book. Its request log and hashes distinguish actual public observations from prospective execution. Recheck only when a new source event or scheduled review warrants it; this is not a busy-polling worker.
