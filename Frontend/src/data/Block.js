const Block = [
  {
    nonce: "12345",
    previous_hash: "0",
    hash: "abcd1234567890efgh",
    timestamp: "2024-02-20T12:00:00Z",
  },
  {
    nonce: "67890",
    previous_hash: "abcd1234567890efgh",
    hash: "efgh1234567890ijkl",
    timestamp: "2024-02-20T12:15:00Z",
  },
  {
    nonce: "54321",
    previous_hash: "efgh1234567890ijkl",
    hash: "ijkl1234567890mnop",
    timestamp: "2024-02-20T12:30:00Z",
  },
  {
    nonce: "98765",
    previous_hash: "ijkl1234567890mnop",
    hash: "mnop1234567890qrst",
    timestamp: "2024-02-20T12:45:00Z",
  },
  {
    nonce: "24680",
    previous_hash: "mnop1234567890qrst",
    hash: "qrst1234567890uvwx",
    timestamp: "2024-02-20T13:00:00Z",
  },
];
export { Block };
