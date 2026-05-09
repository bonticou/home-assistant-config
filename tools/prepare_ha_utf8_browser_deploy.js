#!/usr/bin/env node

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const repo = path.resolve(__dirname, "..");
const defaultFiles = [
  "configuration.yaml",
  "automations.yaml",
  "scripts.yaml",
  "dashboards/calm_mobile.yaml",
  "www/calm-mobile-scrollbars.js",
  "www/house-notices-card.js",
  "www/radon-air-quality-card.js",
  "www/casey-presence-timeline-card.js",
];

const mojibakePatterns = [
  { name: "utf8_as_latin1_emoji", source: "[\\u00f0][\\u009f\\u0178]" },
  { name: "utf8_as_latin1_two_byte", source: "[\\u00c2\\u00c3][\\u0080-\\u00bf\\u00a0-\\u00ff]" },
  { name: "utf8_as_cp1252_symbols", source: "\\u00e2[\\u0080-\\u00bf\\u0152\\u0153\\u0160\\u0161\\u2018-\\u2026]" },
];

function usage() {
  console.log(`Usage:
  node tools/prepare_ha_utf8_browser_deploy.js [options] [local[:remote] ...]

Options:
  --out PATH       Browser JavaScript output path
  --no-reload      Write and verify files without reloading HA config domains
  --help           Show this help

If no files are supplied, the helper deploys the standard Home Assistant config
files used by this repo. Remote paths default to /homeassistant/<local>.
`);
}

function parseArgs(argv) {
  const options = {
    out: path.join(repo, ".tmp-ha-utf8-browser-deploy.js"),
    reload: true,
    specs: [],
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") {
      usage();
      process.exit(0);
    }
    if (arg === "--out") {
      if (!argv[i + 1]) throw new Error("--out requires a path");
      options.out = path.resolve(argv[i + 1]);
      i += 1;
      continue;
    }
    if (arg === "--no-reload") {
      options.reload = false;
      continue;
    }
    if (arg.startsWith("--")) throw new Error(`Unknown option: ${arg}`);
    options.specs.push(arg);
  }

  if (options.specs.length === 0) {
    options.specs = defaultFiles.filter((local) => fs.existsSync(path.join(repo, local)));
  }
  return options;
}

function splitSpec(spec) {
  const index = spec.indexOf(":");
  if (index === -1) return [spec, `/homeassistant/${spec}`];
  return [spec.slice(0, index), spec.slice(index + 1)];
}

function findMojibake(text) {
  for (const pattern of mojibakePatterns) {
    const re = new RegExp(pattern.source);
    const match = re.exec(text);
    if (match) {
      return {
        pattern: pattern.name,
        index: match.index,
        sample: text.slice(Math.max(0, match.index - 20), match.index + 40),
      };
    }
  }
  return null;
}

function readDeployFile(spec) {
  const [local, remote] = splitSpec(spec);
  const absolute = path.resolve(repo, local);
  if (!absolute.startsWith(repo + path.sep)) {
    throw new Error(`Refusing to read outside repo: ${local}`);
  }
  const bytes = fs.readFileSync(absolute);
  const text = bytes.toString("utf8");
  const mojibake = findMojibake(text);
  if (mojibake) {
    throw new Error(`Local file already contains likely mojibake: ${local} (${mojibake.pattern}) near ${JSON.stringify(mojibake.sample)}`);
  }
  return {
    local,
    remote,
    b64: bytes.toString("base64"),
    sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    bytes: bytes.length,
  };
}

