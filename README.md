![Feel24-logo](https://raw.githubusercontent.com/isimagan/HA-Feel24-Visitors/master/brand/logo.png)

**Norsk** | [English](https://github.com/isimagan/HA-Feel24-Visitors/blob/master/README.en.md)

# HA Feel24 Visitors

En tilpasset Home Assistant-integrasjon for besøksdata fra Feel24.

Dette er et uoffisielt fellesskapsprosjekt og er ikke utviklet eller støttet av
Feel24.

## Installasjon med HACS

Repoet er ikke listet i HACS-katalogen. Det kan installeres ved å legge det til
som et tilpasset pakkelager:

1. Åpne HACS og velg **Custom repositories / Tilpassede pakkelagre**.
2. Legg til `https://github.com/isimagan/HA-Feel24-Visitors`.
3. Velg **Integration** som kategori.
4. Last ned **HA Feel24 Visitors** og start Home Assistant på nytt.
5. Åpne **Innstillinger → Enheter og tjenester → Legg til integrasjon** og
   velg **Feel24 Visitors**.

## Konfigurasjon

I konfigurasjonsveilederen kan du begynne å skrive navnet på et Feel24-senter
for å filtrere listen med forslag. Du kan velge et forslag eller la det
valgfrie feltet stå tomt. Et ukjent senternavn gir en feilmelding og kan ikke
lagres.

Du kan kjøre veilederen flere ganger for å legge til flere sentre. Hvert valgt
senter får sin egen oppføring, enhetsside og besøkssensor. Det samme senteret
kan ikke legges til to ganger.

Hvis feltet står tomt, opprettes `select.feel24_chosen_gym`, slik at aktivt
treningssenter kan endres senere i Home Assistant.

## Enheter

| Enhet | Ikon | Beskrivelse |
| --- | --- | --- |
| `sensor.feel24_visitors` | `mdi:shoe-sneaker` | Antall besøkende på valgt treningssenter. Enheten bruker det grønne Feel24-symbolet som entity picture og måleenheten `besøkende`. Attributtene `gym` og `gym_id` viser senterets navn og iBooking-ID. |
| `select.feel24_chosen_gym` | `mdi:weight-lifter` | Velger hvilket treningssenter som påvirker besøkssensoren. Opprettes bare når veiviseren fullføres uten et valgt senter. |

Home Assistant kan legge til et suffiks i entity-ID-en når flere besøkssensorer
har samme navn. Alle sensorene vises på hver sin enhetsside under integrasjonen.

## Utvikling

Integrasjonsfilene ligger i `custom_components/feel24_visitors/`. Feel24-appen
henter besøkstall fra et autentisert Membro/iBooking-endepunkt. Integrasjonen
mangler foreløpig den tilhørende innloggingsflyten, og besøkssensoren er derfor
utilgjengelig til denne er implementert. Det publiseres ikke oppdiktede tall.

Hold versjonen i `manifest.json` synkronisert med GitHub-utgivelser.

## Lisens

MIT
