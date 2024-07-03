export enum Genre {
    action = "action",
    adventure = "adventure",
    animation = "animation",
    biography = "biography",
    comedy = "comedy",
    crime = "crime",
    documentary = "documentary",
    drama = "drama",
    family = "family",
    fantasy = "fantasy",
    noir = "noir",
    gangster = "gangster",
    history = "history",
    horror = "horror",
    military = "military",
    music = "music",
    musical = "musical",
    mystery = "mystery",
    nature = "nature",
    period = "period",
    romance = "romance",
    sciFi = "sci-fi",
    short = "short",
    spy = "spy",
    superhero = "superhero",
    thriller = "thriller",
    war = "war",
    western = "western"
}

export function toString(genre: Genre): string {
    return genre;
}