const { runAgent } = require('./agent');

const args = process.argv.slice(2);
const topic = args.length > 0 ? args.join(' ') : "Operating Systems";

runAgent(topic);
