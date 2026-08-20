"""Known Feel24 gyms."""

from __future__ import annotations

from dataclasses import dataclass

# Source: https://feel24.no/treningssentre
# The IDs are the current iBooking IDs published with the center data.
# Last synchronized: 2026-08-20


@dataclass(frozen=True)
class Gym:
    """A Feel24 gym and its iBooking ID."""

    id: int
    name: str


GYM_DATA: tuple[Gym, ...] = (
    Gym(2893, "Feel24 Alstad"),
    Gym(2764, "Feel24 Alta Bossekop"),
    Gym(2101, "Feel24 Alta Kronstad"),
    Gym(2405, "Feel24 Alta Nordlysbadet"),
    Gym(1227, "Feel24 Alta Parksenteret"),
    Gym(3004, "Feel24 Andenes"),
    Gym(2146, "Feel24 Ankenes"),
    Gym(2803, "Feel24 Asker Langenga"),
    Gym(2890, "Feel24 Balanse"),
    Gym(2558, "Feel24 Bardu"),
    Gym(2555, "Feel24 Bardufoss"),
    Gym(2680, "Feel24 Beitostølen"),
    Gym(2713, "Feel24 Billingstad"),
    Gym(2561, "Feel24 Bjerkvik"),
    Gym(2248, "Feel24 Bodø Mørkved"),
    Gym(2254, "Feel24 Bodø Olav V"),
    Gym(2887, "Feel24 Bodø Performance"),
    Gym(2390, "Feel24 Bodø Sentrum"),
    Gym(2257, "Feel24 Bodø Tverlandet"),
    Gym(2251, "Feel24 Bodø Vestbyen"),
    Gym(2716, "Feel24 Borkenes"),
    Gym(2981, "Feel24 Brobekk Vollebekk"),
    Gym(2929, "Feel24 Brumunddal"),
    Gym(2278, "Feel24 Brygga"),
    Gym(2833, "Feel24 Buran"),
    Gym(3022, "Feel24 Byåsen"),
    Gym(3341, "Feel24 Dalgård"),
    Gym(3390, "Feel24 Eidkjosen"),
    Gym(2776, "Feel24 Elverum"),
    Gym(2896, "Feel24 Fauske"),
    Gym(1224, "Feel24 Finnsnes"),
    Gym(2914, "Feel24 Fornebu"),
    Gym(2998, "Feel24 Gamlebyen Panorama"),
    Gym(3145, "Feel24 Gard Senter"),
    Gym(2806, "Feel24 Grorud Senter"),
    Gym(3034, "Feel24 Hagan"),
    Gym(2746, "Feel24 Hammerfest"),
    Gym(2402, "Feel24 Harstad Grottebadet"),
    Gym(2152, "Feel24 Harstad Medkila"),
    Gym(2155, "Feel24 Harstad Sama"),
    Gym(2149, "Feel24 Harstad Seljestad"),
    Gym(2399, "Feel24 Harstad Sentrum"),
    Gym(3223, "Feel24 Haugesund Sentrum"),
    Gym(2710, "Feel24 Heggedal"),
    Gym(2689, "Feel24 Heimdal"),
    Gym(3263, "Feel24 Hokksund"),
    Gym(3028, "Feel24 Høvik"),
    Gym(2830, "Feel24 Ilsvika"),
    Gym(2173, "Feel24 Kirkenes"),
    Gym(3031, "Feel24 Krokstadelva"),
    Gym(2206, "Feel24 Leknes"),
    Gym(2983, "Feel24 Levanger"),
    Gym(2785, "Feel24 Lien"),
    Gym(2740, "Feel24 Lommedalen"),
    Gym(2363, "Feel24 Lyngen"),
    Gym(3007, "Feel24 Melbu"),
    Gym(2899, "Feel24 Misvær"),
    Gym(2260, "Feel24 Mo Amfi"),
    Gym(2263, "Feel24 Mo Gruben"),
    Gym(2269, "Feel24 Mo Ytteren"),
    Gym(2932, "Feel24 Molde"),
    Gym(2272, "Feel24 Mosjøen"),
    Gym(2647, "Feel24 Myre"),
    Gym(2911, "Feel24 Myrvoll"),
    Gym(2143, "Feel24 Narvik Sentrum"),
    Gym(2552, "Feel24 Nordkjosbotn"),
    Gym(3332, "Feel24 Oppegård"),
    Gym(2902, "Feel24 Oppsal"),
    Gym(3025, "Feel24 Risvollan"),
    Gym(2653, "Feel24 Rognan"),
    Gym(3203, "Feel24 Rotnes"),
    Gym(2926, "Feel24 Rælingen"),
    Gym(2884, "Feel24 Rønvika"),
    Gym(2281, "Feel24 Salhus"),
    Gym(2275, "Feel24 Sandnessjøen"),
    Gym(2396, "Feel24 Sandnessjøen Lyngåsen"),
    Gym(2140, "Feel24 Skjervøy"),
    Gym(3019, "Feel24 Skjetten"),
    Gym(3212, "Feel24 Skytta Gjelleråsen"),
    Gym(2935, "Feel24 Skåla"),
    Gym(2674, "Feel24 Slemmestad"),
    Gym(2284, "Feel24 Sortland Kjøpmannsgata"),
    Gym(2212, "Feel24 Sortland Rådhusgata"),
    Gym(2206, "Feel24 Stamsund"),
    Gym(2989, "Feel24 Steinkjer"),
    Gym(2692, "Feel24 Stjørdal"),
    Gym(2287, "Feel24 Stokmarknes Sentrum"),
    Gym(2215, "Feel24 Stokmarknes Søndre"),
    Gym(2476, "Feel24 Stormyra Panorama"),
    Gym(3232, "Feel24 Strømmen"),
    Gym(2905, "Feel24 Sulitjelma"),
    Gym(1678, "Feel24 Svolvær Panorama"),
    Gym(3326, "Feel24 Svolvær Sentrum"),
    Gym(1996, "Feel24 Sørreisa"),
    Gym(3010, "Feel24 Tangen"),
    Gym(3338, "Feel24 Tolvsrød"),
    Gym(2854, "Feel24 Tranby"),
    Gym(575, "Feel24 Tromsø Fagereng"),
    Gym(3365, "Feel24 Tromsø Fløylia"),
    Gym(1065, "Feel24 Tromsø Håpet"),
    Gym(1777, "Feel24 Tromsø Isrenna"),
    Gym(431, "Feel24 Tromsø Skippergata"),
    Gym(3013, "Feel24 Tromsø Sportssenter"),
    Gym(1675, "Feel24 Tromsø Strandgata"),
    Gym(1623, "Feel24 Tromsø The Box"),
    Gym(1717, "Feel24 Tromsø Tomasjord"),
    Gym(3016, "Feel24 Tromsø Treningssenter"),
    Gym(1720, "Feel24 Tromsø Tromsdalen"),
    Gym(2773, "Feel24 Tyholttårnet"),
    Gym(2293, "Feel24 Vadsø"),
    Gym(2393, "Feel24 Valnesfjorden"),
    Gym(2986, "Feel24 Verdal"),
    Gym(2677, "Feel24 Vollen"),
    Gym(2743, "Feel24 Vøyenenga"),
    Gym(2800, "Feel24 Økern Brobekk"),
    Gym(3037, "Feel24 Øren"),
)

GYMS: tuple[str, ...] = tuple(gym.name for gym in GYM_DATA)

_GYMS_BY_NORMALIZED_NAME = {gym.name.casefold(): gym for gym in GYM_DATA}


def get_gym(value: str | None) -> Gym | None:
    """Return the gym for a canonical or normalized name."""
    normalized = " ".join((value or "").split())
    if not normalized:
        return None
    return _GYMS_BY_NORMALIZED_NAME.get(normalized.casefold())


def gym_unique_id(gym: Gym) -> str:
    """Return a stable config-entry unique ID for a gym."""
    return f"{gym.id}:{gym.name.casefold()}"


def resolve_gym(value: str | None) -> str | None:
    """Return the canonical gym name, an empty string, or None if unknown."""
    normalized = " ".join((value or "").split())
    if not normalized:
        return ""
    gym = get_gym(normalized)
    return gym.name if gym else None


def select_effective_gym(fixed_gym: str, chosen_gym: str) -> str:
    """Return the fixed gym, or the runtime choice when no gym is fixed."""
    return fixed_gym or chosen_gym
