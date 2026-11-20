const { readFileSync } = require('node:fs');
const assert = require('node:assert/strict');
const { test } = require('node:test');
const { runInNewContext } = require('node:vm');
const { join } = require('node:path');

const root = join(__dirname, '..');
const html = readFileSync(join(root, 'dashboard/index.html'), 'utf8');
const script = html.split('<script>')[1].split('</script>')[0];
const status = { paky: 1, ok: true, text: "Ciao, sono Paky76.", ip: '192.168.1.43', ssid: 'TestLab', volume: 45, apn: 'iot.example', open: false };
const event = { preventDefault() {} };
const flush = () => new Promise(resolve => setImmediate(resolve));

function launch(pathname, capabilities) {
  const ids = [...html.matchAll(/id="([^"]+)"/g)].map(match => match[1]);
  const elements = Object.fromEntries(ids.map(id => [id, { value: '', textContent: '', classList: { toggle() {} } }]));
  const location = { pathname };
  runInNewContext(script, {
    location, document: { getElementById: id => elements[id] },
    TextEncoder, TextDecoder, setTimeout, clearTimeout, ...capabilities,
  });
  return { elements, location };
}

test('the device and USB dashboard embed the same HTML', () => {
  const header = readFileSync(join(root, 'firmware/include/setup_page.h'), 'utf8');
  assert.equal(header.split('R"PAKYHTML(')[1].split(')PAKYHTML"')[0], html);
});

test('Wi-Fi status, update, test tone and private IP validation', async () => {
  const requests = [];
  const { elements, location } = launch('/setup', {
    fetch: async (url, opts) => {
      requests.push({ url, opts, body: JSON.parse(opts.body) });
      return { ok: true, json: async () => status };
    },
  });
  await flush();
  assert.equal(elements.address.textContent, status.ip);
  assert.equal(elements.ssid.value, status.ssid);
  elements.password.value = 'test-password';
  await elements.settings.onsubmit(event);
  assert.equal(elements.password.value, '');
  await elements.tone.onclick();
  assert.deepEqual(requests.map(req => req.body.cmd), ['status', 'save', 'tone']);
  assert.ok(requests.every(req => req.url === '/api/config' && req.opts.headers['X-Paky-Setup'] === '1'));
  elements.ip.value = '8.8.8.8';
  elements.openip.onsubmit(event);
  assert.equal(location.href, undefined);
  elements.ip.value = status.ip;
  elements.openip.onsubmit(event);
  assert.equal(location.href, 'http://192.168.1.43/setup');
});

test('USB framing, setup key, hotspot recovery and disconnect', async () => {
  let controller;
  const readable = new ReadableStream({ start(c) { controller = c; } });
  const requests = [];
  const writable = new WritableStream({
    write(bytes) {
      const frame = new TextDecoder().decode(bytes);
      assert.ok(frame.endsWith('\n'));
      requests.push(JSON.parse(frame));
      const reply = JSON.stringify({ ...status, setupKey: '0123456789ab', ap: 'Paky76-TEST' });
      controller.enqueue(new TextEncoder().encode(reply.slice(0, 12)));
      controller.enqueue(new TextEncoder().encode(reply.slice(12) + '\n'));
    },
  });
  let closed = false;
  const port = { readable, writable, async open(options) { assert.equal(options.baudRate, 115200); }, async close() { closed = true; } };
  const { elements } = launch('/', { navigator: { serial: { async requestPort() { return port; } } } });
  await elements.usb.onclick();
  assert.equal(elements.transport.textContent, 'USB');
  assert.match(elements.ap.textContent, /0123456789ab/);
  await elements.reopen.onclick();
  assert.equal(requests[1].cmd, 'ap');
  elements.prompt.value = 'ciao';
  await elements.basic.onsubmit(event);
  assert.equal(requests[2].cmd, 'ask_basic');
  assert.equal(requests[2].prompt, 'ciao');
  assert.equal(elements.answer.textContent, status.text);
  await elements.usb.onclick();
  await flush();
  assert.ok(closed);
  assert.equal(elements.save.disabled, true);
});
