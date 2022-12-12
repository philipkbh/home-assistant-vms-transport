// Dresden Transport Timetable Card

class DresdenTransportTimetableCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({
            mode: 'open'
        });
    }

    /* This is called every time sensor is updated */
    set hass(hass) {

        const config = this.config;
        const maxEntries = config.max_entries || 10;
        const showStopName = config.show_stop_name;
        const entityIds = config.entity ? [config.entity] : config.entities || [];

        let content = "";

        for (const entityId of entityIds) {
            const entity = hass.states[entityId];
            if (!entity) {
                throw new Error("Entity State Unavailable");
            }

            if (showStopName) {
                content += `<div class="stop">${entity.attributes.friendly_name}</div>`;
            }

            const timetable = entity.attributes.departures.slice(0, maxEntries).map((departure) => 
                `<div class="departure">
                    <div class="line">
                        <div class="line-icon" style="background-color: ${departure.color}">${departure.line_name}</div>
                        <div class="line-pl">${departure.platform}</div>
                    </div>
                    <div class="direction">${departure.direction}</div>
                    <div class="time-slot">
                        <div class="todeparture">(+${departure.gap})</div>
                        <div class="time">${departure.time}</div>
                    </div>
                </div>`
            );

            content += `<div class="departures">` + timetable.join("\n") + `</div>`;
        }

       this.shadowRoot.getElementById('container').innerHTML = content;
    }

    /* This is called only when config is updated */
    setConfig(config) {
        const root = this.shadowRoot;
        if (root.lastChild) root.removeChild(root.lastChild);

        this.config = config;

        const card = document.createElement('ha-card');
        const content = document.createElement('div');
        const style = document.createElement('style')
  
        style.textContent = `
        .container {
            padding: 10px;
            font-size: 130%;
            display: flex;
            flex-direction: column;
        }
        .stop {
            opacity: 0.6;
            font-weight: 400;
            width: 100%;
            text-align: left;
            padding: 10px 10px 5px 5px;
            color: rgb(220, 221, 221);
        }      
        .departures {
            width: 100%;
            font-weight: 400;
            line-height: 1.5em;
            padding-bottom: 20px;
            display: flex;
            flex-direction: column;
        }
        .departure {
            padding-top: 10px;
            min-height: 40px;
            display: flex;
            flex-wrap: nowrap;
            align-items: center;
            gap: 15px;
            color: rgb(220, 221, 221);
        }
        .line {
            min-width: 70px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 5px;
        }
        .line-icon {
            display: inline-block;
            border-radius: 20px;
            padding: 7px 10px 5px;
            font-size: 120%;
            font-weight: 700;
            line-height: 1em;
            color: #FFFFFF;
            text-align: center;
            flex: 1;
        }
        .line-pl {
            border-radius: 5px;
            padding: 5px;
            font-size: 60%;
            font-weight: 600;
            line-height: 1em;
            color: #FFFFFF;
            text-align: center;
            background-color: gray;
        }
        .direction {
            align-self: center;
            flex-grow: 1;
        }
        .time {
            align-self: flex-start;
            font-weight: 700;
            padding-right: 0px;
        }
        .todeparture {
            font-size: 12px;
        }
        .time-slot {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 5px;
        }
        `;
     
        content.id = "container";
        content.className = "container";
        card.header = config.title;
        card.appendChild(style);
        card.appendChild(content);

        root.appendChild(card);
      }
  
    // The height of the card.
    getCardSize() {
      return 5;
    }
}
  
customElements.define('dresden-transport-timetable-card', DresdenTransportTimetableCard);
