![Feel24-logo](https://raw.githubusercontent.com/isimagan/HA-Feel24-Visitors/master/brand/logo.png)

# HA Feel24 Visitors

En uoffisiell Home Assistant-integrasjon for Feel24.

Integrasjonen har en konfigurasjonsveiviser hvor du søker etter og velger et
Feel24-senter. Bare sentre fra den innebygde listen kan velges. Integrasjonen
oppretter deretter en sensor som viser hvor mange som trener på senteret nå.

## Legg til i HACS med lenken

Repoet er ikke listet i HACS-katalogen. Det må legges til manuelt:

1. Åpne HACS og velg **Tilpassede pakkelagre / Custom repositories**.
2. Legg til `https://github.com/isimagan/HA-Feel24-Visitors`.
3. Velg **Integration** som kategori.
4. Velg **Legg til**.

## Konfigurasjon

1. Installer integrasjonen gjennom HACS og start Home Assistant på nytt.
2. Åpne **Innstillinger → Enheter og tjenester**.
3. Velg **Legg til integrasjon** og søk etter **Feel24 Visitors**.
4. Begynn å skrive navnet på senteret ditt, og velg senteret fra listen.

Senter-ID-en lagres automatisk. Det finnes ingen andre innstillinger ennå.

## Sensor

For et senter som **Feel24 Billingstad** opprettes normalt:

```text
sensor.feel24_billingstad_visitors
```

Sensoren:

- viser antall registrerte treningsgjester akkurat nå
- bruker enheten `besøkende`
- bruker ikonet `mdi:shoe-sneaker` og Feel24-bildet
- har attributtet `center_id`
- oppdateres hvert femte minutt

Hvert senter registreres også som en enhet i Home Assistant. Det gir senteret
en egen enhetsside med sensoren, i stedet for bare en løs entitet i listen.

Bare brukere som har GitHub-lenken og legger den inn som et tilpasset
pakkelager, finner repoet i HACS. Repoet er ikke sendt inn til HACS sin
standardliste.

## Status

- Konfigurasjonsveiviser med søkbart sentervalg
- Norsk grensesnitt og dokumentasjon
- Sensor for antall besøkende
- Egen enhetsside for hvert konfigurert senter

Dette er et uoffisielt fellesskapsprosjekt og er ikke utviklet, godkjent eller
støttet av Feel24.

## Lisens

MIT
