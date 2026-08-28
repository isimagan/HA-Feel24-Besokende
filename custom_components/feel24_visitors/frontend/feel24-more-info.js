class Feel24MoreInfo extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          color: var(--primary-text-color);
          font-family: var(--paper-font-body1_-_font-family, inherit);
        }

        .content {
          display: grid;
          justify-items: center;
          gap: 26px;
          padding: 54px 32px 60px;
        }

        .logo-surface {
          display: grid;
          place-items: center;
          width: min(78%, 300px);
          padding: 14px 18px;
          border-radius: 14px;
          background: rgb(0 0 0 / 6%);
        }

        :host([dark-mode]) .logo-surface {
          background: transparent;
        }

        .logo {
          display: block;
          width: 100%;
          height: auto;
        }

        .copy {
          display: grid;
          justify-items: center;
          gap: 8px;
        }

        .reading {
          margin: 0;
          text-align: center;
          font-size: clamp(18px, 4.5vw, 24px);
          font-weight: 400;
          line-height: 1.3;
        }

        .reading strong {
          font-weight: 500;
        }

        .updated {
          margin: 0;
          color: var(--secondary-text-color);
          font-size: 13px;
          font-weight: 400;
          line-height: 1.4;
        }

        @media (max-width: 430px) {
          .content {
            padding: 46px 24px 52px;
          }
        }
      </style>
      <div class="content">
        <div class="logo-surface">
          <img class="logo" alt="Feel24" />
        </div>
        <div class="copy" aria-live="polite">
          <p class="reading"></p>
          <p class="updated"></p>
        </div>
      </div>
    `;

    this._logo = this.shadowRoot.querySelector(".logo");
    this._reading = this.shadowRoot.querySelector(".reading");
    this._updated = this.shadowRoot.querySelector(".updated");
  }

  set hass(value) {
    this._hass = value;
    this.toggleAttribute("dark-mode", Boolean(value?.themes?.darkMode));
    this._update();
  }

  set stateObj(value) {
    this._stateObj = value;
    this._update();
  }

  set entry(value) {
    this._entry = value;
  }

  set editMode(value) {
    this._editMode = value;
  }

  set data(value) {
    this._data = value;
  }

  _update() {
    if (!this._stateObj) {
      return;
    }

    const attributes = this._stateObj.attributes ?? {};
    const state = this._stateObj.state ?? "—";
    const unit = attributes.unit_of_measurement ?? "besøkende";
    const place = attributes.sted ?? "";
    const logoPath = attributes.logo_path ?? "";

    this._logo.src = logoPath;
    this._logo.hidden = !logoPath;

    this._reading.replaceChildren();
    this._reading.append(this._strong(state), ` ${unit}`);
    if (place) {
      this._reading.append(" på ", this._strong(place));
    }

    const updated = this._formatTime(
      this._stateObj.last_updated ?? this._stateObj.last_changed
    );
    this._updated.textContent = `Sist oppdatert: ${updated}`;
  }

  _strong(value) {
    const element = document.createElement("strong");
    element.textContent = value;
    return element;
  }

  _formatTime(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return "—";
    }

    const language = this._hass?.locale?.language ?? navigator.language;
    const options = {
      hour: "2-digit",
      minute: "2-digit",
    };

    if (this._hass?.config?.time_zone) {
      options.timeZone = this._hass.config.time_zone;
    }
    if (this._hass?.locale?.time_format === "12") {
      options.hour12 = true;
    } else if (this._hass?.locale?.time_format === "24") {
      options.hour12 = false;
    }

    return new Intl.DateTimeFormat(language, options).format(date);
  }
}

if (!customElements.get("feel24-more-info")) {
  customElements.define("feel24-more-info", Feel24MoreInfo);
}
