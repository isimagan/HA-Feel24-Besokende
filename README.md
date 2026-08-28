<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/isimagan/HA-Feel24-Besokende/master/brand/logo.png">
  <img alt="Feel24-logo" src="https://raw.githubusercontent.com/isimagan/HA-Feel24-Besokende/master/brand/logo-light.svg">
</picture>

# HA Feel24 Besøkende

En uoffisiell Home Assistant-integrasjon for Feel24.

Krever Home Assistant 2026.5 eller nyere.

Integrasjonen har en konfigurasjonsveiviser hvor du søker etter og velger et
Feel24-senter. Bare sentre fra den innebygde listen kan velges. Integrasjonen
oppretter deretter en sensor som viser hvor mange som trener på senteret nå.

## Legg til i HACS med lenken

Repoet er ikke listet i HACS-katalogen. Det må legges til manuelt:

1. Åpne HACS og velg **Tilpassede pakkelagre / Custom repositories**.
2. Legg til `https://github.com/isimagan/HA-Feel24-Besokende`.
3. Velg **Integration** som kategori.
4. Velg **Legg til**.

## Konfigurasjon

1. Installer integrasjonen gjennom HACS og start Home Assistant på nytt.
2. Åpne **Innstillinger → Enheter og tjenester**.
3. Velg **Legg til integrasjon** og søk etter **Feel24 Besøkende**.
4. Begynn å skrive navnet på senteret ditt, og velg senteret fra listen.

Senter-ID-en lagres automatisk. Varsling konfigureres etterpå fra
integrasjonens meny via **Konfigurer**.

## Sensor

For et senter som **Feel24 Billingstad** opprettes normalt:

```text
sensor.feel24_billingstad_besokende
```

Sensoren:

- viser antall registrerte treningsgjester akkurat nå
- bruker enheten `besøkende`
- bruker ikonet `mdi:shoe-sneaker` og Feel24-bildet
- har attributtene `center_id`, `sted` (`Billingstad` i dette eksemplet) og
  `logo_path` (`/api/feel24_visitors/logo.png`)
- oppdateres hvert femte minutt
- har en egen **Mer info**-visning med Feel24-logo, besøkstall, sted og
  tidspunktet sensoren sist ble oppdatert

Hvert senter registreres også som en enhet i Home Assistant. Det gir senteret
en egen enhetsside med sensoren, i stedet for bare en løs entitet i listen.

## Besøksvarsel

Integrasjonen oppretter også en varslingsswitch. For **Feel24 Billingstad** er
standard-ID-en:

```text
switch.feel24_billingstad_varsel
```

Switchen er av som standard, også når en eksisterende installasjon får
funksjonen gjennom en oppdatering. Når du selv slår den på eller av, gjenoppretter
Home Assistant valget etter restart eller reload. Ikonet er `mdi:bell-ring` når
switchen er på og `mdi:bell-off` når den er av.

Slik konfigurerer du varslingen:

1. Åpne **Innstillinger → Enheter og tjenester**.
2. Finn **Feel24 Besøkende**, åpne menyen for senteret og velg **Konfigurer**.
3. Velg grense, varslingstid og en `notify`-entitet som mottaker.
4. Slå på senterets **Varsel**-switch når funksjonen skal være aktiv.

Det sendes bare varsel når besøkstallet går fra over grensen til lik eller under
grensen. Med grense 2 gir derfor `4 → 3 → 2` ett varsel, mens videre endringer
`2 → 1 → 0` ikke gir flere. Etter at tallet har vært over 2 igjen, armeres
varslingen på nytt. Tidsrom over midnatt, som `22:00–02:00`, støttes.

Varslingen bruker Home Assistants native `notify.send_message` og samme data som
besøkssensoren. Den oppretter derfor ingen ekstra spørringer mot Feel24.

Bare brukere som har GitHub-lenken og legger den inn som et tilpasset
pakkelager, finner repoet i HACS. Repoet er ikke sendt inn til HACS sin
standardliste.

## Status

- Konfigurasjonsveiviser med søkbart sentervalg
- Norsk grensesnitt og dokumentasjon
- Sensor for antall besøkende
- Egen enhetsside for hvert konfigurert senter
- Egen Mer info-visning for sensoren
- Konfigurerbart pushvarsel med terskel, tidsrom, mottaker og av/på-switch

Dette er et uoffisielt fellesskapsprosjekt og er ikke utviklet, godkjent eller
støttet av Feel24.

## Lisens

MIT
