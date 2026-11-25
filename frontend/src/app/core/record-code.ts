export function newRecordCode(): string {
  return Array.from(crypto.getRandomValues(new Uint8Array(5)), byte =>
    byte.toString(16).padStart(2, '0')
  ).join('');
}
