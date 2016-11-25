## Instructions for nodeMCU on encryption

To send a message to the cloud, do the following:

1. Send a GET request to `http://vast-lake-95491.herokuapp.com/nonce`
1. Save the `cookie` found in the response headers.
1. The response body is the `nonce_hex`.
1. Hex-decode the `nonce_hex` to get `nonce_bytes`.
1. Hex-decode the contents of `security/keys/public/server` to get `server_public_bytes`.
1. Hex-decode the contents of `security/keys/private/node` to get `node_secret_bytes`.
1. Hex-decode the contents of `security/keys/sign/node` to get `node_sign_bytes`.
1. Encrypt your `plaintext` message using `nonce_bytes`, `node_secret_bytes`, and `server_public_bytes` to get `ciphertext`.
1. Sign the `ciphertext` using `node_sign_bytes` to get `signedtext`.
1. Hex-encode `signedtext` to get `signedtext_hex`.
1. Prepend `node_` to `signedtext_hex` to get `transmittext_hex`.
1. Put `transmittext_hex` as the raw body of the HTTP POST.
1. Add a header key `Cookie`, with value `cookie` from step 2.
1. Send the HTTP POST to `http://vast-lake-95491.herokuapp.com/send_message`.
1. The response you should get is the `plaintext`.  Your message was accepted.  Hooray!

There is a Python example for the above actions in [client.py](security/tests/client.py).

A note on keys and sender name to prepend:

- If you are `node03`, use the `private` and `sign` keys with filename `node03`.
- If you are `node03`, prepend `node03_` to `signedtext_hex` before sending.

