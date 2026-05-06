class RadonAirQualityCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._horizon = "30d";
    this._history = {};
    this._loadingKey = "";
    this._error = "";
    this._config = {};
  }

  setConfig(config) {
    this._config = {
      entity: "sensor.basement_air_quality_radon",
      title: "Radon",
      ...config,
    };
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
    this.ensureHistory();
  }

  connectedCallback() {
    this.render();
    this.ensureHistory();
  }

  horizons() {
    return {
      "24h": { label: "24h", title: "Last 24 hours", ms: 24 * 60 * 60 * 1000, bucket: 30 * 60 * 1000 },
      "7d": { label: "7d", title: "Last 7 days", ms: 7 * 24 * 60 * 60 * 1000, bucket: 4 * 60 * 60 * 1000 },
      "30d": { label: "30d", title: "Last 30 days", ms: 30 * 24 * 60 * 60 * 1000, bucket: 12 * 60 * 60 * 1000 },
    };
  }

  async ensureHistory() {
    if (!this._hass || !this._config.entity) return;
    const horizon = this._horizon;
    const key = `${this._config.entity}:${horizon}`;
    const cached = this._history[horizon];
    if (cached && Date.now() - cached.fetchedAt < 4 * 60 * 1000) return;
    if (this._loadingKey === key) return;

    this._loadingKey = key;
    this._error = "";
    this.render();

    try {
      const horizonConfig = this.horizons()[horizon];
      const end = new Date();
      const start = new Date(end.getTime() - horizonConfig.ms);
      const path = `history/period/${start.toISOString()}?filter_entity_id=${encodeURIComponent(this._config.entity)}&end_time=${encodeURIComponent(end.toISOString())}`;
      const response = await this._hass.callApi("GET", path);
      const rows = Array.isArray(response?.[0]) ? response[0] : [];
      const data = rows
        .map((row) => {
          const value = Number(row.state);
          const at = new Date(row.last_changed || row.last_updated || row.last_reported || "").getTime();
          if (!Number.isFinite(value) || !Number.isFinite(at)) return null;
          return [at, this.bqToPci(value)];
        })
        .filter(Boolean)
        .sort((a, b) => a[0] - b[0]);

      const current = this.currentPoint();
      if (current && (!data.length || data[data.length - 1][0] < current[0] - 60 * 1000)) data.push(current);

      this._history[horizon] = {
        raw: data,
        bucketed: this.bucketData(data, horizonConfig.bucket),
        fetchedAt: Date.now(),
      };
    } catch (error) {
      this._error = "Could not load radon history.";
    } finally {
      this._loadingKey = "";
      this.render();
    }
  }

  currentPoint() {
    const state = this._hass?.states?.[this._config.entity];
    const bq = Number(state?.state);
    if (!Number.isFinite(bq)) return null;
    const at = new Date(state.last_changed || state.last_updated || Date.now()).getTime();
    return [at, this.bqToPci(bq)];
  }

  bqToPci(value) {
    return value / 37;
  }

  bucketData(data, bucketMs) {
    if (!data.length) return [];
    const buckets = new Map();
    data.forEach(([at, value]) => {
      const bucket = Math.floor(at / bucketMs) * bucketMs;
      const existing = buckets.get(bucket) || { sum: 0, count: 0, lastAt: at };
      existing.sum += value;
      existing.count += 1;
      existing.lastAt = Math.max(existing.lastAt, at);
      buckets.set(bucket, existing);
    });
    return Array.from(buckets.entries())
      .map(([, item]) => [item.lastAt, item.sum / item.count])
      .sort((a, b) => a[0] - b[0]);
  }

  statusFor(value) {
    if (!Number.isFinite(value)) {
      return { label: "Waiting for data", className: "unknown", color: "#94a3b8", copy: "Waiting on the Airthings sensor." };
    }
    if (value >= 4) {
      return { label: "Action band", className: "high", color: "#ef4444", copy: "Basement radon is high enough to deserve attention if it stays here." };
    }
    if (value >= 2.7) {
      return { label: "Watch", className: "watch", color: "#fbbf24", copy: "Basement radon is elevated; the longer trend matters most." };
    }
    return { label: "Good", className: "good", color: "#4ade80", copy: "Basement air is in the good range." };
  }

  statsFor(horizon) {
    const raw = this._history[horizon]?.raw || [];
    const current = this.currentPoint();
    const values = raw.length ? raw.map(([, value]) => value).filter(Number.isFinite) : current ? [current[1]] : [];
    if (!values.length) return { avg: null, min: null, max: null };
    const sum = values.reduce((total, value) => total + value, 0);
    return {
      avg: sum / values.length,
      min: Math.min(...values),
      max: Math.max(...values),
    };
  }

  render() {
    if (!this.shadowRoot) return;
    const current = this.currentPoint();
    const currentValue = current?.[1] ?? null;
    const status = this.statusFor(currentValue);
    const h24 = Number(this._hass?.states?.["sensor.basement_radon_24h_stats"]?.state);
    const avg24 = Number.isFinite(h24) ? this.bqToPci(h24) : null;
    const heroCopy = `${status.copy}${avg24 !== null ? ` Last day averaged ${this.formatNumber(avg24, 1)} pCi/L.` : ""}`;
    const horizons = this.horizons();
    const horizon = horizons[this._horizon] || horizons["30d"];
    const stats = this.statsFor(this._horizon);

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          color: #f8fafc;
          --radon-green: #4ade80;
          --radon-yellow: #fbbf24;
          --radon-red: #ef4444;
          --radon-ink: rgba(248, 250, 252, 0.92);
          --radon-muted: rgba(226, 232, 240, 0.64);
          --radon-line: rgba(226, 232, 240, 0.22);
        }
        ha-card {
          border: 1px solid rgba(148, 163, 184, 0.22);
          border-radius: 30px;
          overflow: hidden;
          padding: 0;
          background:
            radial-gradient(circle at 80% 0%, rgba(45, 212, 191, 0.14), transparent 34%),
            linear-gradient(180deg, rgba(17, 24, 39, 0.98), rgba(10, 15, 25, 0.98));
          box-shadow: 0 24px 70px rgba(0, 0, 0, 0.42);
        }
        .hero {
          display: grid;
          grid-template-columns: 52px minmax(0, 1fr);
          gap: 14px;
          align-items: center;
          padding: 24px 22px 18px;
        }
        .mark {
          width: 52px;
          height: 52px;
          display: grid;
          place-items: center;
          border-radius: 18px;
          background: rgba(248, 250, 252, 0.08);
          color: ${status.color};
        }
        .mark ha-icon {
          --mdc-icon-size: 29px;
        }
        .eyebrow {
          color: var(--radon-muted);
          font-size: 12px;
          font-weight: 700;
          letter-spacing: 0;
          text-transform: uppercase;
        }
        .metric {
          margin-top: 3px;
          color: #f8fafc;
          font-size: 38px;
          font-weight: 720;
          line-height: 1;
        }
        .metric span {
          font-size: 17px;
          font-weight: 650;
          color: rgba(226, 232, 240, 0.86);
        }
        .subcopy {
          margin-top: 8px;
          color: rgba(226, 232, 240, 0.72);
          font-size: 14px;
          line-height: 1.42;
        }
        .tabs {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0;
          margin: 0 18px 18px;
          padding: 4px;
          border-radius: 17px;
          background: rgba(248, 250, 252, 0.10);
        }
        button.tab {
          min-width: 0;
          min-height: 38px;
          border: 0;
          border-radius: 13px;
          background: transparent;
          color: rgba(248, 250, 252, 0.68);
          font: inherit;
          font-size: 14px;
          font-weight: 680;
          cursor: pointer;
        }
        button.tab.active {
          color: #f8fafc;
          background: rgba(248, 250, 252, 0.22);
          box-shadow: inset 0 0 0 1px rgba(248, 250, 252, 0.08), 0 8px 18px rgba(0, 0, 0, 0.18);
        }
        .chart-panel {
          padding: 0 0 8px;
          background: rgba(15, 23, 42, 0.22);
        }
        .chart-wrap {
          position: relative;
          padding: 0;
        }
        svg {
          display: block;
          width: 100%;
          height: auto;
          overflow: visible;
        }
        .grid-line {
          stroke: rgba(226, 232, 240, 0.40);
          stroke-width: 1;
          stroke-dasharray: 7 8;
        }
        .soft-line {
          stroke: rgba(226, 232, 240, 0.12);
          stroke-width: 1;
        }
        .threshold-watch {
          stroke: rgba(251, 191, 36, 0.78);
          stroke-width: 1;
        }
        .threshold-high {
          stroke: rgba(239, 68, 68, 0.80);
          stroke-width: 1;
        }
        .threshold-label {
          font-size: 18px;
          font-weight: 650;
          dominant-baseline: middle;
        }
        .axis-pill {
          fill: rgba(30, 41, 59, 0.72);
        }
        .axis-text {
          fill: rgba(248, 250, 252, 0.84);
          font-size: 18px;
          font-weight: 560;
          dominant-baseline: middle;
          text-anchor: middle;
        }
        .date-pill {
          fill: rgba(30, 41, 59, 0.78);
        }
        .date-text {
          fill: rgba(248, 250, 252, 0.82);
          font-size: 16px;
          font-weight: 560;
          dominant-baseline: middle;
          text-anchor: middle;
        }
        .radon-line {
          fill: none;
          stroke-width: 8;
          stroke-linecap: round;
          stroke-linejoin: round;
          filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.26));
        }
        .marker-ring {
          fill: #f8fafc;
        }
        .marker-core {
          fill: ${status.color};
        }
        .summary {
          display: grid;
          grid-template-columns: 6px minmax(0, 1fr);
          gap: 16px;
          align-items: center;
          margin: 12px 18px 20px;
          padding: 15px 17px;
          border-radius: 22px;
          border: 2px solid ${status.color};
          background: rgba(15, 23, 42, 0.56);
        }
        .summary-bar {
          width: 6px;
          height: 74px;
          border-radius: 999px;
          background: ${status.color};
        }
        .summary-kicker {
          display: flex;
          align-items: center;
          gap: 9px;
          color: rgba(226, 232, 240, 0.78);
          font-size: 14px;
          line-height: 1.2;
        }
        .summary-kicker ha-icon {
          --mdc-icon-size: 19px;
        }
        .summary-main {
          margin-top: 4px;
          color: #f8fafc;
          font-size: 25px;
          font-weight: 740;
          line-height: 1.05;
        }
        .summary-range {
          margin-top: 4px;
          color: rgba(226, 232, 240, 0.78);
          font-size: 14px;
          line-height: 1.3;
        }
        .loading,
        .error {
          margin: 0 18px 18px;
          padding: 12px 14px;
          border-radius: 16px;
          color: rgba(226, 232, 240, 0.74);
          background: rgba(248, 250, 252, 0.07);
          font-size: 13px;
        }
        @media (max-width: 420px) {
          .hero {
            padding: 22px 18px 16px;
          }
          .metric {
            font-size: 34px;
          }
          .summary-main {
            font-size: 23px;
          }
        }
      </style>
      <ha-card>
        <section class="hero">
          <div class="mark"><ha-icon icon="mdi:radioactive"></ha-icon></div>
          <div>
            <div class="eyebrow">${this.escape(status.label)}</div>
            <div class="metric">${this.formatNumber(currentValue, 1)} <span>pCi/L</span></div>
            <div class="subcopy">${this.escape(heroCopy)}</div>
          </div>
        </section>
        <div class="tabs" role="tablist" aria-label="Radon chart horizon">
          ${Object.entries(horizons).map(([key, item]) => `
            <button class="tab ${key === this._horizon ? "active" : ""}" data-horizon="${this.escapeAttr(key)}" role="tab" aria-selected="${key === this._horizon ? "true" : "false"}">${this.escape(item.label)}</button>
          `).join("")}
        </div>
        <section class="chart-panel">
          ${this._error ? `<div class="error">${this.escape(this._error)}</div>` : ""}
          ${this._loadingKey ? `<div class="loading">Loading ${this.escape(horizon.title.toLowerCase())}...</div>` : ""}
          ${this.renderChart(this._horizon)}
          <div class="summary">
            <div class="summary-bar"></div>
            <div>
              <div class="summary-kicker"><ha-icon icon="mdi:calendar-range"></ha-icon><span>${this.escape(horizon.title)}</span></div>
              <div class="summary-main">Average ${this.formatNumber(stats.avg, 1)} pCi/L</div>
              <div class="summary-range">Range ${this.formatNumber(stats.min, 1)} pCi/L - ${this.formatNumber(stats.max, 1)} pCi/L</div>
            </div>
          </div>
        </section>
      </ha-card>
    `;

    this.shadowRoot.querySelectorAll("[data-horizon]").forEach((button) => {
      button.addEventListener("click", () => {
        const horizonKey = button.getAttribute("data-horizon");
        if (!this.horizons()[horizonKey] || horizonKey === this._horizon) return;
        this._horizon = horizonKey;
        this.render();
        this.ensureHistory();
      });
    });
  }

  renderChart(horizonKey) {
    const horizon = this.horizons()[horizonKey] || this.horizons()["30d"];
    const now = Date.now();
    const xMin = now - horizon.ms;
    const xMax = now;
    const raw = this._history[horizonKey]?.raw || [];
    let data = this._history[horizonKey]?.bucketed || [];
    const current = this.currentPoint();
    if (!data.length && current) data = [[xMin, current[1]], current];
    if (data.length === 1) data = [[xMin, data[0][1]], data[0]];

    const values = data.map(([, value]) => value).filter(Number.isFinite);
    const maxData = values.length ? Math.max(...values) : 4;
    const minData = values.length ? Math.min(...values) : 0.8;
    const yMin = Math.max(0, Math.floor((minData - 0.7) * 10) / 10);
    const yMax = Math.max(4.2, Math.ceil((maxData + 0.35) * 10) / 10);

    const width = 720;
    const height = 430;
    const pad = { top: 36, right: 72, bottom: 62, left: 22 };
    const innerWidth = width - pad.left - pad.right;
    const innerHeight = height - pad.top - pad.bottom;
    const xFor = (time) => pad.left + ((time - xMin) / (xMax - xMin || 1)) * innerWidth;
    const yFor = (value) => pad.top + (1 - ((value - yMin) / (yMax - yMin || 1))) * innerHeight;
    const points = data.map(([time, value]) => [xFor(time), yFor(value)]).filter(([x, y]) => Number.isFinite(x) && Number.isFinite(y));
    const path = this.smoothPath(points);
    const latest = points[points.length - 1];
    const latestValue = data[data.length - 1]?.[1] ?? null;
    const latestStatus = this.statusFor(latestValue);
    const clipIds = {
      high: `radon-clip-high-${horizonKey}`,
      watch: `radon-clip-watch-${horizonKey}`,
      good: `radon-clip-good-${horizonKey}`,
    };
    const gridTicks = this.xTicks(xMin, xMax, horizonKey);
    const yLabels = [0.9, 1.8, 2.7, 3.6].filter((value) => value >= yMin && value <= yMax);
    const bandClips = this.thresholdClipRects(clipIds, yFor(4), yFor(2.7), pad, innerWidth, innerHeight);

    return `
      <div class="chart-wrap">
        <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${this.escapeAttr(horizon.title)} radon chart">
          <defs>
            ${bandClips.defs}
          </defs>
          ${gridTicks.map((tick) => `<line class="grid-line" x1="${xFor(tick)}" x2="${xFor(tick)}" y1="${pad.top}" y2="${pad.top + innerHeight}"></line>`).join("")}
          ${yLabels.map((value) => `<line class="soft-line" x1="${pad.left}" x2="${pad.left + innerWidth}" y1="${yFor(value)}" y2="${yFor(value)}"></line>`).join("")}
          <line class="threshold-high" x1="${pad.left}" x2="${pad.left + innerWidth}" y1="${yFor(4)}" y2="${yFor(4)}"></line>
          <line class="threshold-watch" x1="${pad.left}" x2="${pad.left + innerWidth}" y1="${yFor(2.7)}" y2="${yFor(2.7)}"></line>
          <text class="threshold-label" fill="#ef4444" x="${pad.left}" y="${yFor(4) - 16}">4.0</text>
          <text class="threshold-label" fill="#fbbf24" x="${pad.left}" y="${yFor(2.7) - 16}">2.7</text>
          ${yLabels.map((value) => `
            <g>
              <rect class="axis-pill" x="${pad.left + innerWidth + 18}" y="${yFor(value) - 16}" width="54" height="32" rx="16"></rect>
              <text class="axis-text" x="${pad.left + innerWidth + 45}" y="${yFor(value)}">${this.formatNumber(value, 1)}</text>
            </g>
          `).join("")}
          ${path ? this.renderThresholdLine(path, clipIds) : ""}
          ${latest ? `
            <circle class="marker-ring" cx="${latest[0]}" cy="${latest[1]}" r="18"></circle>
            <circle class="marker-core" cx="${latest[0]}" cy="${latest[1]}" r="12" fill="${latestStatus.color}"></circle>
          ` : ""}
          ${gridTicks.map((tick) => `
            <g>
              <rect class="date-pill" x="${xFor(tick) - 39}" y="${pad.top + innerHeight + 30}" width="78" height="30" rx="15"></rect>
              <text class="date-text" x="${xFor(tick)}" y="${pad.top + innerHeight + 45}">${this.escape(this.formatTick(tick, horizonKey))}</text>
            </g>
          `).join("")}
        </svg>
      </div>
    `;
  }

  thresholdClipRects(ids, yHigh, yWatch, pad, innerWidth, innerHeight) {
    const top = pad.top;
    const bottom = pad.top + innerHeight;
    const x = pad.left - 24;
    const width = innerWidth + 48;
    const high = this.clamp(yHigh, top, bottom);
    const watch = this.clamp(yWatch, top, bottom);
    const highHeight = Math.max(0, high - top);
    const watchHeight = Math.max(0, watch - high);
    const goodHeight = Math.max(0, bottom - watch);

    const rect = (id, y, height) => `
      <clipPath id="${id}">
        <rect x="${x}" y="${y}" width="${width}" height="${height}"></rect>
      </clipPath>
    `;

    return {
      defs: `
        ${rect(ids.high, top, highHeight)}
        ${rect(ids.watch, high, watchHeight)}
        ${rect(ids.good, watch, goodHeight)}
      `,
    };
  }

  renderThresholdLine(path, ids) {
    return `
      <g clip-path="url(#${ids.good})"><path class="radon-line" d="${path}" stroke="#4ade80"></path></g>
      <g clip-path="url(#${ids.watch})"><path class="radon-line" d="${path}" stroke="#fbbf24"></path></g>
      <g clip-path="url(#${ids.high})"><path class="radon-line" d="${path}" stroke="#ef4444"></path></g>
    `;
  }

  xTicks(xMin, xMax, horizonKey) {
    const count = horizonKey === "24h" ? 5 : 6;
    const step = (xMax - xMin) / (count - 1);
    return Array.from({ length: count }, (_, index) => xMin + step * index);
  }

  formatTick(timestamp, horizonKey) {
    const date = new Date(timestamp);
    if (horizonKey === "24h") {
      let hour = date.getHours();
      const suffix = hour >= 12 ? "p" : "a";
      hour = hour % 12 || 12;
      return `${hour}${suffix}`;
    }
    return `${date.getMonth() + 1}/${date.getDate()}`;
  }

  smoothPath(points) {
    if (!points.length) return "";
    if (points.length === 1) return `M ${points[0][0]} ${points[0][1]}`;
    let path = `M ${points[0][0]} ${points[0][1]}`;
    for (let i = 0; i < points.length - 1; i += 1) {
      const p0 = points[i - 1] || points[i];
      const p1 = points[i];
      const p2 = points[i + 1];
      const p3 = points[i + 2] || p2;
      const cp1x = p1[0] + (p2[0] - p0[0]) / 6;
      const cp1y = p1[1] + (p2[1] - p0[1]) / 6;
      const cp2x = p2[0] - (p3[0] - p1[0]) / 6;
      const cp2y = p2[1] - (p3[1] - p1[1]) / 6;
      path += ` C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${p2[0]} ${p2[1]}`;
    }
    return path;
  }

  formatNumber(value, digits = 1) {
    return Number.isFinite(value) ? value.toFixed(digits) : "--";
  }

  clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  escape(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  escapeAttr(value) {
    return this.escape(value).replace(/`/g, "&#096;");
  }
}