function browserScript(files, reload) {
  const payload = {
    files,
    reload,
    mojibakePatterns,
  };

  return `
(() => {
  const payload = ${JSON.stringify(payload)};
  const resultKey = "__haUtf8DeployResult";
  const setResult = (value) => {
    window[resultKey] = JSON.stringify(value);
    return window[resultKey];
  };

  function findFileEditorFrame() {
    const frames = [];
    const seen = new Set();
    function walk(node) {
      if (!node || seen.has(node)) return;
      seen.add(node);
      if (node.nodeType === 1) {
        if (node.localName === "iframe") frames.push(node);
        if (node.shadowRoot) walk(node.shadowRoot);
      }
      for (const child of node.children || []) walk(child);
    }
    walk(document.documentElement);
    return frames.find((frame) => {
      try {
        return String(frame.src || "").includes("/api/hassio_ingress/");
      } catch (_) {
        return false;
      }
    }) || frames[frames.length - 1] || null;
  }

  function frontendHass() {
    const root = document.querySelector("home-assistant");
    return root && root.hass ? root.hass : null;
  }

  function authToken() {
    for (const key of Object.keys(localStorage)) {
      try {
        const parsed = JSON.parse(localStorage.getItem(key) || "null");
        if (parsed && typeof parsed === "object") {
          if (typeof parsed.access_token === "string") return parsed.access_token;
          if (parsed.data && typeof parsed.data.access_token === "string") return parsed.data.access_token;
        }
      } catch (_) {}
    }
    return null;
  }

  async function haRequest(method, endpoint, payload) {
    const token = authToken();
    if (token) {
      const response = await fetch(endpoint, {
        method,
        credentials: "include",
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload || {}),
      });
      const text = await response.text();
      if (!response.ok) throw new Error(method + " " + endpoint + " -> " + response.status + ": " + text.slice(0, 500));
      try { return JSON.parse(text); } catch (_) { return text; }
    }

    const hass = frontendHass();
    if (!hass) throw new Error("Could not find Home Assistant auth token or frontend hass object");
    const apiPath = endpoint.replace(/^\\/api\\//, "").replace(/^\\//, "");
    return hass.callApi(method, apiPath, payload);
  }

  async function boundedHaRequest(label, method, endpoint, payload, timeoutMs = 8000) {
    let timeoutId;
    const timeout = new Promise((resolve) => {
      timeoutId = setTimeout(() => resolve({ label, ok: false, timeout: true }), timeoutMs);
    });
    const request = haRequest(method, endpoint, payload)
      .then((response) => ({ label, ok: true, response }))
      .catch((error) => ({ label, ok: false, error: String(error && (error.message || error) || error) }))
      .finally(() => clearTimeout(timeoutId));
    return Promise.race([request, timeout]);
  }

  async function digestHex(text) {
    const bytes = new TextEncoder().encode(text);
    const hash = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(hash)).map((byte) => byte.toString(16).padStart(2, "0")).join("");
  }

  function decodeBase64Utf8(value) {
    const binary = atob(value);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
    return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  }

  function findMojibake(text) {
    for (const pattern of payload.mojibakePatterns) {
      const match = new RegExp(pattern.source).exec(text);
      if (match) {
        return {
          pattern: pattern.name,
          index: match.index,
          sample: text.slice(Math.max(0, match.index - 20), match.index + 40),
        };
      }
    }
    return null;
  }

  function firstDifference(left, right) {
    const max = Math.min(left.length, right.length);
    for (let i = 0; i < max; i += 1) {
      if (left[i] !== right[i]) return i;
    }
    return left.length === right.length ? -1 : max;
  }

  const inner = async (incoming) => {
    const writes = [];
    const fileBase = "";

    function decodeBase64Utf8(value) {
      const binary = atob(value);
      const bytes = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
      return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    }

    function findMojibake(text) {
      for (const pattern of incoming.mojibakePatterns) {
        const match = new RegExp(pattern.source).exec(text);
        if (match) {
          return {
            pattern: pattern.name,
            index: match.index,
            sample: text.slice(Math.max(0, match.index - 20), match.index + 40),
          };
        }
      }
      return null;
    }

    function firstDifference(left, right) {
      const max = Math.min(left.length, right.length);
      for (let i = 0; i < max; i += 1) {
        if (left[i] !== right[i]) return i;
      }
      return left.length === right.length ? -1 : max;
    }

    async function fileRequest(method, endpoint, body) {
      const options = { method, credentials: "include" };
      if (body !== undefined) options.body = body;
      const response = await fetch(endpoint, options);
      const text = await response.text();
      if (!response.ok) {
        throw new Error(method + " " + endpoint + " -> " + response.status + ": " + text.slice(0, 500));
      }
      return text;
    }

    async function readFile(filename) {
      return fileRequest("GET", fileBase + "api/file?filename=" + encodeURIComponent(filename));
    }

    async function saveFile(filename, text) {
      const body = new URLSearchParams({ filename, text });
      await fileRequest("POST", fileBase + "api/save", body);
    }

    for (const file of incoming.files) {
      const text = decodeBase64Utf8(file.b64);
      const localMojibake = findMojibake(text);
      if (localMojibake) {
        throw new Error("Decoded local payload contains likely mojibake in " + file.local + ": " + JSON.stringify(localMojibake));
      }

      await saveFile(file.remote, text);
      const readBack = await readFile(file.remote);
      const readBackMojibake = findMojibake(readBack);
      if (readBackMojibake) {
        throw new Error("Read-back contains likely mojibake in " + file.remote + ": " + JSON.stringify(readBackMojibake));
      }

      if (readBack !== text) {
        const index = firstDifference(text, readBack);
        throw new Error("Read-back mismatch for " + file.remote + " at offset " + index);
      }

      writes.push({ file: file.remote, bytes: text.length, sha256: file.sha256 });
    }
    return { writes };
  };

  (async () => {
    setResult({ ok: null, phase: "starting" });
    const frame = findFileEditorFrame();
    const fileEditorWindow = frame && frame.contentWindow ? frame.contentWindow : window;
    setResult({ ok: null, phase: "writing" });
    const writeResult = await fileEditorWindow.eval("(" + inner.toString() + ")(" + JSON.stringify(payload) + ")");
    setResult({ ok: null, phase: "checking", writes: writeResult.writes });
    const check = await haRequest("POST", "/api/config/core/check_config", {});
    const checkResult = typeof check === "object" ? check : { response: check };
    if (checkResult.result && checkResult.result !== "valid") {
      setResult({ ok: false, phase: "check_config", writes: writeResult.writes, check: checkResult });
      return;
    }
    if (payload.reload) {
      setResult({ ok: null, phase: "reloading", writes: writeResult.writes, check: checkResult });
      const reloads = [];
      reloads.push(await boundedHaRequest("template.reload", "POST", "/api/services/template/reload", {}));
      reloads.push(await boundedHaRequest("script.reload", "POST", "/api/services/script/reload", {}));
      reloads.push(await boundedHaRequest("automation.reload", "POST", "/api/services/automation/reload", {}));
      setResult({ ok: true, phase: "reload_checked", writes: writeResult.writes, check: checkResult, reloads });
      return;
    }
    setResult({ ok: true, phase: payload.reload ? "reload_called" : "verified", writes: writeResult.writes, check: checkResult });
  })().catch((error) => {
    setResult({
      ok: false,
      phase: "error",
      error: String(error && (error.message || error) || error),
      stack: String(error && error.stack || ""),
    });
  });

  return setResult({ ok: null, phase: "queued" });
})();
`;
}

try {
  const options = parseArgs(process.argv.slice(2));
  const files = options.specs.map(readDeployFile);
  const output = browserScript(files, options.reload);
  fs.writeFileSync(options.out, output, "ascii");
  console.log(JSON.stringify({
    ok: true,
    browserJs: options.out,
    resultKey: "__haUtf8DeployResult",
    reload: options.reload,
    files: files.map(({ local, remote, bytes, sha256 }) => ({ local, remote, bytes, sha256 })),
  }, null, 2));
} catch (error) {
  console.error(error && error.stack || error);
  process.exit(1);
}
