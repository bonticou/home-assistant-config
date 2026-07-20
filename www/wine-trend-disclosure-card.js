class WineTrendDisclosureCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._hass = null;
    this._expanded = false;
    this._chart = null;
    this._chartPromise = null;
    this._renderShell();
  }

  setConfig(config) {
    if (!config?.title || !config?.range || !config?.temperature_entity || !config?.humidity_entity) {
      throw new Error("Wine trend disclosure requires title, range, temperature_entity, and humidity_entity");
    }
    this._config = { ...config };
    this._expanded = false;
    this._destroyChart();
    this._sync();
  }

  set hass(hass) {
    this._hass = hass;
    if (this._chart) this._chart.hass = hass;
    this._sync();
  }

  connectedCallback() {
    // Disclosure state is intentionally local and ephemeral. Re-entering or
    // reloading the view always starts collapsed and does not mount a chart.
    this._expanded = false;
    this._destroyChart();
    this._sync();
  }

  disconnectedCallback() {
    this._expanded = false;
    this._destroyChart();
  }

  getCardSize() {
    return this._expanded ? 4 : 1;
  }

  _renderShell() {
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; }
        ha-card {
          background: rgba(15, 23, 42, 0.72);
          border: 1px solid rgba(148, 163, 184, 0.18);
          border-radius: 20px;
          box-shadow: 0 8px 18px rgba(2, 8, 23, 0.14);
          overflow: hidden;
          transition: border-color 160ms ease, background 160ms ease;
        }
        ha-card.expanded {
          border-color: rgba(148, 163, 184, 0.22);
          background: rgba(15, 23, 42, 0.78);
        }
        button {
          align-items: center;
          appearance: none;
          background: transparent;
          border: 0;
          color: inherit;
          cursor: pointer;
          display: grid;
          font: inherit;
          gap: 12px;
          grid-template-columns: minmax(0, 1fr) auto 22px;
          min-height: 60px;
          padding: 14px 16px;
          text-align: left;
          width: 100%;
        }
        button:focus-visible {
          outline: 2px solid rgba(96, 165, 250, 0.68);
          outline-offset: -3px;
        }
        .title {
          color: #f8fafc;
          font-size: 17px;
          font-weight: 600;
          line-height: 1.2;
          min-width: 0;
        }
        .metrics {
          align-items: center;
          color: rgba(226, 232, 240, 0.82);
          display: flex;
          flex-wrap: nowrap;
          font-size: 13px;
          font-variant-numeric: tabular-nums;
          font-weight: 650;
          gap: 12px;
          white-space: nowrap;
        }
        .metric {
          align-items: center;
          display: inline-flex;
          gap: 4px;
        }
        .metric ha-icon { --mdc-icon-size: 15px; }
        .metric.temperature ha-icon { color: #ef5350; }
        .metric.humidity ha-icon { color: #42a5f5; }
        .chevron {
          align-items: center;
          color: rgba(203, 213, 225, 0.78);
          display: flex;
          justify-content: center;
        }
        .chevron ha-icon {
          --mdc-icon-size: 20px;
          transition: transform 180ms ease;
        }
        .expanded .chevron ha-icon { transform: rotate(180deg); }
        .chart-shell {
          border-top: 1px solid rgba(148, 163, 184, 0.12);
          display: none;
          min-height: 0;
          padding: 8px 8px 0;
        }
        .expanded .chart-shell { display: block; }
        @media (max-width: 360px) {
          button { gap: 9px; padding-inline: 14px; }
          .metrics { gap: 8px; }
          .title { font-size: 16px; }
        }
      </style>
      <ha-card>
        <button type="button" aria-expanded="false">
          <span class="title"></span>
          <span class="metrics">
            <span class="metric temperature"><ha-icon icon="mdi:thermometer"></ha-icon><span class="temperature-value">--</span></span>
            <span class="metric humidity"><ha-icon icon="mdi:water-percent"></ha-icon><span class="humidity-value">--</span></span>
          </span>
          <span class="chevron"><ha-icon icon="mdi:chevron-down"></ha-icon></span>
        </button>
        <div class="chart-shell"></div>
      </ha-card>
    `;
    this.shadowRoot.querySelector("button").addEventListener("click", () => this._toggle());
  }

  _format(entityId, digits, suffix) {
    const raw = Number(this._hass?.states?.[entityId]?.state);
    return Number.isFinite(raw) ? `${raw.toFixed(digits)}${suffix}` : "--";
  }

  _sync() {
    const card = this.shadowRoot.querySelector("ha-card");
    const button = this.shadowRoot.querySelector("button");
    if (!card || !button) return;
    card.classList.toggle("expanded", this._expanded);
    button.setAttribute("aria-expanded", String(this._expanded));
    this.shadowRoot.querySelector(".title").textContent = this._config.title || "Trends";
    this.shadowRoot.querySelector(".temperature-value").textContent = this._format(this._config.temperature_entity, 1, "°F");
    this.shadowRoot.querySelector(".humidity-value").textContent = this._format(this._config.humidity_entity, 0, "%");
  }

  async _toggle() {
    this._expanded = !this._expanded;
    this._sync();
    if (this._expanded) await this._mountChart();
    else this._destroyChart();
  }

  _chartConfig() {
    const range = this._config.range;
    const is24h = range === "24h";
    const is30d = range === "30d";
    const config = {
      type: "custom:apexcharts-card",
      graph_span: range,
      header: { show: false },
      apex_config: {
        chart: { height: 230, background: "transparent" },
        stroke: { curve: "straight" },
        grid: { borderColor: "rgba(120, 120, 120, 0.16)" },
        legend: { show: false },
        tooltip: { theme: "dark" },
      },
      yaxis: [
        { id: "temp", min: is24h ? "~52" : "~50", max: is24h ? "~60" : "~62", align_to: 1, decimals: 1, ...(is24h ? { apex_config: { tickAmount: 4 } } : {}) },
        { id: "humidity", min: "~45", max: "~72", align_to: 1, opposite: true, decimals: 0, ...(is24h ? { apex_config: { tickAmount: 4 } } : {}) },
      ],
      series: [
        { entity: "sensor.wine_temperature", name: "Temperature", yaxis_id: "temp", type: "line", color: "#ef5350", stroke_width: 1.5, group_by: { func: "avg", duration: is24h ? "10min" : is30d ? "12h" : "2h", fill: "last" } },
        { entity: "sensor.wine_humidity", name: "Humidity", yaxis_id: "humidity", type: "line", color: "#42a5f5", stroke_width: 1.5, group_by: { func: "avg", duration: is24h ? "10min" : is30d ? "12h" : "2h", fill: "last" } },
      ],
      card_mod: {
        style: `
          ha-card {
            background: transparent !important;
            border: 0 !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            overflow: hidden;
            padding: 0;
            --primary-text-color: #f8fafc;
            --secondary-text-color: #94a3b8;
          }
          #graph-wrapper { background: transparent !important; padding: 2px 2px 0 !important; }
          .apexcharts-canvas, .apexcharts-svg, .apexcharts-inner, svg { background: transparent !important; }
        `,
      },
    };

    if (is24h) {
      const formatter = `EVAL:function(value, timestamp) {
        const source = timestamp ?? value;
        if (source === null || source === undefined || source === '') return value ?? '';
        const numeric = typeof source === 'number' ? source : Number(source);
        const date = Number.isFinite(numeric) ? new Date(numeric) : new Date(source);
        if (Number.isNaN(date.getTime())) return value ?? '';
        let hour = date.getHours();
        const suffix = hour >= 12 ? 'p' : 'a';
        hour = hour % 12 || 12;
        return hour + suffix;
      }`;
      config.apex_config.xaxis = { tickAmount: 6, labels: { formatter }, tooltip: { enabled: false } };
    } else if (is30d) {
      config.apex_config.xaxis = { tickAmount: 6, labels: { format: "d MMM" } };
    }
    return config;
  }

  async _mountChart() {
    if (!this._expanded || this._chart || this._chartPromise) return;
    this._chartPromise = window.loadCardHelpers()
      .then((helpers) => {
        if (!this._expanded || !this.isConnected) return;
        const chart = helpers.createCardElement(this._chartConfig());
        chart.hass = this._hass;
        this._chart = chart;
        this.shadowRoot.querySelector(".chart-shell").replaceChildren(chart);
      })
      .finally(() => { this._chartPromise = null; });
    await this._chartPromise;
  }

  _destroyChart() {
    if (this._chart) this._chart.remove();
    this._chart = null;
    const shell = this.shadowRoot?.querySelector(".chart-shell");
    if (shell) shell.replaceChildren();
  }
}

if (!customElements.get("wine-trend-disclosure-card")) {
  customElements.define("wine-trend-disclosure-card", WineTrendDisclosureCard);
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: "wine-trend-disclosure-card",
  name: "Wine Trend Disclosure",
  description: "Locally collapsed, lazy-mounted wine trend chart disclosure.",
});
