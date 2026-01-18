# @jailbreak-shield/node

Official Node.js client for Jailbreak Shield Aegis.

## Usage

```bash
npm install @jailbreak-shield/node
```

```javascript
import { AegisClient } from '@jailbreak-shield/node';

const client = new AegisClient({
  baseUrl: 'http://localhost:8000/api/v1'
});

const result = await client.analyze("Drop database");

if (!result.safe) {
  console.log("Blocked:", result.explanation);
}
```
