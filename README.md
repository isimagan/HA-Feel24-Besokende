![Feel24-logo](https://raw.githubusercontent.com/isimagan/HA-Feel24-Visitors/master/brand/logo.png)

**Norsk** | [English](https://github.com/isimagan/HA-Feel24-Visitors/blob/master/README.en.md)

# HA Feel24 Visitors

En uoffisiell Home Assistant-integrasjon for Feel24.

Integrasjonen har en konfigurasjonsveiviser hvor du søker etter og velger et
Feel24-senter. Bare sentre fra den innebygde listen kan velges. Sensorer og
innhenting av besøkstall kommer i en senere versjon.

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

Bare brukere som har GitHub-lenken og legger den inn som et tilpasset
pakkelager, finner repoet i HACS. Repoet er ikke sendt inn til HACS sin
standardliste.

## Status

- Konfigurasjonsveiviser med søkbart sentervalg
- Norsk og engelsk grensesnitt
- Ingen sensorer ennå

Dette er et uoffisielt fellesskapsprosjekt og er ikke utviklet, godkjent eller
støttet av Feel24.

## Lisens

MIT
