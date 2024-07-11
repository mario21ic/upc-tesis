# Question
What elliptic curve algorithms can be used in certificate chains according to the CA/Browser Forum’s Baseline Requirements for the Issuance and Management of Publicly-Trusted TLS Server Certificates and the Mozilla Root Store Policy?

Rationale for the question
Considering that a public CA needs that their certificates work in any browser it is important to choose only the intersection of allowed algorithms across all the relevant specifications.

Expected answer
Only the curves P-256 and P-384 are supported by both specifications. Other curves like P-521, Curve25519, and Curve448 are not compatible with both specifications at the same time.

Sources
https://raw.githubusercontent.com/cabforum/servercert/main/docs/BR.md allows three curves:

6.1.5 Key sizes
…

For ECDSA key pairs, the CA SHALL:

* Ensure that the key represents a valid point on the NIST P-256, NIST P-384 or NIST P-521 elliptic curve.

No other algorithms or key sizes are permitted.

While https://raw.githubusercontent.com/mozilla/pkipolicy/master/rootstore/policy.md indicates that only two of the previous three are supported:

Root certificates in our root store, and any certificate that chains up to them, MUST use only algorithms and key sizes from the following set:

…

* ECDSA keys using one of the following curves:

* P-256; *or*

* P-384.

The following curves are not prohibited, but are not currently supported: P-521, Curve25519, and Curve448.

Example ChatGPT chat
https://chatgpt.com/share/b6b06c76-a9f9-4fb7-aa56-e36c1e5a85cf
