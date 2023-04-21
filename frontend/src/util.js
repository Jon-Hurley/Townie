const LEVEL_MULT = 0.2;

const ranks = [
    { cutoff: 5, name: 'Beginner' },
    { cutoff: 15, name: 'Tourist' },
    { cutoff: 25, name: 'Adventurer' },
    { cutoff: 50, name: 'Traveler' },
    { cutoff: 75, name: 'Citizen' },
    { cutoff: 100, name: 'Resident' }
]

export const pointsToLevel = (points) => {
    return 1 + Math.floor(LEVEL_MULT * Math.sqrt(points));
};

export const levelToPoints = (level) => {
    return (level - 1) * (level - 1) / (LEVEL_MULT * LEVEL_MULT);
};

export const pointsToProgress = (points) => {
    const currLevel = pointsToLevel(points);
    const nextLevel = currLevel + 1;

    const minCurrPoints = levelToPoints(currLevel);
    const minNextPoints = levelToPoints(nextLevel);

    const outOf = minNextPoints - minCurrPoints;
    const progress = points - minCurrPoints;
    console.log(outOf, progress)
    return (progress / outOf) || 0;
}

export const pointsToRank = (points) => {
    const level = pointsToLevel(points);
    for (let r of ranks) {
        if (level < r.cutoff) {
            return r.name;
        }
    }
    return 'Townie';
};