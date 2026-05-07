class CaseyPresenceTimelineCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._config = {};
    this._history = null;
    this._loading = false;
    this._error = "";
  }

  setConfig(config) {
    this._config = {
      entity: "device_tracker.unifi_default_42_15_78_4a_d9_f8",
      hours: 24,
      limit: 24,
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

  async ensureHistory(force = false) {
    if (!this._hass || !this._config.entity) return;
    if (this._loading) return;
    if (!force && this._history && Date.now() - this._history.fetchedAt < 90 * 1000) return;

    this._loading = true;
    this._error = "";
    this.render();

    try {
      const end = new Date();
      const start = new Date(end.getTime() - Number(this._config.hours || 24) * 60 * 60 * 1000);
      const path = `history/period/${start.toISOString()}?filter_entity_id=${encodeURIComponent(this._config.entity)}&end_time=${encodeURIComponent(end.toISOString())}`;
      const response = await this._hass.callApi("GET", path);
      const rows = Array.isArray(response?.[0]) ? response[0] : [];
      this._history = {
        rows,
        start: start.getTime(),
        end: end.getTime(),
        fetchedAt: Date.now(),
      };
    } catch (error) {
      this._error = "Could not load Casey's history.";
    } finally {
      this._loading = false;
      this.render();
    }
  }

  currentEntity() {
    return this._hass?.states?.[this._config.entity] || null;
  }

  validState(state) {
    return state === "home" || state === "not_home";
  }

  labelFor(state) {
    return state === "home" ? "Home" : "Away";
  }

  wordFor(state) {
    return state === "home" ? "home" : "away";
  }

  toneFor(state) {
    return state === "home" ? "home" : "away";
  }

  rowTime(row) {
    const value = row?.last_changed || row?.last_updated || row?.last_reported || "";
    const time = new Date(value).getTime();
    return Number.isFinite(time) ? time : null;
  }

  periods() {
    const entity = this.currentEntity();
    const now = Date.now();
    const start = this._history?.start || now - Number(this._config.hours || 24) * 60 * 60 * 1000;
    const end = now;
    const currentState = this.validState(entity?.state) ? entity.state : null;
    const currentChanged = new Date(entity?.last_changed || entity?.last_updated || now).getTime();

    const points = (this._history?.rows || [])
      .map((row) => ({ state: row.state, at: this.rowTime(row) }))
      .filter((point) => this.validState(point.state) && Number.isFinite(point.at))
      .sort((a, b) => a.at - b.at);

    if (currentState && Number.isFinite(currentChanged)) {
      points.push({ state: currentState, at: currentChanged });
      points.sort((a, b) => a.at - b.at);
    }

    if (!points.length && currentState) {
      return [{
        state: currentState,
        start: Math.max(start, Number.isFinite(currentChanged) ? currentChanged : start),
        end,
        current: true,
      }];
    }

    const periods = [];
    let active = null;

    points.forEach((point, index) => {
      const at = Math.max(start, Math.min(end, point.at));
      if (!active) {
        const closeToWindowStart = Math.abs(at - start) < 5 * 60 * 1000;
        active = { state: point.state, start: closeToWindowStart ? start : at };
        return;
      }
      if (point.state === active.state) return;
      if (at > active.start) periods.push({ state: active.state, start: active.start, end: at, current: false });
      active = { state: point.state, start: at };
    });

    if (active) {
      if (currentState && active.state !== currentState && Number.isFinite(currentChanged) && currentChanged > active.start) {
        periods.push({ state: active.state, start: active.start, end: currentChanged, current: false });
        active = { state: currentState, start: Math.max(start, Math.min(end, currentChanged)) };
      }
      periods.push({ state: active.state, start: active.start, end, current: active.state === currentState });
    }

    return periods
      .filter((period) => this.validState(period.state) && period.end > period.start)
      .sort((a, b) => {
        if (a.current && !b.current) return -1;
        if (!a.current && b.current) return 1;
        return b.end - a.end;
      })
      .slice(0, Number(this._config.limit || 24));
  }

  durationLabel(ms) {
    const minutes = Math.max(0, Math.round(ms / 60000));
    if (minutes < 1) return "just now";
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const rest = minutes % 60;
    if (hours < 24) return rest ? `${hours}h ${rest}m` : `${hours}h`;
    const days = Math.floor(hours / 24);
    const dayHours = hours % 24;
    return dayHours ? `${days}d ${dayHours}h` : `${days}d`;
  }

  timeLabel(time) {
    const date = new Date(time);
    if (!Number.isFinite(date.getTime())) return "recently";
    return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }

  periodLabel(start, end) {
    const startDate = new Date(start);
    const endDate = new Date(end);
    const sameDay = startDate.toDateString() === endDate.toDateString();
    if (sameDay) return `${this.timeLabel(start)} - ${this.timeLabel(end)}`;
    const startLabel = `${startDate.toLocaleDateString([], { month: "short", day: "numeric" })} ${this.timeLabel(start)}`;
    const endLabel = `${endDate.toLocaleDateString([], { month: "short", day: "numeric" })} ${this.timeLabel(end)}`;
    return `${startLabel} - ${endLabel}`;
  }

  sourceLine() {
    const entity = this.currentEntity();
    const updated = new Date(entity?.last_updated || entity?.last_changed || Date.now()).getTime();
    const age = this.durationLabel(Date.now() - updated);
    return `Router presence history from the last ${Number(this._config.hours || 24)} hours. Last checked ${age} ago.`;
  }

  render() {
    if (!this.shadowRoot) return;
    const periods = this.periods();
    const rows = periods.map((period) => this.renderPeriod(period)).join("");
    const empty = !rows && !this._loading && !this._error
      ? `<div class="empty">No home/away periods recorded in the last ${Number(this._config.hours || 24)} hours.</div>`
      : "";
    const loading = this._loading && !this._history ? `<div class="empty">Loading the last ${Number(this._config.hours || 24)} hours...</div>` : "";
    const error = this._error ? `<div class="empty error">${this._error}</div>` : "";

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          color: #f8fafc;
          --casey-blue: #38bdf8;
          --casey-red: #fb7185;
          --casey-muted: rgba(203, 213, 225, 0.72);
        }
        ha-card {
          border: 1px solid rgba(148, 163, 184, 0.22);
          border-radius: 30px;
          overflow: hidden;
          padding: 13px 12px 12px;
          background:
            radial-gradient(circle at 22px 26px, rgba(56, 189, 248, 0.13), transparent 34%),
            linear-gradient(180deg, rgba(15, 23, 42, 0.97), rgba(15, 23, 42, 0.91));
          box-shadow: 0 18px 44px rgba(2, 8, 23, 0.30);
        }
        .head {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 10px;
          padding: 1px 2px 10px 34px;
        }
        .head-title {
          color: #f8fafc;
          font-size: 14px;
          font-weight: 760;
          letter-spacing: 0;
        }
        .head-meta {
          color: rgba(203, 213, 225, 0.58);
          font-size: 12px;
          font-weight: 650;
          letter-spacing: 0;
          text-align: right;
        }
        .timeline {
          position: relative;
          display: grid;
          gap: 7px;
          width: 100%;
          box-sizing: border-box;
          overflow: hidden;
        }
        .timeline:before {
          content: "";
          position: absolute;
          left: 12px;
          top: 17px;
          bottom: 18px;
          width: 2px;
          border-radius: 999px;
          background: linear-gradient(180deg, rgba(56, 189, 248, 0.76), rgba(251, 113, 133, 0.52), rgba(148, 163, 184, 0.18));
        }
        .period {
          position: relative;
          display: grid;
          grid-template-columns: 26px minmax(0, 1fr);
          gap: 8px;
          align-items: stretch;
          width: 100%;
          max-width: 100%;
        }
        .rail {
          position: relative;
          z-index: 1;
          display: flex;
          justify-content: center;
          padding-top: 15px;
        }
        .dot {
          position: relative;
          z-index: 1;
          width: 11px;
          height: 11px;
          border-radius: 999px;
          border: 1px solid rgba(15, 23, 42, 0.92);
          box-sizing: border-box;
        }
        .home .dot {
          background: var(--casey-blue);
          box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.16);
        }
        .away .dot {
          background: var(--casey-red);
          box-shadow: 0 0 0 4px rgba(251, 113, 133, 0.15);
        }
        .copy {
          min-width: 0;
          max-width: 100%;
          padding: 10px 11px 11px;
          border: 1px solid rgba(148, 163, 184, 0.14);
          border-radius: 18px;
          background: linear-gradient(180deg, rgba(30, 41, 59, 0.54), rgba(15, 23, 42, 0.42));
          box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
          overflow: hidden;
        }
        .home .copy {
          border-color: rgba(56, 189, 248, 0.20);
          background: linear-gradient(180deg, rgba(14, 116, 144, 0.24), rgba(15, 23, 42, 0.44));
        }
        .away .copy {
          border-color: rgba(251, 113, 133, 0.18);
          background: linear-gradient(180deg, rgba(127, 29, 29, 0.20), rgba(15, 23, 42, 0.44));
        }
        .stamp {
          display: inline-flex;
          align-items: center;
          width: fit-content;
          max-width: 100%;
          min-height: 20px;
          padding: 3px 8px;
          border-radius: 999px;
          color: #cbd5e1;
          font-size: 10px;
          font-weight: 740;
          line-height: 1.1;
          letter-spacing: 0;
          white-space: normal;
          overflow-wrap: anywhere;
        }
        .stamp-line {
          display: flex;
          align-items: center;
          gap: 8px;
          min-width: 0;
        }
        .duration {
          min-width: 0;
          color: rgba(203, 213, 225, 0.70);
          font-size: 12px;
          font-weight: 680;
          line-height: 1.2;
          letter-spacing: 0;
          white-space: nowrap;
        }
        .home .stamp {
          background: rgba(56, 189, 248, 0.14);
          color: #bae6fd;
        }
        .away .stamp {
          background: rgba(251, 113, 133, 0.13);
          color: #fecdd3;
        }
        .title {
          margin-top: 7px;
          color: #f8fafc;
          font-size: 14px;
          font-weight: 760;
          line-height: 1.18;
          letter-spacing: 0;
          white-space: normal;
          overflow-wrap: anywhere;
        }
        .body {
          margin-top: 3px;
          color: #cbd5e1;
          font-size: 12px;
          line-height: 1.32;
          white-space: normal;
          overflow-wrap: anywhere;
        }
        .empty {
          margin: 0 0 0 36px;
          padding: 14px;
          border-radius: 20px;
          border: 1px solid rgba(148, 163, 184, 0.14);
          background: rgba(15, 23, 42, 0.42);
          color: var(--casey-muted);
          font-size: 13px;
          line-height: 1.35;
        }
        .empty.error {
          color: #fecdd3;
          border-color: rgba(251, 113, 133, 0.18);
          background: rgba(127, 29, 29, 0.18);
        }
      </style>
      <ha-card>
        <div class="head">
          <div class="head-title">Last 24 hours</div>
          <div class="head-meta">${this._loading && this._history ? "Updating" : "Home / away"}</div>
        </div>
        <div class="timeline">${rows}${loading}${empty}${error}</div>
      </ha-card>
    `;
  }

  renderPeriod(period) {
    const tone = this.toneFor(period.state);
    const label = this.labelFor(period.state);
    const duration = this.durationLabel(period.end - period.start);
    const title = period.current
      ? `${label} for ${duration}`
      : this.periodLabel(period.start, period.end);
    const body = period.current
      ? `Since ${this.timeLabel(period.start)}${period.state === "not_home" ? " · UniFi can lag" : ""}.`
      : "";
    const stamp = period.current ? "Now" : label;
    const durationBadge = period.current ? "" : `<div class="duration">${duration}</div>`;
    const bodyMarkup = body ? `<div class="body">${body}</div>` : "";

    return `
      <div class="period ${tone}">
        <div class="rail"><span class="dot"></span></div>
        <div class="copy">
          <div class="stamp-line"><div class="stamp">${stamp}</div>${durationBadge}</div>
          <div class="title">${title}</div>
          ${bodyMarkup}
        </div>
      </div>
    `;
  }
}

if (!customElements.get("casey-presence-timeline-card")) {
  customElements.define("casey-presence-timeline-card", CaseyPresenceTimelineCard);
}