if (!customElements.get("radon-air-quality-card")) {
  customElements.define("radon-air-quality-card", RadonAirQualityCard);
}

const openRadonAirQualityPopup = (options = {}) => {
  const prior = document.querySelector("[data-radon-air-overlay]");
  if (prior) prior.remove();

  const overlay = document.createElement("div");
  overlay.setAttribute("data-radon-air-overlay", "");
  overlay.style.cssText = `
    position: fixed;
    inset: 0;
    z-index: 2147483647;
    display: grid;
    place-items: center;
    padding: 20px;
    background: rgba(2, 6, 23, 0.52);
    backdrop-filter: blur(26px) saturate(170%);
    -webkit-backdrop-filter: blur(26px) saturate(170%);
  `;

  const panel = document.createElement("div");
  panel.style.cssText = `
    position: relative;
    width: min(560px, calc(100vw - 24px));
    max-height: calc(100vh - 32px);
    overflow: auto;
    border-radius: 32px;
    box-shadow: 0 30px 90px rgba(0, 0, 0, 0.46);
    scrollbar-width: none;
  `;

  const close = document.createElement("button");
  close.setAttribute("aria-label", "Close");
  close.innerHTML = '<ha-icon icon="mdi:close"></ha-icon>';
  close.style.cssText = `
    position: absolute;
    top: 16px;
    right: 16px;
    z-index: 2;
    display: grid;
    place-items: center;
    width: 44px;
    height: 44px;
    border: 1px solid rgba(148, 163, 184, 0.28);
    border-radius: 999px;
    color: rgba(248, 250, 252, 0.86);
    background: rgba(15, 23, 42, 0.76);
    cursor: pointer;
  `;

  const card = document.createElement("radon-air-quality-card");
  card.setConfig({
    entity: options.entity || "sensor.basement_air_quality_radon",
    title: options.title || "Radon",
  });
  card.hass = options.hass || document.querySelector("home-assistant")?.hass;

  const dismiss = () => {
    document.removeEventListener("keydown", onKey);
    overlay.remove();
  };
  const onKey = (event) => {
    if (event.key === "Escape") dismiss();
  };
  close.addEventListener("click", dismiss);
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) dismiss();
  });
  document.addEventListener("keydown", onKey);

  panel.append(close, card);
  overlay.append(panel);
  document.body.append(overlay);
};

window.openRadonAirQualityPopup = openRadonAirQualityPopup;

if (!window.__radonAirQualityPopupListener) {
  window.__radonAirQualityPopupListener = true;
  const handleRadonAirQualityPopupEvent = (event) => {
    if (!event.detail?.radon_air_quality_popup) return;
    if (event.__radonAirQualityPopupHandled) return;
    event.__radonAirQualityPopupHandled = true;
    openRadonAirQualityPopup();
  };
  document.addEventListener("ll-custom", handleRadonAirQualityPopupEvent);
  window.addEventListener("ll-custom", handleRadonAirQualityPopupEvent);
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: "radon-air-quality-card",
  name: "Radon Air Quality Card",
  preview: true,
  description: "A calm Airthings-inspired radon chart with horizon tabs.",
});
